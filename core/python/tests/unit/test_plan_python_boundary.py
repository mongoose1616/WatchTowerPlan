import importlib
import sys
from pathlib import Path

import pytest

import watchtower_core.evidence as public_evidence
import watchtower_core.query as public_query
import watchtower_core.rebuild as public_rebuild
import watchtower_core.routing as public_routing
import watchtower_core.sync as public_sync
import watchtower_core.validation as public_validation
import watchtower_core.workflow_execution as public_workflow_execution
from watchtower_core.query import CommandQueryService
from watchtower_plan.sync.command_index import CommandIndexSyncService
from watchtower_plan.validation import (
    DocumentSemanticsValidationService,
    resolve_pack_validation_suite_targets,
)
from watchtower_core.validation.all import ValidationAllService

PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "src" / "watchtower_core"


def test_public_query_root_exports_generic_query_services_and_fails_closed_for_plan_queries() -> None:
    assert public_query.AcceptanceContractQueryService.__module__ == (
        "watchtower_core.query.acceptance"
    )
    assert public_query.CommandQueryService.__module__ == "watchtower_core.query.commands"
    assert public_query.FoundationQueryService.__module__ == "watchtower_core.query.foundations"
    assert public_query.ReferenceQueryService.__module__ == "watchtower_core.query.references"
    assert public_query.RepositoryPathQueryService.__module__ == (
        "watchtower_core.query.repository"
    )
    assert public_query.RoutePreviewService.__module__ == "watchtower_core.query.routes"
    assert public_query.StandardQueryService.__module__ == "watchtower_core.query.standards"
    assert public_query.TraceabilityQueryService.__module__ == (
        "watchtower_core.query.traceability"
    )
    assert public_query.ValidationEvidenceQueryService.__module__ == (
        "watchtower_core.query.evidence"
    )
    assert (
        public_query.GovernanceSurfaceQueryService.__module__
        == "watchtower_core.query.governance_surfaces"
    )
    assert (
        public_query.ArtifactFamilyQueryService.__module__
        == "watchtower_core.query.artifact_families"
    )

    with pytest.raises(AttributeError, match="watchtower_plan.query"):
        _ = public_query.CoordinationQueryService


def test_public_sync_root_fails_closed_with_plan_boundary_guidance() -> None:
    assert public_sync.SyncHarness.__module__ == "watchtower_core.sync.harness"
    assert public_sync.SyncTargetSpec.__module__ == "watchtower_core.sync.harness"
    with pytest.raises(AttributeError, match="watchtower_plan.sync"):
        _ = public_sync.CommandIndexSyncService


def test_public_rebuild_root_fails_closed_with_plan_boundary_guidance() -> None:
    assert public_rebuild.RebuildHarness.__module__ == "watchtower_core.rebuild.harness"
    assert public_rebuild.RebuildTargetSpec.__module__ == "watchtower_core.rebuild.harness"
    assert public_rebuild.RenderedViewBuilder.__module__ == "watchtower_core.rebuild.rendered_views"
    assert (
        public_rebuild.MarkdownReconciliationHelper.__module__
        == "watchtower_core.rebuild.rendered_views"
    )
    with pytest.raises(AttributeError, match="watchtower_plan"):
        _ = public_rebuild.PlanWorkspaceService


def test_public_workflow_execution_root_fails_closed_with_plan_boundary_guidance() -> None:
    assert (
        public_workflow_execution.WorkflowExecutionHarness.__module__
        == "watchtower_core.workflow_execution.harness"
    )
    assert (
        public_workflow_execution.WorkflowExecutionStep.__module__
        == "watchtower_core.workflow_execution.harness"
    )
    with pytest.raises(AttributeError, match="watchtower_plan"):
        _ = public_workflow_execution.InitiativePackageService


def test_public_evidence_root_exports_reusable_evidence_surfaces() -> None:
    assert public_evidence.ValidationEvidenceRecorder.__module__ == (
        "watchtower_core.evidence.validation_evidence"
    )
    assert public_evidence.EvidenceBundleHelper.__module__ == "watchtower_core.evidence.bundles"


def test_public_routing_root_exports_reusable_routing_engine() -> None:
    assert public_routing.RoutingEngine.__module__ == "watchtower_core.routing.engine"
    assert public_routing.RoutePreviewResult.__module__ == "watchtower_core.query.routes"
    with pytest.raises(AttributeError, match="watchtower_core.routing exports only"):
        _ = public_routing.UnknownRoutingSurface


def test_public_validation_root_fails_closed_with_plan_boundary_guidance() -> None:
    with pytest.raises(AttributeError, match="watchtower_core.validation.all"):
        _ = public_validation.ValidationAllService
    with pytest.raises(AttributeError, match="watchtower_plan.validation"):
        _ = public_validation.DocumentSemanticsValidationService


def test_public_package_roots_do_not_ship_repo_specific_leaf_modules() -> None:
    assert not (PACKAGE_ROOT / "repo_local_bootstrap.py").exists()
    assert sorted(path.name for path in (PACKAGE_ROOT / "query").glob("*.py")) == [
        "__init__.py",
        "acceptance.py",
        "artifact_families.py",
        "authority.py",
        "commands.py",
        "common.py",
        "evidence.py",
        "foundations.py",
        "governance_surfaces.py",
        "references.py",
        "repository.py",
        "routes.py",
        "standards.py",
        "traceability.py",
        "workflows.py",
    ]
    assert sorted(path.name for path in (PACKAGE_ROOT / "sync").glob("*.py")) == [
        "__init__.py",
        "harness.py",
    ]
    assert sorted(path.name for path in (PACKAGE_ROOT / "rebuild").glob("*.py")) == [
        "__init__.py",
        "harness.py",
        "rendered_views.py",
    ]
    assert sorted(path.name for path in (PACKAGE_ROOT / "workflow_execution").glob("*.py")) == [
        "__init__.py",
        "harness.py",
    ]
    assert sorted(path.name for path in (PACKAGE_ROOT / "evidence").glob("*.py")) == [
        "__init__.py",
        "bundles.py",
        "validation_evidence.py",
    ]
    assert sorted(path.name for path in (PACKAGE_ROOT / "routing").glob("*.py")) == [
        "__init__.py",
        "engine.py",
    ]


@pytest.mark.parametrize(
    "module_name",
    (
        "watchtower_core.control_plane.planning_vocabulary",
        "watchtower_core.query.coordination",
        "watchtower_core.query.planning",
        "watchtower_core.repo_local_bootstrap",
        "watchtower_core.rebuild.plan_workspace",
        "watchtower_core.rebuild.project_workspace",
        "watchtower_plan.query.authority",
        "watchtower_plan.query.acceptance",
        "watchtower_plan.query.commands",
        "watchtower_plan.query.evidence",
        "watchtower_plan.query.foundations",
        "watchtower_plan.query.references",
        "watchtower_plan.query.repository",
        "watchtower_plan.query.routes",
        "watchtower_plan.query.standards",
        "watchtower_plan.query.traceability",
        "watchtower_plan.query.workflows",
        "watchtower_core.sync.all",
        "watchtower_core.sync.command_index",
        "watchtower_core.sync.traceability",
        "watchtower_core.validation.document_semantics",
        "watchtower_core.validation.registry",
        "watchtower_core.workflow_execution.initiative_packages",
        "watchtower_plan.validation.all",
        "watchtower_plan.validation.registry",
    ),
)
def test_retired_wrapper_modules_are_not_importable(module_name: str) -> None:
    sys.modules.pop(module_name, None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(module_name)


def test_plan_python_boundary_owners_remain_available() -> None:
    assert CommandQueryService.__module__ == "watchtower_core.query.commands"
    assert CommandIndexSyncService.__module__ == "watchtower_plan.sync.command_index"
    assert ValidationAllService.__module__ == "watchtower_core.validation.all"
    assert (
        DocumentSemanticsValidationService.__module__
        == "watchtower_plan.validation.document_semantics"
    )
    assert (
        resolve_pack_validation_suite_targets.__module__
        == "watchtower_plan.validation.targets"
    )


def test_plan_query_root_fails_closed_for_generic_query_exports() -> None:
    import watchtower_plan.query as public_plan_query

    with pytest.raises(AttributeError):
        _ = public_plan_query.CommandQueryService
    with pytest.raises(AttributeError):
        _ = public_plan_query.FoundationQueryService
    with pytest.raises(AttributeError):
        _ = public_plan_query.TraceabilityQueryService
