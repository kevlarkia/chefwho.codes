import json
import sqlite3
from pathlib import Path

from forensic_archive.pipeline import ForensicArchiver

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
    conn.close()


def test_swm_profile_is_available_and_labels_items(tmp_path) -> None:
    archiver = ForensicArchiver(profile="swm", provider="dummy")
    result = archiver.run(FIXTURES / "swm-source.md", tmp_path / "swm-out")
    assert result.profile == "swm"
    assert any(item.get("evidence") == "VERBATIM" for item in result.inclusions)
    assert any(item.get("rule") == "placeholder" for item in result.exclusions)
    assert (tmp_path / "swm-out" / "ARCHIVE.md").is_file()
