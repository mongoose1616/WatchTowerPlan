"""Deterministic rebuild helpers for the initiative index."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.plan_runtime.plan_workspace import (
    PLAN_INITIATIVE_INDEX_PATH,
    PlanWorkspaceService,
)

INITIATIVE_INDEX_ARTIFACT_PATH = PLAN_INITIATIVE_INDEX_PATH
PHASE_ORDER = {
    "prd": 1,
    "design": 2,
    "implementation_planning": 3,
    "execution": 4,
    "validation": 5,
    "closeout": 6,
    "closed": 7,
}


class InitiativeIndexSyncService:
    """Build and write the initiative index from current planning and task surfaces."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> InitiativeIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        return PlanWorkspaceService(self._loader).build_initiative_index_document()

    def write_document(
        self,
        document: dict[str, object],
        destination: Path | None = None,
    ) -> Path:
        """Write the generated initiative index to disk."""
        target = destination or (self._repo_root / INITIATIVE_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target
