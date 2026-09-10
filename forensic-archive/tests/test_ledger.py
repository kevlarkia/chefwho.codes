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


def test_ledger_stores_openai_request_ids(tmp_path) -> None:
    ledger = ForensicLedger(tmp_path / "forensic_archive.sqlite")
    ledger.record_run(
        run_id="run-http",
        started_at="2026-09-10T00:00:00+00:00",
        finished_at="2026-09-10T00:00:01+00:00",
        profile="generic",
        provider="openai",
        source_path="source.md",
        source_sha256="abc",
        archive_path="runs/run-http/archive.json",
        archive_sha256="def",
        prompt_template_sha256="aaa",
        profile_sha256="bbb",
        extracted_ids=["EXT-001"],
        dangling_exclusion_ids=[],
        calls=[
            {
                "role": "primary_extraction",
                "prompt_id": "TEMP-ARC-001",
                "provider": "openai",
                "prompt_sha256": "p",
                "response_sha256": "r",
                "response_text": "ok",
                "created_at": "2026-09-10T00:00:00+00:00",
                "client_request_id": "run-http:primary",
                "provider_request_id": "req_abc",
                "http_meta": {"surface": "responses", "openai-version": "2020-10-01"},
            }
        ],
        inclusions=[{"id": "EXT-001", "text": "kept"}],
        exclusions=[],
    )
    row = ledger.fetch_calls("run-http")[0]
    assert row["client_request_id"] == "run-http:primary"
    assert row["provider_request_id"] == "req_abc"
    assert "responses" in row["http_meta_json"]
    version = ledger._conn.execute(
        "SELECT value FROM schema_meta WHERE key = 'schema_version'"
    ).fetchone()[0]
    assert version == "3"
    ledger.close()


def test_verify_open_does_not_alter_v2_columns(tmp_path) -> None:
    path = tmp_path / "legacy.sqlite"
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE archive_runs (
            run_id TEXT PRIMARY KEY, started_at TEXT, finished_at TEXT,
            profile TEXT, provider TEXT, source_path TEXT, source_sha256 TEXT,
            archive_path TEXT, archive_sha256 TEXT, prompt_template_sha256 TEXT,
            profile_sha256 TEXT, extracted_ids_json TEXT,
            dangling_exclusion_ids_json TEXT, item_count INTEGER, exclusion_count INTEGER
        );
        CREATE TABLE llm_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, role TEXT,
            prompt_id TEXT, provider TEXT, prompt_sha256 TEXT,
            response_sha256 TEXT, response_text TEXT, created_at TEXT
        );
        CREATE TABLE inclusions (id INTEGER PRIMARY KEY, run_id TEXT, item_id TEXT, item_json TEXT);
        CREATE TABLE exclusions (id INTEGER PRIMARY KEY, run_id TEXT, item_id TEXT, item_json TEXT);
        INSERT INTO schema_meta(key, value) VALUES ('schema_version', '2');
        """
    )
    conn.commit()
    conn.close()
    opened = ForensicLedger(path, migrate=False)
    columns = {row[1] for row in opened._conn.execute("PRAGMA table_info(llm_calls)")}
    assert "client_request_id" not in columns
    opened.close()
    mutated = ForensicLedger(path, migrate=True)
    columns = {row[1] for row in mutated._conn.execute("PRAGMA table_info(llm_calls)")}
    assert "client_request_id" in columns
    mutated.close()
