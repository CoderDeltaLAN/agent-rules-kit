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

    def test_doctor_clean_fixture_matches_golden_output(self) -> None:
        repository = FIXTURE_ROOT / "single-agent"

        result = run_cli(["doctor", str(repository)])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout,
            f"agent-rules-kit doctor: {repository}\n"
            "Status: ok\n"
            "Supported instruction files: 1\n"
            "Findings: 0\n"
            "Next step: no governance findings were detected by implemented checks.\n",
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

    def test_current_cli_contract_matrix_matches_expected_channels_and_exit_codes(self) -> None:
        cases = [
            {
                "name": "version",
                "args": ["--version"],
                "exit_code": 0,
                "stdout_contains": ["agent-rules-kit 0.2.3\n"],
                "stderr": "",
            },
            {
                "name": "help-without-command",
                "args": [],
                "exit_code": 0,
                "stdout_contains": ["usage: agent-rules-kit", "check", "init"],
                "stderr": "",
            },
            {
                "name": "check-console-clean",
                "args": ["check", str(FIXTURE_ROOT / "single-agent")],
                "exit_code": 0,
                "stdout_contains": [
                    "Found 1 supported instruction file(s):",
                    "- AGENTS.md [agents]",
                ],
                "stderr": "",
            },
            {
                "name": "check-console-empty",
                "args": ["check", str(FIXTURE_ROOT / "empty-repo")],
                "exit_code": 1,
                "stdout_contains": ["No supported agent instruction files found."],
                "stderr": "",
            },
            {
                "name": "check-json-clean",
                "args": ["check", str(FIXTURE_ROOT / "single-agent"), "--format", "json"],
                "exit_code": 0,
                "json_status": "ok",
                "stderr": "",
            },
            {
                "name": "check-json-empty",
                "args": ["check", str(FIXTURE_ROOT / "empty-repo"), "--format", "json"],
                "exit_code": 1,
                "json_status": "no_instruction_files",
                "stderr": "",
            },
            {
                "name": "check-markdown-clean",
                "args": ["check", str(FIXTURE_ROOT / "single-agent"), "--format", "markdown"],
                "exit_code": 0,
                "stdout_contains": ["# agent-rules-kit check", "- Status: ok"],
                "stderr": "",
            },
            {
                "name": "check-markdown-empty",
                "args": ["check", str(FIXTURE_ROOT / "empty-repo"), "--format", "markdown"],
                "exit_code": 1,
                "stdout_contains": ["# agent-rules-kit check", "- Status: no_instruction_files"],
                "stderr": "",
            },
            {
                "name": "doctor-clean",
                "args": ["doctor", str(FIXTURE_ROOT / "single-agent")],
                "exit_code": 0,
                "stdout_contains": ["Status: ok", "Supported instruction files: 1"],
                "stderr": "",
            },
            {
                "name": "doctor-empty",
                "args": ["doctor", str(FIXTURE_ROOT / "empty-repo")],
                "exit_code": 1,
                "stdout_contains": ["Status: no_instruction_files", "Findings: 0"],
                "stderr": "",
            },
            {
                "name": "init-dry-run",
                "args": ["init", str(FIXTURE_ROOT / "single-agent"), "--dry-run"],
                "exit_code": 0,
                "stdout_contains": ["Mode: dry-run", "No files will be modified."],
                "stderr": "",
            },
            {
                "name": "init-missing-mode",
                "args": ["init", str(FIXTURE_ROOT / "single-agent")],
                "exit_code": 2,
                "stdout": "",
                "stderr": "ERROR: init currently requires --dry-run or --write.\n",
            },
        ]

        for case in cases:
            with self.subTest(case=case["name"]):
                result = run_cli(case["args"])

                self.assertEqual(result.exit_code, case["exit_code"])
                if "stdout" in case:
                    self.assertEqual(result.stdout, case["stdout"])
                for expected_text in case.get("stdout_contains", []):
                    self.assertIn(expected_text, result.stdout)
                if "json_status" in case:
                    payload = json.loads(result.stdout)
                    self.assertEqual(payload["status"], case["json_status"])
                self.assertEqual(result.stderr, case["stderr"])


if __name__ == "__main__":
    unittest.main()
