from __future__ import annotations

import json
from pathlib import Path

from graph_pim.cli import main

from .fakes import FIXTURES, FakeGraph, FakeResponse, load_fixture


def test_parse_fixture_prints_activatable_row(capsys) -> None:
    path = FIXTURES / "filter-by-current-user.json"
    assert main(["parse", str(path), "--activatable-only"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert len(output["value"]) == 1
    assert output["value"][0]["justification"].startswith("Assign Attribute Assignment Admin")


def test_assign_dry_run_skips_http(capsys) -> None:
    code = main(
        [
            "assign",
            "--dry-run",
            "--principal-id",
            "071cc716-8147-4397-a5ba-b2105951cc0b",
            "--role-definition-id",
            "attribute-assignment-administrator",
            "--justification",
            "Assign Attribute Assignment Admin eligibility to restricted user",
            "--start-date-time",
            "2022-04-10T00:00:00Z",
            "--end-date-time",
            "2024-04-10T00:00:00Z",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["method"] == "POST"
    assert payload["path"] == "/roleManagement/directory/roleEligibilityScheduleRequests"
    assert payload["body"] == load_fixture("admin-assign-request.json")


def test_activate_dry_run_uses_assignment_path(capsys) -> None:
    code = main(
        [
            "activate",
            "--dry-run",
            "--principal-id",
            "aaaaaaaa-bbbb-cccc-1111-222222222222",
            "--role-definition-id",
            "8424c6f0-a189-499e-bbd0-26c1753c96d4",
            "--justification",
            "need the role",
            "--start-date-time",
            "2022-04-14T00:00:00.000Z",
            "--duration",
            "PT5H",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["path"] == "/roleManagement/directory/roleAssignmentScheduleRequests"
    assert payload["body"]["action"] == "selfActivate"


def test_mine_uses_injected_client(monkeypatch, capsys) -> None:
    fake = FakeGraph()
    fake.route(
        "GET",
        "filterByCurrentUser(on='principal')",
        FakeResponse(200, load_fixture("filter-by-current-user.json")),
    )

    def fake_client(**kwargs):
        return __import__("graph_pim.client", fromlist=["GraphPimClient"]).GraphPimClient(
            token="test-token",
            opener=fake,
        )

    monkeypatch.setattr("graph_pim.cli.GraphPimClient", fake_client)
    assert main(["mine", "--activatable-only"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["value"][0]["id"] == "50d34326-f243-4540-8bb5-2af6692aafd0"


def test_parse_revoked_entity(capsys) -> None:
    path = Path(FIXTURES / "get-revoked-entity.json")
    assert main(["parse", str(path)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "Revoked"
    assert output["action"] == "adminRemove"
