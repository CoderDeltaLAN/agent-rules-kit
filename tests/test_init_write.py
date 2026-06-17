from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from agent_rules_kit.cli import main
from agent_rules_kit.init_plan import InitPlanAction
from agent_rules_kit.init_write import BASELINE_AGENTS_CONTENT, write_init_files


class InitWriteTests(unittest.TestCase):
    def test_write_init_files_creates_agents_file_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            result = write_init_files(repository)

            agents_file = repository / "AGENTS.md"

            self.assertEqual(result.repository, str(repository))
            self.assertEqual(result.files[0].path, "AGENTS.md")
            self.assertEqual(result.files[0].action, InitPlanAction.CREATE)
            self.assertEqual(result.files[0].backup_path, None)
            self.assertEqual(agents_file.read_text(encoding="utf-8"), BASELINE_AGENTS_CONTENT)

    def test_write_init_files_backs_up_existing_agents_file_before_replacing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            agents_file = repository / "AGENTS.md"
            agents_file.write_text("existing instructions\n", encoding="utf-8")

            result = write_init_files(repository)

            backup_file = repository / "AGENTS.md.agent-rules-kit.bak"

            self.assertEqual(result.files[0].path, "AGENTS.md")
            self.assertEqual(result.files[0].action, InitPlanAction.BACKUP_AND_REPLACE)
            self.assertEqual(result.files[0].backup_path, "AGENTS.md.agent-rules-kit.bak")
            self.assertEqual(
                backup_file.read_text(encoding="utf-8"),
                "existing instructions\n",
            )
            self.assertEqual(agents_file.read_text(encoding="utf-8"), BASELINE_AGENTS_CONTENT)

    def test_write_init_files_does_not_overwrite_existing_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            agents_file = repository / "AGENTS.md"
            first_backup = repository / "AGENTS.md.agent-rules-kit.bak"

            agents_file.write_text("existing instructions\n", encoding="utf-8")
            first_backup.write_text("older backup\n", encoding="utf-8")

            result = write_init_files(repository)

            second_backup = repository / "AGENTS.md.agent-rules-kit.bak.1"

            self.assertEqual(result.files[0].backup_path, "AGENTS.md.agent-rules-kit.bak.1")
            self.assertEqual(first_backup.read_text(encoding="utf-8"), "older backup\n")
            self.assertEqual(
                second_backup.read_text(encoding="utf-8"),
                "existing instructions\n",
            )
            self.assertEqual(agents_file.read_text(encoding="utf-8"), BASELINE_AGENTS_CONTENT)

    def test_write_init_files_rejects_missing_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing_root = Path(temporary_directory) / "missing"

            with self.assertRaises(ValueError):
                write_init_files(missing_root)

    def test_generated_baseline_passes_current_governance_check(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            write_init_files(repository)

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["check", str(repository), "--format", "json"])

            payload = json.loads(stdout.getvalue())

            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["summary"]["finding_count"], 0)
            self.assertEqual(payload["findings"], [])


if __name__ == "__main__":
    unittest.main()
