# Graph PIM toolkit

Operational Microsoft Graph v1.0 client for Privileged Identity Management
**directory role eligibility** requests. Guest tree in chefwho.codes — not part
of the public site.

The contract is the official PIM how-to sample: list eligibilities the signed-in
user can activate, then optionally self-activate.

- [Get eligible roles (`filterByCurrentUser`)](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-how-to-activate-role)
- [unifiedRoleEligibilityScheduleRequest](https://learn.microsoft.com/en-us/graph/api/resources/unifiedroleeligibilityschedulerequest?view=graph-rest-1.0)
- [PIM API overview](https://learn.microsoft.com/en-us/graph/api/resources/privilegedidentitymanagementv3-overview?view=graph-rest-1.0)

`fixtures/filter-by-current-user.json` is the Microsoft Learn HTTP response for:

```http
GET https://graph.microsoft.com/v1.0/roleManagement/directory/roleEligibilityScheduleRequests/filterByCurrentUser(on='principal')
```

That sample is a **Provisioned** `adminAssign` of Attribute Assignment
Administrator (`8424c6f0-a189-499e-bbd0-26c1753c96d4`) to
`aaaaaaaa-bbbb-cccc-1111-222222222222`.

## What this does not return

Graph does **not** return role eligibility granted only through group
membership from `filterByCurrentUser` on eligibility **requests**. Use
[unifiedRoleEligibilitySchedule: filterByCurrentUser](https://learn.microsoft.com/en-us/graph/api/unifiedroleeligibilityschedule-filterbycurrentuser?view=graph-rest-1.0)
if you need current schedule instances instead of request history.

## Permissions

Least privileged: `RoleEligibilitySchedule.ReadWrite.Directory`.
Higher: `RoleManagement.ReadWrite.Directory`.

Delegated calls also require a supported Entra role (read: Global Reader,
Security Operator, Security Reader, Security Administrator, or Privileged Role
Administrator; write: Privileged Role Administrator). Personal Microsoft
accounts are not supported.

Activation (`selfActivate`) is a
`unifiedRoleAssignmentScheduleRequest` and typically needs MFA in the session.

## Install and test

Python 3.11+. Stdlib only at runtime.

```bash
cd graph-pim
pip install -r requirements-dev.txt
pytest -q
ruff check .
```

No Graph token is required for tests. Fixtures replay the official samples.

## Auth

Copy `.env.example` and export a bearer token. This toolkit does not implement
token acquisition.

```bash
export GRAPH_ACCESS_TOKEN="$(az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv)"
```

`AZURE_ACCESS_TOKEN` is accepted as an alias. Set `GRAPH_BASE_URL` for national
clouds (include `/v1.0`).

## CLI

```bash
python -m graph_pim parse fixtures/filter-by-current-user.json --activatable-only
python -m graph_pim mine --activatable-only
python -m graph_pim list --filter "status eq 'Provisioned'"
python -m graph_pim get 50d34326-f243-4540-8bb5-2af6692aafd0
```

Writes default to dry-run JSON. Drop `--dry-run` only when you intend to POST.

```bash
python -m graph_pim assign --dry-run \
  --principal-id 071cc716-8147-4397-a5ba-b2105951cc0b \
  --role-definition-id attribute-assignment-administrator \
  --justification "Assign Attribute Assignment Admin eligibility to restricted user" \
  --start-date-time 2022-04-10T00:00:00Z \
  --end-date-time 2024-04-10T00:00:00Z

python -m graph_pim activate --dry-run \
  --principal-id aaaaaaaa-bbbb-cccc-1111-222222222222 \
  --role-definition-id 8424c6f0-a189-499e-bbd0-26c1753c96d4 \
  --justification "Need Attribute Assignment Admin for restricted AUs" \
  --start-date-time 2022-04-14T00:00:00.000Z \
  --duration PT5H
```

`--validate-only` sets `isValidationOnly` so Graph checks policy (including MFA)
without committing the request.

Cancel only works when status is `Granted`. `Provisioned` / `Failed` return
`400 Bad Request`.

## Library

```python
from graph_pim import GraphPimClient, parse_graph_payload

client = GraphPimClient.from_env()
mine = client.filter_eligibility_by_current_user(on="principal")
for row in mine.activatable():
    print(row.role_definition_id, row.target_schedule_id)
```

Every call sends `client-request-id`. Failures include Graph `request-id` and
`client-request-id` for support.

## Official endpoints

| Action | Method | Path |
| --- | --- | --- |
| Eligible roles for current user | GET | `/roleManagement/directory/roleEligibilityScheduleRequests/filterByCurrentUser(on='principal')` |
| List requests | GET | `/roleManagement/directory/roleEligibilityScheduleRequests` |
| Get request | GET | `/roleManagement/directory/roleEligibilityScheduleRequests/{id}` |
| Create assign/remove/extend | POST | `/roleManagement/directory/roleEligibilityScheduleRequests` |
| Cancel granted request | POST | `/roleManagement/directory/roleEligibilityScheduleRequests/{id}/cancel` |
| Self-activate eligible role | POST | `/roleManagement/directory/roleAssignmentScheduleRequests` |
