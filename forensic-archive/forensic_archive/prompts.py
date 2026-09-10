"""Load TEMP-ARC prompt templates and archive profiles."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
PROFILES_DIR = ROOT / "profiles"

SOURCE_BEGIN = "<<<ARC_SOURCE>>>"
SOURCE_END = "<<<END_ARC_SOURCE>>>"
EXTRACTION_BEGIN = "<<<ARC_EXTRACTION>>>"
EXTRACTION_END = "<<<END_ARC_EXTRACTION>>>"

PRIMARY_PROMPT_ID = "TEMP-ARC-001"
SECONDARY_PROMPT_ID = "TEMP-ARC-002"


@dataclass(frozen=True)
class ArchiveProfile:
    id: str
    addendum: str


def load_profile(profile_id: str) -> ArchiveProfile:
    path = PROFILES_DIR / f"{profile_id}.md"
    if not path.is_file():
        known = sorted(p.stem for p in PROFILES_DIR.glob("*.md"))
        raise ValueError(f"unknown archive profile {profile_id!r}; expected one of {known}")
    return ArchiveProfile(id=profile_id, addendum=path.read_text(encoding="utf-8"))


def _template(name: str) -> str:
    path = PROMPTS_DIR / name
    return path.read_text(encoding="utf-8")


def wrap_source(source_text: str) -> str:
    return f"{SOURCE_BEGIN}\n{source_text.rstrip()}\n{SOURCE_END}"


def render_primary_prompt(source_text: str, profile: ArchiveProfile) -> str:
    return (
        f"{_template('TEMP-ARC-001-primary-extraction.md')}\n\n"
        f"PROFILE: {profile.id}\n{profile.addendum}\n\n"
        f"{wrap_source(source_text)}\n"
    )


def render_secondary_prompt(
    source_text: str, extraction: str, profile: ArchiveProfile
) -> str:
    return (
        f"{_template('TEMP-ARC-002-secondary-validation.md')}\n\n"
        f"PROFILE: {profile.id}\n{profile.addendum}\n\n"
        f"{wrap_source(source_text)}\n\n"
        f"{EXTRACTION_BEGIN}\n{extraction.rstrip()}\n{EXTRACTION_END}\n"
    )


def extract_delimited(text: str, begin: str, end: str) -> str:
    start = text.rfind(begin)
    if start == -1:
        return ""
    stop = text.find(end, start + len(begin))
    if stop == -1:
        return ""
    return text[start + len(begin) : stop].strip()
