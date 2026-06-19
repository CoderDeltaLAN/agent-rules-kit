from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_rules_kit.dedupe import build_dedupe_report
from agent_rules_kit.discovery import discover_instruction_files


class DedupeTests(unittest.TestCase):
    def test_reports_duplicate_instruction_lines_across_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            duplicate = "Run unit tests before opening a pull request."
            (root / "AGENTS.md").write_text(
                f"# Agent instructions\n\n- {duplicate}\n",
                encoding="utf-8",
            )
            (root / "CLAUDE.md").write_text(
                f"# Claude instructions\n\n{duplicate}\n",
                encoding="utf-8",
            )

            report = build_dedupe_report(root, discover_instruction_files(root))

        self.assertEqual(report.duplicate_group_count, 1)
        self.assertEqual(report.duplicate_line_count, 2)
        self.assertEqual(report.groups[0].normalized_text, duplicate.lower())
        self.assertEqual(
            [location.path for location in report.groups[0].locations],
            ["AGENTS.md", "CLAUDE.md"],
        )

    def test_ignores_short_boilerplate_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text("# Scope\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("# Scope\n", encoding="utf-8")

            report = build_dedupe_report(root, discover_instruction_files(root))

        self.assertEqual(report.duplicate_group_count, 0)

    def test_rejects_symlinked_instruction_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            target = root / "REAL.md"
            target.write_text("Run unit tests before opening a pull request.\n", encoding="utf-8")
            (root / "AGENTS.md").symlink_to(target)

            with self.assertRaisesRegex(ValueError, "symlink"):
                build_dedupe_report(root, discover_instruction_files(root))


if __name__ == "__main__":
    unittest.main()
