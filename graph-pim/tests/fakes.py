from __future__ import annotations

import json
from email.message import EmailMessage
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def load_fixture(name: str) -> dict:
    with (FIXTURES / name).open(encoding="utf-8") as handle:
        return json.load(handle)


class FakeResponse:
    def __init__(
        self,
        status: int,
        body: dict | list | str | bytes | None,
        headers: dict[str, str] | None = None,
    ) -> None:
        if body is None:
            raw = b""
        elif isinstance(body, bytes | bytearray):
            raw = bytes(body)
        elif isinstance(body, str):
            raw = body.encode("utf-8")
        else:
            raw = json.dumps(body).encode("utf-8")
        self.status = status
        self._body = raw
        self.headers = {key.lower(): value for key, value in (headers or {}).items()}

    def read(self) -> bytes:
        return self._body

    def getheader(self, name: str, default: str | None = None) -> str | None:
        return self.headers.get(name.lower(), default)

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *args: object) -> bool:
        return False


class FakeGraph:
    def __init__(self) -> None:
        self.calls: list[Request] = []
        self._routes: list[tuple[str, str, FakeResponse | HTTPError]] = []

    def route(self, method: str, substring: str, response: FakeResponse | HTTPError) -> None:
        self._routes.append((method.upper(), substring, response))

    def __call__(self, request: Request, timeout: float | None = None) -> FakeResponse:
        del timeout
        self.calls.append(request)
        url = request.full_url
        method = request.get_method()
        for route_method, substring, response in self._routes:
            if method == route_method and substring in url:
                if isinstance(response, HTTPError):
                    raise response
                return response
        raise AssertionError(f"No fake route for {method} {url}")


def http_error(url: str, status: int, payload: dict, headers: dict[str, str] | None = None) -> HTTPError:
    msg = EmailMessage()
    for key, value in (headers or {}).items():
        msg[key] = value
    body = json.dumps(payload).encode("utf-8")
    return HTTPError(url, status, "Error", msg, BytesIO(body))
