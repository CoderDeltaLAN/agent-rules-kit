from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_rules_kit.discovery import (
    InstructionFile,
    InstructionFileKind,
    discover_instruction_files,
)
from agent_rules_kit.governance import find_governance_findings
from agent_rules_kit.init_plan import InitPlanAction, build_init_plan
from agent_rules_kit.init_write import BASELINE_AGENTS_CONTENT, write_init_files


class PathBoundaryTests(unittest.TestCase):
    def test_discovery_reports_repository_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            cursor_rule = repository / ".cursor" / "rules" / "agent.mdc"
            cursor_rule.parent.mkdir(parents=True)
            cursor_rule.write_text("Cursor rule\n", encoding="utf-8")

            self.assertEqual(
                discover_instruction_files(repository),
                (
                    InstructionFile(
                        path=".cursor/rules/agent.mdc",
                        kind=InstructionFileKind.CURSOR_RULE,
                    ),
                ),
            )

    def test_discovery_ignores_backup_and_temporary_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            (repository / "AGENTS.md.agent-rules-kit.bak").write_text(
                "backup\n",
                encoding="utf-8",
            )
            (repository / ".AGENTS.md.agent-rules-kit.tmp").write_text(
                "temporary\n",
                encoding="utf-8",
            )

            self.assertEqual(discover_instruction_files(repository), ())

    def test_init_plan_only_targets_root_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            nested_agents = repository / "docs" / "AGENTS.md"
            nested_agents.parent.mkdir()
            nested_agents.write_text("nested instructions\n", encoding="utf-8")

            plan = build_init_plan(repository)

            self.assertEqual(plan.files[0].path, "AGENTS.md")
            self.assertEqual(plan.files[0].action, InitPlanAction.CREATE)
            self.assertEqual(
                nested_agents.read_text(encoding="utf-8"),
                "nested instructions\n",
            )

    def test_write_init_files_creates_only_root_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            with tempfile.TemporaryDirectory() as outside_directory_name:
                outside_agents = Path(outside_directory_name) / "AGENTS.md"
                outside_agents.write_text("outside instructions\n", encoding="utf-8")

                result = write_init_files(repository)

                self.assertEqual(result.files[0].path, "AGENTS.md")
                self.assertEqual(result.files[0].action, InitPlanAction.CREATE)
                self.assertEqual(
                    (repository / "AGENTS.md").read_text(encoding="utf-8"),
                    BASELINE_AGENTS_CONTENT,
                )
                self.assertEqual(
                    outside_agents.read_text(encoding="utf-8"),
                    "outside instructions\n",
                )

    def test_write_init_files_backs_up_only_root_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            root_agents = repository / "AGENTS.md"
            nested_agents = repository / "docs" / "AGENTS.md"
            nested_agents.parent.mkdir()

            root_agents.write_text("root instructions\n", encoding="utf-8")
            nested_agents.write_text("nested instructions\n", encoding="utf-8")

            result = write_init_files(repository)

            self.assertEqual(result.files[0].path, "AGENTS.md")
            self.assertEqual(result.files[0].action, InitPlanAction.BACKUP_AND_REPLACE)
            self.assertEqual(result.files[0].backup_path, "AGENTS.md.agent-rules-kit.bak")
            self.assertEqual(
                (repository / "AGENTS.md.agent-rules-kit.bak").read_text(
                    encoding="utf-8"
                ),
                "root instructions\n",
            )
            self.assertEqual(root_agents.read_text(encoding="utf-8"), BASELINE_AGENTS_CONTENT)
            self.assertEqual(
                nested_agents.read_text(encoding="utf-8"),
                "nested instructions\n",
            )

    def test_write_init_files_leaves_no_atomic_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            write_init_files(repository)

            self.assertFalse((repository / ".AGENTS.md.agent-rules-kit.tmp").exists())

    def test_governance_reports_symlinked_instruction_file_without_following_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            outside_file = Path(temporary_directory) / "outside-instructions.md"
            outside_file.write_text(
                "Scope: outside file\n"
                "Secret handling: do not commit tokens.\n"
                "- Commit directly to main.\n",
                encoding="utf-8",
            )
            (repository / "AGENTS.md").symlink_to(outside_file)

            instruction_files = discover_instruction_files(repository)
            findings = find_governance_findings(repository, instruction_files)

            self.assertEqual(
                instruction_files,
                (
                    InstructionFile(
                        path="AGENTS.md",
                        kind=InstructionFileKind.AGENTS,
                    ),
                ),
            )
            self.assertEqual([finding.rule_id for finding in findings], ["AIRK-SYS002"])
            self.assertEqual(
                findings[0].message,
                "Instruction file path is a symlink and was not analyzed.",
            )
            self.assertEqual(findings[0].path, "AGENTS.md")
            self.assertIsNone(findings[0].line)
            self.assertIsNone(findings[0].evidence)

    def test_governance_reports_parent_symlinked_exact_instruction_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            outside_claude_directory = Path(temporary_directory) / "outside-claude"
            outside_claude_directory.mkdir()
            outside_claude_file = outside_claude_directory / "CLAUDE.md"
            outside_claude_file.write_text(
                "Scope: outside file\n"
                "Secret handling: do not commit tokens.\n"
                "- Commit directly to main.\n",
                encoding="utf-8",
            )
            (repository / ".claude").symlink_to(
                outside_claude_directory,
                target_is_directory=True,
            )

            instruction_files = discover_instruction_files(repository)
            findings = find_governance_findings(repository, instruction_files)

            self.assertEqual(
                instruction_files,
                (
                    InstructionFile(
                        path=".claude/CLAUDE.md",
                        kind=InstructionFileKind.CLAUDE,
                    ),
                ),
            )
            self.assertEqual([finding.rule_id for finding in findings], ["AIRK-SYS002"])
            self.assertEqual(findings[0].path, ".claude/CLAUDE.md")

    def test_discovery_does_not_traverse_symlinked_cursor_rules_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            cursor_directory = repository / ".cursor"
            cursor_directory.mkdir()
            outside_rules_directory = Path(temporary_directory) / "outside-rules"
            outside_rules_directory.mkdir()
            (outside_rules_directory / "agent.mdc").write_text(
                "outside cursor rule\n",
                encoding="utf-8",
            )
            (cursor_directory / "rules").symlink_to(
                outside_rules_directory,
                target_is_directory=True,
            )

            self.assertEqual(discover_instruction_files(repository), ())

    def test_discovery_does_not_traverse_symlinked_github_instructions_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            github_directory = repository / ".github"
            github_directory.mkdir()
            outside_instructions_directory = Path(temporary_directory) / "outside-instructions"
            outside_instructions_directory.mkdir()
            (outside_instructions_directory / "agents.instructions.md").write_text(
                "outside GitHub instruction\n",
                encoding="utf-8",
            )
            (github_directory / "instructions").symlink_to(
                outside_instructions_directory,
                target_is_directory=True,
            )

            self.assertEqual(discover_instruction_files(repository), ())

    def test_init_plan_rejects_symlinked_root_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            outside_file = Path(temporary_directory) / "outside-agents.md"
            outside_file.write_text("outside instructions\n", encoding="utf-8")
            (repository / "AGENTS.md").symlink_to(outside_file)

            with self.assertRaisesRegex(ValueError, "symlinked path"):
                build_init_plan(repository)

            self.assertEqual(
                outside_file.read_text(encoding="utf-8"),
                "outside instructions\n",
            )

    def test_write_init_files_rejects_symlinked_root_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            outside_file = Path(temporary_directory) / "outside-agents.md"
            outside_file.write_text("outside instructions\n", encoding="utf-8")
            agents_file = repository / "AGENTS.md"
            agents_file.symlink_to(outside_file)

            with self.assertRaisesRegex(ValueError, "symlinked path"):
                write_init_files(repository)

            self.assertTrue(agents_file.is_symlink())
            self.assertEqual(
                outside_file.read_text(encoding="utf-8"),
                "outside instructions\n",
            )

    def test_write_init_files_does_not_follow_symlinked_temporary_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            outside_temporary_target = Path(temporary_directory) / "outside-temp.txt"
            temporary_link = repository / ".AGENTS.md.agent-rules-kit.tmp"
            temporary_link.symlink_to(outside_temporary_target)

            result = write_init_files(repository)

            agents_file = repository / "AGENTS.md"

            self.assertEqual(result.files[0].action, InitPlanAction.CREATE)
            self.assertFalse(outside_temporary_target.exists())
            self.assertTrue(temporary_link.is_symlink())
            self.assertFalse(agents_file.is_symlink())
            self.assertEqual(
                agents_file.read_text(encoding="utf-8"),
                BASELINE_AGENTS_CONTENT,
            )

    def test_write_init_files_does_not_follow_symlinked_backup_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            agents_file = repository / "AGENTS.md"
            agents_file.write_text("root instructions\n", encoding="utf-8")
            outside_backup_target = Path(temporary_directory) / "outside-backup.txt"
            backup_link = repository / "AGENTS.md.agent-rules-kit.bak"
            backup_link.symlink_to(outside_backup_target)

            result = write_init_files(repository)

            second_backup = repository / "AGENTS.md.agent-rules-kit.bak.1"

            self.assertEqual(result.files[0].action, InitPlanAction.BACKUP_AND_REPLACE)
            self.assertEqual(result.files[0].backup_path, "AGENTS.md.agent-rules-kit.bak.1")
            self.assertFalse(outside_backup_target.exists())
            self.assertTrue(backup_link.is_symlink())
            self.assertEqual(
                second_backup.read_text(encoding="utf-8"),
                "root instructions\n",
            )
            self.assertFalse(agents_file.is_symlink())
            self.assertEqual(
                agents_file.read_text(encoding="utf-8"),
                BASELINE_AGENTS_CONTENT,
            )


if __name__ == "__main__":
    unittest.main()
