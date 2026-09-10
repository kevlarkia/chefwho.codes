from __future__ import annotations

import json

import pytest

from graph_pim.client import GraphPimClient
from graph_pim.constants import ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID
from graph_pim.errors import GraphAuthError, GraphHttpError, GraphValidationError
from graph_pim.models import admin_assign_eligibility

from .fakes import FakeGraph, FakeResponse, http_error, load_fixture


def _client(fake: FakeGraph) -> GraphPimClient:
    return GraphPimClient(
        token="test-token",
        opener=fake,
        client_request_id_factory=lambda: "fixed-client-request-id",
    )


def test_filter_by_current_user_hits_official_path() -> None:
    fake = FakeGraph()
    fake.route(
        "GET",
        "filterByCurrentUser(on='principal')",
        FakeResponse(200, load_fixture("filter-by-current-user.json")),
    )
    collection = _client(fake).filter_eligibility_by_current_user()
    assert len(collection.value) == 1
    assert collection.value[0].id == "50d34326-f243-4540-8bb5-2af6692aafd0"
    request = fake.calls[0]
    assert request.get_method() == "GET"
    assert request.full_url.endswith(
        "/roleManagement/directory/roleEligibilityScheduleRequests/"
        "filterByCurrentUser(on='principal')"
    )
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request.get_header("Client-request-id") == "fixed-client-request-id"


def test_filter_by_current_user_rejects_unsupported_on() -> None:
    fake = FakeGraph()
    with pytest.raises(GraphValidationError, match="principal and approver"):
        _client(fake).filter_eligibility_by_current_user(on="createdBy")


def test_list_supports_odata_query() -> None:
    fake = FakeGraph()
    fake.route(
        "GET",
        "/roleEligibilityScheduleRequests?",
        FakeResponse(200, {"@odata.context": "x", "value": []}),
    )
    _client(fake).list_eligibility_requests(
        select="id,status,action",
        odata_filter="status eq 'Provisioned'",
        top=10,
    )
    url = fake.calls[0].full_url
    assert "$select=id,status,action" in url
    assert "$top=10" in url
    assert "$filter=" in url


def test_get_eligibility_request() -> None:
    fake = FakeGraph()
    payload = load_fixture("get-revoked-entity.json")
    fake.route(
        "GET",
        f"/roleEligibilityScheduleRequests/{payload['id']}",
        FakeResponse(200, payload),
    )
    entity = _client(fake).get_eligibility_request(payload["id"])
    assert entity.status == "Revoked"
    assert entity.action == "adminRemove"


def test_create_admin_assign_posts_official_body() -> None:
    fake = FakeGraph()
    fake.route(
        "POST",
        "/roleManagement/directory/roleEligibilityScheduleRequests",
        FakeResponse(201, load_fixture("admin-assign-response.json")),
    )
    official = load_fixture("admin-assign-request.json")
    created = _client(fake).create_eligibility_request(
        admin_assign_eligibility(
            principal_id=official["principalId"],
            role_definition_id=official["roleDefinitionId"],
            justification=official["justification"],
            directory_scope_id=official["directoryScopeId"],
            start_date_time=official["scheduleInfo"]["startDateTime"],
            end_date_time=official["scheduleInfo"]["expiration"]["endDateTime"],
        )
    )
    assert created.status == "Provisioned"
    assert created.id == "50877283-9d40-433c-bab8-7986dc10458a"
    posted = json.loads(fake.calls[0].data.decode("utf-8"))
    assert posted == official
    assert fake.calls[0].get_method() == "POST"


def test_cancel_posts_empty_body_and_accepts_204() -> None:
    fake = FakeGraph()
    request_id = "532bef1f-c677-4564-aa6f-811444a4f018"
    fake.route(
        "POST",
        f"/roleEligibilityScheduleRequests/{request_id}/cancel",
        FakeResponse(204, None),
    )
    _client(fake).cancel_eligibility_request(request_id)
    assert fake.calls[0].data is None
    assert fake.calls[0].full_url.endswith(f"{request_id}/cancel")


def test_self_activate_posts_to_assignment_endpoint() -> None:
    fake = FakeGraph()
    fake.route(
        "POST",
        "/roleManagement/directory/roleAssignmentScheduleRequests",
        FakeResponse(201, load_fixture("self-activate-response.json")),
    )
    official = load_fixture("self-activate-request.json")
    created = _client(fake).self_activate(
        principal_id=official["principalId"],
        role_definition_id=official["roleDefinitionId"],
        justification=official["justification"],
        start_date_time=official["scheduleInfo"]["startDateTime"],
        duration=official["scheduleInfo"]["expiration"]["duration"],
        ticket_number=official["ticketInfo"]["ticketNumber"],
        ticket_system=official["ticketInfo"]["ticketSystem"],
    )
    assert created.action == "selfActivate"
    assert created.status == "Granted"
    assert created.role_definition_id == ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID
    url = fake.calls[0].full_url
    assert url.endswith("/roleManagement/directory/roleAssignmentScheduleRequests")
    posted = json.loads(fake.calls[0].data.decode("utf-8"))
    assert posted["action"] == "selfActivate"
    assert posted["scheduleInfo"]["expiration"]["duration"] == "PT5H"


def test_pagination_follows_next_link() -> None:
    fake = FakeGraph()
    first = {
        "@odata.context": (
            "https://graph.microsoft.com/v1.0/$metadata"
            "#Collection(unifiedRoleEligibilityScheduleRequest)"
        ),
        "@odata.nextLink": "https://graph.microsoft.com/v1.0/roleManagement/directory/roleEligibilityScheduleRequests?$skiptoken=abc",
        "value": [load_fixture("filter-by-current-user.json")["value"][0]],
    }
    second = {
        "@odata.context": first["@odata.context"],
        "value": [load_fixture("get-revoked-entity.json")],
    }
    fake.route("GET", "$skiptoken=abc", FakeResponse(200, second))
    fake.route("GET", "/roleEligibilityScheduleRequests", FakeResponse(200, first))
    collection = _client(fake).list_eligibility_requests()
    assert len(collection.value) == 2
    assert collection.value[0].id == "50d34326-f243-4540-8bb5-2af6692aafd0"
    assert collection.value[1].id == "f341269e-c926-41fa-a905-cef3b01b2a67"
    assert collection.odata_next_link is None
    assert len(fake.calls) == 2


def test_graph_error_includes_request_ids() -> None:
    fake = FakeGraph()
    url = (
        "https://graph.microsoft.com/v1.0/roleManagement/directory/"
        "roleEligibilityScheduleRequests/filterByCurrentUser(on='principal')"
    )
    fake.route(
        "GET",
        "filterByCurrentUser",
        http_error(url, 403, load_fixture("graph-error.json")),
    )
    with pytest.raises(GraphHttpError) as exc_info:
        _client(fake).filter_eligibility_by_current_user()
    err = exc_info.value
    assert err.status == 403
    assert err.code == "AccessDenied"
    assert err.request_id == "11111111-2222-3333-4444-555555555555"
    assert err.client_request_id == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    assert "client-request-id=" in str(err)
    assert "request-id=" in str(err)


def test_missing_token_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GRAPH_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("AZURE_ACCESS_TOKEN", raising=False)
    with pytest.raises(GraphAuthError, match="GRAPH_ACCESS_TOKEN"):
        GraphPimClient()
