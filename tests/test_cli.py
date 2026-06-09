from __future__ import annotations

import io
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


if __name__ == "__main__":
    unittest.main()
