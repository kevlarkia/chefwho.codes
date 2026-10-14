#!/usr/bin/env python3
"""Hunt design files on the operator Mac and file them into one corpus.

Hunt is read-only. Apply copies or moves only when invoked with
``--confirm consolidate``. Live git working trees are never moved.
Frozen preservation trees are copied unless
``--include-frozen-moves`` is set. Private paths are counted and omitted.
"""

from __future__ import annotations

import argparse
import csv
import errno
import hashlib
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

CORPUS_DIRNAME = "Design_Corpus"
MANIFEST_DIRNAME = "_MANIFEST"
ARCHIVE_RELATIVE = Path("Documents") / "AFSTYLE_BUSINESS_MASTER_ARCHIVE"
OVERSIZE_BYTES = 2_000_000_000
SOURCE_EXTS = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".py",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".java",
    ".kt",
    ".swift",
    ".vue",
    ".svelte",
}
WEAK_AUTO_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".heic",
    ".tif",
    ".tiff",
    ".svg",
    ".pdf",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".afdesign",
    ".afphoto",
    ".afpub",
    ".sketch",
    ".fig",
    ".xd",
    ".ase",
    ".aco",
    ".ai",
    ".eps",
    ".psd",
    ".indd",
    ".idml",
    ".otf",
    ".ttf",
    ".woff",
    ".woff2",
}
DESIGN_NATIVE_EXTS = {
    ".afdesign",
    ".afphoto",
    ".afpub",
    ".sketch",
    ".fig",
    ".xd",
    ".ase",
    ".aco",
    ".ai",
    ".eps",
    ".psd",
    ".indd",
    ".idml",
}
ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".dmg", ".iso", ".pkg"}
COPYABLE_KINDS = {
    "logo",
    "art-direction",
    "design-system",
    "brand-doc",
    "token",
    "mockup",
    "moodboard",
    "font",
    "ui-export",
    "prompt",
}
PRUNE_DIR_NAMES = {
    "node_modules",
    ".git",
    ".next",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
    "deriveddata",
    "caches",
    "cache",
    "mail",
    "messages",
    ".trash",
    "keychains",
    "cookies",
}
PRUNE_SUFFIXES = {".app", ".photoslibrary", ".bundle", ".framework"}
PRIVATE_SEGMENTS = {
    "medical",
    "health",
    "therapy",
    "crisis",
    "hipaa",
    "tax",
    "taxes",
    "banking",
    "bank",
    "passwords",
    "secrets",
    "credentials",
    "private",
}
PRIVATE_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "secrets.json",
}
HEADER = [
    "id",
    "disposition",
    "lane",
    "concept",
    "kind",
    "bytes",
    "mtime",
    "in_git",
    "frozen",
    "origin",
    "dest",
    "reason",
]
SEED_HOMES = [
    "07_Portfolio_Evidence/ChefWho_Design_System",
    "07_Portfolio_Evidence/Esther_AI_Art_Direction",
    "07_Portfolio_Evidence/Prompt_Library_2.5",
    "07_Portfolio_Evidence/TRH_WTF_System",
]
STRONG_DIR_RES = [
    re.compile(r"^chefwho[-_ ]?design[-_ ]?system$", re.I),
    re.compile(r"^esther[-_ ]?ai[-_ ]?art[-_ ]?direction$", re.I),
    re.compile(r"^design[-_ ]?system$", re.I),
    re.compile(r"^art[-_ ]?direction$", re.I),
    re.compile(r"^style[-_ ]?guide$", re.I),
    re.compile(r"^styleguide$", re.I),
    re.compile(r"^mood[-_ ]?boards?$", re.I),
    re.compile(r"^visual[-_ ]?identity$", re.I),
    re.compile(r"^design[-_ ]?tokens?$", re.I),
    re.compile(r"^ui[-_ ]?kit$", re.I),
    re.compile(r"^brand[-_ ]?(standards|kit|book|guide|identity)$", re.I),
    re.compile(r"^logos?$", re.I),
    re.compile(r"^mock[-_ ]?ups?$", re.I),
    re.compile(r"^wireframes?$", re.I),
    re.compile(r"^lookbook$", re.I),
    re.compile(r"^wordmarks?$", re.I),
]
WEAK_DIR_RES = [
    re.compile(r"^design$", re.I),
    re.compile(r"^brand$", re.I),
    re.compile(r"^brands$", re.I),
    re.compile(r"^figma$", re.I),
    re.compile(r"^canva$", re.I),
    re.compile(r"^framer$", re.I),
    re.compile(r"^webflow$", re.I),
    re.compile(r"^adobe$", re.I),
]
STRONG_PHRASE_RE = re.compile(
    r"design[-_ ]?system|art[-_ ]?direction|style[-_ ]?guide|styleguide|"
    r"visual[-_ ]?identity|mood[-_ ]?boards?|design[-_ ]?tokens?|"
    r"ui[-_ ]?kit|lookbook|wordmarks?|mock[-_ ]?ups?|wireframes?|"
    r"brand[-_ ]?(standards|kit|book|guide|identity)|"
    r"(^|[^a-z0-9])logos?([^a-z0-9]|$)",
    re.I,
)
LANE_RULES: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"(^|[^a-z0-9])karina([^a-z0-9]|$)", re.I), "SWM Filings", "Karina"),
    (
        re.compile(r"(^|[^a-z0-9])(trh|wtf[-_ ]?system)([^a-z0-9]|$)", re.I),
        "Prompt Library TRH",
        "TRH",
    ),
    (re.compile(r"prompt[-_ ]library", re.I), "Prompt Library TRH", "Prompt Library"),
    (re.compile(r"chefs?[-_ ]?who", re.I), "ChefsWho.codes", "ChefWho"),
    (re.compile(r"(^|[^a-z0-9])esther([^a-z0-9]|$)", re.I), "Unmapped", "Esther"),
    (re.compile(r"rose[-_ ]?rocket", re.I), "Rose Rocket", "Rose Rocket"),
    (
        re.compile(r"(^|[^a-z0-9])(swm|okram|signel|sdrwm)([^a-z0-9]|$)", re.I),
        "SWM Filings",
        "SWM",
    ),
    (re.compile(r"smart[-_ ]workforce|hazel[-_ ]warden", re.I), "SWM Filings", "SWM"),
    (re.compile(r"af\.?style|name[-_ ]identity", re.I), "Unmapped", "AF.Style"),
]


@dataclass
class Row:
    id: str
    disposition: str
    lane: str
    concept: str
    kind: str
    bytes: int
    mtime: str
    in_git: str
    frozen: str
    origin: str
    dest: str
    reason: str

    def as_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "disposition": self.disposition,
            "lane": self.lane,
            "concept": self.concept,
            "kind": self.kind,
            "bytes": str(self.bytes),
            "mtime": self.mtime,
            "in_git": self.in_git,
            "frozen": self.frozen,
            "origin": self.origin,
            "dest": self.dest,
            "reason": self.reason,
        }


def default_corpus(home: Path) -> Path:
    return home / ARCHIVE_RELATIVE / CORPUS_DIRNAME


def default_roots(home: Path) -> list[Path]:
    named = [
        home / "Desktop",
        home / "Documents",
        home / "Downloads",
        home / "Pictures",
        home / "Library" / "CloudStorage",
        home / "Library" / "Mobile Documents" / "com~apple~CloudDocs",
    ]
    volumes = Path("/Volumes")
    if volumes.is_dir():
        for entry in sorted(volumes.iterdir()):
            name = entry.name
            if name in {"Macintosh HD"} or name.startswith((".", "com.apple")):
                continue
            if "Time Machine" in name:
                continue
            named.append(entry)
    return [path for path in named if path.exists()]


def is_private(path: Path) -> bool:
    if path.name in PRIVATE_FILENAMES or path.name.startswith(".env"):
        return True
    for part in path.parts:
        if part.lower() in PRIVATE_SEGMENTS:
            return True
    return False


def is_frozen(path: Path) -> bool:
    text = path.as_posix()
    return (
        "/90_SOURCE_PRESERVATION/" in text
        or "CURSOR_SOURCE_BUNDLE_" in text
        or "/Cold Archive/" in text
        or "/Cold_Archive/" in text
    )


def is_dataless(path: Path) -> bool:
    try:
        out = subprocess.check_output(
            ["ls", "-ldO", str(path)],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return False
    return "dataless" in out


def git_root(path: Path) -> Path | None:
    current = path.parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return None


def dir_strength(name: str) -> str:
    if any(pattern.search(name) for pattern in STRONG_DIR_RES):
        return "strong"
    if any(pattern.search(name) for pattern in WEAK_DIR_RES):
        return "weak"
    return "none"


def path_strength(path: Path) -> str:
    strongest = "none"
    for part in path.parts[:-1]:
        level = dir_strength(part)
        if level == "strong":
            return "strong"
        if level == "weak":
            strongest = "weak"
    if path.suffix.lower() in DESIGN_NATIVE_EXTS:
        return "strong"
    if STRONG_PHRASE_RE.search(path.as_posix()):
        return "strong"
    return strongest


def is_visual_file(path: Path) -> bool:
    return path.suffix.lower() in WEAK_AUTO_EXTS or path.suffix.lower() in DESIGN_NATIVE_EXTS


def lane_and_concept(path: Path) -> tuple[str, str]:
    for part in reversed(path.parts):
        for pattern, lane, concept in LANE_RULES:
            if pattern.search(part):
                return lane, concept
    text = path.as_posix()
    for pattern, lane, concept in LANE_RULES:
        if pattern.search(text):
            return lane, concept
    for part in reversed(path.parts[:-1]):
        if dir_strength(part) != "none":
            label = part.replace("_", " ").replace("-", " ")
            return "Unmapped", label
    return "Unmapped", "Unspecified"


def kind_for(path: Path, lane_concept: str) -> str:
    name = path.as_posix().lower()
    ext = path.suffix.lower()
    if re.search(r"(^|[^a-z0-9])logos?([^a-z0-9]|$)", name):
        return "logo"
    if "art-direction" in name or "art_direction" in name or "art direction" in name:
        return "art-direction"
    if "moodboard" in name or "mood-board" in name or "mood_board" in name:
        return "moodboard"
    if "mockup" in name or "mock-up" in name or "wireframe" in name:
        return "mockup"
    if "token" in name or ext in {".ase", ".aco"}:
        return "token"
    if ext in {".otf", ".ttf", ".woff", ".woff2"}:
        return "font"
    if "design-system" in name or "design_system" in name or "design system" in name:
        return "design-system"
    if ext in {".pdf", ".md", ".txt", ".html"} and re.search(
        r"brand|style|guide|identity", name
    ):
        return "brand-doc"
    if "prompt" in name and ext in {".md", ".txt", ".json"}:
        return "prompt"
    if lane_concept == "Esther":
        return "art-direction"
    if is_visual_file(path):
        return "ui-export"
    return "other"


def disposition_for(
    *,
    strength: str,
    path: Path,
    in_git: bool,
    frozen: bool,
    dataless: bool,
    kind: str,
    size: int,
) -> tuple[str, str]:
    ext = path.suffix.lower()
    if dataless:
        return "INDEX-ONLY", "dataless"
    if size > OVERSIZE_BYTES or ext in ARCHIVE_EXTS:
        return "REVIEW", "archive" if ext in ARCHIVE_EXTS else "oversize"
    if strength == "weak":
        return "REVIEW", "weak-folder"
    if in_git and ext in SOURCE_EXTS and kind not in COPYABLE_KINDS:
        return "INDEX-ONLY", "git-source"
    if frozen:
        return "COPY", "frozen-preservation"
    if in_git:
        return "COPY", "git-asset"
    return "MOVE", "loose-file"


def classify(path: Path, *, size: int, mtime: str) -> tuple[str, Row | None]:
    """Return ``exclude``, ``ignore``, or ``keep`` plus a row."""
    if is_private(path):
        return "exclude", None
    strength = path_strength(path)
    if strength == "none":
        return "ignore", None
    if strength == "weak" and path.suffix.lower() in WEAK_AUTO_EXTS:
        strength = "strong"
    frozen = is_frozen(path)
    dataless = is_dataless(path)
    repo = git_root(path)
    in_git = repo is not None
    lane, concept = lane_and_concept(path)
    kind = kind_for(path, concept)
    disposition, reason = disposition_for(
        strength=strength,
        path=path,
        in_git=in_git,
        frozen=frozen,
        dataless=dataless,
        kind=kind,
        size=size,
    )
    if strength == "strong" and reason == "loose-file":
        reason = "design-match"
    digest = hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:12]
    dest = "-"
    if disposition in {"MOVE", "COPY", "REVIEW"}:
        dest = str(dest_for(path, lane, concept, kind, digest))
    return "keep", Row(
        id=digest,
        disposition=disposition,
        lane=lane,
        concept=concept,
        kind=kind,
        bytes=size,
        mtime=mtime,
        in_git="yes" if in_git else "no",
        frozen="yes" if frozen else "no",
        origin=str(path),
        dest=dest,
        reason=reason,
    )


def dest_for(path: Path, lane: str, concept: str, kind: str, digest: str) -> Path:
    """Placeholder joined later under the corpus. Stored relative to the corpus."""
    return Path(lane) / concept / kind / f"{path.stem}__{digest}{path.suffix}"


def should_prune(directory: Path, corpus: Path) -> bool:
    name = directory.name
    if name.lower() in PRUNE_DIR_NAMES:
        return True
    if directory.suffix.lower() in PRUNE_SUFFIXES:
        return True
    try:
        if directory.resolve() == corpus.resolve():
            return True
    except OSError:
        return False
    return False


def walk_files(root: Path, corpus: Path, found_leaves: set[str]):
    seed_leaves = {Path(item).name for item in SEED_HOMES}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        if current.name in seed_leaves:
            found_leaves.add(current.name)
        kept: list[str] = []
        for name in dirnames:
            child = current / name
            if should_prune(child, corpus):
                continue
            kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            yield current / name


def hunt(roots: list[Path], corpus: Path, stamp: str) -> int:
    manifest_dir = corpus / MANIFEST_DIRNAME
    manifest_dir.mkdir(parents=True, exist_ok=True)
    rows: list[Row] = []
    seen: set[tuple[int, int]] = set()
    found_leaves: set[str] = set()
    excluded = 0
    permission_errors = 0
    walked = 0
    for root in roots:
        for path in walk_files(root, corpus, found_leaves):
            walked += 1
            if walked % 5000 == 0:
                print(f"walked {walked}", file=sys.stderr)
            try:
                info = path.lstat()
            except OSError:
                permission_errors += 1
                continue
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
                continue
            inode = (info.st_dev, info.st_ino)
            if inode in seen:
                continue
            seen.add(inode)
            try:
                action, row = classify(
                    path,
                    size=info.st_size,
                    mtime=datetime.fromtimestamp(info.st_mtime).isoformat(timespec="seconds"),
                )
            except OSError:
                permission_errors += 1
                continue
            if action == "exclude":
                excluded += 1
                continue
            if row is not None:
                rows.append(row)
    candidates = manifest_dir / f"candidates-{stamp}.tsv"
    write_tsv(candidates, rows)
    review = [row for row in rows if row.disposition == "REVIEW"]
    manifest = manifest_dir / f"manifest-{stamp}.tsv"
    if not review:
        write_tsv(manifest, rows)
    roots_file = manifest_dir / f"roots-{stamp}.txt"
    roots_file.write_text("".join(f"{root}\n" for root in roots), encoding="utf-8")
    summary = manifest_dir / f"summary-{stamp}.md"
    write_summary(
        summary,
        rows=rows,
        roots=roots,
        excluded=excluded,
        permission_errors=permission_errors,
        walked=walked,
        manifest=manifest if not review else candidates,
        review_blocks_apply=bool(review),
        found_leaves=found_leaves,
    )
    print(f"HUNT_COMPLETE candidates={len(rows)} review={len(review)}")
    print(f"SUMMARY {summary}")
    return 0


def write_tsv(path: Path, rows: list[Row]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row.as_dict())


def write_summary(
    path: Path,
    *,
    rows: list[Row],
    roots: list[Path],
    excluded: int,
    permission_errors: int,
    walked: int,
    manifest: Path,
    review_blocks_apply: bool,
    found_leaves: set[str],
) -> None:
    by_disp = Counter(row.disposition for row in rows)
    by_lane = Counter(row.lane for row in rows)
    by_kind = Counter(row.kind for row in rows)
    parents = Counter(str(Path(row.origin).parent) for row in rows)
    lines = [
        "# Design corpus hunt",
        "",
        f"- Files walked: {walked}",
        f"- Candidates: {len(rows)}",
        f"- Private paths omitted: {excluded}",
        f"- Unreadable paths: {permission_errors}",
        f"- Manifest: `{manifest}`",
        "",
        "## Roots",
        "",
    ]
    lines.extend(f"- `{root}`" for root in roots)
    lines.extend(["", "## Seed homes", ""])
    for suffix in SEED_HOMES:
        state = "FOUND" if Path(suffix).name in found_leaves else "MISSING"
        lines.append(f"- {state} `{suffix}`")
    lines.extend(["", "## Disposition", ""])
    for name in ("MOVE", "COPY", "INDEX-ONLY", "REVIEW", "REJECT"):
        lines.append(f"- {name}: {by_disp.get(name, 0)}")
    lines.extend(["", "## Lane", ""])
    for name, count in sorted(by_lane.items()):
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Kind", ""])
    for name, count in sorted(by_kind.items()):
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Top folders", ""])
    for folder, count in parents.most_common(15):
        lines.append(f"- {count} `{folder}`")
    review_rows = [row for row in rows if row.disposition == "REVIEW"]
    lines.extend(["", "## Review", ""])
    if not review_rows:
        lines.append("None. The manifest is ready to file.")
    else:
        lines.append("Resolve these rows in the manifest before consolidate.")
        for row in review_rows[:50]:
            lines.append(f"- `{row.origin}` ({row.reason})")
        if len(review_rows) > 50:
            lines.append(f"- {len(review_rows) - 50} more in the candidates file")
    lines.extend(["", "## Next step", ""])
    if review_blocks_apply:
        lines.append("Set every REVIEW row to MOVE, COPY, INDEX-ONLY, or REJECT.")
        lines.append("Save that file as the manifest, then consolidate.")
    else:
        lines.append("Send `Design hunt: consolidate` to file this manifest.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_roots(manifest: Path) -> list[Path]:
    stamp = manifest.stem.split("-", 1)[1]
    roots_file = manifest.parent / f"roots-{stamp}.txt"
    if not roots_file.is_file():
        raise SystemExit(f"Missing roots file: {roots_file}")
    return [Path(line) for line in roots_file.read_text(encoding="utf-8").splitlines() if line]


def inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def unique_dest(dest: Path, source_hash: str | None) -> Path:
    if dest.is_file() and source_hash is not None and sha256(dest) == source_hash:
        return dest
    candidate = dest
    number = 2
    while candidate.exists():
        candidate = dest.with_name(f"{dest.stem}__{number}{dest.suffix}")
        number += 1
    return candidate


def copy_verified(source: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    source_hash = sha256(source)
    if sha256(dest) != source_hash:
        dest.unlink(missing_ok=True)
        raise OSError(f"hash mismatch after copy: {source}")
    return source_hash


def move_verified(source: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.rename(source, dest)
    except OSError as exc:
        if exc.errno != errno.EXDEV:
            raise
        digest = copy_verified(source, dest)
        source.unlink()
        return digest
    return sha256(dest)


def effective_disposition(row: dict[str, str], *, include_frozen_moves: bool) -> str:
    origin = Path(row["origin"])
    asked = row["disposition"].upper()
    if asked in {"INDEX-ONLY", "REJECT"}:
        return asked
    if asked == "REVIEW":
        return "REVIEW"
    frozen = is_frozen(origin)
    in_git = git_root(origin) is not None
    if asked == "MOVE" and in_git:
        return "COPY"
    if asked == "MOVE" and frozen and not include_frozen_moves:
        return "COPY"
    return asked


def apply_manifest(
    manifest: Path,
    corpus: Path,
    *,
    include_frozen_moves: bool,
) -> int:
    rows = read_tsv(manifest)
    if any(row["disposition"].upper() == "REVIEW" for row in rows):
        print("APPLY_BLOCKED review rows remain", file=sys.stderr)
        return 3
    roots = load_roots(manifest)
    log_path = manifest.parent / f"MOVE_LOG_{datetime.now().strftime('%Y%m%dT%H%M%S')}.tsv"
    acted: list[dict[str, str]] = []
    for row in rows:
        origin = Path(row["origin"])
        if not any(inside(origin, root) for root in roots):
            acted.append(log_row(row, "FAILED", "", "origin outside hunt roots"))
            continue
        if is_private(origin):
            acted.append(
                {
                    "action": "EXCLUDED",
                    "origin": "[omitted]",
                    "dest": "",
                    "sha256": "",
                    "detail": "private",
                    "bytes": "",
                }
            )
            continue
        action = effective_disposition(row, include_frozen_moves=include_frozen_moves)
        if action in {"INDEX-ONLY", "REJECT"}:
            acted.append(log_row(row, action, "", "left in place"))
            continue
        if not origin.is_file() or origin.is_symlink():
            acted.append(log_row(row, "FAILED", "", "missing or symlink"))
            continue
        dest = corpus / row["dest"]
        if not inside(dest, corpus) or MANIFEST_DIRNAME in dest.parts:
            acted.append(log_row(row, "FAILED", "", "dest escaped corpus"))
            continue
        try:
            source_hash = sha256(origin)
            dest = unique_dest(dest, source_hash)
            if dest.exists() and dest.is_file() and sha256(dest) == source_hash:
                acted.append(log_row(row, "SKIP-EXISTS", str(dest), source_hash))
                continue
            if action == "COPY":
                digest = copy_verified(origin, dest)
                acted.append(log_row(row, "COPIED", str(dest), digest))
            elif action == "MOVE":
                digest = move_verified(origin, dest)
                acted.append(log_row(row, "MOVED", str(dest), digest))
            else:
                acted.append(log_row(row, "FAILED", "", f"unknown disposition {action}"))
        except OSError as exc:
            acted.append(log_row(row, "FAILED", "", str(exc)))
    write_log(log_path, acted)
    counts = Counter(item["action"] for item in acted)
    print(
        "APPLY_COMPLETE "
        + " ".join(f"{name}={counts.get(name, 0)}" for name in ("MOVED", "COPIED", "SKIP-EXISTS", "FAILED"))
    )
    print(f"MOVE_LOG {log_path}")
    return 0 if counts.get("FAILED", 0) == 0 else 1


def log_row(row: dict[str, str], action: str, dest: str, detail: str) -> dict[str, str]:
    return {
        "action": action,
        "origin": row["origin"],
        "dest": dest,
        "sha256": detail if len(detail) == 64 else "",
        "detail": detail,
        "bytes": row.get("bytes", ""),
    }


def write_log(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["action", "origin", "dest", "sha256", "detail", "bytes"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def latest_move_log(manifest_dir: Path) -> Path:
    logs = sorted(manifest_dir.glob("MOVE_LOG_*.tsv"), key=lambda item: item.stat().st_mtime)
    if not logs:
        raise SystemExit(f"No move log in {manifest_dir}")
    return logs[-1]


def undo(corpus: Path) -> int:
    manifest_dir = corpus / MANIFEST_DIRNAME
    log_path = latest_move_log(manifest_dir)
    rows = read_tsv(log_path)
    undo_rows: list[dict[str, str]] = []
    for row in rows:
        action = row["action"]
        origin = Path(row["origin"]) if row["origin"] else None
        dest = Path(row["dest"]) if row["dest"] else None
        recorded = row.get("sha256", "")
        if action == "COPIED" and dest and dest.is_file() and origin and origin.is_file():
            if sha256(dest) == recorded and sha256(origin) == recorded:
                dest.unlink()
                undo_rows.append({**row, "action": "UNDO-COPY"})
            else:
                undo_rows.append({**row, "action": "FAILED", "detail": "hash changed"})
        elif action == "MOVED" and dest and dest.is_file() and origin and not origin.exists():
            if sha256(dest) == recorded:
                origin.parent.mkdir(parents=True, exist_ok=True)
                os.rename(dest, origin)
                undo_rows.append({**row, "action": "UNDO-MOVE"})
            else:
                undo_rows.append({**row, "action": "FAILED", "detail": "hash changed"})
        elif action in {"MOVED", "COPIED"}:
            undo_rows.append({**row, "action": "FAILED", "detail": "origin state changed"})
        else:
            undo_rows.append({**row, "action": "SKIP", "detail": action})
    undo_path = manifest_dir / f"UNDO_LOG_{datetime.now().strftime('%Y%m%dT%H%M%S')}.tsv"
    write_log(undo_path, undo_rows)
    print(f"UNDO_COMPLETE log={undo_path}")
    return 0


def cmd_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "disk"
        corpus = Path(tmp) / "Design_Corpus"
        loose = root / "Desktop" / "ChefWho_Design_System"
        frozen = (
            root
            / "Documents"
            / "AFSTYLE_BUSINESS_MASTER_ARCHIVE"
            / "90_SOURCE_PRESERVATION"
            / "Cursor"
            / "CURSOR_SOURCE_BUNDLE_2026-07-21"
            / "ChefWho_Design_System"
        )
        private = root / "Documents" / "medical"
        repo = root / "Documents" / "repo"
        esther = root / "Downloads"
        weak = root / "Desktop" / "design"
        for directory in (loose, frozen, private, repo / "app", repo / "design-system", esther, weak):
            directory.mkdir(parents=True)
        (repo / ".git").mkdir()
        (loose / "logo.png").write_bytes(b"logo-loose")
        (loose / "archive.zip").write_bytes(b"zip")
        (frozen / "logo.png").write_bytes(b"logo-frozen")
        (private / "logo.png").write_bytes(b"secret")
        (repo / "app" / "page.tsx").write_text("export default function Page(){return null}")
        (repo / "design-system" / "tokens.css").write_text(":root { --bg: #fff; }")
        (repo / "public").mkdir()
        (repo / "public" / "swm-logo.svg").write_text("<svg></svg>")
        (esther / "moodboard-esther.png").write_bytes(b"esther")
        (esther / "logout.png").write_bytes(b"nope")
        (esther / "random.png").write_bytes(b"nope")
        (esther / "Inter.woff2").write_bytes(b"font")
        (loose / "Display.otf").write_bytes(b"font")
        (weak / "notes.txt").write_text("maybe")
        (root / "Desktop" / "logout.png").write_bytes(b"nope")
        stamp = "2099-01-01"
        code = hunt([root], corpus, stamp)
        if code != 0:
            return code
        by_origin = {
            row["origin"]: row
            for row in read_tsv(corpus / MANIFEST_DIRNAME / f"candidates-{stamp}.tsv")
        }
        failures = []
        wanted = {
            str(loose / "logo.png"): ("MOVE", "ChefsWho.codes", "ChefWho", "logo"),
            str(loose / "Display.otf"): ("MOVE", "ChefsWho.codes", "ChefWho", "font"),
            str(loose / "archive.zip"): ("REVIEW", "ChefsWho.codes", "ChefWho", "design-system"),
            str(frozen / "logo.png"): ("COPY", "ChefsWho.codes", "ChefWho", "logo"),
            str(repo / "design-system" / "tokens.css"): ("COPY", "Unmapped", "design system", "token"),
            str(repo / "public" / "swm-logo.svg"): ("COPY", "SWM Filings", "SWM", "logo"),
            str(esther / "moodboard-esther.png"): ("MOVE", "Unmapped", "Esther", "moodboard"),
            str(weak / "notes.txt"): ("REVIEW", "Unmapped", "design", "other"),
        }
        for origin, expected in wanted.items():
            row = by_origin.get(origin)
            if row is None:
                failures.append(f"missing {origin}")
                continue
            actual = (row["disposition"], row["lane"], row["concept"], row["kind"])
            if actual != expected:
                failures.append(f"{origin}: {actual} != {expected}")
        for absent in (
            private / "logo.png",
            esther / "logout.png",
            esther / "random.png",
            repo / "app" / "page.tsx",
            root / "Desktop" / "logout.png",
            esther / "Inter.woff2",
        ):
            if str(absent) in by_origin:
                failures.append(f"should ignore {absent}")
        manifest = corpus / MANIFEST_DIRNAME / f"manifest-{stamp}.tsv"
        if manifest.exists():
            failures.append("manifest written while REVIEW rows exist")
        blocked = apply_manifest(corpus / MANIFEST_DIRNAME / f"candidates-{stamp}.tsv", corpus, include_frozen_moves=False)
        if blocked != 3:
            failures.append(f"apply should block review, got {blocked}")
        ready = [row for row in read_tsv(corpus / MANIFEST_DIRNAME / f"candidates-{stamp}.tsv") if row["disposition"] != "REVIEW"]
        ready_path = corpus / MANIFEST_DIRNAME / f"manifest-{stamp}.tsv"
        write_tsv_dicts(ready_path, ready)
        # roots file already written for this stamp
        apply_code = apply_manifest(ready_path, corpus, include_frozen_moves=False)
        if apply_code != 0:
            failures.append(f"apply failed {apply_code}")
        if (loose / "logo.png").exists():
            failures.append("loose logo was not moved")
        if not (frozen / "logo.png").exists():
            failures.append("frozen logo was moved")
        if not (repo / "public" / "swm-logo.svg").exists():
            failures.append("git logo was moved")
        copied = list((corpus / "ChefsWho.codes" / "ChefWho" / "logo").glob("logo__*.png"))
        if len(copied) != 2:
            failures.append(f"expected 2 chefwho logos in corpus, found {len(copied)}")
        moved = [path for path in copied if path.read_bytes() == b"logo-loose"]
        if len(moved) != 1:
            failures.append("loose logo bytes missing from corpus")
        undo_code = undo(corpus)
        if undo_code != 0:
            failures.append(f"undo failed {undo_code}")
        if not (loose / "logo.png").exists():
            failures.append("undo did not restore loose logo")
        if not (frozen / "logo.png").exists():
            failures.append("undo removed frozen original")
        if list((corpus / "ChefsWho.codes" / "ChefWho" / "logo").glob("logo__*.png")):
            failures.append("undo left chefwho logo copies in the corpus")
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        print("SELF_TEST_OK")
        return 0


def write_tsv_dicts(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hunt and file local design material.")
    sub = parser.add_subparsers(dest="command", required=True)
    hunt_parser = sub.add_parser("hunt")
    hunt_parser.add_argument("--home", type=Path, default=Path.home())
    hunt_parser.add_argument("--root", type=Path, action="append", dest="roots")
    hunt_parser.add_argument("--corpus", type=Path)
    hunt_parser.add_argument("--stamp")
    apply_parser = sub.add_parser("apply")
    apply_parser.add_argument("--manifest", type=Path, required=True)
    apply_parser.add_argument("--corpus", type=Path)
    apply_parser.add_argument("--home", type=Path, default=Path.home())
    apply_parser.add_argument("--confirm", required=True)
    apply_parser.add_argument("--include-frozen-moves", action="store_true")
    undo_parser = sub.add_parser("undo")
    undo_parser.add_argument("--corpus", type=Path)
    undo_parser.add_argument("--home", type=Path, default=Path.home())
    undo_parser.add_argument("--confirm", required=True)
    sub.add_parser("self-test")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "self-test":
        return cmd_self_test()
    home = args.home
    corpus = args.corpus or default_corpus(home)
    if args.command == "hunt":
        roots = args.roots or default_roots(home)
        roots = [path for path in roots if path.exists()]
        if not roots:
            print("NO_ROOTS readable search roots are missing", file=sys.stderr)
            return 2
        stamp = args.stamp or datetime.now().strftime("%Y-%m-%d")
        return hunt(roots, corpus, stamp)
    if args.command == "apply":
        if args.confirm != "consolidate":
            print("APPLY_BLOCKED confirmation must be consolidate", file=sys.stderr)
            return 3
        return apply_manifest(args.manifest, corpus, include_frozen_moves=args.include_frozen_moves)
    if args.command == "undo":
        if args.confirm != "undo":
            print("UNDO_BLOCKED confirmation must be undo", file=sys.stderr)
            return 3
        return undo(corpus)
    return 2


if __name__ == "__main__":
    sys.exit(main())
