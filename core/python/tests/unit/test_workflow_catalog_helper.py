from pathlib import Path

import pytest

from watchtower_core.control_plane import ControlPlaneLoader, WorkflowCatalogHelper

REPO_ROOT = Path(__file__).resolve().parents[4]


def _helper() -> WorkflowCatalogHelper:
    return WorkflowCatalogHelper.from_loader(ControlPlaneLoader(REPO_ROOT))


def test_workflow_catalog_helper_resolves_metadata_companions_and_routes() -> None:
    helper = _helper()

    snapshot = helper.snapshot("workflow.code_implementation")

    assert snapshot.workflow.doc_path == "core/workflows/modules/code_implementation.md"
    assert snapshot.metadata.phase_type == "execution"
    assert snapshot.metadata.task_family == "engineering"
    assert [entry.workflow_id for entry in snapshot.companion_workflows] == [
        "workflow.code_validation",
        "workflow.documentation_refresh",
        "workflow.task_handoff_review",
    ]
    assert [entry.route_id for entry in snapshot.route_bindings] == [
        "route.code_implementation",
        "route.test_suite_optimization",
    ]
    assert "workflow.code_validation" in {
        entry.workflow_id for entry in snapshot.compatible_workflows
    }
    assert "workflow.task_scope_definition" in {
        entry.workflow_id for entry in snapshot.compatible_workflows
    }
    assert "workflow.code_implementation" not in {
        entry.workflow_id for entry in snapshot.compatible_workflows
    }


def test_workflow_catalog_helper_fails_closed_on_unknown_workflows() -> None:
    helper = _helper()

    with pytest.raises(KeyError):
        helper.workflow("workflow.missing")

    with pytest.raises(KeyError):
        helper.metadata("workflow.missing")


def test_workflow_catalog_helper_tracks_adversarial_overlay_pairings() -> None:
    helper = _helper()

    snapshot = helper.snapshot("workflow.adversarial_reviewer")

    assert snapshot.metadata.task_family == "adversarial_lens"
    assert {
        entry.workflow_id for entry in snapshot.companion_workflows
    } >= {
        "workflow.code_implementation",
        "workflow.code_review",
        "workflow.documentation_review",
        "workflow.performance_benchmarking",
        "workflow.repository_review",
        "workflow.review_remediation",
        "workflow.review_remediation_loop",
    }
    assert {
        entry.workflow_id for entry in snapshot.compatible_workflows
    } >= {
        "workflow.code_implementation",
        "workflow.code_review",
        "workflow.documentation_review",
        "workflow.performance_benchmarking",
        "workflow.repository_review",
        "workflow.review_remediation_loop",
    }
