from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.planning_scaffolds import (
    PlanBootstrapParams,
    PlanningScaffoldService,
    PlanScaffoldParams,
)
from watchtower_core.validation.acceptance import AcceptanceReconciliationService

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "docs" / "planning", repo_root / "docs" / "planning")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def test_plan_scaffold_write_refreshes_prd_surfaces(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = PlanningScaffoldService(ControlPlaneLoader(repo_root))

    result = service.scaffold(
        PlanScaffoldParams(
            kind="prd",
            trace_id="trace.unit_test_scaffold",
            document_id="prd.unit_test_scaffold",
            title="Unit Test Scaffold PRD",
            summary="Creates a PRD scaffold for testing.",
            file_stem="unit_test_scaffold_prd",
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=True,
    )

    assert result.wrote is True
    written_path = repo_root / result.doc_path
    assert written_path.exists()
    written_text = written_path.read_text(encoding="utf-8")
    assert "Unit Test Scaffold PRD" in written_text

    prd_index = json.loads(
        (repo_root / "core/control_plane/indexes/prds/prd_index.v1.json").read_text(
            encoding="utf-8"
        )
    )
    assert any(entry["prd_id"] == "prd.unit_test_scaffold" for entry in prd_index["entries"])

def test_plan_bootstrap_can_write_full_chain_with_decision(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = PlanningScaffoldService(ControlPlaneLoader(repo_root))

    result = service.bootstrap(
        PlanBootstrapParams(
            trace_id="trace.unit_test_bootstrap",
            title="Unit Test Bootstrap",
            summary="Bootstraps a planning chain for tests.",
            file_stem="unit_test_bootstrap",
            include_decision=True,
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=True,
    )

    assert result.wrote is True
    assert result.sync_refreshed is True
    assert len(result.documents) == 4
    assert result.acceptance_contract.wrote is True
    assert result.validation_evidence.wrote is True
    assert result.task_result.wrote is True

    assert (repo_root / "docs/planning/prds/unit_test_bootstrap.md").exists()
    assert (repo_root / "docs/planning/design/features/unit_test_bootstrap.md").exists()
    assert (repo_root / "docs/planning/design/implementation/unit_test_bootstrap.md").exists()
    assert (repo_root / "docs/planning/decisions/unit_test_bootstrap_direction.md").exists()
    assert (
        repo_root
        / "core/control_plane/contracts/acceptance/unit_test_bootstrap_acceptance.v1.json"
    ).exists()
    assert (
        repo_root
        / (
            "core/control_plane/ledgers/validation_evidence/"
            "unit_test_bootstrap_planning_baseline.v1.json"
        )
    ).exists()
    assert (repo_root / "docs/planning/tasks/open/unit_test_bootstrap_bootstrap.md").exists()

    feature_design_text = (
        repo_root / "docs/planning/design/features/unit_test_bootstrap.md"
    ).read_text(encoding="utf-8")
    assert "## Foundations References Applied" in feature_design_text
    assert "## Internal Standards and Canonical References Applied" in feature_design_text

    implementation_plan_text = (
        repo_root / "docs/planning/design/implementation/unit_test_bootstrap.md"
    ).read_text(encoding="utf-8")
    assert "## Internal Standards and Canonical References Applied" in implementation_plan_text

    decision_text = (
        repo_root / "docs/planning/decisions/unit_test_bootstrap_direction.md"
    ).read_text(encoding="utf-8")
    assert "## Applied References and Implications" in decision_text

    initiative_index = json.loads(
        (repo_root / "core/control_plane/indexes/initiatives/initiative_index.v1.json").read_text(
            encoding="utf-8"
        )
    )
    assert any(
        entry["trace_id"] == "trace.unit_test_bootstrap"
        for entry in initiative_index["entries"]
    )
    validation_result = AcceptanceReconciliationService(
        ControlPlaneLoader(repo_root)
    ).validate("trace.unit_test_bootstrap")
    assert validation_result.passed is True


def test_plan_scaffold_write_refreshes_coordination_for_existing_trace(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = PlanningScaffoldService(ControlPlaneLoader(repo_root))
    trace_id = "trace.unit_test_scaffold_existing"
    decision_id = "decision.unit_test_scaffold_existing.followup"

    service.bootstrap(
        PlanBootstrapParams(
            trace_id=trace_id,
            title="Unit Test Scaffold Existing",
            summary="Bootstraps a trace before adding one more planning document.",
            file_stem="unit_test_scaffold_existing",
            include_decision=False,
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=True,
    )

    result = service.scaffold(
        PlanScaffoldParams(
            kind="decision",
            trace_id=trace_id,
            document_id=decision_id,
            title="Unit Test Scaffold Existing Follow-Up Decision",
            summary="Adds a follow-up decision to an existing traced initiative.",
            linked_prd_ids=("prd.unit_test_scaffold_existing",),
            linked_design_ids=("design.features.unit_test_scaffold_existing",),
            linked_plan_ids=("design.implementation.unit_test_scaffold_existing",),
            file_stem="unit_test_scaffold_existing_followup_decision",
            updated_at="2026-03-11T00:05:00Z",
        ),
        write=True,
    )

    assert result.wrote is True
    written_text = (
        repo_root / "docs/planning/decisions/unit_test_scaffold_existing_followup_decision.md"
    ).read_text(encoding="utf-8")
    assert "## Applied References and Implications" in written_text

    loader = ControlPlaneLoader(repo_root)
    trace_entry = loader.load_traceability_index().get(trace_id)
    assert decision_id in trace_entry.decision_ids

    initiative_entry = loader.load_initiative_index().get(trace_id)
    assert decision_id in initiative_entry.decision_ids
    assert (
        "docs/planning/decisions/unit_test_scaffold_existing_followup_decision.md"
        in initiative_entry.related_paths
    )

    planning_entry = loader.load_planning_catalog().get(trace_id)
    assert decision_id in planning_entry.decision_ids
    assert any(
        entry.decision_id == decision_id for entry in planning_entry.decisions
    )


def test_plan_scaffold_rejects_duplicate_doc_path(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = PlanningScaffoldService(ControlPlaneLoader(repo_root))

    service.scaffold(
        PlanScaffoldParams(
            kind="prd",
            trace_id="trace.unit_test_duplicate",
            document_id="prd.unit_test_duplicate",
            title="Duplicate PRD",
            summary="Writes the first scaffold.",
            file_stem="unit_test_duplicate",
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=True,
    )

    with pytest.raises(
        ValueError,
        match="Planning scaffold path already exists: docs/planning/prds/unit_test_duplicate.md",
    ):
        service.scaffold(
            PlanScaffoldParams(
                kind="prd",
                trace_id="trace.unit_test_duplicate_second",
                document_id="prd.unit_test_duplicate_second",
                title="Duplicate PRD Second",
                summary="Attempts to reuse the same path.",
                file_stem="unit_test_duplicate",
                updated_at="2026-03-10T23:59:59Z",
            ),
            write=False,
        )


def test_plan_scaffold_rejects_invalid_kind(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = PlanningScaffoldService(ControlPlaneLoader(repo_root))

    with pytest.raises(ValueError, match="kind must be one of:"):
        service.scaffold(
            PlanScaffoldParams(
                kind="bad-kind",  # type: ignore[arg-type]
                trace_id="trace.unit_test_invalid_kind",
                document_id="prd.unit_test_invalid_kind",
                title="Invalid kind",
                summary="Uses an invalid scaffold kind.",
            ),
            write=False,
        )
