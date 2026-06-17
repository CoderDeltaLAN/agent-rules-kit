"""Read-only init planning for agent instruction files."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class InitPlanAction(StrEnum):
    """Supported init actions."""

    CREATE = "create"
    BACKUP_AND_REPLACE = "backup-and-replace"


@dataclass(frozen=True, slots=True)
class PlannedInitFile:
    """A file action planned by init."""

    path: str
    action: InitPlanAction
    reason: str


@dataclass(frozen=True, slots=True)
class InitPlan:
    """Read-only init plan for a repository."""

    repository: str
    files: tuple[PlannedInitFile, ...]


def build_init_plan(root: Path | str) -> InitPlan:
    """Build a read-only init plan without modifying files."""
    root_path = Path(root)

    if not root_path.exists():
        raise ValueError(f"repository root does not exist: {root_path}")
    if not root_path.is_dir():
        raise ValueError(f"repository root is not a directory: {root_path}")

    target_path = "AGENTS.md"
    candidate = root_path / target_path

    if candidate.is_symlink():
        raise ValueError("refusing to plan init for symlinked path: AGENTS.md")

    if candidate.exists():
        action = InitPlanAction.BACKUP_AND_REPLACE
        reason = "existing file would be backed up before replacement"
    else:
        action = InitPlanAction.CREATE
        reason = "baseline agent instruction file would be created"

    return InitPlan(
        repository=str(root_path),
        files=(
            PlannedInitFile(
                path=target_path,
                action=action,
                reason=reason,
            ),
        ),
    )


__all__ = [
    "InitPlan",
    "InitPlanAction",
    "PlannedInitFile",
    "build_init_plan",
]
