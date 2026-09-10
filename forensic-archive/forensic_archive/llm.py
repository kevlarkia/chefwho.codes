"""LLM client protocol plus dummy and live provider wrappers.

Swap `primary_extraction_call` / `secondary_validation_call` by changing
`FORENSIC_LLM_PROVIDER` or by constructing `ForensicArchiver(client=...)`.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Protocol

from .parse import parse_items
from .prompts import (
    EXTRACTION_BEGIN,
    EXTRACTION_END,
    SOURCE_BEGIN,
    SOURCE_END,
    extract_delimited,
)

PROVIDER_ENV = "FORENSIC_LLM_PROVIDER"
TIMEOUT_ENV = "FORENSIC_LLM_TIMEOUT"
DEFAULT_TIMEOUT = 60.0

PLACEHOLDER_RE = re.compile(
    r"\b(TBD|TODO|PLACEHOLDER|lorem ipsum)\b",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)


class LLMClient(Protocol):
    name: str

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        """Return the model text for one TEMP-ARC call."""


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


def post_json(url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=_timeout()) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM HTTP {exc.code} from {url}: {detail[:500]}") from exc
    return json.loads(raw)


class DummyLLMClient:
    """Deterministic offline stand-in. Replace via provider env or injection."""

    name = "dummy"

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        del system
        if EXTRACTION_BEGIN in prompt:
            return self._validate(prompt)
        return self._extract(prompt)

    def _extract(self, prompt: str) -> str:
        source = extract_delimited(prompt, SOURCE_BEGIN, SOURCE_END)
        items = _items_from_source(source, swm="profile: swm" in prompt.lower())
        lines = ["PRIMARY EXTRACTION", ""]
        for item in items:
            lines.append(f"- {item['id']} [{item['evidence']}] {item['text']}")
        lines.extend(["", "```json", json.dumps({"items": items}, indent=2), "```"])
        return "\n".join(lines)

    def _validate(self, prompt: str) -> str:
        extraction = extract_delimited(prompt, EXTRACTION_BEGIN, EXTRACTION_END)
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

    @classmethod
    def from_env(cls) -> AnthropicLLMClient:
        key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is required for provider=anthropic")
        model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514").strip()
        return cls(api_key=key, model=model)

    def complete(self, prompt: str, *, system: str | None = None) -> str:
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
        blocks = data.get("content") or []
        texts = [block.get("text", "") for block in blocks if isinstance(block, dict)]
        return "".join(texts)


@dataclass
class OpenAILLMClient:
    api_key: str
    model: str
    name: str = "openai"

    @classmethod
    def from_env(cls) -> OpenAILLMClient:
        key = os.getenv("OPENAI_API_KEY", "").strip()
        if not key:
            raise RuntimeError("OPENAI_API_KEY is required for provider=openai")
        model = os.getenv("OPENAI_MODEL", "gpt-4.1").strip()
        return cls(api_key=key, model=model)

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        data = post_json(
            "https://api.openai.com/v1/chat/completions",
            {
                "content-type": "application/json",
                "authorization": f"Bearer {self.api_key}",
            },
            {"model": self.model, "messages": messages},
        )
        choices = data.get("choices") or []
        if not choices:
            return ""
        return str(choices[0].get("message", {}).get("content") or "")


@dataclass
class VertexLLMClient:
    project: str
    location: str
    model: str
    access_token: str
    name: str = "vertex"

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

    def complete(self, prompt: str, *, system: str | None = None) -> str:
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
