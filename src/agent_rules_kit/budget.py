"""Instruction-file budget approximation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent_rules_kit.discovery import InstructionFile


@dataclass(frozen=True, slots=True)
class BudgetFile:
    """Local size metrics for one supported instruction file."""

    path: str
    kind: str
    byte_count: int
    character_count: int
    line_count: int
    approximate_word_count: int


@dataclass(frozen=True, slots=True)
class BudgetReport:
    """Local size metrics for discovered instruction files."""

    files: tuple[BudgetFile, ...]

    @property
    def total_bytes(self) -> int:
        return sum(file_item.byte_count for file_item in self.files)

    @property
    def total_characters(self) -> int:
        return sum(file_item.character_count for file_item in self.files)

    @property
    def total_lines(self) -> int:
        return sum(file_item.line_count for file_item in self.files)

    @property
    def total_approximate_words(self) -> int:
        return sum(file_item.approximate_word_count for file_item in self.files)


def build_budget_report(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> BudgetReport:
    """Build deterministic local size metrics for supported instruction files."""
    budget_files: list[BudgetFile] = []

    for instruction_file in instruction_files:
        file_path = repository_root / instruction_file.path

        if file_path.is_symlink():
            raise ValueError(
                "instruction file path is a symlink and cannot be budgeted: "
                f"{instruction_file.path}"
            )

        raw_content = file_path.read_bytes()

        try:
            text_content = raw_content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(
                "instruction file is not valid UTF-8 and cannot be budgeted: "
                f"{instruction_file.path}"
            ) from error

        budget_files.append(
            BudgetFile(
                path=instruction_file.path,
                kind=instruction_file.kind.value,
                byte_count=len(raw_content),
                character_count=len(text_content),
                line_count=_count_lines(text_content),
                approximate_word_count=len(text_content.split()),
            )
        )

    return BudgetReport(files=tuple(budget_files))


def _count_lines(text: str) -> int:
    if not text:
        return 0

    return text.count("\n") + (0 if text.endswith("\n") else 1)


__all__ = ["BudgetFile", "BudgetReport", "build_budget_report"]
