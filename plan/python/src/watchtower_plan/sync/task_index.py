"""Deterministic rebuild helpers for the task index."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_plan.workspace.service import PLAN_TASK_INDEX_PATH, PlanWorkspaceService

TASK_INDEX_ARTIFACT_PATH = PLAN_TASK_INDEX_PATH


class TaskIndexSyncService:
    """Build and write the task index from initiative-local task state."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> TaskIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        return PlanWorkspaceService(self._loader).build_task_index_document()

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated task index to disk."""
        target = destination or (self._repo_root / TASK_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target
