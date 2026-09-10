"""Command-line entry for the dual-pass archive pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .errors import MuseumIntegrityError, MuseumPackageError
from .llm import PROVIDER_ENV
from .pipeline import ForensicArchiver
from .verify import verify_package


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="forensic-archive",
        description=(
            "Run TEMP-ARC-001 then TEMP-ARC-002 and package archive.json "
            "with forensic_archive.sqlite."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    archive = sub.add_parser("archive", help="Generate an archive + SQLite ledger")
    archive.add_argument("source", type=Path, help="Source file to archive")
    archive.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directory that will hold archive.json and forensic_archive.sqlite",
    )
    archive.add_argument(
        "--profile",
        default="generic",
        help="Archive profile (generic or swm). SWM is one domain, not the toolkit.",
    )
    archive.add_argument(
        "--provider",
        default=None,
        help=f"LLM provider (dummy, anthropic, openai, vertex). Overrides {PROVIDER_ENV}.",
    )

    verify = sub.add_parser("verify", help="Verify a packaged museum archive")
    verify.add_argument("package", type=Path, help="Output directory to verify")
    verify.add_argument("--run-id", default=None, help="Verify a specific run id")

    sub.add_parser("providers", help="List LLM provider ids")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "providers":
        print("dummy")
        print("anthropic")
        print("openai")
        print("vertex")
        return 0

    if args.command == "verify":
        report = verify_package(args.package, run_id=args.run_id)
        print(
            json.dumps(
                {
                    "ok": report.ok,
                    "run_id": report.run_id,
                    "errors": report.errors,
                    "warnings": report.warnings,
                    "checks": report.checks,
                },
                indent=2,
            )
        )
        return 0 if report.ok else 2

    source = args.source
    if not source.is_file():
        parser.error(f"source file not found: {source}")

    try:
        archiver = ForensicArchiver(profile=args.profile, provider=args.provider)
        result = archiver.run(source, args.output)
    except (MuseumPackageError, MuseumIntegrityError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    print(
        json.dumps(
            {
                "ok": True,
                "run_id": result.run_id,
                "profile": result.profile,
                "provider": result.provider,
                "archive": str(result.archive_path),
                "snapshot": str(result.snapshot_path),
                "ledger": str(result.ledger_path),
                "inclusions": len(result.inclusions),
                "exclusions": len(result.exclusions),
                "verified": bool(result.verification and result.verification.ok),
                "llm": result.llm_traces,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
