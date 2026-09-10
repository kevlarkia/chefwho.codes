"""Microsoft Graph PIM v1.0 client for unifiedRoleEligibilityScheduleRequest."""

from .client import GraphPimClient, resolve_access_token
from .constants import (
    ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID,
    ELIGIBILITY_REQUESTS_PATH,
    WELL_KNOWN_DIRECTORY_ROLES,
)
from .errors import GraphAuthError, GraphHttpError, GraphPimError, GraphValidationError
from .models import (
    RoleScheduleRequestCollection,
    UnifiedRoleEligibilityScheduleRequest,
    UnifiedRoleScheduleRequest,
    admin_assign_eligibility,
    admin_remove_eligibility,
    parse_graph_payload,
    self_activate_assignment,
)

__all__ = [
    "ATTRIBUTE_ASSIGNMENT_ADMINISTRATOR_ID",
    "ELIGIBILITY_REQUESTS_PATH",
    "GraphAuthError",
    "GraphHttpError",
    "GraphPimClient",
    "GraphPimError",
    "GraphValidationError",
    "RoleScheduleRequestCollection",
    "UnifiedRoleEligibilityScheduleRequest",
    "UnifiedRoleScheduleRequest",
    "WELL_KNOWN_DIRECTORY_ROLES",
    "admin_assign_eligibility",
    "admin_remove_eligibility",
    "parse_graph_payload",
    "resolve_access_token",
    "self_activate_assignment",
]
