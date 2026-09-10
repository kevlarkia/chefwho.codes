"""LLM client protocol plus dummy and live provider wrappers.

Swap `primary_extraction_call` / `secondary_validation_call` by changing
`FORENSIC_LLM_PROVIDER` or by constructing `ForensicArchiver(client=...)`.

The OpenAI wrapper follows the official API overview: Responses is the
default surface, bearer auth from an API key or short-lived access token,
optional organization/project headers, `X-Client-Request-Id` on every
call, and captured `x-request-id` / rate-limit headers for the ledger.
"""

from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass, field
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .errors import LLMHttpError
from .parse import parse_items
from .prompts import discover_markers, extract_kind

PROVIDER_ENV = "FORENSIC_LLM_PROVIDER"
TIMEOUT_ENV = "FORENSIC_LLM_TIMEOUT"
DEFAULT_TIMEOUT = 60.0

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_DEFAULT_MODEL = "gpt-4.1"
OPENAI_DEFAULT_SURFACE = "responses"

HEADER_BUDGET_BYTES = 64 * 1024
CUSTOM_HEADER_VALUE_BUDGET_BYTES = 60 * 1024
CLIENT_REQUEST_ID_MAX = 512
REQUIRED_HEADER_NAMES = frozenset(
    {
        "authorization",
        "content-type",
        "user-agent",
        "host",
        "accept",
        "content-length",
    }
)
RATE_LIMIT_HEADER_NAMES = (
    "x-ratelimit-limit-requests",
    "x-ratelimit-limit-tokens",
    "x-ratelimit-remaining-requests",
    "x-ratelimit-remaining-tokens",
    "x-ratelimit-reset-requests",
    "x-ratelimit-reset-tokens",
    "x-ratelimit-limit-project-tokens",
    "x-ratelimit-remaining-project-tokens",
    "x-ratelimit-reset-project-tokens",
)

PLACEHOLDER_RE = re.compile(
    r"\b(TBD|TODO|PLACEHOLDER|lorem ipsum)\b",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)


class LLMClient(Protocol):
    name: str

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        client_request_id: str | None = None,
    ) -> str:
        """Return the model text for one TEMP-ARC call."""


@dataclass
class LLMCallTrace:
    """Last-call HTTP metadata for ledger and support lookup."""

    client_request_id: str | None = None
    provider_request_id: str | None = None
    organization: str | None = None
    processing_ms: str | None = None
    api_version: str | None = None
    surface: str | None = None
    url: str | None = None
    status: int | None = None
    rate_limits: dict[str, str] = field(default_factory=dict)

    def as_http_meta(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.organization:
            payload["openai-organization"] = self.organization
        if self.processing_ms:
            payload["openai-processing-ms"] = self.processing_ms
        if self.api_version:
            payload["openai-version"] = self.api_version
        if self.surface:
            payload["surface"] = self.surface
        if self.url:
            payload["url"] = self.url
        if self.status is not None:
            payload["status"] = self.status
        if self.rate_limits:
            payload["rate_limits"] = dict(self.rate_limits)
        return payload


@dataclass
class HttpJsonResult:
    body: dict[str, Any]
    status: int
    headers: dict[str, str]
    client_request_id: str | None = None

    @property
    def request_id(self) -> str | None:
        return header_get(self.headers, "x-request-id")


def env_provider() -> str:
    return os.getenv(PROVIDER_ENV, "dummy").strip().lower() or "dummy"


def client_from_env(provider: str | None = None) -> LLMClient:
    chosen = (provider or env_provider()).strip().lower()
    if chosen in {"dummy", "offline", "local"}:
        return DummyLLMClient()
    if chosen == "anthropic":
        return AnthropicLLMClient.from_env()
    if chosen == "openai":
        return OpenAILLMClient.from_env()
    if chosen in {"vertex", "google", "google-vertex"}:
        return VertexLLMClient.from_env()
    raise ValueError(
        f"unsupported {PROVIDER_ENV}={chosen!r}; "
        "use dummy, anthropic, openai, or vertex"
    )


def _timeout() -> float:
    raw = os.getenv(TIMEOUT_ENV, "").strip()
    return float(raw) if raw else DEFAULT_TIMEOUT


def header_get(headers: dict[str, str], name: str) -> str | None:
    wanted = name.lower()
    for key, value in headers.items():
        if key.lower() == wanted:
            return value
    return None


def lowercase_headers(headers: Any) -> dict[str, str]:
    items = getattr(headers, "items", None)
    if items is None:
        return {}
    return {str(key): str(value) for key, value in items()}


def validate_client_request_id(value: str) -> str:
    if not value:
        raise ValueError("X-Client-Request-Id must not be empty")
    if len(value) > CLIENT_REQUEST_ID_MAX:
        raise ValueError(
            f"X-Client-Request-Id must be <= {CLIENT_REQUEST_ID_MAX} characters"
        )
    try:
        value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("X-Client-Request-Id must be ASCII") from exc
    return value


def new_client_request_id() -> str:
    return str(uuid.uuid4())


def assert_header_budget(headers: dict[str, str]) -> None:
    encoded = {str(key): str(value) for key, value in headers.items()}
    total = sum(len(key.encode("utf-8")) + len(value.encode("utf-8")) + 4 for key, value in encoded.items())
    if total >= HEADER_BUDGET_BYTES:
        raise ValueError(
            f"OpenAI request headers are {total} bytes; keep the total under 64 KiB"
        )
    custom_values = sum(
        len(value.encode("utf-8"))
        for key, value in encoded.items()
        if key.lower() not in REQUIRED_HEADER_NAMES
    )
    if custom_values > CUSTOM_HEADER_VALUE_BUDGET_BYTES:
        raise ValueError(
            "OpenAI custom header values exceed 60 KiB; "
            "the request may fail before it reaches the API"
        )


def rate_limit_headers(headers: dict[str, str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for name in RATE_LIMIT_HEADER_NAMES:
        value = header_get(headers, name)
        if value:
            found[name] = value
    return found


def extract_openai_text(data: dict[str, Any], *, surface: str = "responses") -> str:
    """Read model text from Responses `output` or Chat Completions `choices`."""
    if surface == "chat":
        choices = data.get("choices") or []
        if not choices or not isinstance(choices[0], dict):
            return ""
        return str(choices[0].get("message", {}).get("content") or "")
    if isinstance(data.get("output_text"), str) and data["output_text"]:
        return data["output_text"]
    chunks: list[str] = []
    for item in data.get("output") or []:
        if not isinstance(item, dict):
            continue
        if item.get("type") not in {None, "message"} and "content" not in item:
            continue
        for part in item.get("content") or []:
            if not isinstance(part, dict):
                continue
            if part.get("type") in {"output_text", "text"} and part.get("text"):
                chunks.append(str(part["text"]))
    return "".join(chunks)


def _http_error_from_urllib(
    exc: HTTPError,
    *,
    url: str,
    client_request_id: str | None,
) -> LLMHttpError:
    detail = exc.read().decode("utf-8", errors="replace")
    headers = lowercase_headers(getattr(exc, "headers", {}) or {})
    request_id = header_get(headers, "x-request-id")
    parts = [f"LLM HTTP {exc.code} from {url}"]
    if request_id:
        parts.append(f"x-request-id={request_id}")
    if client_request_id:
        parts.append(f"X-Client-Request-Id={client_request_id}")
    if detail:
        parts.append(detail[:500])
    return LLMHttpError(
        ": ".join(parts),
        status=int(exc.code),
        url=url,
        request_id=request_id,
        client_request_id=client_request_id,
        headers=headers,
        body=detail,
    )


def request_json(
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    *,
    client_request_id: str | None = None,
) -> HttpJsonResult:
    assert_header_budget(headers)
    body = json.dumps(payload).encode("utf-8")
    request = Request(url, data=body, headers=headers, method="POST")
    try:
        with urlopen(request, timeout=_timeout()) as response:
            raw = response.read().decode("utf-8")
            status = int(getattr(response, "status", 200) or 200)
            response_headers = lowercase_headers(response.headers)
    except HTTPError as exc:
        raise _http_error_from_urllib(exc, url=url, client_request_id=client_request_id) from exc
    except URLError as exc:
        raise RuntimeError(f"LLM request to {url} failed: {exc.reason}") from exc
    return HttpJsonResult(
        body=json.loads(raw),
        status=status,
        headers=response_headers,
        client_request_id=client_request_id,
    )


def post_json(url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
    return request_json(url, headers, payload).body


def consume_call_trace(client: LLMClient) -> LLMCallTrace | None:
    trace = getattr(client, "last_trace", None)
    return trace if isinstance(trace, LLMCallTrace) else None


class DummyLLMClient:
    """Deterministic offline stand-in. Replace via provider env or injection."""

    name = "dummy"

    def __init__(self) -> None:
        self.last_trace = LLMCallTrace(surface="dummy")

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        client_request_id: str | None = None,
    ) -> str:
        del system
        self.last_trace = LLMCallTrace(
            client_request_id=client_request_id,
            surface="dummy",
        )
        if discover_markers(prompt, "EXTRACTION"):
            return self._validate(prompt)
        return self._extract(prompt)

    def _extract(self, prompt: str) -> str:
        source = extract_kind(prompt, "SOURCE")
        items = _items_from_source(source, swm="profile: swm" in prompt.lower())
        lines = ["PRIMARY EXTRACTION", ""]
        for item in items:
            lines.append(f"- {item['id']} [{item['evidence']}] {item['text']}")
        lines.extend(["", "```json", json.dumps({"items": items}, indent=2), "```"])
        return "\n".join(lines)

    def _validate(self, prompt: str) -> str:
        extraction = extract_kind(prompt, "EXTRACTION")
        items = parse_items(extraction) if extraction.strip() else []
        exclusions: list[dict[str, str]] = []
        for item in items:
            text = item.get("text") or ""
            if PLACEHOLDER_RE.search(text):
                exclusions.append(
                    {
                        "id": item["id"],
                        "reason": "Placeholder or unfinished language is not archive-ready.",
                        "rule": "placeholder",
                    }
                )
            elif len(text) < 20:
                exclusions.append(
                    {
                        "id": item["id"],
                        "reason": "Item is too thin to keep in a museum-quality archive.",
                        "rule": "too-thin",
                    }
                )
        narrative = (
            "SECONDARY VALIDATION (TEMP-ARC-002)\n"
            f"Reviewed {len(items)} extracted item(s); "
            f"excluded {len(exclusions)}."
        )
        payload = {"exclusions": exclusions}
        return f"{narrative}\n\n```json\n{json.dumps(payload, indent=2)}\n```"


def _items_from_source(source: str, *, swm: bool) -> list[dict[str, str]]:
    chunks: list[str] = []
    headings = [match.group(1).strip() for match in HEADING_RE.finditer(source)]
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", source) if part.strip()]
    if headings and len(paragraphs) > 1:
        for part in paragraphs:
            heading = HEADING_RE.match(part)
            body = HEADING_RE.sub("", part).strip()
            if heading and body:
                chunks.append(f"{heading.group(1).strip()}: {body}")
            elif body:
                chunks.append(body)
            elif heading:
                chunks.append(heading.group(1).strip())
    else:
        chunks = [line.strip() for line in source.splitlines() if line.strip()]
        chunks = [line for line in chunks if not line.startswith("#")]
    items: list[dict[str, str]] = []
    for index, text in enumerate(chunks, start=1):
        evidence = "VERBATIM" if swm else "SOURCE-SUMMARY"
        category = "swm" if swm else "documentary"
        items.append(
            {
                "id": f"EXT-{index:03d}",
                "category": category,
                "text": text,
                "evidence": evidence,
            }
        )
    return items


@dataclass
class AnthropicLLMClient:
    api_key: str
    model: str
    name: str = "anthropic"
    last_trace: LLMCallTrace = field(default_factory=LLMCallTrace)

    @classmethod
    def from_env(cls) -> AnthropicLLMClient:
        key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is required for provider=anthropic")
        model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514").strip()
        return cls(api_key=key, model=model)

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        client_request_id: str | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system
        data = post_json(
            "https://api.anthropic.com/v1/messages",
            {
                "content-type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            payload,
        )
        self.last_trace = LLMCallTrace(
            client_request_id=client_request_id,
            surface="anthropic-messages",
            url="https://api.anthropic.com/v1/messages",
        )
        blocks = data.get("content") or []
        texts = [block.get("text", "") for block in blocks if isinstance(block, dict)]
        return "".join(texts)


@dataclass
class OpenAILLMClient:
    """Official OpenAI HTTP client: Responses by default, Chat as opt-in."""

    api_key: str
    model: str
    organization: str | None = None
    project: str | None = None
    surface: str = OPENAI_DEFAULT_SURFACE
    store: bool = False
    max_output_tokens: int = 8192
    name: str = "openai"
    last_trace: LLMCallTrace = field(default_factory=LLMCallTrace)

    @classmethod
    def from_env(cls) -> OpenAILLMClient:
        token = os.getenv("OPENAI_ACCESS_TOKEN", "").strip() or os.getenv(
            "OPENAI_API_KEY", ""
        ).strip()
        if not token:
            raise RuntimeError(
                "OPENAI_API_KEY or OPENAI_ACCESS_TOKEN is required for provider=openai"
            )
        model = os.getenv("OPENAI_MODEL", OPENAI_DEFAULT_MODEL).strip() or OPENAI_DEFAULT_MODEL
        organization = (
            os.getenv("OPENAI_ORGANIZATION", "").strip()
            or os.getenv("OPENAI_ORG_ID", "").strip()
            or None
        )
        project = os.getenv("OPENAI_PROJECT", "").strip() or None
        surface = os.getenv("OPENAI_API_SURFACE", OPENAI_DEFAULT_SURFACE).strip().lower()
        if surface not in {"responses", "chat"}:
            raise ValueError(
                f"unsupported OPENAI_API_SURFACE={surface!r}; use responses or chat"
            )
        store_raw = os.getenv("OPENAI_STORE", "false").strip().lower()
        store = store_raw in {"1", "true", "yes", "on"}
        max_raw = os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "").strip()
        max_output_tokens = int(max_raw) if max_raw else 8192
        return cls(
            api_key=token,
            model=model,
            organization=organization,
            project=project,
            surface=surface,
            store=store,
            max_output_tokens=max_output_tokens,
        )

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        client_request_id: str | None = None,
    ) -> str:
        request_id = validate_client_request_id(
            client_request_id or new_client_request_id()
        )
        headers = self._headers(request_id)
        if self.surface == "chat":
            url = OPENAI_CHAT_URL
            messages: list[dict[str, str]] = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            payload: dict[str, Any] = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_output_tokens,
            }
        else:
            url = OPENAI_RESPONSES_URL
            payload = {
                "model": self.model,
                "input": prompt,
                "store": self.store,
                "max_output_tokens": self.max_output_tokens,
            }
            if system:
                payload["instructions"] = system
        result = request_json(url, headers, payload, client_request_id=request_id)
        self.last_trace = self._trace_from_result(result, url=url)
        return extract_openai_text(result.body, surface=self.surface)

    def _headers(self, client_request_id: str) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-Client-Request-Id": client_request_id,
        }
        if self.organization:
            headers["OpenAI-Organization"] = self.organization
        if self.project:
            headers["OpenAI-Project"] = self.project
        return headers

    def _trace_from_result(self, result: HttpJsonResult, *, url: str) -> LLMCallTrace:
        headers = result.headers
        provider_id = result.request_id
        if not provider_id and isinstance(result.body.get("id"), str):
            provider_id = result.body["id"]
        return LLMCallTrace(
            client_request_id=result.client_request_id,
            provider_request_id=provider_id,
            organization=header_get(headers, "openai-organization") or self.organization,
            processing_ms=header_get(headers, "openai-processing-ms"),
            api_version=header_get(headers, "openai-version"),
            surface=self.surface,
            url=url,
            status=result.status,
            rate_limits=rate_limit_headers(headers),
        )


@dataclass
class VertexLLMClient:
    project: str
    location: str
    model: str
    access_token: str
    name: str = "vertex"
    last_trace: LLMCallTrace = field(default_factory=LLMCallTrace)

    @classmethod
    def from_env(cls) -> VertexLLMClient:
        project = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
        token = os.getenv("VERTEX_ACCESS_TOKEN", "").strip()
        if not project or not token:
            raise RuntimeError(
                "GOOGLE_CLOUD_PROJECT and VERTEX_ACCESS_TOKEN are required "
                "for provider=vertex (or inject your own Vertex wrapper)"
            )
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip()
        model = os.getenv("VERTEX_MODEL", "gemini-2.0-flash").strip()
        return cls(project=project, location=location, model=model, access_token=token)

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        client_request_id: str | None = None,
    ) -> str:
        url = (
            f"https://{self.location}-aiplatform.googleapis.com/v1/"
            f"projects/{self.project}/locations/{self.location}/"
            f"publishers/google/models/{self.model}:generateContent"
        )
        parts = [{"text": prompt}]
        payload: dict[str, Any] = {"contents": [{"role": "user", "parts": parts}]}
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        data = post_json(
            url,
            {
                "content-type": "application/json",
                "authorization": f"Bearer {self.access_token}",
            },
            payload,
        )
        self.last_trace = LLMCallTrace(
            client_request_id=client_request_id,
            surface="vertex-generateContent",
            url=url,
        )
        candidates = data.get("candidates") or []
        if not candidates:
            return ""
        content = candidates[0].get("content") or {}
        texts = [
            part.get("text", "")
            for part in content.get("parts") or []
            if isinstance(part, dict)
        ]
        return "".join(texts)
