"""Fail-closed errors for museum-grade packaging."""

from __future__ import annotations


class MuseumPackageError(ValueError):
    """Raised when a run cannot produce a trustworthy archive."""


class MuseumIntegrityError(ValueError):
    """Raised when an existing package fails verification."""


class LLMHttpError(RuntimeError):
    """HTTP failure from a live LLM provider, with request IDs for support."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        url: str,
        request_id: str | None = None,
        client_request_id: str | None = None,
        headers: dict[str, str] | None = None,
        body: str = "",
    ) -> None:
        super().__init__(message)
        self.status = status
        self.url = url
        self.request_id = request_id
        self.client_request_id = client_request_id
        self.headers = headers or {}
        self.body = body
