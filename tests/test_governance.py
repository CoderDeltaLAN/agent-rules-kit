from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_rules_kit.discovery import discover_instruction_files
from agent_rules_kit.governance import find_unsupported_claim_findings


class GovernanceFindingTests(unittest.TestCase):
    def test_reports_unsupported_security_and_maturity_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            (repository / "AGENTS.md").write_text(
                "\n".join(
                    [
                        "# AGENTS.md",
                        "",
                        "Rules:",
                        "",
                        "- This process guarantees security for the repository.",
                        "- This project is enterprise-grade and production-ready.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            instruction_files = discover_instruction_files(repository)
            findings = find_unsupported_claim_findings(repository, instruction_files)

        self.assertEqual(
            [finding.rule_id for finding in findings],
            ["AIRK-GOV006", "AIRK-GOV006"],
        )
        self.assertEqual([finding.line for finding in findings], [5, 6])
        self.assertEqual([finding.path for finding in findings], ["AGENTS.md", "AGENTS.md"])

    def test_ignores_negative_guidance_about_unsupported_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            (repository / "AGENTS.md").write_text(
                "\n".join(
                    [
                        "# AGENTS.md",
                        "",
                        "Rules:",
                        "",
                        "- Do not claim this repository is enterprise-grade.",
                        "- Never say this process guarantees security.",
                        "- This tool is not a security scanner.",
                        "- Avoid production-ready claims.",
                        "- The tool must not claim complete secret scanning.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            instruction_files = discover_instruction_files(repository)
            findings = find_unsupported_claim_findings(repository, instruction_files)

        self.assertEqual(findings, ())

    def test_scans_only_supported_instruction_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            (repository / "README.md").write_text(
                "This project is enterprise-grade and guarantees security.\n",
                encoding="utf-8",
            )

            instruction_files = discover_instruction_files(repository)
            findings = find_unsupported_claim_findings(repository, instruction_files)

        self.assertEqual(instruction_files, ())
        self.assertEqual(findings, ())


if __name__ == "__main__":
    unittest.main()
