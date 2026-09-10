"""Microsoft Graph v1.0 client for PIM role eligibility schedule requests.

Follows the official contract:

- GET .../roleEligibilityScheduleRequests/filterByCurrentUser(on='principal')
- GET/POST .../roleEligibilityScheduleRequests
- GET .../roleEligibilityScheduleRequests/{id}
- POST .../roleEligibilityScheduleRequests/{id}/cancel
- POST .../roleAssignmentScheduleRequests  (selfActivate companion)

Bearer auth only. Supply a token via GRAPH_ACCESS_TOKEN (or AZURE_ACCESS_TOKEN).
This toolkit does not implement token acquisition.
"""

from __future__ import annotations

import json
import os
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .constants import (
    ALL_FILTER_BY_CURRENT_USER_OPTIONS,
    ASSIGNMENT_REQUESTS_PATH,
    DEFAULT_GRAPH_BASE_URL,
    DEFAULT_TIMEOUT_SECONDS,
    ELIGIBILITY_REQUESTS_PATH,
    FILTER_BY_CURRENT_USER_OPTIONS,
)
from .errors import GraphAuthError, GraphHttpError, GraphValidationError
from .models import (
    RoleScheduleRequestCollection,
    UnifiedRoleScheduleRequest,
    admin_assign_eligibility,
    admin_remove_eligibility,
    self_activate_assignment,
)

TOKEN_ENV_VARS = ("GRAPH_ACCESS_TOKEN", "AZURE_ACCESS_TOKEN")
BASE_URL_ENV = "GRAPH_BASE_URL"
TIMEOUT_ENV = "GRAPH_TIMEOUT"
USER_AGENT = "chefwho-graph-pim/0.1"

Opener = Callable[..., Any]


def _header_map(headers: Any) -> dict[str, str]:
    if headers is None:
        return {}
    if hasattr(headers, "items"):
        return {str(key).lower(): str(value) for key, value in headers.items()}
    mapped: dict[str, str] = {}
    for key, value in headers:
        mapped[str(key).lower()] = str(value)
    return mapped


def _read_body(stream: Any) -> bytes:
    raw = stream.read() if stream is not None else b""
    return raw if isinstance(raw, bytes | bytearray) else str(raw).encode("utf-8")


def resolve_access_token(explicit: str | None = None) -> str:
    if explicit and explicit.strip():
        return explicit.strip()
    for name in TOKEN_ENV_VARS:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    raise GraphAuthError(
        "Missing Graph bearer token. Set GRAPH_ACCESS_TOKEN (or AZURE_ACCESS_TOKEN). "
        "Example: az account get-access-token --resource https://graph.microsoft.com "
        "--query accessToken -o tsv"
    )


def parse_graph_error_payload(body: str) -> dict[str, Any]:
    if not body:
        return {}
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


@dataclass
class GraphCallTrace:
    """Last-call HTTP metadata for support lookup (Graph request-id)."""

    method: str | None = None
    url: str | None = None
    status: int | None = None
    client_request_id: str | None = None
    request_id: str | None = None
    headers: dict[str, str] = field(default_factory=dict)

    def as_meta(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.method:
            payload["method"] = self.method
        if self.url:
            payload["url"] = self.url
        if self.status is not None:
            payload["status"] = self.status
        if self.client_request_id:
            payload["client-request-id"] = self.client_request_id
        if self.request_id:
            payload["request-id"] = self.request_id
        return payload


class GraphPimClient:
    def __init__(
        self,
        *,
        token: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        opener: Opener | None = None,
        client_request_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self.token = resolve_access_token(token)
        self.base_url = (base_url or os.environ.get(BASE_URL_ENV) or DEFAULT_GRAPH_BASE_URL).rstrip(
            "/"
        )
        if timeout is None:
            raw_timeout = os.environ.get(TIMEOUT_ENV)
            self.timeout = float(raw_timeout) if raw_timeout else DEFAULT_TIMEOUT_SECONDS
        else:
            self.timeout = timeout
        self._opener = opener or urlopen
        self._id_factory = client_request_id_factory or (lambda: str(uuid.uuid4()))
        self.last_trace = GraphCallTrace()

    @classmethod
    def from_env(cls, **kwargs: Any) -> GraphPimClient:
        return cls(**kwargs)

    def filter_eligibility_by_current_user(
        self,
        *,
        on: str = "principal",
        select: str | None = None,
        odata_filter: str | None = None,
        expand: str | None = None,
        top: int | None = None,
        follow_next_link: bool = True,
    ) -> RoleScheduleRequestCollection:
        """GET filterByCurrentUser — official PIM 'roles you can activate' query.

        Does not return eligibilities granted only through group membership.
        Only `principal` and `approver` are currently supported by Graph.
        """
        if on not in ALL_FILTER_BY_CURRENT_USER_OPTIONS:
            raise GraphValidationError(
                f"Unsupported filterByCurrentUser on={on!r}. "
                f"Expected one of: {sorted(ALL_FILTER_BY_CURRENT_USER_OPTIONS)}"
            )
        if on not in FILTER_BY_CURRENT_USER_OPTIONS:
            raise GraphValidationError(
                f"filterByCurrentUser on={on!r} is in the enum but Graph currently "
                "supports only principal and approver"
            )
        path = f"{ELIGIBILITY_REQUESTS_PATH}/filterByCurrentUser(on='{on}')"
        return self._get_collection(
            path,
            select=select,
            odata_filter=odata_filter,
            expand=expand,
            top=top,
            follow_next_link=follow_next_link,
        )

    def list_eligibility_requests(
        self,
        *,
        select: str | None = None,
        odata_filter: str | None = None,
        expand: str | None = None,
        top: int | None = None,
        follow_next_link: bool = True,
    ) -> RoleScheduleRequestCollection:
        return self._get_collection(
            ELIGIBILITY_REQUESTS_PATH,
            select=select,
            odata_filter=odata_filter,
            expand=expand,
            top=top,
            follow_next_link=follow_next_link,
        )

    def get_eligibility_request(self, request_id: str) -> UnifiedRoleScheduleRequest:
        if not request_id or not request_id.strip():
            raise GraphValidationError("request id is required")
        payload = self.request(
            "GET", f"{ELIGIBILITY_REQUESTS_PATH}/{request_id.strip()}"
        )
        if not isinstance(payload, dict):
            raise GraphHttpError(
                "Expected a JSON object for the eligibility request",
                status=self.last_trace.status or 200,
                url=self.last_trace.url or "",
            )
        return UnifiedRoleScheduleRequest.from_graph(payload)

    def create_eligibility_request(
        self, request: UnifiedRoleScheduleRequest | dict[str, Any]
    ) -> UnifiedRoleScheduleRequest:
        body = (
            request.to_create_payload()
            if isinstance(request, UnifiedRoleScheduleRequest)
            else UnifiedRoleScheduleRequest.from_graph(request).to_create_payload()
        )
        payload = self.request("POST", ELIGIBILITY_REQUESTS_PATH, json_body=body)
        if not isinstance(payload, dict):
            raise GraphHttpError(
                "Expected a JSON object for the created eligibility request",
                status=self.last_trace.status or 201,
                url=self.last_trace.url or "",
            )
        return UnifiedRoleScheduleRequest.from_graph(payload)

    def cancel_eligibility_request(self, request_id: str) -> None:
        """Cancel a request whose status is Granted (204 No Content)."""
        if not request_id or not request_id.strip():
            raise GraphValidationError("request id is required")
        self.request(
            "POST",
            f"{ELIGIBILITY_REQUESTS_PATH}/{request_id.strip()}/cancel",
            expected=(204,),
        )

    def create_assignment_schedule_request(
        self, request: UnifiedRoleScheduleRequest | dict[str, Any]
    ) -> UnifiedRoleScheduleRequest:
        """POST unifiedRoleAssignmentScheduleRequest (selfActivate / selfDeactivate)."""
        body = (
            request.to_create_payload()
            if isinstance(request, UnifiedRoleScheduleRequest)
            else UnifiedRoleScheduleRequest.from_graph(request).to_create_payload()
        )
        payload = self.request("POST", ASSIGNMENT_REQUESTS_PATH, json_body=body)
        if not isinstance(payload, dict):
            raise GraphHttpError(
                "Expected a JSON object for the assignment schedule request",
                status=self.last_trace.status or 201,
                url=self.last_trace.url or "",
            )
        return UnifiedRoleScheduleRequest.from_graph(payload)

    def admin_assign(self, **kwargs: Any) -> UnifiedRoleScheduleRequest:
        return self.create_eligibility_request(admin_assign_eligibility(**kwargs))

    def admin_remove(self, **kwargs: Any) -> UnifiedRoleScheduleRequest:
        return self.create_eligibility_request(admin_remove_eligibility(**kwargs))

    def self_activate(self, **kwargs: Any) -> UnifiedRoleScheduleRequest:
        return self.create_assignment_schedule_request(self_activate_assignment(**kwargs))

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        expected: tuple[int, ...] = (200, 201, 204),
    ) -> dict[str, Any] | None:
        url = path if path.startswith("http://") or path.startswith("https://") else self._url(path, query)
        client_request_id = self._id_factory()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
            "client-request-id": client_request_id,
        }
        data: bytes | None = None
        if json_body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(json_body).encode("utf-8")

        http_request = Request(url, data=data, headers=headers, method=method.upper())
        try:
            with self._opener(http_request, timeout=self.timeout) as response:
                status = int(getattr(response, "status", 200))
                response_headers = _header_map(getattr(response, "headers", None))
                raw = _read_body(response)
        except HTTPError as exc:
            error_headers = _header_map(getattr(exc, "headers", None))
            raw_error = _read_body(getattr(exc, "fp", None) or exc)
            body_text = raw_error.decode("utf-8", errors="replace")
            self._store_trace(
                method=method.upper(),
                url=url,
                status=int(exc.code),
                client_request_id=client_request_id,
                headers=error_headers,
            )
            raise self._http_error(
                status=int(exc.code),
                url=url,
                client_request_id=client_request_id,
                headers=error_headers,
                body=body_text,
            ) from exc
        except URLError as exc:
            self._store_trace(
                method=method.upper(),
                url=url,
                status=None,
                client_request_id=client_request_id,
                headers={},
            )
            raise GraphHttpError(
                f"Graph request failed: {exc.reason}",
                status=0,
                url=url,
                client_request_id=client_request_id,
            ) from exc

        body_text = raw.decode("utf-8", errors="replace") if raw else ""
        self._store_trace(
            method=method.upper(),
            url=url,
            status=status,
            client_request_id=client_request_id,
            headers=response_headers,
        )
        if status not in expected:
            raise self._http_error(
                status=status,
                url=url,
                client_request_id=client_request_id,
                headers=response_headers,
                body=body_text,
            )
        if status == 204 or not body_text.strip():
            return None
        try:
            parsed = json.loads(body_text)
        except json.JSONDecodeError as exc:
            raise GraphHttpError(
                "Graph returned non-JSON body",
                status=status,
                url=url,
                client_request_id=client_request_id,
                request_id=self.last_trace.request_id,
                headers=response_headers,
                body=body_text,
            ) from exc
        if not isinstance(parsed, dict):
            raise GraphHttpError(
                "Graph JSON body must be an object",
                status=status,
                url=url,
                client_request_id=client_request_id,
                request_id=self.last_trace.request_id,
                headers=response_headers,
                body=body_text,
            )
        return parsed

    def _get_collection(
        self,
        path: str,
        *,
        select: str | None,
        odata_filter: str | None,
        expand: str | None,
        top: int | None,
        follow_next_link: bool,
    ) -> RoleScheduleRequestCollection:
        query = _odata_query(select=select, odata_filter=odata_filter, expand=expand, top=top)
        first = self.request("GET", path, query=query or None)
        if not isinstance(first, dict):
            raise GraphHttpError(
                "Expected a JSON collection",
                status=self.last_trace.status or 200,
                url=self.last_trace.url or "",
            )
        collection = RoleScheduleRequestCollection.from_graph(first)
        if not follow_next_link:
            return collection

        items = list(collection.value)
        next_link = collection.odata_next_link
        context = collection.odata_context
        extra = dict(collection.extra)
        while next_link:
            page = self.request("GET", next_link)
            if not isinstance(page, dict):
                raise GraphHttpError(
                    "Expected a JSON collection page",
                    status=self.last_trace.status or 200,
                    url=self.last_trace.url or "",
                )
            parsed = RoleScheduleRequestCollection.from_graph(page)
            items.extend(parsed.value)
            next_link = parsed.odata_next_link
            extra.update(parsed.extra)
        return RoleScheduleRequestCollection(
            odata_context=context,
            value=items,
            odata_next_link=None,
            extra=extra,
        )

    def _url(self, path: str, query: dict[str, Any] | None) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query, doseq=True, safe='$(),=')}"
        return url

    def _store_trace(
        self,
        *,
        method: str,
        url: str,
        status: int | None,
        client_request_id: str,
        headers: dict[str, str],
    ) -> None:
        request_id = headers.get("request-id") or None
        self.last_trace = GraphCallTrace(
            method=method,
            url=url,
            status=status,
            client_request_id=headers.get("client-request-id") or client_request_id,
            request_id=request_id,
            headers=headers,
        )

    def _http_error(
        self,
        *,
        status: int,
        url: str,
        client_request_id: str,
        headers: dict[str, str],
        body: str,
    ) -> GraphHttpError:
        payload = parse_graph_error_payload(body)
        error = payload.get("error") if isinstance(payload.get("error"), dict) else {}
        code = error.get("code") if isinstance(error, dict) else None
        message = error.get("message") if isinstance(error, dict) else None
        inner = error.get("innerError") if isinstance(error, dict) else None
        request_id = headers.get("request-id")
        inner_client_id = None
        if isinstance(inner, dict):
            request_id = inner.get("request-id") or request_id
            inner_client_id = inner.get("client-request-id")
        resolved_client_id = (
            inner_client_id or headers.get("client-request-id") or client_request_id
        )
        self.last_trace.request_id = request_id
        self.last_trace.client_request_id = resolved_client_id
        summary = message or body or f"HTTP {status}"
        prefix = f"Graph {status}"
        if code:
            prefix = f"{prefix} {code}"
        ids = []
        if resolved_client_id:
            ids.append(f"client-request-id={resolved_client_id}")
        if request_id:
            ids.append(f"request-id={request_id}")
        suffix = f" ({', '.join(ids)})" if ids else ""
        return GraphHttpError(
            f"{prefix}: {summary}{suffix}",
            status=status,
            url=url,
            code=code,
            request_id=request_id,
            client_request_id=resolved_client_id,
            headers=headers,
            body=body,
            payload=payload,
        )


def _odata_query(
    *,
    select: str | None,
    odata_filter: str | None,
    expand: str | None,
    top: int | None,
) -> dict[str, Any]:
    query: dict[str, Any] = {}
    if select:
        query["$select"] = select
    if odata_filter:
        query["$filter"] = odata_filter
    if expand:
        query["$expand"] = expand
    if top is not None:
        query["$top"] = str(top)
    return query
