"""Independent verification of a packaged museum archive."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .errors import MuseumIntegrityError
from .hashes import read_sha256sums, sha256_file, sha256_text
from .ledger import LEDGER_FILENAME, ForensicLedger

ARCHIVE_FILENAME = "archive.json"
MANIFEST_FILENAME = "MANIFEST.json"
SHA256SUMS_FILENAME = "SHA256SUMS"
README_FILENAME = "ARCHIVE.md"


@dataclass
class VerificationReport:
    ok: bool
    run_id: str | None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)

    def raise_if_failed(self) -> None:
        if not self.ok:
            detail = "; ".join(self.errors) or "package failed verification"
            raise MuseumIntegrityError(detail)


def _check(report: VerificationReport, name: str, passed: bool, error: str | None = None) -> None:
    report.checks[name] = passed
    if not passed and error:
        report.errors.append(error)


def verify_package(output_dir: Path, *, run_id: str | None = None) -> VerificationReport:
    output_dir = Path(output_dir)
    report = VerificationReport(ok=True, run_id=run_id)
    archive_path = output_dir / ARCHIVE_FILENAME
    ledger_path = output_dir / LEDGER_FILENAME
    manifest_path = output_dir / MANIFEST_FILENAME
    sums_path = output_dir / SHA256SUMS_FILENAME

    if not archive_path.is_file():
        _check(report, "archive_present", False, f"missing {ARCHIVE_FILENAME}")
        report.ok = False
        return report
    if not ledger_path.is_file():
        _check(report, "ledger_present", False, f"missing {LEDGER_FILENAME}")
        report.ok = False
        return report

    try:
        archive = json.loads(archive_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _check(report, "archive_json", False, f"archive.json is not valid JSON: {exc}")
        report.ok = False
        return report

    current_id = str(run_id or archive.get("run_id") or "")
    report.run_id = current_id or None
    _check(report, "archive_json", True)

    ledger = ForensicLedger(ledger_path, migrate=False)
    try:
        _verify_ledger(report, ledger, archive, current_id, archive_path)
        _verify_snapshots(report, output_dir, ledger)
    finally:
        ledger.close()

    if manifest_path.is_file():
        _verify_manifest(report, output_dir, manifest_path, current_id)
    else:
        _check(report, "manifest_present", False, f"missing {MANIFEST_FILENAME}")

    if sums_path.is_file():
        _verify_sums(report, output_dir, sums_path)
    else:
        _check(report, "sha256sums_present", False, f"missing {SHA256SUMS_FILENAME}")

    report.ok = not report.errors
    return report


def _verify_ledger(
    report: VerificationReport,
    ledger: ForensicLedger,
    archive: dict[str, Any],
    run_id: str,
    archive_path: Path,
) -> None:
    _check(
        report,
        "foreign_keys",
        ledger.foreign_keys_enabled(),
        "SQLite foreign_keys pragma is off",
    )
    expected_triggers = {
        f"{table}_no_update" for table in ("schema_meta", "archive_runs", "llm_calls", "inclusions", "exclusions")
    } | {
        f"{table}_no_delete" for table in ("schema_meta", "archive_runs", "llm_calls", "inclusions", "exclusions")
    }
    present = ledger.trigger_names()
    _check(
        report,
        "append_only_triggers",
        expected_triggers <= present,
        f"missing immutability triggers: {sorted(expected_triggers - present)}",
    )

    if not run_id:
        _check(report, "run_id", False, "archive.json has no run_id")
        return
    row = ledger.fetch_run(run_id)
    if row is None:
        _check(report, "ledger_run", False, f"run {run_id} is not in the ledger")
        return
    _check(report, "ledger_run", True)

    _check(
        report,
        "source_hash",
        archive.get("source", {}).get("sha256") == row["source_sha256"],
        "archive source sha256 does not match ledger",
    )
    _check(
        report,
        "profile",
        archive.get("profile") == row["profile"],
        "archive profile does not match ledger",
    )
    archive_sha = sha256_file(archive_path)
    snapshot = archive.get("snapshot")
    if snapshot:
        snapshot_path = archive_path.parent / snapshot
        if snapshot_path.is_file():
            archive_sha = sha256_file(snapshot_path)
            _check(
                report,
                "snapshot_matches_head",
                snapshot_path.read_bytes() == archive_path.read_bytes(),
                "current archive.json does not match the immutable run snapshot",
            )
        else:
            _check(report, "snapshot_present", False, f"missing snapshot {snapshot}")
    _check(
        report,
        "archive_hash",
        archive_sha == row["archive_sha256"],
        "archive sha256 does not match ledger.archive_sha256",
    )

    inclusions = [json.loads(item["item_json"]) for item in ledger.fetch_inclusions(run_id)]
    exclusions = [json.loads(item["item_json"]) for item in ledger.fetch_exclusions(run_id)]
    _check(
        report,
        "inclusion_count",
        len(inclusions) == len(archive.get("inclusions") or []) == row["item_count"],
        "inclusion counts disagree between archive and ledger",
    )
    _check(
        report,
        "exclusion_count",
        len(exclusions) == len(archive.get("exclusions") or []) == row["exclusion_count"],
        "exclusion counts disagree between archive and ledger",
    )
    _check(
        report,
        "inclusion_ids",
        {item["id"] for item in inclusions} == {item["id"] for item in archive.get("inclusions") or []},
        "inclusion ids disagree between archive and ledger",
    )
    overlap = {item["id"] for item in inclusions} & {item["id"] for item in exclusions}
    _check(report, "no_id_overlap", not overlap, f"ids present in both sets: {sorted(overlap)}")

    dangling = json.loads(row["dangling_exclusion_ids_json"])
    _check(
        report,
        "no_dangling_exclusions",
        dangling == [],
        f"dangling exclusion ids: {dangling}",
    )

    calls = ledger.fetch_calls(run_id)
    roles = [call["role"] for call in calls]
    _check(
        report,
        "llm_roles",
        roles == ["primary_extraction", "secondary_validation"],
        f"unexpected LLM call roles: {roles}",
    )
    llm_meta = archive.get("llm") if isinstance(archive.get("llm"), dict) else {}
    for call in calls:
        recomputed = sha256_text(call["response_text"])
        if recomputed != call["response_sha256"]:
            _check(
                report,
                f"response_hash_{call['role']}",
                False,
                f"{call['role']} response_text does not match stored sha256",
            )
        else:
            _check(report, f"response_hash_{call['role']}", True)
        keys = set(call.keys())
        if "client_request_id" in keys and llm_meta:
            expected = (llm_meta.get(call["role"]) or {}).get("client_request_id")
            stored = call["client_request_id"]
            if expected and stored and expected != stored:
                _check(
                    report,
                    f"client_request_id_{call['role']}",
                    False,
                    f"{call['role']} X-Client-Request-Id disagrees between archive and ledger",
                )
            elif expected or stored:
                _check(report, f"client_request_id_{call['role']}", True)


def _verify_snapshots(report: VerificationReport, output_dir: Path, ledger: ForensicLedger) -> None:
    for stored_id in ledger.list_run_ids():
        snapshot = output_dir / "runs" / stored_id / ARCHIVE_FILENAME
        row = ledger.fetch_run(stored_id)
        if not snapshot.is_file():
            _check(report, f"snapshot_{stored_id}", False, f"missing snapshot for {stored_id}")
            continue
        digest = sha256_file(snapshot)
        _check(
            report,
            f"snapshot_hash_{stored_id}",
            bool(row) and digest == row["archive_sha256"],
            f"snapshot hash mismatch for {stored_id}",
        )


def _verify_manifest(
    report: VerificationReport, output_dir: Path, manifest_path: Path, run_id: str
) -> None:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _check(report, "manifest_json", False, f"MANIFEST.json is not valid JSON: {exc}")
        return
    _check(report, "manifest_present", True)
    if run_id and manifest.get("current_run_id") != run_id:
        report.warnings.append(
            f"MANIFEST current_run_id {manifest.get('current_run_id')} != archive run {run_id}"
        )
    files = manifest.get("files") or {}
    for relative, expected in files.items():
        path = output_dir / relative
        if not path.is_file():
            _check(report, f"manifest_{relative}", False, f"MANIFEST lists missing file {relative}")
            continue
        actual = sha256_file(path)
        _check(
            report,
            f"manifest_{relative}",
            actual == expected,
            f"MANIFEST hash mismatch for {relative}",
        )


def _verify_sums(report: VerificationReport, output_dir: Path, sums_path: Path) -> None:
    _check(report, "sha256sums_present", True)
    listed = read_sha256sums(sums_path)
    for relative, expected in listed.items():
        path = output_dir / relative
        if not path.is_file():
            _check(report, f"sum_{relative}", False, f"SHA256SUMS lists missing file {relative}")
            continue
        actual = sha256_file(path)
        _check(
            report,
            f"sum_{relative}",
            actual == expected,
            f"SHA256SUMS mismatch for {relative}",
        )
