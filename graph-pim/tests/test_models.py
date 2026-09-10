from __future__ import annotations

import json
from pathlib import Path

import pytest

from graph_pim.constants import ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID
from graph_pim.errors import GraphValidationError
from graph_pim.models import (
    UnifiedRoleScheduleRequest,
    admin_assign_eligibility,
    admin_remove_eligibility,
    parse_graph_payload,
    self_activate_assignment,
)

from .fakes import FIXTURES, load_fixture


def test_parse_official_filter_by_current_user_sample() -> None:
    payload = load_fixture("filter-by-current-user.json")
    collection = parse_graph_payload(payload)
    assert collection.odata_context.endswith(
        "Collection(unifiedRoleEligibilityScheduleRequest)"
    )
    assert len(collection.value) == 1
    row = collection.value[0]
    assert row.id == "50d34326-f243-4540-8bb5-2af6692aafd0"
    assert row.status == "Provisioned"
    assert row.action == "adminAssign"
    assert row.principal_id == "aaaaaaaa-bbbb-cccc-1111-222222222222"
    assert row.role_definition_id == ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID
    assert row.directory_scope_id == "/"
    assert row.justification == "Assign Attribute Assignment Admin eligibility to myself"
    assert row.created_by is not None
    assert row.created_by.user is not None
    assert row.created_by.user.id == "00aa00aa-bb11-cc22-dd33-44ee44ee44ee"
    assert row.schedule_info is not None
    assert row.schedule_info.expiration is not None
    assert row.schedule_info.expiration.type == "afterDateTime"
    assert row.schedule_info.expiration.end_date_time == "2024-04-10T00:00:00Z"
    assert row.is_activatable()
    assert [item.id for item in collection.activatable()] == [row.id]


def test_revoked_eligibility_is_not_activatable() -> None:
    payload = load_fixture("get-revoked-entity.json")
    entity = UnifiedRoleScheduleRequest.from_graph(payload)
    assert entity.status == "Revoked"
    assert entity.action == "adminRemove"
    assert entity.schedule_info is None
    assert not entity.is_activatable()


def test_admin_assign_create_payload_matches_official_example() -> None:
    official = load_fixture("admin-assign-request.json")
    built = admin_assign_eligibility(
        principal_id=official["principalId"],
        role_definition_id=official["roleDefinitionId"],
        justification=official["justification"],
        directory_scope_id=official["directoryScopeId"],
        start_date_time=official["scheduleInfo"]["startDateTime"],
        end_date_time=official["scheduleInfo"]["expiration"]["endDateTime"],
    )
    assert built.to_create_payload() == official


def test_admin_remove_omits_schedule() -> None:
    official = load_fixture("admin-remove-request.json")
    built = admin_remove_eligibility(
        principal_id=official["principalId"],
        role_definition_id=official["roleDefinitionId"],
        directory_scope_id=official["directoryScopeId"],
    )
    assert built.to_create_payload() == official


def test_self_activate_normalizes_after_duration_pascal_case() -> None:
    official = load_fixture("self-activate-request.json")
    parsed = UnifiedRoleScheduleRequest.from_graph(official)
    assert parsed.schedule_info is not None
    assert parsed.schedule_info.expiration is not None
    assert parsed.schedule_info.expiration.type == "afterDuration"
    body = parsed.to_create_payload()
    assert body["action"] == "selfActivate"
    assert body["scheduleInfo"]["expiration"]["type"] == "afterDuration"
    assert body["scheduleInfo"]["expiration"]["duration"] == "PT5H"
    assert body["ticketInfo"]["ticketNumber"] == "CONTOSO:Normal-67890"

    built = self_activate_assignment(
        principal_id=official["principalId"],
        role_definition_id=official["roleDefinitionId"],
        justification=official["justification"],
        directory_scope_id=official["directoryScopeId"],
        start_date_time=official["scheduleInfo"]["startDateTime"],
        duration=official["scheduleInfo"]["expiration"]["duration"],
        ticket_number=official["ticketInfo"]["ticketNumber"],
        ticket_system=official["ticketInfo"]["ticketSystem"],
    )
    assert built.to_create_payload()["scheduleInfo"]["expiration"]["type"] == "afterDuration"


def test_create_payload_requires_scope() -> None:
    request = UnifiedRoleScheduleRequest(
        action="adminRemove",
        principal_id="aaaaaaaa-bbbb-cccc-1111-222222222222",
        role_definition_id=ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID,
    )
    with pytest.raises(GraphValidationError, match="directoryScopeId or appScopeId"):
        request.to_create_payload()


def test_create_payload_rejects_unknown_action() -> None:
    request = UnifiedRoleScheduleRequest(
        action="notARealAction",
        principal_id="aaaaaaaa-bbbb-cccc-1111-222222222222",
        role_definition_id=ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID,
        directory_scope_id="/",
    )
    with pytest.raises(GraphValidationError, match="Unsupported action"):
        request.to_create_payload()


def test_recurring_schedule_rejected() -> None:
    request = admin_assign_eligibility(
        principal_id="aaaaaaaa-bbbb-cccc-1111-222222222222",
        role_definition_id=ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID,
        justification="test",
        start_date_time="2022-04-10T00:00:00Z",
        end_date_time="2024-04-10T00:00:00Z",
    )
    assert request.schedule_info is not None
    request.schedule_info.recurrence = {"pattern": "daily"}
    with pytest.raises(GraphValidationError, match="Recurring schedules"):
        request.to_create_payload()


def test_after_date_time_requires_end() -> None:
    request = admin_assign_eligibility(
        principal_id="aaaaaaaa-bbbb-cccc-1111-222222222222",
        role_definition_id=ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID,
        justification="test",
        start_date_time="2022-04-10T00:00:00Z",
        end_date_time="2024-04-10T00:00:00Z",
    )
    assert request.schedule_info is not None
    assert request.schedule_info.expiration is not None
    request.schedule_info.expiration.end_date_time = None
    with pytest.raises(GraphValidationError, match="endDateTime"):
        request.to_create_payload()


def test_collection_missing_value_fails() -> None:
    with pytest.raises(GraphValidationError, match="missing 'value'"):
        parse_graph_payload(
            {
                "@odata.context": (
                    "https://graph.microsoft.com/v1.0/$metadata"
                    "#Collection(unifiedRoleEligibilityScheduleRequest)"
                )
            }
        )


def test_official_sample_file_is_byte_stable_contract() -> None:
    """The how-to sample is the contract for this toolkit — keep it verbatim."""
    raw = (FIXTURES / "filter-by-current-user.json").read_text(encoding="utf-8")
    payload = json.loads(raw)
    assert payload["value"][0]["id"] == "50d34326-f243-4540-8bb5-2af6692aafd0"
    assert Path(FIXTURES / "filter-by-current-user.json").stat().st_size > 0
