from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from agent_rules_kit.cli import main

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "repositories"


class CliTests(unittest.TestCase):
    def test_version_flag_prints_version(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["--version"])

        self.assertEqual(exit_code, 0)
        self.assertIn("agent-rules-kit 0.1.0", output.getvalue())

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

    def test_init_dry_run_skips_existing_agents_file_without_writing(self) -> None:
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

        self.assertIn("- AGENTS.md [skip-existing] - file already exists", text)

    def test_init_requires_dry_run_until_write_mode_exists(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as temporary_directory:
            with redirect_stderr(output):
                exit_code = main(["init", temporary_directory])

        self.assertEqual(exit_code, 2)
        self.assertIn("ERROR: init currently requires --dry-run.", output.getvalue())

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


if __name__ == "__main__":
    unittest.main()
