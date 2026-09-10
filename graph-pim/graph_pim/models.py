"""Dataclasses for unifiedRoleEligibilityScheduleRequest and related types.

Field names on the wire match Microsoft Graph v1.0 JSON (camelCase). Python
attributes are snake_case. Unknown properties are preserved so Graph can add
fields without breaking parse.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .constants import (
    ACTIVATABLE_STATUSES,
    ELIGIBILITY_ACTIONS,
    EXPIRATION_TYPES,
    ODATA_TYPE_ASSIGNMENT_REQUEST,
    ODATA_TYPE_ELIGIBILITY_REQUEST,
)
from .errors import GraphValidationError

_EXPIRATION_TYPE_ALIASES = {
    "notspecified": "notSpecified",
    "noexpiration": "noExpiration",
    "afterdatetime": "afterDateTime",
    "afterduration": "afterDuration",
    "unknownfuturevalue": "unknownFutureValue",
}


def _omit_none(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}


def normalize_expiration_type(value: str) -> str:
    """Accept official camelCase and the PascalCase used in some how-to samples."""
    key = value.replace("_", "").replace("-", "").lower()
    normalized = _EXPIRATION_TYPE_ALIASES.get(key)
    if normalized is None:
        raise GraphValidationError(
            f"Unsupported expiration type {value!r}. "
            f"Expected one of: {sorted(EXPIRATION_TYPES)}"
        )
    return normalized


@dataclass
class GraphIdentity:
    id: str | None = None
    display_name: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_graph(cls, payload: dict[str, Any] | None) -> GraphIdentity | None:
        if payload is None:
            return None
        known = {"id", "displayName"}
        extra = {key: value for key, value in payload.items() if key not in known}
        return cls(
            id=payload.get("id"),
            display_name=payload.get("displayName"),
            extra=extra,
        )

    def to_graph(self) -> dict[str, Any]:
        payload = {"id": self.id, "displayName": self.display_name, **self.extra}
        return payload


@dataclass
class IdentitySet:
    application: GraphIdentity | None = None
    device: GraphIdentity | None = None
    user: GraphIdentity | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_graph(cls, payload: dict[str, Any] | None) -> IdentitySet | None:
        if payload is None:
            return None
        known = {"application", "device", "user"}
        extra = {key: value for key, value in payload.items() if key not in known}
        return cls(
            application=GraphIdentity.from_graph(payload.get("application")),
            device=GraphIdentity.from_graph(payload.get("device")),
            user=GraphIdentity.from_graph(payload.get("user")),
            extra=extra,
        )

    def to_graph(self) -> dict[str, Any]:
        payload: dict[str, Any] = {**self.extra}
        payload["application"] = self.application.to_graph() if self.application else None
        payload["device"] = self.device.to_graph() if self.device else None
        payload["user"] = self.user.to_graph() if self.user else None
        return payload


@dataclass
class TicketInfo:
    ticket_number: str | None = None
    ticket_system: str | None = None

    @classmethod
    def from_graph(cls, payload: dict[str, Any] | None) -> TicketInfo | None:
        if payload is None:
            return None
        return cls(
            ticket_number=payload.get("ticketNumber"),
            ticket_system=payload.get("ticketSystem"),
        )

    def to_graph(self) -> dict[str, Any]:
        return {
            "ticketNumber": self.ticket_number,
            "ticketSystem": self.ticket_system,
        }

    def to_create_payload(self) -> dict[str, Any] | None:
        payload = _omit_none(self.to_graph())
        return payload or None


@dataclass
class ExpirationPattern:
    type: str | None = None
    end_date_time: str | None = None
    duration: str | None = None

    @classmethod
    def from_graph(cls, payload: dict[str, Any] | None) -> ExpirationPattern | None:
        if payload is None:
            return None
        raw_type = payload.get("type")
        normalized = (
            normalize_expiration_type(raw_type) if isinstance(raw_type, str) else raw_type
        )
        return cls(
            type=normalized,
            end_date_time=payload.get("endDateTime"),
            duration=payload.get("duration"),
        )

    def to_graph(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "endDateTime": self.end_date_time,
            "duration": self.duration,
        }

    def to_create_payload(self) -> dict[str, Any]:
        if self.type:
            normalize_expiration_type(self.type)
        payload = _omit_none(self.to_graph())
        if not payload:
            raise GraphValidationError("scheduleInfo.expiration must include a type")
        self.validate()
        return payload

    def validate(self) -> None:
        if self.type is None:
            return
        expiration_type = normalize_expiration_type(self.type)
        if expiration_type == "afterDateTime" and not self.end_date_time:
            raise GraphValidationError(
                "expiration.type afterDateTime requires expiration.endDateTime"
            )
        if expiration_type == "afterDuration" and not self.duration:
            raise GraphValidationError(
                "expiration.type afterDuration requires expiration.duration (ISO 8601)"
            )


@dataclass
class RequestSchedule:
    start_date_time: str | None = None
    recurrence: Any = None
    expiration: ExpirationPattern | None = None

    @classmethod
    def from_graph(cls, payload: dict[str, Any] | None) -> RequestSchedule | None:
        if payload is None:
            return None
        return cls(
            start_date_time=payload.get("startDateTime"),
            recurrence=payload.get("recurrence"),
            expiration=ExpirationPattern.from_graph(payload.get("expiration")),
        )

    def to_graph(self) -> dict[str, Any]:
        return {
            "startDateTime": self.start_date_time,
            "recurrence": self.recurrence,
            "expiration": self.expiration.to_graph() if self.expiration else None,
        }

    def to_create_payload(self) -> dict[str, Any]:
        if self.recurrence is not None:
            raise GraphValidationError(
                "Recurring schedules are currently unsupported by Graph PIM"
            )
        payload = _omit_none(
            {
                "startDateTime": self.start_date_time,
                "expiration": (
                    self.expiration.to_create_payload() if self.expiration else None
                ),
            }
        )
        if not payload:
            raise GraphValidationError("scheduleInfo must include startDateTime or expiration")
        return payload


@dataclass
class UnifiedRoleScheduleRequest:
    """Shared request shape for eligibility and assignment schedule requests."""

    id: str | None = None
    status: str | None = None
    created_date_time: str | None = None
    completed_date_time: str | None = None
    approval_id: str | None = None
    custom_data: str | None = None
    action: str | None = None
    principal_id: str | None = None
    role_definition_id: str | None = None
    directory_scope_id: str | None = None
    app_scope_id: str | None = None
    is_validation_only: bool | None = None
    target_schedule_id: str | None = None
    justification: str | None = None
    created_by: IdentitySet | None = None
    schedule_info: RequestSchedule | None = None
    ticket_info: TicketInfo | None = None
    odata_type: str | None = None
    odata_context: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_graph(cls, payload: dict[str, Any]) -> UnifiedRoleScheduleRequest:
        if not isinstance(payload, dict):
            raise GraphValidationError("Graph entity must be a JSON object")
        known = {
            "@odata.type",
            "@odata.context",
            "id",
            "status",
            "createdDateTime",
            "completedDateTime",
            "approvalId",
            "customData",
            "action",
            "principalId",
            "roleDefinitionId",
            "directoryScopeId",
            "appScopeId",
            "isValidationOnly",
            "targetScheduleId",
            "justification",
            "createdBy",
            "scheduleInfo",
            "ticketInfo",
        }
        extra = {key: value for key, value in payload.items() if key not in known}
        return cls(
            id=payload.get("id"),
            status=payload.get("status"),
            created_date_time=payload.get("createdDateTime"),
            completed_date_time=payload.get("completedDateTime"),
            approval_id=payload.get("approvalId"),
            custom_data=payload.get("customData"),
            action=payload.get("action"),
            principal_id=payload.get("principalId"),
            role_definition_id=payload.get("roleDefinitionId"),
            directory_scope_id=payload.get("directoryScopeId"),
            app_scope_id=payload.get("appScopeId"),
            is_validation_only=payload.get("isValidationOnly"),
            target_schedule_id=payload.get("targetScheduleId"),
            justification=payload.get("justification"),
            created_by=IdentitySet.from_graph(payload.get("createdBy")),
            schedule_info=RequestSchedule.from_graph(payload.get("scheduleInfo")),
            ticket_info=TicketInfo.from_graph(payload.get("ticketInfo")),
            odata_type=payload.get("@odata.type"),
            odata_context=payload.get("@odata.context"),
            extra=extra,
        )

    def to_graph(self) -> dict[str, Any]:
        payload: dict[str, Any] = dict(self.extra)
        if self.odata_type:
            payload["@odata.type"] = self.odata_type
        if self.odata_context:
            payload["@odata.context"] = self.odata_context
        payload.update(
            {
                "id": self.id,
                "status": self.status,
                "createdDateTime": self.created_date_time,
                "completedDateTime": self.completed_date_time,
                "approvalId": self.approval_id,
                "customData": self.custom_data,
                "action": self.action,
                "principalId": self.principal_id,
                "roleDefinitionId": self.role_definition_id,
                "directoryScopeId": self.directory_scope_id,
                "appScopeId": self.app_scope_id,
                "isValidationOnly": self.is_validation_only,
                "targetScheduleId": self.target_schedule_id,
                "justification": self.justification,
                "createdBy": self.created_by.to_graph() if self.created_by else None,
                "scheduleInfo": self.schedule_info.to_graph() if self.schedule_info else None,
                "ticketInfo": self.ticket_info.to_graph() if self.ticket_info else None,
            }
        )
        return payload

    def to_create_payload(self) -> dict[str, Any]:
        if not self.action:
            raise GraphValidationError("action is required")
        if self.action not in ELIGIBILITY_ACTIONS:
            raise GraphValidationError(
                f"Unsupported action {self.action!r}. "
                f"Expected one of: {sorted(ELIGIBILITY_ACTIONS)}"
            )
        if not self.principal_id:
            raise GraphValidationError("principalId is required")
        if not self.role_definition_id:
            raise GraphValidationError("roleDefinitionId is required")
        if not self.directory_scope_id and not self.app_scope_id:
            raise GraphValidationError(
                "Either directoryScopeId or appScopeId is required"
            )

        payload: dict[str, Any] = {
            "action": self.action,
            "principalId": self.principal_id,
            "roleDefinitionId": self.role_definition_id,
            "directoryScopeId": self.directory_scope_id,
            "appScopeId": self.app_scope_id,
            "justification": self.justification,
        }
        if self.is_validation_only is not None:
            payload["isValidationOnly"] = self.is_validation_only
        if self.schedule_info is not None:
            payload["scheduleInfo"] = self.schedule_info.to_create_payload()
        elif self.action not in {"adminRemove", "selfDeactivate"}:
            raise GraphValidationError(
                "scheduleInfo is required unless action is adminRemove or selfDeactivate"
            )
        if self.ticket_info is not None:
            ticket = self.ticket_info.to_create_payload()
            if ticket:
                payload["ticketInfo"] = ticket
        return _omit_none(payload)

    def is_activatable(self) -> bool:
        """True when this eligibility request provisioned a live schedule.

        Matches the PIM how-to: list filterByCurrentUser, then self-activate
        using principalId + roleDefinitionId from a Provisioned row.
        """
        return (
            self.status in ACTIVATABLE_STATUSES
            and bool(self.target_schedule_id)
            and self.action in {"adminAssign", "adminUpdate", "adminExtend", "adminRenew"}
        )


# Official resource name alias.
UnifiedRoleEligibilityScheduleRequest = UnifiedRoleScheduleRequest


@dataclass
class RoleScheduleRequestCollection:
    odata_context: str | None
    value: list[UnifiedRoleScheduleRequest]
    odata_next_link: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_graph(cls, payload: dict[str, Any]) -> RoleScheduleRequestCollection:
        if not isinstance(payload, dict):
            raise GraphValidationError("Graph collection must be a JSON object")
        if "value" not in payload:
            raise GraphValidationError(
                "Graph collection is missing 'value' (expected "
                "Collection(unifiedRoleEligibilityScheduleRequest))"
            )
        raw_value = payload.get("value")
        if not isinstance(raw_value, list):
            raise GraphValidationError("Graph collection 'value' must be an array")
        known = {"@odata.context", "@odata.nextLink", "value"}
        extra = {key: value for key, value in payload.items() if key not in known}
        return cls(
            odata_context=payload.get("@odata.context"),
            value=[UnifiedRoleScheduleRequest.from_graph(item) for item in raw_value],
            odata_next_link=payload.get("@odata.nextLink"),
            extra=extra,
        )

    def to_graph(self) -> dict[str, Any]:
        payload: dict[str, Any] = dict(self.extra)
        if self.odata_context is not None:
            payload["@odata.context"] = self.odata_context
        if self.odata_next_link is not None:
            payload["@odata.nextLink"] = self.odata_next_link
        payload["value"] = [item.to_graph() for item in self.value]
        return payload

    def activatable(self) -> list[UnifiedRoleScheduleRequest]:
        return [item for item in self.value if item.is_activatable()]


def parse_graph_payload(
    payload: dict[str, Any],
) -> RoleScheduleRequestCollection | UnifiedRoleScheduleRequest:
    """Parse a collection or a single request entity."""
    if not isinstance(payload, dict):
        raise GraphValidationError("Graph payload must be a JSON object")
    context = payload.get("@odata.context")
    if "value" in payload:
        return RoleScheduleRequestCollection.from_graph(payload)
    if isinstance(context, str) and "Collection(" in context:
        raise GraphValidationError(
            "Graph collection is missing 'value' (expected "
            "Collection(unifiedRoleEligibilityScheduleRequest))"
        )
    return UnifiedRoleScheduleRequest.from_graph(payload)


def admin_assign_eligibility(
    *,
    principal_id: str,
    role_definition_id: str,
    justification: str,
    directory_scope_id: str = "/",
    start_date_time: str,
    end_date_time: str,
    is_validation_only: bool | None = None,
    ticket_number: str | None = None,
    ticket_system: str | None = None,
) -> UnifiedRoleScheduleRequest:
    """Build the official adminAssign eligibility example shape."""
    ticket = None
    if ticket_number or ticket_system:
        ticket = TicketInfo(ticket_number=ticket_number, ticket_system=ticket_system)
    return UnifiedRoleScheduleRequest(
        odata_type=ODATA_TYPE_ELIGIBILITY_REQUEST,
        action="adminAssign",
        principal_id=principal_id,
        role_definition_id=role_definition_id,
        directory_scope_id=directory_scope_id,
        justification=justification,
        is_validation_only=is_validation_only,
        schedule_info=RequestSchedule(
            start_date_time=start_date_time,
            expiration=ExpirationPattern(type="afterDateTime", end_date_time=end_date_time),
        ),
        ticket_info=ticket,
    )


def admin_remove_eligibility(
    *,
    principal_id: str,
    role_definition_id: str,
    directory_scope_id: str = "/",
    justification: str | None = None,
    is_validation_only: bool | None = None,
) -> UnifiedRoleScheduleRequest:
    return UnifiedRoleScheduleRequest(
        action="adminRemove",
        principal_id=principal_id,
        role_definition_id=role_definition_id,
        directory_scope_id=directory_scope_id,
        justification=justification,
        is_validation_only=is_validation_only,
    )


def self_activate_assignment(
    *,
    principal_id: str,
    role_definition_id: str,
    justification: str,
    directory_scope_id: str = "/",
    start_date_time: str,
    duration: str,
    ticket_number: str | None = None,
    ticket_system: str | None = None,
    is_validation_only: bool | None = None,
) -> UnifiedRoleScheduleRequest:
    """Build the official PIM how-to selfActivate assignment request."""
    ticket = None
    if ticket_number or ticket_system:
        ticket = TicketInfo(ticket_number=ticket_number, ticket_system=ticket_system)
    return UnifiedRoleScheduleRequest(
        odata_type=ODATA_TYPE_ASSIGNMENT_REQUEST,
        action="selfActivate",
        principal_id=principal_id,
        role_definition_id=role_definition_id,
        directory_scope_id=directory_scope_id,
        justification=justification,
        is_validation_only=is_validation_only,
        schedule_info=RequestSchedule(
            start_date_time=start_date_time,
            expiration=ExpirationPattern(type="afterDuration", duration=duration),
        ),
        ticket_info=ticket,
    )
