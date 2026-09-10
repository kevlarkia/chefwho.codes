"""Append-only SQLite ledger packaged beside the museum archive file."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LEDGER_FILENAME = "forensic_archive.sqlite"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS archive_runs (
    run_id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    finished_at TEXT NOT NULL,
    profile TEXT NOT NULL,
    provider TEXT NOT NULL,
    source_path TEXT NOT NULL,
    source_sha256 TEXT NOT NULL,
    archive_path TEXT NOT NULL,
    item_count INTEGER NOT NULL,
    exclusion_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS llm_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    role TEXT NOT NULL,
    prompt_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    prompt_sha256 TEXT NOT NULL,
    response_sha256 TEXT NOT NULL,
    response_text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES archive_runs(run_id)
);

CREATE TABLE IF NOT EXISTS inclusions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    item_json TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES archive_runs(run_id)
);

CREATE TABLE IF NOT EXISTS exclusions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    item_json TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES archive_runs(run_id)
);
"""

_IMMUTABLE_TABLES = (
    "schema_meta",
    "archive_runs",
    "llm_calls",
    "inclusions",
    "exclusions",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class ForensicLedger:
    """Single-file immutable ledger proving how an archive was generated."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.executescript(_SCHEMA)
        for table in _IMMUTABLE_TABLES:
            self._conn.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS {table}_no_update
                BEFORE UPDATE ON {table}
                BEGIN
                    SELECT RAISE(ABORT, '{table} is append-only');
                END;
                """
            )
            self._conn.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS {table}_no_delete
                BEFORE DELETE ON {table}
                BEGIN
                    SELECT RAISE(ABORT, '{table} is append-only');
                END;
                """
            )
        existing = self._conn.execute(
            "SELECT value FROM schema_meta WHERE key = 'schema_version'"
        ).fetchone()
        if existing is None:
            self._conn.execute(
                "INSERT INTO schema_meta(key, value) VALUES (?, ?)",
                ("schema_version", "1"),
            )
        self._conn.commit()

    def record_run(
        self,
        *,
        run_id: str,
        started_at: str,
        finished_at: str,
        profile: str,
        provider: str,
        source_path: str,
        source_sha256: str,
        archive_path: str,
        calls: list[dict[str, str]],
        inclusions: list[dict[str, Any]],
        exclusions: list[dict[str, Any]],
    ) -> None:
        try:
            self._conn.execute("BEGIN")
            self._conn.execute(
                """
                INSERT INTO archive_runs(
                    run_id, started_at, finished_at, profile, provider,
                    source_path, source_sha256, archive_path,
                    item_count, exclusion_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    started_at,
                    finished_at,
                    profile,
                    provider,
                    source_path,
                    source_sha256,
                    archive_path,
                    len(inclusions),
                    len(exclusions),
                ),
            )
            for call in calls:
                self._conn.execute(
                    """
                    INSERT INTO llm_calls(
                        run_id, role, prompt_id, provider,
                        prompt_sha256, response_sha256, response_text, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        call["role"],
                        call["prompt_id"],
                        call["provider"],
                        call["prompt_sha256"],
                        call["response_sha256"],
                        call["response_text"],
                        call["created_at"],
                    ),
                )
            for item in inclusions:
                self._conn.execute(
                    "INSERT INTO inclusions(run_id, item_id, item_json) VALUES (?, ?, ?)",
                    (run_id, item["id"], json.dumps(item, sort_keys=True)),
                )
            for item in exclusions:
                self._conn.execute(
                    "INSERT INTO exclusions(run_id, item_id, item_json) VALUES (?, ?, ?)",
                    (run_id, item["id"], json.dumps(item, sort_keys=True)),
                )
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise

    def run_count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) AS n FROM archive_runs").fetchone()
        return int(row["n"])

    def fetch_run(self, run_id: str) -> sqlite3.Row | None:
        return self._conn.execute(
            "SELECT * FROM archive_runs WHERE run_id = ?", (run_id,)
        ).fetchone()

    def fetch_exclusions(self, run_id: str) -> list[sqlite3.Row]:
        return list(
            self._conn.execute(
                "SELECT * FROM exclusions WHERE run_id = ? ORDER BY id", (run_id,)
            )
        )

    def close(self) -> None:
        self._conn.close()
