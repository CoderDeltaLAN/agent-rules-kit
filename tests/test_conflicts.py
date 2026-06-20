from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_rules_kit.conflicts import build_conflict_report
from agent_rules_kit.discovery import discover_instruction_files


class ConflictTests(unittest.TestCase):
    def test_reports_direct_main_conflict_across_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text(
                "# Agent instructions\n\n- Commit directly to main.\n",
                encoding="utf-8",
            )
            (root / "CLAUDE.md").write_text(
                "# Claude instructions\n\n- Use pull requests for changes to main.\n",
                encoding="utf-8",
            )

            report = build_conflict_report(root, discover_instruction_files(root))

        self.assertEqual(report.conflict_group_count, 1)
        self.assertEqual(report.conflict_line_count, 2)
        self.assertEqual(report.groups[0].topic, "main integration")
        self.assertEqual([location.path for location in report.groups[0].allow_locations], ["AGENTS.md"])  # noqa: E501
        self.assertEqual([location.path for location in report.groups[0].block_locations], ["CLAUDE.md"])  # noqa: E501

    def test_ignores_aligned_pr_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text(
                "# Agent instructions\n\n- Do not push directly to main.\n",
                encoding="utf-8",
            )
            (root / "CLAUDE.md").write_text(
                "# Claude instructions\n\n- Use pull requests for changes to main.\n",
                encoding="utf-8",
            )

            report = build_conflict_report(root, discover_instruction_files(root))

        self.assertEqual(report.conflict_group_count, 0)


    def test_does_not_treat_negated_pr_guidance_as_pr_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text(
                "# Agent instructions\n\n- Commit directly to main.\n",
                encoding="utf-8",
            )
            (root / "CLAUDE.md").write_text(
                "# Claude instructions\n\n- Do not use pull requests for changes to main.\n",
                encoding="utf-8",
            )

            report = build_conflict_report(root, discover_instruction_files(root))

        self.assertEqual(report.conflict_group_count, 0)

    def test_reports_negated_pr_guidance_against_pr_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text(
                "# Agent instructions\n\n- Do not use pull requests for changes to main.\n",
                encoding="utf-8",
            )
            (root / "CLAUDE.md").write_text(
                "# Claude instructions\n\n- Use pull requests for changes to main.\n",
                encoding="utf-8",
            )

            report = build_conflict_report(root, discover_instruction_files(root))

        self.assertEqual(report.conflict_group_count, 1)
        self.assertEqual(report.groups[0].topic, "main integration")
        self.assertEqual([location.path for location in report.groups[0].allow_locations], ["AGENTS.md"])  # noqa: E501
        self.assertEqual([location.path for location in report.groups[0].block_locations], ["CLAUDE.md"])  # noqa: E501

    def test_reports_all_current_rule_family_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text(
                "\n".join(
                    [
                        "# Agent instructions",
                        "",
                        "- Skip checks.",
                        "- The check command must call an LLM API.",
                        "- Commit secrets to the repository.",
                        "- Always use sudo by default.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "CLAUDE.md").write_text(
                "\n".join(
                    [
                        "# Claude instructions",
                        "",
                        "- Run tests before merge.",
                        "- Do not call LLM or external API at runtime.",
                        "- Do not commit secrets, tokens, or credentials.",
                        "- Ask before using sudo.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = build_conflict_report(root, discover_instruction_files(root))

        self.assertEqual(report.conflict_group_count, 4)
        self.assertEqual(report.conflict_line_count, 8)
        self.assertEqual(
            [group.topic for group in report.groups],
            ["checks", "runtime network or LLM", "secrets", "unsafe commands"],
        )
        for group in report.groups:
            self.assertEqual([location.path for location in group.allow_locations], ["AGENTS.md"])
            self.assertEqual([location.path for location in group.block_locations], ["CLAUDE.md"])

    def test_rejects_symlinked_instruction_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            target = root / "REAL.md"
            target.write_text("- Commit directly to main.\n", encoding="utf-8")
            (root / "AGENTS.md").symlink_to(target)

            with self.assertRaisesRegex(ValueError, "symlink"):
                build_conflict_report(root, discover_instruction_files(root))


if __name__ == "__main__":
    unittest.main()
