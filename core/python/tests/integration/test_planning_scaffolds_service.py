from __future__ import annotations

from pathlib import Path
from shutil import copytree

from tests.integration.fixture_repo_support import materialize_governed_applies_to_targets
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.planning_scaffolds import (
    PlanBootstrapParams,
    PlanningScaffoldService,
    PlanScaffoldParams,
)
from watchtower_core.repo_ops.query import (
    DesignDocumentQueryService,
    DesignDocumentSearchParams,
    InitiativeQueryService,
    PrdQueryService,
    PrdSearchParams,
    TaskQueryService,
    TaskSearchParams,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    copytree(REPO_ROOT / "docs", repo_root / "docs")
    materialize_governed_applies_to_targets(repo_root)
    return repo_root


def test_plan_scaffold_write_creates_prd_and_refreshes_prd_index(tmp_path: Path) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.planning_scaffold_service_preview"
    prd_id = "prd.planning_scaffold_service_preview"
    service = PlanningScaffoldService(ControlPlaneLoader(repo_root))

    result = service.scaffold(
        PlanScaffoldParams(
            kind="prd",
            trace_id=trace_id,
            document_id=prd_id,
            title="Planning Scaffold Preview PRD",
            summary="Frames the planning scaffold preview initiative.",
        ),
        write=True,
    )

    assert result.wrote is True
    assert result.doc_path == "docs/planning/prds/planning_scaffold_preview_prd.md"
    assert (repo_root / result.doc_path).exists()

    loader = ControlPlaneLoader(repo_root)
    prd_entries = PrdQueryService(loader).search(PrdSearchParams(trace_id=trace_id))
    assert [entry.prd_id for entry in prd_entries] == [prd_id]


def test_plan_bootstrap_write_creates_traced_chain_and_bootstrap_task(tmp_path: Path) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.planning_scaffold_bootstrap_preview"
    service = PlanningScaffoldService(ControlPlaneLoader(repo_root))

    result = service.bootstrap(
        PlanBootstrapParams(
            trace_id=trace_id,
            title="Planning Scaffold Bootstrap Preview",
            summary="Bootstraps the planning scaffold preview initiative.",
            include_decision=True,
        ),
        write=True,
    )

    assert result.wrote is True
    assert len(result.documents) == 4
    assert result.acceptance_contract.wrote is True
    assert result.validation_evidence.wrote is True
    assert result.task_result.wrote is True
    assert (repo_root / result.task_result.doc_path).exists()
    assert all((repo_root / document.doc_path).exists() for document in result.documents)
    assert (repo_root / result.acceptance_contract.doc_path).exists()
    assert (repo_root / result.validation_evidence.doc_path).exists()
    decision_text = (
        repo_root / "docs/planning/decisions/planning_scaffold_bootstrap_preview_direction.md"
    ).read_text(encoding="utf-8")
    assert "## Applied References and Implications" in decision_text

    loader = ControlPlaneLoader(repo_root)
    prd_entries = PrdQueryService(loader).search(PrdSearchParams(trace_id=trace_id))
    assert [entry.prd_id for entry in prd_entries] == ["prd.planning_scaffold_bootstrap_preview"]

    design_entries = DesignDocumentQueryService(loader).search(
        DesignDocumentSearchParams(trace_id=trace_id)
    )
    assert {entry.family for entry in design_entries} == {
        "feature_design",
        "implementation_plan",
    }

    task_entries = TaskQueryService(loader).search(TaskSearchParams(trace_id=trace_id))
    assert [entry.task_id for entry in task_entries] == [
        "task.planning_scaffold_bootstrap_preview.bootstrap.001"
    ]

    initiative_entry = InitiativeQueryService(loader).get(trace_id)
    assert initiative_entry.trace_id == trace_id
    assert initiative_entry.current_phase == "implementation_planning"
    assert task_entries[0].task_id in initiative_entry.active_task_ids
    assert initiative_entry.acceptance_contract_ids == (
        "contract.acceptance.planning_scaffold_bootstrap_preview",
    )
    planning_entry = loader.load_planning_catalog().get(trace_id)
    assert planning_entry.current_phase == "implementation_planning"
