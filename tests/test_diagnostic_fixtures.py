from __future__ import annotations

import unittest
from pathlib import Path

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "repositories"

EXPECTED_FIXTURE_FILES = {
    "empty-repo/.gitkeep",
    "single-agent/AGENTS.md",
    "multi-agent-overlap/AGENTS.md",
    "claude-dotdir/.claude/CLAUDE.md",
    "multi-agent-overlap/CLAUDE.md",
    "multi-agent-overlap/GEMINI.md",
    "multi-agent-overlap/.cursor/rules/agent-rules.mdc",
    "multi-agent-overlap/.github/copilot-instructions.md",
    "multi-agent-overlap/.github/instructions/agents.instructions.md",
    "missing-authority-scope/AGENTS.md",
    "missing-secret-boundary/AGENTS.md",
    "risky-instructions/AGENTS.md",
    "runtime-network-llm/AGENTS.md",
    "unsafe-command-execution/AGENTS.md",
    "unsupported-claim/AGENTS.md",
}

SUPPORTED_INSTRUCTION_PATHS = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursor/rules/agent-rules.mdc",
    ".github/copilot-instructions.md",
    ".github/instructions/agents.instructions.md",
}

DISALLOWED_SECRET_MARKERS = (
    "sk-",
    "sk-ant-",
    "ghp_",
    "AKIA",
    "-----BEGIN",
    "hf_",
    "xoxb-",
    "npm_",
)


class DiagnosticFixtureTests(unittest.TestCase):
    def test_diagnostic_fixture_files_exist(self) -> None:
        missing = [
            relative_path
            for relative_path in sorted(EXPECTED_FIXTURE_FILES)
            if not (FIXTURE_ROOT / relative_path).is_file()
        ]

        self.assertEqual(missing, [])

    def test_supported_instruction_file_shapes_are_represented(self) -> None:
        represented_paths = {
            path.relative_to(FIXTURE_ROOT / "multi-agent-overlap").as_posix()
            for path in (FIXTURE_ROOT / "multi-agent-overlap").rglob("*")
            if path.is_file()
        }

        self.assertTrue(SUPPORTED_INSTRUCTION_PATHS.issubset(represented_paths))

    def test_fixtures_do_not_contain_raw_secret_values(self) -> None:
        combined_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in FIXTURE_ROOT.rglob("*")
            if path.is_file() and path.name != ".gitkeep"
        )

        for marker in DISALLOWED_SECRET_MARKERS:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, combined_text)


if __name__ == "__main__":
    unittest.main()
