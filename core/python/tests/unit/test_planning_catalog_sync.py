from __future__ import annotations
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query.planning import (
    PlanningCatalogQueryService,
    PlanningCatalogSearchParams,
)
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
    assert entry["initiative_status"] == "active"
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
    service.write_document(service.build_document())

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
