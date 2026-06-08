"""Command line entry point for agent-rules-kit."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from agent_rules_kit import __version__


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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"agent-rules-kit {__version__}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
