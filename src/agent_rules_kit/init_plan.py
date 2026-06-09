"""Read-only init planning for agent instruction files."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class InitPlanAction(StrEnum):
    """Supported dry-run init actions."""

    CREATE = "create"
    SKIP_EXISTING = "skip-existing"


@dataclass(frozen=True, slots=True)
class PlannedInitFile:
    """A file action planned by init dry-run."""

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

    if candidate.exists():
        action = InitPlanAction.SKIP_EXISTING
        reason = "file already exists"
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
