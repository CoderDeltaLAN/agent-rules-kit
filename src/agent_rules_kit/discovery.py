"""Instruction file discovery for supported agent rule files."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class InstructionFileKind(StrEnum):
    """Supported instruction file family."""

    AGENTS = "agents"
    CLAUDE = "claude"
    GEMINI = "gemini"
    CURSOR_RULE = "cursor-rule"
    COPILOT = "copilot"
    GITHUB_INSTRUCTION = "github-instruction"


@dataclass(frozen=True, slots=True)
class InstructionFile:
    """A discovered instruction file."""

    path: str
    kind: InstructionFileKind


def discover_instruction_files(root: Path | str) -> tuple[InstructionFile, ...]:
    """Discover supported instruction files below a repository root.

    Discovery is intentionally limited to known instruction file locations. It
    does not execute repository commands, call the network, or inspect file
    contents.
    """
    root_path = Path(root)

    if not root_path.exists():
        raise ValueError(f"repository root does not exist: {root_path}")
    if not root_path.is_dir():
        raise ValueError(f"repository root is not a directory: {root_path}")

    discovered: list[InstructionFile] = []

    for relative_path, kind in _exact_instruction_paths():
        candidate = root_path / relative_path
        if _is_supported_instruction_path(candidate):
            discovered.append(InstructionFile(path=relative_path, kind=kind))

    cursor_rules_dir = root_path / ".cursor" / "rules"
    if _is_safe_instruction_directory(root_path, cursor_rules_dir):
        for candidate in sorted(cursor_rules_dir.glob("*.mdc")):
            if _is_supported_instruction_path(candidate):
                discovered.append(
                    InstructionFile(
                        path=candidate.relative_to(root_path).as_posix(),
                        kind=InstructionFileKind.CURSOR_RULE,
                    )
                )

    github_instructions_dir = root_path / ".github" / "instructions"
    if _is_safe_instruction_directory(root_path, github_instructions_dir):
        for candidate in sorted(github_instructions_dir.glob("*.md")):
            if _is_supported_instruction_path(candidate):
                discovered.append(
                    InstructionFile(
                        path=candidate.relative_to(root_path).as_posix(),
                        kind=InstructionFileKind.GITHUB_INSTRUCTION,
                    )
                )

    return tuple(discovered)


def _is_supported_instruction_path(candidate: Path) -> bool:
    return candidate.is_file() or candidate.is_symlink()


def _is_safe_instruction_directory(root_path: Path, candidate: Path) -> bool:
    return candidate.is_dir() and not _has_symlink_component(root_path, candidate)


def _has_symlink_component(root_path: Path, candidate: Path) -> bool:
    relative_path = candidate.relative_to(root_path)
    current = root_path

    for part in relative_path.parts:
        current = current / part
        if current.is_symlink():
            return True

    return False


def _exact_instruction_paths() -> tuple[tuple[str, InstructionFileKind], ...]:
    return (
        ("AGENTS.md", InstructionFileKind.AGENTS),
        ("CLAUDE.md", InstructionFileKind.CLAUDE),
        (".claude/CLAUDE.md", InstructionFileKind.CLAUDE),
        ("GEMINI.md", InstructionFileKind.GEMINI),
        (".github/copilot-instructions.md", InstructionFileKind.COPILOT),
    )


__all__ = [
    "InstructionFile",
    "InstructionFileKind",
    "discover_instruction_files",
]
