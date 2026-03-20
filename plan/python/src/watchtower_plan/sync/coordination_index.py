"""Deterministic rebuild helpers for the coordination index."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_plan.plan_workspace import (
    PLAN_COORDINATION_INDEX_PATH,
    PlanWorkspaceService,
)

COORDINATION_INDEX_ARTIFACT_PATH = PLAN_COORDINATION_INDEX_PATH


class CoordinationIndexSyncService:
    """Build and write the coordination index from the initiative index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> CoordinationIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        return PlanWorkspaceService(self._loader).build_coordination_index_document()

    def write_document(
        self,
        document: dict[str, object],
        destination: Path | None = None,
    ) -> Path:
        """Write the generated coordination index to disk."""
        target = destination or (self._repo_root / COORDINATION_INDEX_ARTIFACT_PATH)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target
