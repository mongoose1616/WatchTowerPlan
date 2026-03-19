"""Coordinated rebuild helpers for machine and human coordination surfaces."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.all import AllSyncResult, AllSyncService
from watchtower_core.repo_ops.sync.registry import (
    COORDINATION_SYNC_GROUP,
    sync_target_specs_for_group,
)

CLOSEOUT_SHARED_OUTPUT_TARGETS = frozenset(
    {
        "initiative-index",
        "planning-catalog",
        "coordination-index",
        "initiative-tracking",
        "coordination-tracking",
    }
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
        specs = sync_target_specs_for_group(COORDINATION_SYNC_GROUP)
        return self.run_specs(specs, write=write, output_dir=output_dir)

    def run_closeout_shared_outputs(
        self,
        *,
        write: bool = False,
        output_dir: Path | None = None,
    ) -> AllSyncResult:
        """Run only the bounded shared closeout outputs approved for sync reuse."""

        specs = tuple(
            spec
            for spec in sync_target_specs_for_group(COORDINATION_SYNC_GROUP)
            if spec.target in CLOSEOUT_SHARED_OUTPUT_TARGETS
        )
        return self.run_specs(specs, write=write, output_dir=output_dir)
