from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from agent_rules_kit.cli import main

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "repositories"

REVIEW_CI_BYPASS_MESSAGE = (
    "Instruction file appears to encourage bypassing review, CI, or safe integration "
    "boundaries."
)
COMMAND_CONFIRMATION_MESSAGE = (
    "Instruction file appears to encourage unsafe command execution without an explicit "
    "confirmation boundary."
)
RUNTIME_NETWORK_LLM_MESSAGE = (
    "Instruction file appears to encourage runtime network, LLM, or external API use that "
    "conflicts with local-first boundaries."
)


class CliTests(unittest.TestCase):
    def test_version_flag_prints_version(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["--version"])

        self.assertEqual(exit_code, 0)
        self.assertIn("agent-rules-kit 0.2.0", output.getvalue())

    def test_help_is_default(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main([])

        self.assertEqual(exit_code, 0)
        self.assertIn("usage:", output.getvalue())
        self.assertIn("check", output.getvalue())

    def test_check_reports_discovered_instruction_files(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "multi-agent-overlap")])

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Found 6 supported instruction file(s):", text)
        self.assertIn("- AGENTS.md [agents]", text)
        self.assertIn("- CLAUDE.md [claude]", text)
        self.assertIn("- GEMINI.md [gemini]", text)
        self.assertIn("- .cursor/rules/agent-rules.mdc [cursor-rule]", text)
        self.assertIn("- .github/copilot-instructions.md [copilot]", text)
        self.assertIn(
            "- .github/instructions/agents.instructions.md [github-instruction]",
            text,
        )

    def test_check_returns_one_when_no_instruction_files_are_found(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "empty-repo")])

        self.assertEqual(exit_code, 1)
        self.assertIn("No supported agent instruction files found.", output.getvalue())

    def test_check_returns_two_for_invalid_repository_root(self) -> None:
        output = io.StringIO()

        with redirect_stderr(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "missing-repo")])

        self.assertEqual(exit_code, 2)
        self.assertIn("ERROR: repository root does not exist:", output.getvalue())

    def test_check_reports_discovered_instruction_files_as_json(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "multi-agent-overlap"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["command"], "check")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["error"], None)
        self.assertEqual(payload["summary"]["supported_instruction_file_count"], 6)
        self.assertEqual(
            payload["instruction_files"],
            [
                {"path": "AGENTS.md", "kind": "agents"},
                {"path": "CLAUDE.md", "kind": "claude"},
                {"path": "GEMINI.md", "kind": "gemini"},
                {
                    "path": ".github/copilot-instructions.md",
                    "kind": "copilot",
                },
                {
                    "path": ".cursor/rules/agent-rules.mdc",
                    "kind": "cursor-rule",
                },
                {
                    "path": ".github/instructions/agents.instructions.md",
                    "kind": "github-instruction",
                },
            ],
        )

    def test_check_json_returns_one_when_no_instruction_files_are_found(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "empty-repo"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 1)
        self.assertEqual(payload["status"], "no_instruction_files")
        self.assertEqual(payload["instruction_files"], [])
        self.assertEqual(payload["summary"]["supported_instruction_file_count"], 0)
        self.assertEqual(payload["error"], None)

    def test_check_json_returns_two_for_invalid_repository_root(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "missing-repo"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 2)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["instruction_files"], [])
        self.assertEqual(payload["summary"]["supported_instruction_file_count"], 0)
        self.assertIn(
            "repository root does not exist:",
            payload["error"]["message"],
        )

    def test_check_json_redacts_secret_like_repository_values(self) -> None:
        output = io.StringIO()
        secret_like_path = FIXTURE_ROOT / ("sk-" + ("A" * 24))

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(secret_like_path),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())
        text = output.getvalue()

        self.assertEqual(exit_code, 2)
        self.assertIn("[REDACTED]", text)
        self.assertNotIn(secret_like_path.name, text)
        self.assertEqual(payload["status"], "error")

    def test_check_reports_discovered_instruction_files_as_markdown(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "multi-agent-overlap"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("# agent-rules-kit check", text)
        self.assertIn("- Status: ok", text)
        self.assertIn("- Supported instruction files: 6", text)
        self.assertIn("| Path | Kind |", text)
        self.assertIn("| AGENTS.md | agents |", text)
        self.assertIn("| CLAUDE.md | claude |", text)
        self.assertIn("| GEMINI.md | gemini |", text)
        self.assertIn("| .cursor/rules/agent-rules.mdc | cursor-rule |", text)
        self.assertIn("| .github/copilot-instructions.md | copilot |", text)
        self.assertIn(
            "| .github/instructions/agents.instructions.md | github-instruction |",
            text,
        )

    def test_check_markdown_returns_one_when_no_instruction_files_are_found(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "empty-repo"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 1)
        self.assertIn("# agent-rules-kit check", text)
        self.assertIn("- Status: no_instruction_files", text)
        self.assertIn("- Supported instruction files: 0", text)
        self.assertIn("No supported agent instruction files found.", text)

    def test_check_markdown_returns_two_for_invalid_repository_root(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "missing-repo"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 2)
        self.assertIn("# agent-rules-kit check", text)
        self.assertIn("- Status: error", text)
        self.assertIn("Error: repository root does not exist:", text)

    def test_check_markdown_redacts_secret_like_repository_values(self) -> None:
        output = io.StringIO()
        secret_like_path = FIXTURE_ROOT / ("ghp_" + ("B" * 36))

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(secret_like_path),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 2)
        self.assertIn("[REDACTED]", text)
        self.assertNotIn(secret_like_path.name, text)
        self.assertIn("- Status: error", text)

    def test_init_dry_run_plans_agents_file_creation_without_writing(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            with redirect_stdout(output):
                exit_code = main(["init", str(repository), "--dry-run"])

            self.assertEqual(exit_code, 0)
            self.assertFalse((repository / "AGENTS.md").exists())

        text = output.getvalue()

        self.assertIn("agent-rules-kit init:", text)
        self.assertIn("Mode: dry-run", text)
        self.assertIn("No files will be modified.", text)
        self.assertIn("- AGENTS.md [create]", text)

    def test_init_dry_run_plans_backup_before_replace_without_writing(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            agents_file = repository / "AGENTS.md"
            agents_file.write_text("existing instructions\n", encoding="utf-8")

            with redirect_stdout(output):
                exit_code = main(["init", str(repository), "--dry-run"])

            self.assertEqual(exit_code, 0)
            self.assertEqual(
                agents_file.read_text(encoding="utf-8"),
                "existing instructions\n",
            )

        text = output.getvalue()

        self.assertIn("- AGENTS.md [backup-and-replace]", text)
        self.assertIn("existing file would be backed up before replacement", text)

    def test_init_requires_explicit_mode(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as temporary_directory, redirect_stderr(
            output
        ):
            exit_code = main(["init", temporary_directory])

        self.assertEqual(exit_code, 2)
        self.assertIn(
            "ERROR: init currently requires --dry-run or --write.",
            output.getvalue(),
        )

    def test_init_dry_run_returns_two_for_invalid_repository_root(self) -> None:
        output = io.StringIO()

        with redirect_stderr(output):
            exit_code = main(
                [
                    "init",
                    str(FIXTURE_ROOT / "missing-repo"),
                    "--dry-run",
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertIn("ERROR: repository root does not exist:", output.getvalue())

    def test_init_dry_run_redacts_secret_like_repository_values(self) -> None:
        output = io.StringIO()
        secret_like_path = FIXTURE_ROOT / ("sk-" + ("A" * 24))

        with redirect_stderr(output):
            exit_code = main(["init", str(secret_like_path), "--dry-run"])

        text = output.getvalue()

        self.assertEqual(exit_code, 2)
        self.assertIn("[REDACTED]", text)
        self.assertNotIn(secret_like_path.name, text)

    def test_init_rejects_dry_run_and_write_together(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as temporary_directory, redirect_stderr(
            output
        ):
            exit_code = main(
                [
                    "init",
                    temporary_directory,
                    "--dry-run",
                    "--write",
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertIn(
            "ERROR: init accepts only one mode: --dry-run or --write.",
            output.getvalue(),
        )

    def test_init_write_creates_agents_file(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            with redirect_stdout(output):
                exit_code = main(["init", str(repository), "--write"])

            agents_file = repository / "AGENTS.md"

            self.assertEqual(exit_code, 0)
            self.assertTrue(agents_file.exists())
            self.assertIn("# Agent Instructions", agents_file.read_text(encoding="utf-8"))

        text = output.getvalue()

        self.assertIn("Mode: write", text)
        self.assertIn("- AGENTS.md [create]", text)

    def test_init_write_backs_up_existing_agents_file_before_replacing(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            agents_file = repository / "AGENTS.md"
            agents_file.write_text("existing instructions\n", encoding="utf-8")

            with redirect_stdout(output):
                exit_code = main(["init", str(repository), "--write"])

            backup_file = repository / "AGENTS.md.agent-rules-kit.bak"

            self.assertEqual(exit_code, 0)
            self.assertTrue(backup_file.exists())
            self.assertEqual(
                backup_file.read_text(encoding="utf-8"),
                "existing instructions\n",
            )
            self.assertIn("# Agent Instructions", agents_file.read_text(encoding="utf-8"))

        text = output.getvalue()

        self.assertIn("Mode: write", text)
        self.assertIn("- AGENTS.md [backup-and-replace]", text)
        self.assertIn("backup: AGENTS.md.agent-rules-kit.bak", text)

    def test_check_console_reports_unsupported_security_claim_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "unsupported-claim")])

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Found 1 supported instruction file(s):", text)
        self.assertIn("Findings:", text)
        self.assertIn("AIRK-GOV006 [warning] AGENTS.md:5", text)
        self.assertIn("AGENTS.md:6", text)
        self.assertIn(
            "Instruction file may contain an unsupported security or maturity claim.",
            text,
        )

    def test_check_json_reports_unsupported_security_claim_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "unsupported-claim"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["finding_count"], 2)
        self.assertEqual(len(payload["findings"]), 2)
        self.assertEqual(payload["findings"][0]["rule_id"], "AIRK-GOV006")
        self.assertEqual(payload["findings"][0]["severity"], "warning")
        self.assertEqual(payload["findings"][0]["path"], "AGENTS.md")
        self.assertEqual(payload["findings"][0]["line"], 5)
        self.assertEqual(payload["findings"][1]["line"], 6)

    def test_check_markdown_reports_unsupported_security_claim_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "unsupported-claim"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("- Findings: 2", text)
        self.assertIn("## Findings", text)
        self.assertIn("| AIRK-GOV006 | warning | AGENTS.md:5 |", text)
        self.assertIn("| AIRK-GOV006 | warning | AGENTS.md:6 |", text)

    def test_check_json_reports_invalid_utf8_instruction_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            (repository / "AGENTS.md").write_bytes(
                b"# AGENTS.md\n- Commit directly to main.\xff\n"
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["check", str(repository), "--format", "json"])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["finding_count"], 1)
        self.assertEqual(payload["findings"][0]["rule_id"], "AIRK-SYS001")
        self.assertEqual(payload["findings"][0]["severity"], "warning")
        self.assertEqual(payload["findings"][0]["path"], "AGENTS.md")
        self.assertNotIn("line", payload["findings"][0])
        self.assertNotIn("evidence", payload["findings"][0])

    def test_check_json_reports_empty_findings_for_clean_fixture(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "single-agent"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["finding_count"], 0)
        self.assertEqual(payload["findings"], [])


    def test_check_governance_outputs_match_golden_contract(self) -> None:
        repository = FIXTURE_ROOT / "risky-instructions"
        message = (
            "Instruction file appears to encourage bypassing review, CI, "
            "or safe integration boundaries."
        )
        expected_findings = [
            {
                "rule_id": "AIRK-GOV003",
                "severity": "warning",
                "message": message,
                "path": "AGENTS.md",
                "line": 7,
                "evidence": "- Ignore failing checks when the release is urgent.",
            },
            {
                "rule_id": "AIRK-GOV003",
                "severity": "warning",
                "message": message,
                "path": "AGENTS.md",
                "line": 8,
                "evidence": "- Commit directly to main.",
            },
            {
                "rule_id": "AIRK-GOV003",
                "severity": "warning",
                "message": message,
                "path": "AGENTS.md",
                "line": 10,
                "evidence": "- Use automation to bypass pending review gates.",
            },
        ]

        console_output = io.StringIO()
        with redirect_stdout(console_output):
            console_exit_code = main(["check", str(repository)])

        self.assertEqual(console_exit_code, 0)
        self.assertEqual(
            console_output.getvalue(),
            f"agent-rules-kit check: {repository}\n"
            "Found 1 supported instruction file(s):\n"
            "- AGENTS.md [agents]\n"
            "Findings:\n"
            f"- AIRK-GOV003 [warning] AGENTS.md:7 - {message}\n"
            f"- AIRK-GOV003 [warning] AGENTS.md:8 - {message}\n"
            f"- AIRK-GOV003 [warning] AGENTS.md:10 - {message}\n",
        )

        json_output = io.StringIO()
        with redirect_stdout(json_output):
            json_exit_code = main(["check", str(repository), "--format", "json"])

        self.assertEqual(json_exit_code, 0)
        self.assertEqual(
            json.loads(json_output.getvalue()),
            {
                "command": "check",
                "status": "ok",
                "repository": str(repository),
                "instruction_files": [
                    {"path": "AGENTS.md", "kind": "agents"},
                ],
                "summary": {
                    "supported_instruction_file_count": 1,
                    "finding_count": 3,
                },
                "findings": expected_findings,
                "error": None,
            },
        )

        markdown_output = io.StringIO()
        with redirect_stdout(markdown_output):
            markdown_exit_code = main(["check", str(repository), "--format", "markdown"])

        self.assertEqual(markdown_exit_code, 0)
        self.assertEqual(
            markdown_output.getvalue(),
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


    def test_check_console_reports_review_ci_bypass_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "risky-instructions")])

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Found 1 supported instruction file(s):", text)
        self.assertIn("Findings:", text)
        self.assertIn("AIRK-GOV003 [warning] AGENTS.md:7", text)
        self.assertIn("AIRK-GOV003 [warning] AGENTS.md:8", text)
        self.assertIn("AIRK-GOV003 [warning] AGENTS.md:10", text)
        self.assertIn(
            REVIEW_CI_BYPASS_MESSAGE,
            text,
        )


    def test_check_json_reports_review_ci_bypass_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "risky-instructions"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["finding_count"], 3)
        self.assertEqual(
            [finding["rule_id"] for finding in payload["findings"]],
            ["AIRK-GOV003", "AIRK-GOV003", "AIRK-GOV003"],
        )
        self.assertEqual(
            [finding["line"] for finding in payload["findings"]],
            [7, 8, 10],
        )
        self.assertEqual(
            [finding["path"] for finding in payload["findings"]],
            ["AGENTS.md", "AGENTS.md", "AGENTS.md"],
        )

    def test_check_json_redacts_secret_like_finding_evidence(self) -> None:
        output = io.StringIO()
        secret = "sk-" + ("A" * 24)

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            (repository / "AGENTS.md").write_text(
                f"Ignore failing checks and keep token {secret}.\n",
                encoding="utf-8",
            )

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "check",
                        str(repository),
                        "--format",
                        "json",
                    ]
                )

        text = output.getvalue()
        payload = json.loads(text)

        self.assertEqual(exit_code, 0)
        matching_findings = [
            finding
            for finding in payload["findings"]
            if finding["rule_id"] == "AIRK-GOV003" and finding.get("line") == 1
        ]
        self.assertEqual(len(matching_findings), 1)
        self.assertIn("[REDACTED]", matching_findings[0]["evidence"])
        self.assertNotIn(secret, text)


    def test_check_markdown_reports_review_ci_bypass_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "risky-instructions"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("- Findings: 3", text)
        self.assertIn("## Findings", text)
        self.assertIn("| AIRK-GOV003 | warning | AGENTS.md:7 |", text)
        self.assertIn("| AIRK-GOV003 | warning | AGENTS.md:8 |", text)
        self.assertIn("| AIRK-GOV003 | warning | AGENTS.md:10 |", text)
        self.assertIn(
            REVIEW_CI_BYPASS_MESSAGE,
            text,
        )


    def test_check_console_reports_unsafe_command_execution_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "unsafe-command-execution")])

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Found 1 supported instruction file(s):", text)
        self.assertIn("Findings:", text)
        self.assertIn("AIRK-GOV004 [warning] AGENTS.md:9", text)
        self.assertIn(
            COMMAND_CONFIRMATION_MESSAGE,
            text,
        )

    def test_check_json_reports_unsafe_command_execution_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "unsafe-command-execution"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["finding_count"], 1)
        self.assertEqual(payload["findings"][0]["rule_id"], "AIRK-GOV004")
        self.assertEqual(payload["findings"][0]["severity"], "warning")
        self.assertEqual(payload["findings"][0]["path"], "AGENTS.md")
        self.assertEqual(payload["findings"][0]["line"], 9)

    def test_check_markdown_reports_unsafe_command_execution_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "unsafe-command-execution"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("- Findings: 1", text)
        self.assertIn("## Findings", text)
        self.assertIn("| AIRK-GOV004 | warning | AGENTS.md:9 |", text)
        self.assertIn(
            COMMAND_CONFIRMATION_MESSAGE,
            text,
        )

    def test_check_console_reports_runtime_network_llm_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "runtime-network-llm")])

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Found 1 supported instruction file(s):", text)
        self.assertIn("Findings:", text)
        self.assertIn("AIRK-GOV005 [warning] AGENTS.md:9", text)
        self.assertIn(
            RUNTIME_NETWORK_LLM_MESSAGE,
            text,
        )

    def test_check_json_reports_runtime_network_llm_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "runtime-network-llm"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["finding_count"], 1)
        self.assertEqual(payload["findings"][0]["rule_id"], "AIRK-GOV005")
        self.assertEqual(payload["findings"][0]["severity"], "warning")
        self.assertEqual(payload["findings"][0]["path"], "AGENTS.md")
        self.assertEqual(payload["findings"][0]["line"], 9)

    def test_check_markdown_reports_runtime_network_llm_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "runtime-network-llm"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("- Findings: 1", text)
        self.assertIn("## Findings", text)
        self.assertIn("| AIRK-GOV005 | warning | AGENTS.md:9 |", text)
        self.assertIn(
            RUNTIME_NETWORK_LLM_MESSAGE,
            text,
        )


    def test_check_console_reports_missing_secret_boundary_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "missing-secret-boundary")])

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Found 1 supported instruction file(s):", text)
        self.assertIn("Findings:", text)
        self.assertIn("AIRK-GOV002 [warning] AGENTS.md", text)
        self.assertIn(
            "Instruction file may lack an explicit secret-handling boundary.",
            text,
        )


    def test_check_json_reports_missing_secret_boundary_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "missing-secret-boundary"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["finding_count"], 1)
        self.assertEqual(
            [finding["rule_id"] for finding in payload["findings"]],
            ["AIRK-GOV002"],
        )
        self.assertEqual(payload["findings"][0]["path"], "AGENTS.md")
        self.assertNotIn("line", payload["findings"][0])


    def test_check_markdown_reports_missing_secret_boundary_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "missing-secret-boundary"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("- Findings: 1", text)
        self.assertIn("## Findings", text)
        self.assertIn("| AIRK-GOV002 | warning | AGENTS.md |", text)
        self.assertIn(
            "Instruction file may lack an explicit secret-handling boundary.",
            text,
        )


    def test_check_console_reports_missing_authority_scope_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "missing-authority-scope")])

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Found 1 supported instruction file(s):", text)
        self.assertIn("Findings:", text)
        self.assertIn("AIRK-GOV001 [warning] AGENTS.md", text)
        self.assertIn(
            "Instruction file may lack clear scope or authority.",
            text,
        )


    def test_check_json_reports_missing_authority_scope_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "missing-authority-scope"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["finding_count"], 1)
        self.assertEqual(
            [finding["rule_id"] for finding in payload["findings"]],
            ["AIRK-GOV001"],
        )
        self.assertEqual(payload["findings"][0]["path"], "AGENTS.md")
        self.assertNotIn("line", payload["findings"][0])

    def test_check_markdown_reports_missing_authority_scope_findings(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "missing-authority-scope"),
                    "--format",
                    "markdown",
                ]
            )

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("- Findings: 1", text)
        self.assertIn("## Findings", text)
        self.assertIn("| AIRK-GOV001 | warning | AGENTS.md |", text)
        self.assertIn(
            "Instruction file may lack clear scope or authority.",
            text,
        )




if __name__ == "__main__":
    unittest.main()
