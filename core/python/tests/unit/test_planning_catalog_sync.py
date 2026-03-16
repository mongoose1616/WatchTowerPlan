from __future__ import annotations

from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.planning_projection_catalog_composition import (
    build_trace_planning_catalog_aggregation,
)
from watchtower_core.repo_ops.planning_projection_snapshot import (
    build_trace_planning_coordination_snapshot,
    build_trace_planning_projection_snapshots,
)
from watchtower_core.repo_ops.query.planning import (
    PlanningCatalogQueryService,
    PlanningCatalogSearchParams,
)
from watchtower_core.repo_ops.sync.initiative_index import InitiativeIndexSyncService
from watchtower_core.repo_ops.sync.planning_catalog import PlanningCatalogSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_control_plane_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def test_planning_catalog_sync_builds_explicit_status_sections(tmp_path: Path) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)

    document = PlanningCatalogSyncService(loader).build_document()

    assert document["id"] == "index.planning_catalog"
    entries = document["entries"]
    assert isinstance(entries, list)
    entry = next(
        item
        for item in entries
        if item["trace_id"] == "trace.planning_authority_unification"
    )
    assert "artifact_status" in entry
    assert entry["initiative_status"] == "completed"
    assert "status" not in entry
    assert entry["coordination"]["current_phase"]
    assert entry["tasks"][0]["task_status"]
    assert "status" not in entry["tasks"][0]
    assert entry["decisions"][0]["record_status"]
    assert entry["decisions"][0]["decision_status"]


def test_planning_catalog_query_service_filters_by_phase_and_owner(tmp_path: Path) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = PlanningCatalogSyncService(loader)
    document = service.build_document()
    entries = document["entries"]
    assert isinstance(entries, list)
    target = next(
        item
        for item in entries
        if item["trace_id"] == "trace.planning_authority_unification"
    )
    coordination = target["coordination"]
    assert isinstance(coordination, dict)
    coordination["current_phase"] = "execution"
    coordination["primary_owner"] = "repository_maintainer"
    coordination["active_owners"] = ["repository_maintainer"]
    coordination["active_task_ids"] = [
        "task.planning_authority_unification.planning_catalog.001"
    ]
    service.write_document(document)

    entries = PlanningCatalogQueryService(ControlPlaneLoader(repo_root)).search(
        PlanningCatalogSearchParams(
            trace_id="trace.planning_authority_unification",
            current_phase="execution",
            owner="repository_maintainer",
        )
    )

    assert len(entries) == 1
    assert entries[0].trace_id == "trace.planning_authority_unification"
    assert entries[0].current_phase == "execution"


def test_planning_catalog_sync_embeds_acceptance_and_evidence_sections(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)

    written = PlanningCatalogSyncService(loader).build_document()
    entry = next(
        item
        for item in written["entries"]
        if item["trace_id"] == "trace.planning_authority_unification"
    )
    assert entry["acceptance_contracts"]
    assert entry["validation_evidence"]
    assert entry["acceptance_contract_ids"]
    assert entry["evidence_ids"]


def test_planning_catalog_aggregation_collects_catalog_only_metadata(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    snapshot = next(
        item
        for item in build_trace_planning_projection_snapshots(loader)
        if item.trace_entry.trace_id == "trace.planning_authority_unification"
    )
    coordination = build_trace_planning_coordination_snapshot(snapshot)

    aggregation = build_trace_planning_catalog_aggregation(snapshot, coordination)

    expected_validator_ids = {
        *snapshot.trace_entry.validator_ids,
        *(
            validator_id
            for contract in snapshot.acceptance_contracts
            for item in contract.entries
            for validator_id in item.required_validator_ids
        ),
        *(
            check.validator_id
            for evidence in snapshot.validation_evidence
            for check in evidence.checks
            if check.validator_id is not None
        ),
    }
    expected_tags = {
        *snapshot.trace_entry.tags,
        *(entry.family for entry in snapshot.design_entries),
        *(task_entry.task_kind for task_entry in snapshot.task_entries),
    }

    assert aggregation.validator_ids == tuple(sorted(expected_validator_ids))
    assert aggregation.tags == tuple(sorted(expected_tags))
    assert coordination.key_surface_path in aggregation.related_paths
    assert coordination.next_surface_path in aggregation.related_paths
    assert snapshot.acceptance_contracts[0].doc_path in aggregation.related_paths
    assert snapshot.validation_evidence[0].doc_path in aggregation.related_paths
    assert snapshot.task_entries[0].doc_path in aggregation.related_paths


def test_planning_catalog_coordination_matches_initiative_projection(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)

    initiative_document = InitiativeIndexSyncService(loader).build_document()
    planning_document = PlanningCatalogSyncService(loader).build_document()

    initiative_entries = initiative_document["entries"]
    planning_entries = planning_document["entries"]
    assert isinstance(initiative_entries, list)
    assert isinstance(planning_entries, list)

    initiative_by_trace = {
        entry["trace_id"]: entry
        for entry in initiative_entries
        if isinstance(entry, dict)
    }
    coordination_keys = (
        "current_phase",
        "key_surface_path",
        "next_action",
        "next_surface_path",
        "open_task_count",
        "blocked_task_count",
        "primary_owner",
        "active_owners",
        "active_task_ids",
        "active_task_summaries",
        "blocked_by_task_ids",
    )

    for planning_entry in planning_entries:
        assert isinstance(planning_entry, dict)
        initiative_entry = initiative_by_trace[planning_entry["trace_id"]]
        expected_coordination = {
            key: initiative_entry[key]
            for key in coordination_keys
            if key in initiative_entry
        }
        assert planning_entry["coordination"] == expected_coordination
