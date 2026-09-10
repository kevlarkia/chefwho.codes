"""Append-only SQLite ledger packaged beside the museum archive file."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LEDGER_FILENAME = "forensic_archive.sqlite"
SCHEMA_VERSION = "3"
LLM_HTTP_COLUMNS = (
    ("client_request_id", "TEXT"),
    ("provider_request_id", "TEXT"),
    ("http_meta_json", "TEXT"),
)

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
    archive_sha256 TEXT NOT NULL,
    prompt_template_sha256 TEXT NOT NULL,
    profile_sha256 TEXT NOT NULL,
    extracted_ids_json TEXT NOT NULL,
    dangling_exclusion_ids_json TEXT NOT NULL,
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
    client_request_id TEXT,
    provider_request_id TEXT,
    http_meta_json TEXT,
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

    def __init__(self, path: Path, *, migrate: bool = True) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, timeout=30)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.execute("PRAGMA journal_mode = DELETE")
        self._conn.execute("PRAGMA synchronous = FULL")
        self._init_schema(migrate=migrate)

    def _init_schema(self, *, migrate: bool) -> None:
        self._conn.executescript(_SCHEMA)
        self._conn.execute("PRAGMA foreign_keys = ON")
        if migrate:
            self._ensure_llm_http_columns()
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
                ("schema_version", SCHEMA_VERSION),
            )
        self._conn.commit()

    def _table_columns(self, table: str) -> set[str]:
        rows = self._conn.execute(f"PRAGMA table_info({table})").fetchall()
        return {row[1] for row in rows}

    def _ensure_llm_http_columns(self) -> None:
        columns = self._table_columns("llm_calls")
        for name, decl in LLM_HTTP_COLUMNS:
            if name not in columns:
                self._conn.execute(f"ALTER TABLE llm_calls ADD COLUMN {name} {decl}")

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
        archive_sha256: str,
        prompt_template_sha256: str,
        profile_sha256: str,
        extracted_ids: list[str],
        dangling_exclusion_ids: list[str],
        calls: list[dict[str, Any]],
        inclusions: list[dict[str, Any]],
        exclusions: list[dict[str, Any]],
    ) -> None:
        try:
            self._conn.execute(
                """
                INSERT INTO archive_runs(
                    run_id, started_at, finished_at, profile, provider,
                    source_path, source_sha256, archive_path, archive_sha256,
                    prompt_template_sha256, profile_sha256,
                    extracted_ids_json, dangling_exclusion_ids_json,
                    item_count, exclusion_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    archive_sha256,
                    prompt_template_sha256,
                    profile_sha256,
                    json.dumps(extracted_ids),
                    json.dumps(dangling_exclusion_ids),
                    len(inclusions),
                    len(exclusions),
                ),
            )
            http_columns = self._table_columns("llm_calls")
            for call in calls:
                meta = call.get("http_meta")
                http_meta_json = (
                    json.dumps(meta, sort_keys=True) if isinstance(meta, dict) and meta else None
                )
                if {"client_request_id", "provider_request_id", "http_meta_json"} <= http_columns:
                    self._conn.execute(
                        """
                        INSERT INTO llm_calls(
                            run_id, role, prompt_id, provider,
                            prompt_sha256, response_sha256, response_text, created_at,
                            client_request_id, provider_request_id, http_meta_json
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                            call.get("client_request_id"),
                            call.get("provider_request_id"),
                            http_meta_json,
                        ),
                    )
                else:
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

    def list_run_ids(self) -> list[str]:
        rows = self._conn.execute(
            "SELECT run_id FROM archive_runs ORDER BY started_at, run_id"
        ).fetchall()
        return [row["run_id"] for row in rows]

    def fetch_run(self, run_id: str) -> sqlite3.Row | None:
        return self._conn.execute(
            "SELECT * FROM archive_runs WHERE run_id = ?", (run_id,)
        ).fetchone()

    def fetch_calls(self, run_id: str) -> list[sqlite3.Row]:
        return list(
            self._conn.execute(
                "SELECT * FROM llm_calls WHERE run_id = ? ORDER BY id", (run_id,)
            )
        )

    def fetch_inclusions(self, run_id: str) -> list[sqlite3.Row]:
        return list(
            self._conn.execute(
                "SELECT * FROM inclusions WHERE run_id = ? ORDER BY id", (run_id,)
            )
        )

    def fetch_exclusions(self, run_id: str) -> list[sqlite3.Row]:
        return list(
            self._conn.execute(
                "SELECT * FROM exclusions WHERE run_id = ? ORDER BY id", (run_id,)
            )
        )

    def trigger_names(self) -> set[str]:
        rows = self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'trigger'"
        ).fetchall()
        return {row["name"] for row in rows}

    def foreign_keys_enabled(self) -> bool:
        row = self._conn.execute("PRAGMA foreign_keys").fetchone()
        return bool(row[0]) if row is not None else False

    def close(self) -> None:
        self._conn.close()
