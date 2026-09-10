"""Load TEMP-ARC prompt templates and archive profiles."""

from __future__ import annotations

import re
import secrets
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
PROFILES_DIR = ROOT / "profiles"

PRIMARY_PROMPT_ID = "TEMP-ARC-001"
SECONDARY_PROMPT_ID = "TEMP-ARC-002"

_MARKER_RE = {
    "SOURCE": re.compile(r"<<<ARC_SOURCE:([A-Za-z0-9]+)>>>"),
    "EXTRACTION": re.compile(r"<<<ARC_EXTRACTION:([A-Za-z0-9]+)>>>"),
}


@dataclass(frozen=True)
class ArchiveProfile:
    id: str
    addendum: str


@dataclass(frozen=True)
class RenderedPrompt:
    text: str
    nonce: str
    begin: str
    end: str
    kind: str


def load_profile(profile_id: str) -> ArchiveProfile:
    path = PROFILES_DIR / f"{profile_id}.md"
    if not path.is_file():
        known = sorted(p.stem for p in PROFILES_DIR.glob("*.md"))
        raise ValueError(f"unknown archive profile {profile_id!r}; expected one of {known}")
    return ArchiveProfile(id=profile_id, addendum=path.read_text(encoding="utf-8"))


def _template(name: str) -> str:
    path = PROMPTS_DIR / name
    return path.read_text(encoding="utf-8")


def new_nonce() -> str:
    return secrets.token_hex(8)


def markers(kind: str, nonce: str) -> tuple[str, str]:
    return f"<<<ARC_{kind}:{nonce}>>>", f"<<<END_ARC_{kind}:{nonce}>>>"


def wrap_block(kind: str, body: str, nonce: str) -> str:
    begin, end = markers(kind, nonce)
    return f"{begin}\n{body.rstrip()}\n{end}"


def discover_markers(text: str, kind: str) -> tuple[str, str] | None:
    match = _MARKER_RE[kind].search(text)
    if not match:
        return None
    begin, end = markers(kind, match.group(1))
    if begin not in text or end not in text:
        return None
    return begin, end


def _nonce_avoiding(*bodies: str) -> str:
    blob = "\n".join(bodies)
    for _ in range(8):
        nonce = new_nonce()
        begin_s, end_s = markers("SOURCE", nonce)
        begin_e, end_e = markers("EXTRACTION", nonce)
        if not any(token in blob for token in (nonce, begin_s, end_s, begin_e, end_e)):
            return nonce
    raise RuntimeError("unable to allocate a collision-free ARC delimiter nonce")


def render_primary_prompt(source_text: str, profile: ArchiveProfile) -> RenderedPrompt:
    nonce = _nonce_avoiding(source_text, profile.addendum)
    begin, end = markers("SOURCE", nonce)
    text = (
        f"{_template('TEMP-ARC-001-primary-extraction.md')}\n\n"
        f"PROFILE: {profile.id}\n{profile.addendum}\n\n"
        f"Read only the nonce-delimited ARC_SOURCE block.\n\n"
        f"{wrap_block('SOURCE', source_text, nonce)}\n"
    )
    return RenderedPrompt(text=text, nonce=nonce, begin=begin, end=end, kind="SOURCE")


def render_secondary_prompt(
    source_text: str, extraction: str, profile: ArchiveProfile
) -> RenderedPrompt:
    nonce = _nonce_avoiding(source_text, extraction, profile.addendum)
    begin, end = markers("EXTRACTION", nonce)
    text = (
        f"{_template('TEMP-ARC-002-secondary-validation.md')}\n\n"
        f"PROFILE: {profile.id}\n{profile.addendum}\n\n"
        f"Source is the nonce-delimited ARC_SOURCE block. "
        f"Primary extraction is the nonce-delimited ARC_EXTRACTION block.\n\n"
        f"{wrap_block('SOURCE', source_text, nonce)}\n\n"
        f"{wrap_block('EXTRACTION', extraction, nonce)}\n"
    )
    return RenderedPrompt(text=text, nonce=nonce, begin=begin, end=end, kind="EXTRACTION")


def extract_delimited(text: str, begin: str, end: str) -> str:
    start = text.rfind(begin)
    if start == -1:
        return ""
    stop = text.find(end, start + len(begin))
    if stop == -1:
        return ""
    return text[start + len(begin) : stop].strip()


def extract_kind(text: str, kind: str) -> str:
    found = discover_markers(text, kind)
    if not found:
        return ""
    return extract_delimited(text, found[0], found[1])
