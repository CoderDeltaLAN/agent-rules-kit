"""Command line entry point for agent-rules-kit."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from agent_rules_kit import __version__
from agent_rules_kit.budget import BudgetReport, build_budget_report
from agent_rules_kit.discovery import InstructionFile, discover_instruction_files
from agent_rules_kit.explain import (
    RuleExplanation,
    get_rule_explanation,
    list_rule_explanations,
)
from agent_rules_kit.findings import Finding
from agent_rules_kit.governance import find_governance_findings
from agent_rules_kit.init_plan import InitPlan, build_init_plan
from agent_rules_kit.init_write import InitWriteResult, write_init_files
from agent_rules_kit.redaction import redact_secret_like_values

OUTPUT_FORMATS = ("console", "json", "markdown")


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
    check_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="console",
        help="Output format. Defaults to console.",
    )

    init_parser = subparsers.add_parser(
        "init",
        help="Plan baseline agent instruction files without writing by default.",
    )
    init_parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )
    init_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview planned file changes without modifying files.",
    )
    init_parser.add_argument(
        "--write",
        action="store_true",
        help="Write baseline files, backing up existing files first.",
    )

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Summarize repository-level instruction health.",
    )
    doctor_parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )

    budget_parser = subparsers.add_parser(
        "budget",
        help="Estimate local instruction-file size and context pressure.",
    )
    budget_parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )

    explain_parser = subparsers.add_parser(
        "explain",
        help="Explain known governance rule IDs.",
    )
    explain_parser.add_argument(
        "rule_id",
        nargs="?",
        help="Known rule ID to explain, such as AIRK-GOV003.",
    )
    explain_parser.add_argument(
        "--list",
        action="store_true",
        dest="list_rules",
        help="List known rule IDs.",
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
        return _run_check(Path(args.repository), output_format=args.format)

    if args.command == "init":
        return _run_init(
            Path(args.repository),
            dry_run=args.dry_run,
            write=args.write,
        )

    if args.command == "doctor":
        return _run_doctor(Path(args.repository))

    if args.command == "budget":
        return _run_budget(Path(args.repository))

    if args.command == "explain":
        return _run_explain(args.rule_id, list_rules=args.list_rules)

    parser.print_help()
    return 0


def _run_explain(rule_id: str | None, *, list_rules: bool) -> int:
    if list_rules and rule_id is not None:
        print("ERROR: explain accepts either --list or a rule ID.", file=sys.stderr)
        return 2

    if list_rules:
        _print_known_rules()
        return 0

    if rule_id is None:
        print("ERROR: explain requires --list or RULE_ID.", file=sys.stderr)
        return 2

    explanation = get_rule_explanation(rule_id)
    if explanation is None:
        print(
            f"ERROR: unknown rule ID: {redact_secret_like_values(rule_id)}",
            file=sys.stderr,
        )
        return 2

    _print_rule_explanation(explanation)
    return 0


def _print_known_rules() -> None:
    print("agent-rules-kit explain")
    print("Known rules:")
    for explanation in list_rule_explanations():
        print(
            f"- {explanation.rule_id} [{explanation.category}] "
            f"{explanation.title}"
        )


def _print_rule_explanation(explanation: RuleExplanation) -> None:
    print(f"agent-rules-kit explain: {explanation.rule_id}")
    print(f"Title: {explanation.title}")
    print(f"Category: {explanation.category}")
    print(f"Summary: {explanation.summary}")
    print(f"Limits: {explanation.limits}")


def _run_budget(repository_root: Path) -> int:
    try:
        instruction_files = discover_instruction_files(repository_root)
        report = build_budget_report(repository_root, instruction_files)
    except ValueError as error:
        print(f"ERROR: {redact_secret_like_values(str(error))}", file=sys.stderr)
        return 2

    return _print_console_budget(repository_root, report)


def _print_console_budget(repository_root: Path, report: BudgetReport) -> int:
    print(f"agent-rules-kit budget: {redact_secret_like_values(str(repository_root))}")

    if not report.files:
        print("Status: no_instruction_files")
        print("Supported instruction files: 0")
        print("Total bytes: 0")
        print("Total characters: 0")
        print("Total lines: 0")
        print("Approximate words: 0")
        print(
            "Next step: add a supported agent instruction file before estimating "
            "context pressure."
        )
        return 1

    print("Status: ok")
    print(f"Supported instruction files: {len(report.files)}")
    print(f"Total bytes: {report.total_bytes}")
    print(f"Total characters: {report.total_characters}")
    print(f"Total lines: {report.total_lines}")
    print(f"Approximate words: {report.total_approximate_words}")
    print("Files:")

    for file_item in report.files:
        path = redact_secret_like_values(file_item.path)
        print(
            f"- {path} [{file_item.kind}] - "
            f"{file_item.byte_count} bytes, "
            f"{file_item.character_count} characters, "
            f"{file_item.line_count} lines, "
            f"{file_item.approximate_word_count} approximate words"
        )

    print("Next step: review large instruction files before adding more agent guidance.")
    return 0


def _run_doctor(repository_root: Path) -> int:
    try:
        instruction_files = discover_instruction_files(repository_root)
    except ValueError as error:
        print(f"ERROR: {redact_secret_like_values(str(error))}", file=sys.stderr)
        return 2

    findings = find_governance_findings(repository_root, instruction_files)
    return _print_console_doctor(repository_root, instruction_files, findings)


def _print_console_doctor(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
    findings: tuple[Finding, ...],
) -> int:
    print(f"agent-rules-kit doctor: {redact_secret_like_values(str(repository_root))}")

    if not instruction_files:
        print("Status: no_instruction_files")
        print("Supported instruction files: 0")
        print("Findings: 0")
        print(
            "Next step: add a supported agent instruction file before reviewing "
            "governance findings."
        )
        return 1

    status = "review" if findings else "ok"
    print(f"Status: {status}")
    print(f"Supported instruction files: {len(instruction_files)}")
    print(f"Findings: {len(findings)}")

    if findings:
        print("Findings by severity:")
        for severity, count in _count_findings_by_severity(findings):
            print(f"- {severity}: {count}")

        print("Findings by rule:")
        for rule_id, count in _count_findings_by_rule(findings):
            print(f"- {rule_id}: {count}")

        print("Next step: review the listed governance findings with `agent-rules-kit check`.")
    else:
        print("Next step: no governance findings were detected by implemented checks.")

    return 0


def _count_findings_by_severity(
    findings: tuple[Finding, ...],
) -> tuple[tuple[str, int], ...]:
    counts: dict[str, int] = {}

    for finding in findings:
        severity = finding.severity.value
        counts[severity] = counts.get(severity, 0) + 1

    return tuple(
        (severity, counts[severity])
        for severity in ("info", "warning", "error")
        if severity in counts
    )


def _count_findings_by_rule(
    findings: tuple[Finding, ...],
) -> tuple[tuple[str, int], ...]:
    counts: dict[str, int] = {}

    for finding in findings:
        counts[finding.rule_id] = counts.get(finding.rule_id, 0) + 1

    return tuple(counts.items())


def _run_check(repository_root: Path, *, output_format: str = "console") -> int:
    try:
        instruction_files = discover_instruction_files(repository_root)
    except ValueError as error:
        payload = _build_check_error_payload(repository_root, error)

        if output_format == "json":
            _print_json(payload)
        elif output_format == "markdown":
            _print_markdown(payload)
        else:
            print(f"ERROR: {payload['error']['message']}", file=sys.stderr)

        return 2

    status = "ok" if instruction_files else "no_instruction_files"
    findings = find_governance_findings(repository_root, instruction_files)
    payload = _build_check_payload(
        repository_root,
        instruction_files,
        findings=findings,
        status=status,
    )

    if output_format == "json":
        _print_json(payload)
    elif output_format == "markdown":
        _print_markdown(payload)
    else:
        return _print_console_check(repository_root, instruction_files, findings)

    return 0 if instruction_files else 1


def _print_console_check(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
    findings: tuple[Finding, ...],
) -> int:
    print(f"agent-rules-kit check: {repository_root}")

    if not instruction_files:
        print("No supported agent instruction files found.")
        return 1

    print(f"Found {len(instruction_files)} supported instruction file(s):")
    for instruction_file in instruction_files:
        print(f"- {instruction_file.path} [{instruction_file.kind.value}]")

    if findings:
        print("Findings:")
        for finding in findings:
            location = _format_finding_location(finding)
            print(
                f"- {finding.rule_id} [{finding.severity.value}] "
                f"{location} - {redact_secret_like_values(finding.message)}"
            )

    return 0


def _run_init(repository_root: Path, *, dry_run: bool, write: bool) -> int:
    if dry_run and write:
        print("ERROR: init accepts only one mode: --dry-run or --write.", file=sys.stderr)
        return 2

    if not dry_run and not write:
        print("ERROR: init currently requires --dry-run or --write.", file=sys.stderr)
        return 2

    try:
        if dry_run:
            plan = build_init_plan(repository_root)
            _print_init_dry_run(plan)
        else:
            result = write_init_files(repository_root)
            _print_init_write(result)
    except ValueError as error:
        print(f"ERROR: {redact_secret_like_values(str(error))}", file=sys.stderr)
        return 2

    return 0


def _print_init_dry_run(plan: InitPlan) -> None:
    print(f"agent-rules-kit init: {redact_secret_like_values(plan.repository)}")
    print("Mode: dry-run")
    print("No files will be modified.")
    print("Planned file actions:")

    for file_item in plan.files:
        path = redact_secret_like_values(file_item.path)
        reason = redact_secret_like_values(file_item.reason)
        print(f"- {path} [{file_item.action.value}] - {reason}")


def _print_init_write(result: InitWriteResult) -> None:
    print(f"agent-rules-kit init: {redact_secret_like_values(result.repository)}")
    print("Mode: write")
    print("Files modified:")

    for file_item in result.files:
        path = redact_secret_like_values(file_item.path)
        if file_item.backup_path is None:
            print(f"- {path} [{file_item.action.value}]")
        else:
            backup_path = redact_secret_like_values(file_item.backup_path)
            print(f"- {path} [{file_item.action.value}] - backup: {backup_path}")


def _build_check_payload(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
    *,
    findings: tuple[Finding, ...],
    status: str,
) -> dict[str, object]:
    return {
        "command": "check",
        "status": status,
        "repository": redact_secret_like_values(str(repository_root)),
        "instruction_files": [
            {
                "path": redact_secret_like_values(instruction_file.path),
                "kind": instruction_file.kind.value,
            }
            for instruction_file in instruction_files
        ],
        "summary": {
            "supported_instruction_file_count": len(instruction_files),
            "finding_count": len(findings),
        },
        "findings": [_build_finding_payload(finding) for finding in findings],
        "error": None,
    }


def _build_check_error_payload(
    repository_root: Path,
    error: ValueError,
) -> dict[str, object]:
    return {
        "command": "check",
        "status": "error",
        "repository": redact_secret_like_values(str(repository_root)),
        "instruction_files": [],
        "summary": {
            "supported_instruction_file_count": 0,
            "finding_count": 0,
        },
        "findings": [],
        "error": {
            "message": redact_secret_like_values(str(error)),
        },
    }


def _print_json(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _print_markdown(payload: dict[str, object]) -> None:
    print("# agent-rules-kit check")
    print()
    print(f"- Repository: {_markdown_value(str(payload['repository']))}")
    print(f"- Status: {_markdown_value(str(payload['status']))}")
    print(
        "- Supported instruction files: "
        f"{payload['summary']['supported_instruction_file_count']}"
    )
    print(f"- Findings: {payload['summary']['finding_count']}")

    error = payload["error"]
    if error is not None:
        print()
        print(f"Error: {_markdown_value(str(error['message']))}")
        return

    instruction_files = payload["instruction_files"]
    if not instruction_files:
        print()
        print("No supported agent instruction files found.")
        return

    print()
    print("| Path | Kind |")
    print("| --- | --- |")
    for instruction_file in instruction_files:
        path = _markdown_value(str(instruction_file["path"]))
        kind = _markdown_value(str(instruction_file["kind"]))
        print(f"| {path} | {kind} |")

    findings = payload["findings"]
    if findings:
        print()
        print("## Findings")
        print()
        print("| Rule | Severity | Location | Message |")
        print("| --- | --- | --- | --- |")
        for finding in findings:
            rule_id = _markdown_value(str(finding["rule_id"]))
            severity = _markdown_value(str(finding["severity"]))
            location = _markdown_value(_format_finding_payload_location(finding))
            message = _markdown_value(str(finding["message"]))
            print(f"| {rule_id} | {severity} | {location} | {message} |")


def _build_finding_payload(finding: Finding) -> dict[str, str | int]:
    payload = finding.to_dict()

    if "message" in payload:
        payload["message"] = redact_secret_like_values(str(payload["message"]))
    if "path" in payload:
        payload["path"] = redact_secret_like_values(str(payload["path"]))
    if "evidence" in payload:
        payload["evidence"] = redact_secret_like_values(str(payload["evidence"]))

    return payload


def _format_finding_location(finding: Finding) -> str:
    if finding.path is None:
        return "repository"
    if finding.line is None:
        return redact_secret_like_values(finding.path)
    return f"{redact_secret_like_values(finding.path)}:{finding.line}"


def _format_finding_payload_location(finding: dict[str, object]) -> str:
    path_value = finding.get("path")
    if path_value is None:
        return "repository"

    line_value = finding.get("line")
    if line_value is None:
        return str(path_value)

    return f"{path_value}:{line_value}"


def _markdown_value(value: str) -> str:
    return redact_secret_like_values(value).replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
