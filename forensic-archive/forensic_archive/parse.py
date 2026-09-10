"""Parse TEMP-ARC structured JSON tails from model responses."""

from __future__ import annotations

import json
import re
from typing import Any

_FENCE_RE = re.compile(
    r"```(?:json)?\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)


class StructuredOutputError(ValueError):
    """Raised when a TEMP-ARC response has no parseable JSON tail."""


def _load_json(raw: str) -> Any | None:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _trailing_json(text: str) -> Any | None:
    decoder = json.JSONDecoder()
    for opener in ("{", "["):
        index = text.rfind(opener)
        if index == -1:
            continue
        try:
            loaded, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        return loaded
    return None


def _coerce_object(loaded: Any) -> dict[str, Any] | None:
    if isinstance(loaded, dict):
        return loaded
    if isinstance(loaded, list):
        return {"exclusions": loaded}
    return None


def _load_tail_object(text: str) -> dict[str, Any]:
    fenced: list[Any] = []
    for match in _FENCE_RE.finditer(text):
        loaded = _load_json(match.group(1).strip())
        if loaded is not None:
            fenced.append(loaded)
    if fenced:
        obj = _coerce_object(fenced[-1])
        if obj is not None:
            return obj
    trailing = _coerce_object(_trailing_json(text))
    if trailing is not None:
        return trailing
    raise StructuredOutputError(
        "TEMP-ARC response must end with structured JSON. "
        "no JSON object or array found"
    )


EVIDENCE_LABELS = frozenset(
    {
        "VERBATIM",
        "SOURCE-SUMMARY",
        "RECONSTRUCTED",
        "INFERRED",
        "REFERENCE-ONLY",
        "CONFLICTING",
        "INCOMPLETE",
        "UNCERTAIN",
        "DUPLICATE",
        "SUPERSEDED-CLAIM",
    }
)


def parse_items(response: str) -> list[dict[str, Any]]:
    """Read the `items` array from a TEMP-ARC-001 response."""
    payload = _load_tail_object(response)
    items = payload.get("items")
    if items is None:
        return []
    if not isinstance(items, list):
        raise StructuredOutputError("TEMP-ARC-001 `items` must be a JSON array")
    normalized = [_normalize_item(item, index) for index, item in enumerate(items, start=1)]
    seen: set[str] = set()
    for item in normalized:
        item_id = item["id"]
        if item_id in seen:
            raise StructuredOutputError(f"duplicate extracted item id {item_id!r}")
        seen.add(item_id)
        if item["evidence"] not in EVIDENCE_LABELS:
            raise StructuredOutputError(
                f"invalid evidence label {item['evidence']!r} on {item_id}"
            )
    return normalized


def parse_exclusions(response: str) -> list[dict[str, Any]]:
    """Read the `exclusions` array from a TEMP-ARC-002 response.

    The validator must emit a JSON array (or an object with an `exclusions`
    key) at the end of its response so the pipeline can assign `exclusions`.
    """
    payload = _load_tail_object(response)
    if "exclusions" in payload:
        exclusions = payload["exclusions"]
    elif "id" in payload:
        exclusions = [payload]
    else:
        exclusions = []
    if exclusions is None:
        return []
    if not isinstance(exclusions, list):
        raise StructuredOutputError("TEMP-ARC-002 `exclusions` must be a JSON array")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(exclusions, start=1):
        if isinstance(item, str):
            normalized.append({"id": item, "reason": "", "rule": "unspecified"})
            continue
        if not isinstance(item, dict):
            raise StructuredOutputError("each exclusion must be an object or id string")
        exclusion_id = str(item.get("id") or item.get("item") or f"EXC-{index:03d}")
        normalized.append(
            {
                "id": exclusion_id,
                "reason": str(item.get("reason") or ""),
                "rule": str(item.get("rule") or "unspecified"),
            }
        )
    return normalized


def _normalize_item(item: Any, index: int) -> dict[str, Any]:
    if isinstance(item, str):
        return {
            "id": f"EXT-{index:03d}",
            "category": "unspecified",
            "text": item,
            "evidence": "SOURCE-SUMMARY",
        }
    if not isinstance(item, dict):
        raise StructuredOutputError("each extracted item must be an object or string")
    return {
        "id": str(item.get("id") or f"EXT-{index:03d}"),
        "category": str(item.get("category") or "unspecified"),
        "text": str(item.get("text") or item.get("item") or ""),
        "evidence": str(item.get("evidence") or "SOURCE-SUMMARY"),
    }


def exclusion_ids(exclusions: list[dict[str, Any]]) -> set[str]:
    return {str(item["id"]) for item in exclusions if item.get("id")}


def dangling_exclusion_ids(
    items: list[dict[str, Any]], exclusions: list[dict[str, Any]]
) -> list[str]:
    known = {item["id"] for item in items}
    return sorted(item_id for item_id in exclusion_ids(exclusions) if item_id not in known)
