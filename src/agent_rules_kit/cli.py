"""Command line entry point for agent-rules-kit."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from agent_rules_kit import __version__
from agent_rules_kit.discovery import discover_instruction_files


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        prog="agent-rules-kit",
        description="Diagnose baseline quality of AI agent instruction files in repositories.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the package version and exit.",
    )

    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser(
        "check",
        help="Discover supported agent instruction files in a repository.",
    )
    check_parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"agent-rules-kit {__version__}")
        return 0

    if args.command == "check":
        return _run_check(Path(args.repository))

    parser.print_help()
    return 0


def _run_check(repository_root: Path) -> int:
    try:
        instruction_files = discover_instruction_files(repository_root)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    print(f"agent-rules-kit check: {repository_root}")

    if not instruction_files:
        print("No supported agent instruction files found.")
        return 1

    print(f"Found {len(instruction_files)} supported instruction file(s):")
    for instruction_file in instruction_files:
        print(f"- {instruction_file.path} [{instruction_file.kind.value}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
