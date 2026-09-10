import sqlite3

import pytest

from forensic_archive.ledger import ForensicLedger


def test_ledger_is_append_only(tmp_path) -> None:
    ledger = ForensicLedger(tmp_path / "forensic_archive.sqlite")
    ledger.record_run(
        run_id="run-1",
        started_at="2026-09-10T00:00:00+00:00",
        finished_at="2026-09-10T00:00:01+00:00",
        profile="generic",
        provider="dummy",
        source_path="source.md",
        source_sha256="abc",
        archive_path="runs/run-1/archive.json",
        archive_sha256="def",
        prompt_template_sha256="aaa",
        profile_sha256="bbb",
        extracted_ids=["EXT-001", "EXT-002"],
        dangling_exclusion_ids=[],
        calls=[],
        inclusions=[{"id": "EXT-001", "text": "kept"}],
        exclusions=[{"id": "EXT-002", "reason": "thin"}],
    )
    assert ledger.run_count() == 1
    assert ledger.foreign_keys_enabled()
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        ledger._conn.execute("UPDATE archive_runs SET profile = 'x' WHERE run_id = 'run-1'")
    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        ledger._conn.execute("DELETE FROM exclusions WHERE run_id = 'run-1'")
    ledger.close()
