from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync import AllSyncService
from watchtower_core.sync.registry import SYNC_TARGET_SPECS

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_all_sync_runs_in_dry_run_mode() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = AllSyncService(loader)

    result = service.run()

    assert result.wrote is False
    assert tuple(record.target for record in result.records) == tuple(
        spec.target for spec in SYNC_TARGET_SPECS
    )


def test_sync_target_registry_is_unique() -> None:
    assert len({spec.target for spec in SYNC_TARGET_SPECS}) == len(SYNC_TARGET_SPECS)
    assert len({spec.relative_output_path for spec in SYNC_TARGET_SPECS}) == len(
        SYNC_TARGET_SPECS
    )


def test_all_sync_can_materialize_to_output_dir(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = AllSyncService(loader)
    output_dir = tmp_path / "sync_all"

    result = service.run(output_dir=output_dir)

    assert result.wrote is True
    assert (output_dir / "core/control_plane/indexes/commands/command_index.v1.json").exists()
    assert (output_dir / "core/control_plane/indexes/foundations/foundation_index.v1.json").exists()
    assert (output_dir / "core/control_plane/indexes/initiatives/initiative_index.v1.json").exists()
    assert (output_dir / "docs/planning/prds/prd_tracking.md").exists()
    assert (output_dir / "docs/planning/initiatives/initiative_tracking.md").exists()
