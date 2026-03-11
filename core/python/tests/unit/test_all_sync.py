from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import AllSyncService, CoordinationSyncService
from watchtower_core.repo_ops.sync.registry import (
    COORDINATION_SYNC_GROUP,
    SYNC_TARGET_SPECS,
    sync_target_specs_for_group,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_coordination_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "docs" / "planning", repo_root / "docs" / "planning")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


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


def test_coordination_sync_group_has_expected_targets_in_order() -> None:
    specs = sync_target_specs_for_group(COORDINATION_SYNC_GROUP)

    assert tuple(spec.target for spec in specs) == (
        "task-index",
        "traceability-index",
        "initiative-index",
        "planning-catalog",
        "coordination-index",
        "task-tracking",
        "initiative-tracking",
        "coordination-tracking",
    )


def test_coordination_sync_runs_in_dry_run_mode() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = CoordinationSyncService(loader)

    result = service.run()

    assert result.wrote is False
    assert tuple(record.target for record in result.records) == (
        "task-index",
        "traceability-index",
        "initiative-index",
        "planning-catalog",
        "coordination-index",
        "task-tracking",
        "initiative-tracking",
        "coordination-tracking",
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


def test_coordination_sync_can_materialize_to_output_dir(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = CoordinationSyncService(loader)
    output_dir = tmp_path / "sync_coordination"

    result = service.run(output_dir=output_dir)

    assert result.wrote is True
    assert (output_dir / "core/control_plane/indexes/tasks/task_index.v1.json").exists()
    assert (
        output_dir / "core/control_plane/indexes/traceability/traceability_index.v1.json"
    ).exists()
    assert (output_dir / "core/control_plane/indexes/initiatives/initiative_index.v1.json").exists()
    assert (output_dir / "core/control_plane/indexes/planning/planning_catalog.v1.json").exists()
    assert (
        output_dir / "core/control_plane/indexes/coordination/coordination_index.v1.json"
    ).exists()
    assert (output_dir / "docs/planning/tasks/task_tracking.md").exists()
    assert (output_dir / "docs/planning/initiatives/initiative_tracking.md").exists()
    assert (output_dir / "docs/planning/coordination_tracking.md").exists()


def test_coordination_sync_output_dir_uses_generated_dependency_artifacts(tmp_path: Path) -> None:
    repo_root = _build_coordination_fixture_repo(tmp_path)
    initiative_index_path = (
        repo_root / "core/control_plane/indexes/initiatives/initiative_index.v1.json"
    )
    initiative_index = json.loads(initiative_index_path.read_text(encoding="utf-8"))
    for entry in initiative_index["entries"]:
        if entry["trace_id"] == "trace.core_export_hardening_followup":
            entry["next_action"] = "STALE SNAPSHOT MARKER"
            break
    initiative_index_path.write_text(
        f"{json.dumps(initiative_index, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    service = CoordinationSyncService(loader)
    output_dir = tmp_path / "sync_coordination_overlay"

    result = service.run(output_dir=output_dir)

    tracker_path = output_dir / "docs/planning/initiatives/initiative_tracking.md"
    tracker_text = tracker_path.read_text(encoding="utf-8")
    coordination_index_path = (
        output_dir / "core/control_plane/indexes/coordination/coordination_index.v1.json"
    )
    coordination_text = coordination_index_path.read_text(encoding="utf-8")
    coordination_tracking_path = output_dir / "docs/planning/coordination_tracking.md"
    coordination_tracking_text = coordination_tracking_path.read_text(encoding="utf-8")
    assert result.wrote is True
    assert "trace.core_export_hardening_followup" in tracker_text
    assert "STALE SNAPSHOT MARKER" not in tracker_text
    assert "STALE SNAPSHOT MARKER" not in coordination_text
    assert "STALE SNAPSHOT MARKER" not in coordination_tracking_text
    planning_catalog_path = (
        output_dir / "core/control_plane/indexes/planning/planning_catalog.v1.json"
    )
    planning_catalog_text = planning_catalog_path.read_text(encoding="utf-8")
    assert "STALE SNAPSHOT MARKER" not in planning_catalog_text


def test_all_sync_rejects_document_targets_without_entries_list() -> None:
    class BrokenDocumentService:
        def build_document(self) -> dict[str, object]:
            return {"id": "index.broken"}

        def write_document(
            self,
            document: dict[str, object],
            destination: Path | None = None,
        ) -> Path:
            raise AssertionError("Broken document targets should fail before write_document runs.")

    loader = ControlPlaneLoader(REPO_ROOT)
    service = AllSyncService(loader)

    with pytest.raises(RuntimeError, match="broken-index document is missing its entries list"):
        service._run_document_sync(
            target="broken-index",
            artifact_kind="index",
            relative_output_path="core/control_plane/indexes/broken/broken_index.v1.json",
            service=BrokenDocumentService(),
            write=False,
            output_dir=None,
        )
