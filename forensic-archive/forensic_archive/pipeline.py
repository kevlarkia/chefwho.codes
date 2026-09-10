"""Two-pass archive generation: extract, validate, ledger, package."""

from __future__ import annotations

import fcntl
import json
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from .errors import MuseumPackageError
from .hashes import sha256_file, sha256_text, write_sha256sums
from .ledger import LEDGER_FILENAME, ForensicLedger, utc_now
from .llm import LLMCallTrace, LLMClient, client_from_env, consume_call_trace
from .parse import dangling_exclusion_ids, exclusion_ids, parse_exclusions, parse_items
from .prompts import (
    PRIMARY_PROMPT_ID,
    PROMPTS_DIR,
    SECONDARY_PROMPT_ID,
    ArchiveProfile,
    load_profile,
    render_primary_prompt,
    render_secondary_prompt,
)
from .verify import (
    ARCHIVE_FILENAME,
    MANIFEST_FILENAME,
    README_FILENAME,
    SHA256SUMS_FILENAME,
    VerificationReport,
    verify_package,
)

PROMPT_TEMPLATE_FILES = (
    "TEMP-ARC-001-primary-extraction.md",
    "TEMP-ARC-002-secondary-validation.md",
)


@dataclass
class ArchiveResult:
    run_id: str
    output_dir: Path
    archive_path: Path
    snapshot_path: Path
    ledger_path: Path
    inclusions: list[dict[str, Any]]
    exclusions: list[dict[str, Any]]
    provider: str
    profile: str
    primary_response: str
    secondary_response: str
    source_sha256: str
    verification: VerificationReport | None = None
    extra: dict[str, Any] = field(default_factory=dict)
    llm_traces: dict[str, dict[str, Any]] = field(default_factory=dict)


@contextmanager
def _package_lock(output_dir: Path) -> Iterator[None]:
    output_dir.mkdir(parents=True, exist_ok=True)
    lock_path = output_dir / ".package.lock"
    with lock_path.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class ForensicArchiver:
    """Generate a museum-quality archive plus `forensic_archive.sqlite`."""

    def __init__(
        self,
        *,
        client: LLMClient | None = None,
        profile: str = "generic",
        provider: str | None = None,
    ) -> None:
        self.profile: ArchiveProfile = load_profile(profile)
        self.client: LLMClient = client or client_from_env(provider)
        self._primary_prompt_text = ""
        self._secondary_prompt_text = ""

    def primary_extraction_call(
        self, source_text: str, *, client_request_id: str | None = None
    ) -> str:
        """TEMP-ARC-001. Swap the client to use Anthropic, OpenAI, or Vertex."""
        rendered = render_primary_prompt(source_text, self.profile)
        self._primary_prompt_text = rendered.text
        return self.client.complete(
            rendered.text,
            system=self.profile.addendum,
            client_request_id=client_request_id,
        )

    def secondary_validation_call(
        self, extraction: str, source_text: str, *, client_request_id: str | None = None
    ) -> str:
        """TEMP-ARC-002. Response must end with an `exclusions` JSON array."""
        rendered = render_secondary_prompt(source_text, extraction, self.profile)
        self._secondary_prompt_text = rendered.text
        return self.client.complete(
            rendered.text,
            system=self.profile.addendum,
            client_request_id=client_request_id,
        )

    def run(self, source: Path, output_dir: Path) -> ArchiveResult:
        source = Path(source)
        output_dir = Path(output_dir)
        try:
            source_text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise MuseumPackageError(f"source is not valid UTF-8: {source}") from exc
        if not source_text.strip():
            raise MuseumPackageError("source is empty")
        with _package_lock(output_dir):
            return self._run_locked(source, output_dir, source_text)

    def _run_locked(self, source: Path, output_dir: Path, source_text: str) -> ArchiveResult:
        source_sha256 = sha256_file(source)
        started_at = utc_now()
        run_id = str(uuid.uuid4())
        primary_request_id = f"{run_id}:primary"
        secondary_request_id = f"{run_id}:secondary"

        primary = self.primary_extraction_call(
            source_text, client_request_id=primary_request_id
        )
        primary_trace = consume_call_trace(self.client)
        secondary = self.secondary_validation_call(
            primary, source_text, client_request_id=secondary_request_id
        )
        secondary_trace = consume_call_trace(self.client)
        items = parse_items(primary)
        if not items:
            raise MuseumPackageError("TEMP-ARC-001 returned no parseable items")
        exclusions = parse_exclusions(secondary)
        dangling = dangling_exclusion_ids(items, exclusions)
        if dangling:
            raise MuseumPackageError(f"TEMP-ARC-002 excluded unknown ids: {dangling}")
        dropped = exclusion_ids(exclusions)
        inclusions = [item for item in items if item["id"] not in dropped]
        empty_kept = [item["id"] for item in inclusions if not str(item.get("text") or "").strip()]
        if empty_kept:
            raise MuseumPackageError(f"inclusions have empty text: {empty_kept}")
        finished_at = utc_now()

        snapshot_dir = output_dir / "runs" / run_id
        snapshot_dir.mkdir(parents=True, exist_ok=False)
        snapshot_rel = f"runs/{run_id}/{ARCHIVE_FILENAME}"
        snapshot_path = output_dir / snapshot_rel
        archive_path = output_dir / ARCHIVE_FILENAME
        ledger_path = output_dir / LEDGER_FILENAME
        llm_traces = {
            "primary_extraction": _trace_record(primary_trace, primary_request_id),
            "secondary_validation": _trace_record(secondary_trace, secondary_request_id),
        }
        payload = {
            "schema": "forensic-archive/v1",
            "run_id": run_id,
            "created_at": finished_at,
            "profile": self.profile.id,
            "provider": self.client.name,
            "source": {
                "path": str(source),
                "sha256": source_sha256,
            },
            "prompts": {
                "primary": PRIMARY_PROMPT_ID,
                "secondary": SECONDARY_PROMPT_ID,
            },
            "llm": llm_traces,
            "inclusions": inclusions,
            "exclusions": exclusions,
            "ledger": LEDGER_FILENAME,
            "snapshot": snapshot_rel,
        }
        serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        snapshot_path.write_text(serialized, encoding="utf-8")
        archive_path.write_text(serialized, encoding="utf-8")
        _write_human_readme(output_dir / README_FILENAME, payload)
        archive_sha256 = sha256_file(snapshot_path)

        template_hash = sha256_text(
            "".join((PROMPTS_DIR / name).read_text(encoding="utf-8") for name in PROMPT_TEMPLATE_FILES)
        )
        profile_hash = sha256_text(self.profile.addendum)

        ledger = ForensicLedger(ledger_path)
        try:
            ledger.record_run(
                run_id=run_id,
                started_at=started_at,
                finished_at=finished_at,
                profile=self.profile.id,
                provider=self.client.name,
                source_path=str(source),
                source_sha256=source_sha256,
                archive_path=snapshot_rel,
                archive_sha256=archive_sha256,
                prompt_template_sha256=template_hash,
                profile_sha256=profile_hash,
                extracted_ids=[item["id"] for item in items],
                dangling_exclusion_ids=dangling,
                calls=[
                    _ledger_call(
                        role="primary_extraction",
                        prompt_id=PRIMARY_PROMPT_ID,
                        provider=self.client.name,
                        prompt_text=self._primary_prompt_text,
                        response_text=primary,
                        created_at=started_at,
                        client_request_id=primary_request_id,
                        trace=primary_trace,
                    ),
                    _ledger_call(
                        role="secondary_validation",
                        prompt_id=SECONDARY_PROMPT_ID,
                        provider=self.client.name,
                        prompt_text=self._secondary_prompt_text,
                        response_text=secondary,
                        created_at=finished_at,
                        client_request_id=secondary_request_id,
                        trace=secondary_trace,
                    ),
                ],
                inclusions=inclusions,
                exclusions=exclusions,
            )
        finally:
            ledger.close()

        _write_manifest(output_dir, run_id)
        verification = verify_package(output_dir, run_id=run_id)
        verification.raise_if_failed()

        return ArchiveResult(
            run_id=run_id,
            output_dir=output_dir,
            archive_path=archive_path,
            snapshot_path=snapshot_path,
            ledger_path=ledger_path,
            inclusions=inclusions,
            exclusions=exclusions,
            provider=self.client.name,
            profile=self.profile.id,
            primary_response=primary,
            secondary_response=secondary,
            source_sha256=source_sha256,
            verification=verification,
            llm_traces=llm_traces,
        )


def _trace_record(trace: LLMCallTrace | None, client_request_id: str) -> dict[str, Any]:
    record: dict[str, Any] = {"client_request_id": client_request_id}
    if trace is None:
        return record
    if trace.client_request_id:
        record["client_request_id"] = trace.client_request_id
    if trace.provider_request_id:
        record["provider_request_id"] = trace.provider_request_id
    if trace.organization:
        record["organization"] = trace.organization
    if trace.processing_ms:
        record["processing_ms"] = trace.processing_ms
    if trace.api_version:
        record["api_version"] = trace.api_version
    if trace.surface:
        record["surface"] = trace.surface
    if trace.rate_limits:
        record["rate_limits"] = dict(trace.rate_limits)
    return record


def _ledger_call(
    *,
    role: str,
    prompt_id: str,
    provider: str,
    prompt_text: str,
    response_text: str,
    created_at: str,
    client_request_id: str,
    trace: LLMCallTrace | None,
) -> dict[str, Any]:
    return {
        "role": role,
        "prompt_id": prompt_id,
        "provider": provider,
        "prompt_sha256": sha256_text(prompt_text),
        "response_sha256": sha256_text(response_text),
        "response_text": response_text,
        "created_at": created_at,
        "client_request_id": (trace.client_request_id if trace and trace.client_request_id else client_request_id),
        "provider_request_id": trace.provider_request_id if trace else None,
        "http_meta": trace.as_http_meta() if trace else {},
    }


def _write_human_readme(path: Path, payload: dict[str, Any]) -> None:
    inclusions = payload["inclusions"]
    exclusions = payload["exclusions"]
    lines = [
        "# Museum archive",
        "",
        f"- Run: `{payload['run_id']}`",
        f"- Profile: `{payload['profile']}`",
        f"- Provider: `{payload['provider']}`",
        f"- Source SHA-256: `{payload['source']['sha256']}`",
        f"- Ledger: `{payload['ledger']}`",
        f"- Snapshot: `{payload['snapshot']}`",
        "",
        "## Inclusions",
        "",
    ]
    if inclusions:
        for item in inclusions:
            lines.append(f"- `{item['id']}` ({item.get('evidence')}): {item.get('text')}")
    else:
        lines.append("- None")
    lines.extend(["", "## Exclusions", ""])
    if exclusions:
        for item in exclusions:
            lines.append(f"- `{item['id']}` ({item.get('rule')}): {item.get('reason')}")
    else:
        lines.append("- None")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_manifest(output_dir: Path, current_run_id: str) -> None:
    run_ids = sorted(path.name for path in (output_dir / "runs").glob("*") if path.is_dir())
    files: dict[str, str] = {}
    for relative in (
        ARCHIVE_FILENAME,
        README_FILENAME,
        LEDGER_FILENAME,
        *[f"runs/{run_id}/{ARCHIVE_FILENAME}" for run_id in run_ids],
    ):
        path = output_dir / relative
        if path.is_file():
            files[relative] = sha256_file(path)
    manifest = {
        "schema": "forensic-archive-manifest/v1",
        "current_run_id": current_run_id,
        "runs": run_ids,
        "files": files,
    }
    manifest_path = output_dir / MANIFEST_FILENAME
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summed = dict(files)
    summed[MANIFEST_FILENAME] = sha256_file(manifest_path)
    write_sha256sums(output_dir / SHA256SUMS_FILENAME, summed)
