"""Deterministic rebuild helpers for the task index."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.cache import (
    SyncCacheInputSpec,
    discover_pack_sync_cache_paths,
    module_relative_path,
    ordered_sync_cache_paths,
)
from watchtower_plan.workspace.service import PLAN_TASK_INDEX_PATH, PlanWorkspaceService

TASK_INDEX_ARTIFACT_PATH = PLAN_TASK_INDEX_PATH


class TaskIndexSyncService:
    """Build and write the task index from initiative-local task state."""

    OUTPUT_PATH = TASK_INDEX_ARTIFACT_PATH

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> TaskIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def sync_cache_inputs(self) -> SyncCacheInputSpec:
        return SyncCacheInputSpec(
            tracked_paths=ordered_sync_cache_paths(
                module_relative_path(self._repo_root, __file__),
                "plan/python/src/watchtower_plan/sync",
                "plan/python/src/watchtower_plan/workspace",
                discover_pack_sync_cache_paths(
                    self._loader,
                    include_machine_manifests=True,
                    include_machine_registries=True,
                    include_python_sources=True,
                    include_workspace_sources=True,
                ),
            )
        )

    def build_document(self) -> dict[str, object]:
        return PlanWorkspaceService(self._loader).build_task_index_document()

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated task index to disk."""
        target = destination or (self._repo_root / TASK_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target
