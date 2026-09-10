"""Fail-closed errors for Microsoft Graph PIM calls."""

from __future__ import annotations

from typing import Any


class GraphPimError(RuntimeError):
    """Base error for the Graph PIM toolkit."""


class GraphValidationError(GraphPimError, ValueError):
    """Raised when a request would violate the official Graph contract."""


class GraphAuthError(GraphPimError):
    """Raised when no bearer token is available."""


class GraphHttpError(GraphPimError):
    """HTTP failure from Microsoft Graph, with request IDs for support."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        url: str,
        code: str | None = None,
        request_id: str | None = None,
        client_request_id: str | None = None,
        headers: dict[str, str] | None = None,
        body: str = "",
        payload: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.url = url
        self.code = code
        self.request_id = request_id
        self.client_request_id = client_request_id
        self.headers = headers or {}
        self.body = body
        self.payload = payload or {}
