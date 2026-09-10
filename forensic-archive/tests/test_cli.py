import json
from pathlib import Path

from forensic_archive.cli import main

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def test_cli_archive_and_providers(tmp_path, capsys) -> None:
    assert main(["providers"]) == 0
    listed = capsys.readouterr().out.splitlines()
    assert listed == ["dummy", "anthropic", "openai", "vertex"]

    output = tmp_path / "packaged"
    code = main(
        [
            "archive",
            str(FIXTURES / "sample-source.md"),
            "--output",
            str(output),
            "--provider",
            "dummy",
        ]
    )
    assert code == 0
    summary = json.loads(capsys.readouterr().out)
    assert (output / "archive.json").is_file()
    assert (output / "forensic_archive.sqlite").is_file()
    assert summary["provider"] == "dummy"
    assert summary["exclusions"] >= 1
    assert summary["ok"] is True
    assert summary["verified"] is True
    assert (output / "MANIFEST.json").is_file()
    assert (output / "SHA256SUMS").is_file()
    assert main(["verify", str(output)]) == 0
    verify = json.loads(capsys.readouterr().out)
    assert verify["ok"] is True
