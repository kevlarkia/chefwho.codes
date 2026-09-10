"""Content addressing for museum packages."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_sha256sums(path: Path, files: dict[str, str]) -> None:
    lines = [f"{digest}  {relative}" for relative, digest in sorted(files.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_sha256sums(path: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        mapping[relative] = digest
    return mapping
