"""Deterministic duplicate instruction detection."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from agent_rules_kit.discovery import InstructionFile


@dataclass(frozen=True, slots=True)
class DuplicateLineLocation:
    """One occurrence of a duplicated instruction line."""

    path: str
    line: int
    evidence: str


@dataclass(frozen=True, slots=True)
class DuplicateLineGroup:
    """A duplicated normalized instruction line and its locations."""

    normalized_text: str
    locations: tuple[DuplicateLineLocation, ...]


@dataclass(frozen=True, slots=True)
class DedupeReport:
    """Duplicate instruction report for supported instruction files."""

    groups: tuple[DuplicateLineGroup, ...]

    @property
    def duplicate_group_count(self) -> int:
        return len(self.groups)

    @property
    def duplicate_line_count(self) -> int:
        return sum(len(group.locations) for group in self.groups)


def build_dedupe_report(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> DedupeReport:
    """Build a conservative exact-line duplicate report."""
    locations_by_normalized_line: dict[str, list[DuplicateLineLocation]] = {}

    for instruction_file in instruction_files:
        file_path = repository_root / instruction_file.path

        if file_path.is_symlink():
            raise ValueError(
                "instruction file path is a symlink and cannot be deduplicated: "
                f"{instruction_file.path}"
            )

        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(
                "instruction file is not valid UTF-8 and cannot be deduplicated: "
                f"{instruction_file.path}"
            ) from error

        for line_number, line_text in enumerate(text.splitlines(), start=1):
            normalized_text = _normalize_instruction_line(line_text)
            if normalized_text is None:
                continue

            locations_by_normalized_line.setdefault(normalized_text, []).append(
                DuplicateLineLocation(
                    path=instruction_file.path,
                    line=line_number,
                    evidence=line_text.strip(),
                )
            )

    groups = [
        DuplicateLineGroup(
            normalized_text=normalized_text,
            locations=tuple(locations),
        )
        for normalized_text, locations in locations_by_normalized_line.items()
        if len({location.path for location in locations}) > 1
    ]

    return DedupeReport(groups=tuple(groups))


def _normalize_instruction_line(line_text: str) -> str | None:
    stripped = line_text.strip()
    if not stripped:
        return None

    if stripped.startswith(("```", "---", "<!--")):
        return None

    stripped = re.sub(r"^#{1,6}\s+", "", stripped)
    stripped = re.sub(r"^[-*+]\s+", "", stripped)
    stripped = re.sub(r"^\d+[.)]\s+", "", stripped)
    stripped = re.sub(r"\s+", " ", stripped).strip().lower()

    if len(stripped) < 24:
        return None

    if not any(character.isalpha() for character in stripped):
        return None

    return stripped


__all__ = [
    "DedupeReport",
    "DuplicateLineGroup",
    "DuplicateLineLocation",
    "build_dedupe_report",
]
