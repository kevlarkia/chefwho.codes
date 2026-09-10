"""Two-pass archive generation: extract, validate, ledger, package."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .ledger import LEDGER_FILENAME, ForensicLedger, utc_now
from .llm import LLMClient, client_from_env
from .parse import exclusion_ids, parse_exclusions, parse_items
from .prompts import (
    PRIMARY_PROMPT_ID,
    SECONDARY_PROMPT_ID,
    ArchiveProfile,
    load_profile,
    render_primary_prompt,
    render_secondary_prompt,
)

ARCHIVE_FILENAME = "archive.json"
README_FILENAME = "ARCHIVE.md"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass
class ArchiveResult:
    run_id: str
    output_dir: Path
    archive_path: Path
    ledger_path: Path
    inclusions: list[dict[str, Any]]
    exclusions: list[dict[str, Any]]
    provider: str
    profile: str
    primary_response: str
    secondary_response: str
    source_sha256: str
    extra: dict[str, Any] = field(default_factory=dict)


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

    def primary_extraction_call(self, source_text: str) -> str:
        """TEMP-ARC-001. Swap the client to use Anthropic, OpenAI, or Vertex."""
        prompt = render_primary_prompt(source_text, self.profile)
        return self.client.complete(prompt, system=self.profile.addendum)

    def secondary_validation_call(self, extraction: str, source_text: str) -> str:
        """TEMP-ARC-002. Response must end with an `exclusions` JSON array."""
        prompt = render_secondary_prompt(source_text, extraction, self.profile)
        return self.client.complete(prompt, system=self.profile.addendum)

    def run(self, source: Path, output_dir: Path) -> ArchiveResult:
        source = Path(source)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        source_text = source.read_text(encoding="utf-8")
        source_sha256 = sha256_file(source)
        started_at = utc_now()
        run_id = str(uuid.uuid4())

        primary = self.primary_extraction_call(source_text)
        secondary = self.secondary_validation_call(primary, source_text)
        items = parse_items(primary)
        exclusions = parse_exclusions(secondary)
        dropped = exclusion_ids(exclusions)
        inclusions = [item for item in items if item["id"] not in dropped]
        finished_at = utc_now()

        archive_path = output_dir / ARCHIVE_FILENAME
        ledger_path = output_dir / LEDGER_FILENAME
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
            "inclusions": inclusions,
            "exclusions": exclusions,
            "ledger": LEDGER_FILENAME,
        }
        archive_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        _write_human_readme(output_dir / README_FILENAME, payload)

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
                archive_path=str(archive_path),
                calls=[
                    {
                        "role": "primary_extraction",
                        "prompt_id": PRIMARY_PROMPT_ID,
                        "provider": self.client.name,
                        "prompt_sha256": sha256_text(
                            render_primary_prompt(source_text, self.profile)
                        ),
                        "response_sha256": sha256_text(primary),
                        "response_text": primary,
                        "created_at": started_at,
                    },
                    {
                        "role": "secondary_validation",
                        "prompt_id": SECONDARY_PROMPT_ID,
                        "provider": self.client.name,
                        "prompt_sha256": sha256_text(
                            render_secondary_prompt(source_text, primary, self.profile)
                        ),
                        "response_sha256": sha256_text(secondary),
                        "response_text": secondary,
                        "created_at": finished_at,
                    },
                ],
                inclusions=inclusions,
                exclusions=exclusions,
            )
        finally:
            ledger.close()

        return ArchiveResult(
            run_id=run_id,
            output_dir=output_dir,
            archive_path=archive_path,
            ledger_path=ledger_path,
            inclusions=inclusions,
            exclusions=exclusions,
            provider=self.client.name,
            profile=self.profile.id,
            primary_response=primary,
            secondary_response=secondary,
            source_sha256=source_sha256,
        )


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
