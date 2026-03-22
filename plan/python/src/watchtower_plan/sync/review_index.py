"""Deterministic rebuild helpers for the review index."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_plan.workspace.service import (
    PLAN_REVIEW_INDEX_PATH,
    PlanWorkspaceService,
)

REVIEW_INDEX_ARTIFACT_PATH = PLAN_REVIEW_INDEX_PATH


class ReviewIndexSyncService:
    """Build and write the review index from initiative-local review state."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> ReviewIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        return PlanWorkspaceService(self._loader).build_review_index_document()

    def write_document(
        self, document: dict[str, object], destination: Path | None = None
    ) -> Path:
        """Write the generated review index to disk."""
        target = destination or (self._repo_root / REVIEW_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target
