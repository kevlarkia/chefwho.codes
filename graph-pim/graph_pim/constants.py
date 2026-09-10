"""Official Microsoft Graph v1.0 PIM directory-role paths and sample IDs."""

from __future__ import annotations

DEFAULT_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
DEFAULT_TIMEOUT_SECONDS = 30.0

ELIGIBILITY_REQUESTS_PATH = "/roleManagement/directory/roleEligibilityScheduleRequests"
ASSIGNMENT_REQUESTS_PATH = "/roleManagement/directory/roleAssignmentScheduleRequests"

# Least privileged Graph permission for these APIs.
LEAST_PRIVILEGED_SCOPE = "RoleEligibilitySchedule.ReadWrite.Directory"
HIGHER_PRIVILEGED_SCOPE = "RoleManagement.ReadWrite.Directory"

# Built-in Microsoft Entra role used in the official PIM samples.
# https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference
ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID = "8424c6f0-a189-499e-bbd0-26c1753c96d4"

WELL_KNOWN_DIRECTORY_ROLES = {
    "attribute-assignment-administrator": ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID,
}

ODATA_TYPE_ELIGIBILITY_REQUEST = (
    "#microsoft.graph.unifiedRoleEligibilityScheduleRequest"
)
ODATA_TYPE_ASSIGNMENT_REQUEST = (
    "#microsoft.graph.unifiedRoleAssignmentScheduleRequest"
)

COLLECTION_CONTEXT_SUFFIX = "Collection(unifiedRoleEligibilityScheduleRequest)"
ENTITY_CONTEXT_SUFFIX = "roleEligibilityScheduleRequests/$entity"

FILTER_BY_CURRENT_USER_OPTIONS = frozenset({"principal", "approver"})
ALL_FILTER_BY_CURRENT_USER_OPTIONS = frozenset(
    {"principal", "createdBy", "approver", "unknownFutureValue"}
)

# unifiedRoleScheduleRequestActions
ELIGIBILITY_ACTIONS = frozenset(
    {
        "adminAssign",
        "adminUpdate",
        "adminRemove",
        "selfActivate",
        "selfDeactivate",
        "adminExtend",
        "adminRenew",
        "selfExtend",
        "selfRenew",
        "unknownFutureValue",
    }
)

# expirationPatternType (Graph JSON is camelCase; some how-to samples use PascalCase)
EXPIRATION_TYPES = frozenset(
    {
        "notSpecified",
        "noExpiration",
        "afterDateTime",
        "afterDuration",
        "unknownFutureValue",
    }
)

ACTIVATABLE_STATUSES = frozenset({"Provisioned"})
CANCELABLE_STATUSES = frozenset({"Granted"})
