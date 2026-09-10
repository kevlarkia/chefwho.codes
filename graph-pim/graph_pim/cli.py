"""CLI for official Graph PIM eligibility and activation requests."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any, TextIO

from .client import GraphPimClient
from .constants import WELL_KNOWN_DIRECTORY_ROLES
from .errors import GraphPimError
from .models import (
    UnifiedRoleScheduleRequest,
    admin_assign_eligibility,
    admin_remove_eligibility,
    parse_graph_payload,
    self_activate_assignment,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="graph-pim",
        description=(
            "Microsoft Graph v1.0 PIM client for unifiedRoleEligibilityScheduleRequest. "
            "Reads use GET; writes POST. Dry-run prints the JSON body and skips HTTP."
        ),
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Graph root including version (default GRAPH_BASE_URL or https://graph.microsoft.com/v1.0)",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Bearer token (default GRAPH_ACCESS_TOKEN / AZURE_ACCESS_TOKEN)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    mine = sub.add_parser(
        "mine",
        help="GET filterByCurrentUser(on=principal|approver)",
    )
    _add_odata_args(mine)
    mine.add_argument(
        "--on",
        default="principal",
        choices=("principal", "approver"),
        help="filterByCurrentUser parameter (Graph currently supports principal and approver)",
    )
    mine.add_argument(
        "--activatable-only",
        action="store_true",
        help="Keep Provisioned rows that have a targetScheduleId",
    )

    listing = sub.add_parser("list", help="GET roleEligibilityScheduleRequests")
    _add_odata_args(listing)

    get_cmd = sub.add_parser("get", help="GET roleEligibilityScheduleRequests/{id}")
    get_cmd.add_argument("id", help="unifiedRoleEligibilityScheduleRequest id")

    assign = sub.add_parser("assign", help="POST adminAssign eligibility")
    _add_identity_args(assign)
    assign.add_argument("--justification", required=True)
    assign.add_argument("--start-date-time", required=True, help="ISO-8601 start")
    assign.add_argument("--end-date-time", required=True, help="ISO-8601 end (afterDateTime)")
    _add_write_args(assign)

    remove = sub.add_parser("remove", help="POST adminRemove eligibility")
    _add_identity_args(remove)
    remove.add_argument("--justification", default=None)
    _add_write_args(remove)

    cancel = sub.add_parser(
        "cancel",
        help="POST .../{id}/cancel (status must be Granted)",
    )
    cancel.add_argument("id", help="unifiedRoleEligibilityScheduleRequest id")
    cancel.add_argument("--dry-run", action="store_true")

    activate = sub.add_parser(
        "activate",
        help="POST selfActivate on roleAssignmentScheduleRequests",
    )
    _add_identity_args(activate)
    activate.add_argument("--justification", required=True)
    activate.add_argument("--start-date-time", required=True)
    activate.add_argument(
        "--duration",
        default="PT5H",
        help="ISO-8601 duration (official sample is PT5H)",
    )
    activate.add_argument("--ticket-number", default=None)
    activate.add_argument("--ticket-system", default=None)
    _add_write_args(activate)

    parse = sub.add_parser(
        "parse",
        help="Parse a Graph JSON file (fixture or saved response) with no HTTP",
    )
    parse.add_argument("path", help="Path to JSON file")
    parse.add_argument(
        "--activatable-only",
        action="store_true",
        help="When the file is a collection, keep only activatable rows",
    )
    return parser


def _add_odata_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--select", default=None, help="OData $select")
    parser.add_argument("--filter", default=None, help="OData $filter")
    parser.add_argument("--expand", default=None, help="OData $expand")
    parser.add_argument("--top", type=int, default=None, help="OData $top")


def _add_identity_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--principal-id", required=True)
    parser.add_argument(
        "--role-definition-id",
        required=True,
        help="GUID or well-known name (attribute-assignment-administrator)",
    )
    parser.add_argument(
        "--directory-scope-id",
        default="/",
        help="Directory scope (default tenant-wide /)",
    )


def _add_write_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Set isValidationOnly true (Graph checks rules such as MFA without submitting)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request JSON and skip HTTP",
    )


def resolve_role_definition_id(value: str) -> str:
    key = value.strip().lower()
    return WELL_KNOWN_DIRECTORY_ROLES.get(key, value.strip())


def _dump(payload: Any, stream: TextIO | None = None) -> None:
    handle = sys.stdout if stream is None else stream
    json.dump(payload, handle, indent=2)
    handle.write("\n")


def _client(args: argparse.Namespace) -> GraphPimClient:
    return GraphPimClient(token=args.token, base_url=args.base_url)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return _dispatch(args)
    except GraphPimError as exc:
        print(str(exc), file=sys.stderr)
        return 2


def _dispatch(args: argparse.Namespace) -> int:
    command = args.command
    if command == "parse":
        return _parse_file(args.path, activatable_only=args.activatable_only)
    if command == "mine":
        client = _client(args)
        collection = client.filter_eligibility_by_current_user(
            on=args.on,
            select=args.select,
            odata_filter=args.filter,
            expand=args.expand,
            top=args.top,
        )
        payload = collection.to_graph()
        if args.activatable_only:
            payload["value"] = [item.to_graph() for item in collection.activatable()]
        _dump(payload)
        return 0
    if command == "list":
        client = _client(args)
        collection = client.list_eligibility_requests(
            select=args.select,
            odata_filter=args.filter,
            expand=args.expand,
            top=args.top,
        )
        _dump(collection.to_graph())
        return 0
    if command == "get":
        client = _client(args)
        entity = client.get_eligibility_request(args.id)
        _dump(entity.to_graph())
        return 0
    if command == "assign":
        request = admin_assign_eligibility(
            principal_id=args.principal_id,
            role_definition_id=resolve_role_definition_id(args.role_definition_id),
            justification=args.justification,
            directory_scope_id=args.directory_scope_id,
            start_date_time=args.start_date_time,
            end_date_time=args.end_date_time,
            is_validation_only=True if args.validate_only else None,
        )
        return _write(args, request, kind="eligibility")
    if command == "remove":
        request = admin_remove_eligibility(
            principal_id=args.principal_id,
            role_definition_id=resolve_role_definition_id(args.role_definition_id),
            directory_scope_id=args.directory_scope_id,
            justification=args.justification,
            is_validation_only=True if args.validate_only else None,
        )
        return _write(args, request, kind="eligibility")
    if command == "cancel":
        if args.dry_run:
            _dump(
                {
                    "method": "POST",
                    "path": (
                        "/roleManagement/directory/roleEligibilityScheduleRequests/"
                        f"{args.id}/cancel"
                    ),
                }
            )
            return 0
        client = _client(args)
        client.cancel_eligibility_request(args.id)
        _dump({"status": "cancelled", "id": args.id})
        return 0
    if command == "activate":
        request = self_activate_assignment(
            principal_id=args.principal_id,
            role_definition_id=resolve_role_definition_id(args.role_definition_id),
            justification=args.justification,
            directory_scope_id=args.directory_scope_id,
            start_date_time=args.start_date_time,
            duration=args.duration,
            ticket_number=args.ticket_number,
            ticket_system=args.ticket_system,
            is_validation_only=True if args.validate_only else None,
        )
        return _write(args, request, kind="assignment")
    raise GraphPimError(f"Unknown command {command}")


def _write(args: argparse.Namespace, request: UnifiedRoleScheduleRequest, *, kind: str) -> int:
    body = request.to_create_payload()
    if args.dry_run:
        path = (
            "/roleManagement/directory/roleEligibilityScheduleRequests"
            if kind == "eligibility"
            else "/roleManagement/directory/roleAssignmentScheduleRequests"
        )
        _dump({"method": "POST", "path": path, "body": body})
        return 0
    client = _client(args)
    if kind == "eligibility":
        created = client.create_eligibility_request(request)
    else:
        created = client.create_assignment_schedule_request(request)
    _dump(created.to_graph())
    return 0


def _parse_file(path: str, *, activatable_only: bool) -> int:
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    parsed = parse_graph_payload(payload)
    if hasattr(parsed, "activatable"):
        data = parsed.to_graph()
        if activatable_only:
            data["value"] = [item.to_graph() for item in parsed.activatable()]
        _dump(data)
    else:
        _dump(parsed.to_graph())
    return 0


if __name__ == "__main__":
    sys.exit(main())
