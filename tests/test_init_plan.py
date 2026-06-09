from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_rules_kit.init_plan import InitPlanAction, build_init_plan


class InitPlanTests(unittest.TestCase):
    def test_build_init_plan_marks_agents_file_for_creation_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            plan = build_init_plan(repository)

            self.assertEqual(plan.repository, str(repository))
            self.assertEqual(plan.files[0].path, "AGENTS.md")
            self.assertEqual(plan.files[0].action, InitPlanAction.CREATE)
            self.assertFalse((repository / "AGENTS.md").exists())

    def test_build_init_plan_marks_existing_agents_file_as_skip_existing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            agents_file = repository / "AGENTS.md"
            agents_file.write_text("existing instructions\n", encoding="utf-8")

            plan = build_init_plan(repository)

            self.assertEqual(plan.files[0].path, "AGENTS.md")
            self.assertEqual(plan.files[0].action, InitPlanAction.SKIP_EXISTING)
            self.assertEqual(
                agents_file.read_text(encoding="utf-8"),
                "existing instructions\n",
            )

    def test_build_init_plan_rejects_missing_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing_root = Path(temporary_directory) / "missing"

            with self.assertRaises(ValueError):
                build_init_plan(missing_root)

    def test_build_init_plan_rejects_file_root(self) -> None:
        with tempfile.NamedTemporaryFile() as temporary_file:
            with self.assertRaises(ValueError):
                build_init_plan(temporary_file.name)


if __name__ == "__main__":
    unittest.main()
