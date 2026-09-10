import json
import sqlite3
from pathlib import Path

from forensic_archive.hashes import sha256_file
from forensic_archive.pipeline import ForensicArchiver
from forensic_archive.verify import verify_package

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def test_generic_run_packages_ledger_beside_archive(tmp_path) -> None:
    archiver = ForensicArchiver(profile="generic", provider="dummy")
    result = archiver.run(FIXTURES / "sample-source.md", tmp_path / "out")

    assert result.archive_path.is_file()
    assert result.ledger_path.is_file()
    assert result.ledger_path.name == "forensic_archive.sqlite"
    assert result.archive_path.parent == result.ledger_path.parent
    assert result.exclusions
    assert any(item["id"] for item in result.inclusions)

    archive = json.loads(result.archive_path.read_text(encoding="utf-8"))
    assert archive["ledger"] == "forensic_archive.sqlite"
    assert archive["profile"] == "generic"
    excluded_ids = {item["id"] for item in archive["exclusions"]}
    included_ids = {item["id"] for item in archive["inclusions"]}
    assert excluded_ids.isdisjoint(included_ids)

    conn = sqlite3.connect(result.ledger_path)
    row = conn.execute(
        "SELECT item_count, exclusion_count FROM archive_runs WHERE run_id = ?",
        (result.run_id,),
    ).fetchone()
    assert row == (len(result.inclusions), len(result.exclusions))
    roles = {
        item[0]
        for item in conn.execute(
            "SELECT role FROM llm_calls WHERE run_id = ?", (result.run_id,)
        )
    }
    assert roles == {"primary_extraction", "secondary_validation"}
    assert archive["llm"]["primary_extraction"]["client_request_id"].endswith(":primary")
    client_ids = [
        item[0]
        for item in conn.execute(
            "SELECT client_request_id FROM llm_calls WHERE run_id = ? ORDER BY id",
            (result.run_id,),
        )
    ]
    assert client_ids == [
        archive["llm"]["primary_extraction"]["client_request_id"],
        archive["llm"]["secondary_validation"]["client_request_id"],
    ]
    conn.close()


def test_swm_profile_is_available_and_labels_items(tmp_path) -> None:
    archiver = ForensicArchiver(profile="swm", provider="dummy")
    result = archiver.run(FIXTURES / "swm-source.md", tmp_path / "swm-out")
    assert result.profile == "swm"
    assert any(item.get("evidence") == "VERBATIM" for item in result.inclusions)
    assert any(item.get("rule") == "placeholder" for item in result.exclusions)
    assert (tmp_path / "swm-out" / "ARCHIVE.md").is_file()
    assert result.verification is not None
    assert result.verification.ok
    assert result.snapshot_path.is_file()


def test_verify_does_not_mutate_ledger(tmp_path) -> None:
    result = ForensicArchiver(profile="generic", provider="dummy").run(
        FIXTURES / "sample-source.md", tmp_path / "out"
    )
    before = sha256_file(result.ledger_path)
    report = verify_package(result.output_dir)
    assert report.ok
    assert sha256_file(result.ledger_path) == before
    assert report.checks.get("client_request_id_primary_extraction") is True
