from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_rules_kit.discovery import (
    InstructionFile,
    InstructionFileKind,
    discover_instruction_files,
)

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "repositories"


class InstructionDiscoveryTests(unittest.TestCase):
    def test_empty_repository_has_no_instruction_files(self) -> None:
        self.assertEqual(
            discover_instruction_files(FIXTURE_ROOT / "empty-repo"),
            (),
        )

    def test_single_agent_repository_discovers_agents_file(self) -> None:
        self.assertEqual(
            discover_instruction_files(FIXTURE_ROOT / "single-agent"),
            (
                InstructionFile(
                    path="AGENTS.md",
                    kind=InstructionFileKind.AGENTS,
                ),
            ),
        )

    def test_multi_agent_repository_discovers_supported_instruction_files(self) -> None:
        self.assertEqual(
            discover_instruction_files(FIXTURE_ROOT / "multi-agent-overlap"),
            (
                InstructionFile(path="AGENTS.md", kind=InstructionFileKind.AGENTS),
                InstructionFile(path="CLAUDE.md", kind=InstructionFileKind.CLAUDE),
                InstructionFile(path="GEMINI.md", kind=InstructionFileKind.GEMINI),
                InstructionFile(
                    path=".github/copilot-instructions.md",
                    kind=InstructionFileKind.COPILOT,
                ),
                InstructionFile(
                    path=".cursor/rules/agent-rules.mdc",
                    kind=InstructionFileKind.CURSOR_RULE,
                ),
                InstructionFile(
                    path=".github/instructions/agents.instructions.md",
                    kind=InstructionFileKind.GITHUB_INSTRUCTION,
                ),
            ),
        )

    def test_claude_dotdir_repository_discovers_project_claude_file(self) -> None:
        self.assertEqual(
            discover_instruction_files(FIXTURE_ROOT / "claude-dotdir"),
            (
                InstructionFile(
                    path=".claude/CLAUDE.md",
                    kind=InstructionFileKind.CLAUDE,
                ),
            ),
        )

    def test_discovery_accepts_string_root(self) -> None:
        discovered = discover_instruction_files(str(FIXTURE_ROOT / "single-agent"))

        self.assertEqual(discovered[0].path, "AGENTS.md")

    def test_discovery_rejects_missing_root(self) -> None:
        with self.assertRaises(ValueError):
            discover_instruction_files(FIXTURE_ROOT / "missing-repo")

    def test_discovery_rejects_file_root(self) -> None:
        with tempfile.NamedTemporaryFile() as temporary_file, self.assertRaises(
            ValueError
        ):
            discover_instruction_files(temporary_file.name)


if __name__ == "__main__":
    unittest.main()
