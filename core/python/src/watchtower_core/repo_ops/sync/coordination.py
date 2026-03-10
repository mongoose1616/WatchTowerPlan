"""Coordinated rebuild helpers for task, initiative, and coordination surfaces."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.all import AllSyncResult, AllSyncService
from watchtower_core.repo_ops.sync.registry import (
    COORDINATION_SYNC_GROUP,
    sync_target_specs_for_group,
)


class CoordinationSyncService(AllSyncService):
    """Run the deterministic coordination rebuild slice in dependency order."""

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> CoordinationSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def run(
        self,
        *,
        write: bool = False,
        output_dir: Path | None = None,
    ) -> AllSyncResult:
        runtime_loader = self._runtime_loader(output_dir)
        records = [
            self._run_registered_sync(
                loader=runtime_loader,
                spec=spec,
                write=write,
                output_dir=output_dir,
            )
            for spec in sync_target_specs_for_group(COORDINATION_SYNC_GROUP)
        ]
        return AllSyncResult(
            records=tuple(records),
            wrote=(write or output_dir is not None),
            output_dir=str(output_dir.resolve()) if output_dir is not None else None,
        )
