from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path

from agent_rules_kit.cli import main

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "repositories"


@dataclass(frozen=True, slots=True)
class CliRun:
    exit_code: int
    stdout: str
    stderr: str


def run_cli(args: list[str]) -> CliRun:
    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = main(args)

    return CliRun(
        exit_code=exit_code,
        stdout=stdout.getvalue(),
        stderr=stderr.getvalue(),
    )


class GoldenOutputTests(unittest.TestCase):
    maxDiff = None

    def test_check_console_clean_fixture_matches_golden_output(self) -> None:
        repository = FIXTURE_ROOT / "single-agent"

        result = run_cli(["check", str(repository)])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout,
            f"agent-rules-kit check: {repository}\n"
            "Found 1 supported instruction file(s):\n"
            "- AGENTS.md [agents]\n",
        )

    def test_check_json_clean_fixture_matches_golden_output(self) -> None:
        repository = FIXTURE_ROOT / "single-agent"

        result = run_cli(["check", str(repository), "--format", "json"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            json.loads(result.stdout),
            {
                "command": "check",
                "error": None,
                "findings": [],
                "instruction_files": [
                    {
                        "kind": "agents",
                        "path": "AGENTS.md",
                    },
                ],
                "repository": str(repository),
                "status": "ok",
                "summary": {
                    "finding_count": 0,
                    "supported_instruction_file_count": 1,
                },
            },
        )
        self.assertEqual(
            result.stdout,
            "{\n"
            '  "command": "check",\n'
            '  "error": null,\n'
            '  "findings": [],\n'
            '  "instruction_files": [\n'
            "    {\n"
            '      "kind": "agents",\n'
            '      "path": "AGENTS.md"\n'
            "    }\n"
            "  ],\n"
            f'  "repository": "{repository}",\n'
            '  "status": "ok",\n'
            '  "summary": {\n'
            '    "finding_count": 0,\n'
            '    "supported_instruction_file_count": 1\n'
            "  }\n"
            "}\n",
        )

    def test_check_console_no_instruction_files_matches_golden_output(self) -> None:
        repository = FIXTURE_ROOT / "empty-repo"

        result = run_cli(["check", str(repository)])

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout,
            f"agent-rules-kit check: {repository}\n"
            "No supported agent instruction files found.\n",
        )

    def test_check_markdown_governance_fixture_matches_golden_output(self) -> None:
        repository = FIXTURE_ROOT / "risky-instructions"
        message = (
            "Instruction file appears to encourage bypassing review, CI, "
            "or safe integration boundaries."
        )

        result = run_cli(["check", str(repository), "--format", "markdown"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout,
            "# agent-rules-kit check\n"
            "\n"
            f"- Repository: {repository}\n"
            "- Status: ok\n"
            "- Supported instruction files: 1\n"
            "- Findings: 3\n"
            "\n"
            "| Path | Kind |\n"
            "| --- | --- |\n"
            "| AGENTS.md | agents |\n"
            "\n"
            "## Findings\n"
            "\n"
            "| Rule | Severity | Location | Message |\n"
            "| --- | --- | --- | --- |\n"
            f"| AIRK-GOV003 | warning | AGENTS.md:7 | {message} |\n"
            f"| AIRK-GOV003 | warning | AGENTS.md:8 | {message} |\n"
            f"| AIRK-GOV003 | warning | AGENTS.md:10 | {message} |\n",
        )

    def test_init_dry_run_existing_agents_file_matches_golden_output(self) -> None:
        repository = FIXTURE_ROOT / "single-agent"

        result = run_cli(["init", str(repository), "--dry-run"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout,
            f"agent-rules-kit init: {repository}\n"
            "Mode: dry-run\n"
            "No files will be modified.\n"
            "Planned file actions:\n"
            "- AGENTS.md [backup-and-replace] - "
            "existing file would be backed up before replacement\n",
        )

    def test_init_without_mode_matches_golden_error_output(self) -> None:
        repository = FIXTURE_ROOT / "single-agent"

        result = run_cli(["init", str(repository)])

        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr,
            "ERROR: init currently requires --dry-run or --write.\n",
        )


if __name__ == "__main__":
    unittest.main()
