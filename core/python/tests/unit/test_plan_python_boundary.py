import ast
import importlib
import sys
from pathlib import Path

import pytest

import watchtower_plan as public_plan
import watchtower_core.evidence as public_evidence
import watchtower_core.closeout as public_closeout
import watchtower_core.query as public_query
import watchtower_core.rebuild as public_rebuild
import watchtower_core.routing as public_routing
import watchtower_core.sync as public_sync
import watchtower_core.validation as public_validation
import watchtower_core.workflow_execution as public_workflow_execution
from watchtower_core.query import CommandQueryService
from watchtower_core.query.common import DataclassSearchAdapter
from watchtower_core.query.rendered_search import RenderedSearchFilters
from watchtower_core.sync.command_index import CommandIndexSyncService
from watchtower_core.sync.rendered_tracking import RenderedTrackingSyncService
from watchtower_core.validation.pack_targets import resolve_pack_validation_suite_targets
from watchtower_plan.closeout import InitiativeCloseoutService
from watchtower_plan.validation import (
    DocumentSemanticsValidationService,
)
from watchtower_core.validation.all import ValidationAllService

CORE_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "src" / "watchtower_core"
PLAN_PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3] / "plan" / "python" / "src" / "watchtower_plan"
)


def _iter_import_modules(package_root: Path) -> list[tuple[str, str]]:
    imports: list[tuple[str, str]] = []
    for path in sorted(package_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        relative_path = path.relative_to(package_root.parent).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((relative_path, alias.name))
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imports.append((relative_path, node.module))
    return imports


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


def test_generic_query_adapter_lives_in_reusable_core() -> None:
    assert DataclassSearchAdapter.__module__ == "watchtower_core.query.common"


def test_public_sync_root_fails_closed_with_plan_boundary_guidance() -> None:
    assert public_sync.SyncHarness.__module__ == "watchtower_core.sync.harness"
    assert public_sync.SyncTargetSpec.__module__ == "watchtower_core.sync.harness"
    with pytest.raises(AttributeError, match="watchtower_core.sync"):
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


def test_public_closeout_root_fails_closed_with_plan_boundary_guidance() -> None:
    with pytest.raises(AttributeError, match="watchtower_plan.closeout"):
        _ = public_closeout.InitiativeCloseoutService
    with pytest.raises(AttributeError, match="watchtower_plan.closeout"):
        _ = public_closeout.TracePurgeService


def test_public_package_roots_reflect_current_core_vs_plan_leaf_modules() -> None:
    assert not (CORE_PACKAGE_ROOT / "repo_local_bootstrap.py").exists()
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "query").glob("*.py")) == [
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
        "rendered_search.py",
        "repository.py",
        "routes.py",
        "standards.py",
        "traceability.py",
        "workflows.py",
    ]
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "sync").glob("*.py")) == [
        "__init__.py",
        "command_index.py",
        "foundation_index.py",
        "harness.py",
        "path_support.py",
        "reference_index.py",
        "reference_resolution.py",
        "rendered_tracking.py",
        "repository_paths.py",
        "route_index.py",
        "standard_index.py",
        "workflow_index.py",
    ]
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "validation").glob("*.py")) == [
        "__init__.py",
        "acceptance.py",
        "all.py",
        "artifact.py",
        "common.py",
        "context.py",
        "errors.py",
        "front_matter.py",
        "models.py",
        "pack_contract.py",
        "pack_targets.py",
        "suite.py",
    ]
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "documentation").glob("*.py")) == [
        "__init__.py",
        "front_matter_paths.py",
        "governed_documents.py",
        "markdown_semantics.py",
        "reference_semantics.py",
        "standards.py",
    ]
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "rebuild").glob("*.py")) == [
        "__init__.py",
        "harness.py",
        "rendered_views.py",
    ]
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "workflow_execution").glob("*.py")) == [
        "__init__.py",
        "harness.py",
    ]
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "evidence").glob("*.py")) == [
        "__init__.py",
        "bundles.py",
        "validation_evidence.py",
    ]
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "closeout").glob("*.py")) == [
        "__init__.py",
    ]
    assert sorted(path.name for path in (CORE_PACKAGE_ROOT / "routing").glob("*.py")) == [
        "__init__.py",
        "engine.py",
    ]


def test_reusable_core_package_does_not_import_plan_runtime_modules() -> None:
    offending_imports = [
        f"{relative_path}: {module_name}"
        for relative_path, module_name in _iter_import_modules(CORE_PACKAGE_ROOT)
        if module_name == "watchtower_plan" or module_name.startswith("watchtower_plan.")
    ]
    assert offending_imports == []


def test_plan_package_does_not_import_host_runtime_modules() -> None:
    offending_imports = [
        f"{relative_path}: {module_name}"
        for relative_path, module_name in _iter_import_modules(PLAN_PACKAGE_ROOT)
        if module_name == "watchtower_host" or module_name.startswith("watchtower_host.")
    ]
    assert offending_imports == []


@pytest.mark.parametrize(
    "module_name",
    (
        "watchtower_core.control_plane.planning_vocabulary",
        "watchtower_core.query.coordination",
        "watchtower_core.query.planning",
        "watchtower_core.repo_local_bootstrap",
        "watchtower_core.rebuild.plan_workspace",
        "watchtower_core.rebuild.project_workspace",
        "watchtower_core.closeout.initiative",
        "watchtower_core.closeout.initiative_package",
        "watchtower_core.closeout.purge_trace",
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
        "watchtower_core.sync.traceability",
        "watchtower_plan.front_matter_paths",
        "watchtower_plan.governed_documents",
        "watchtower_plan.markdown_semantics",
        "watchtower_plan.reference_semantics",
        "watchtower_plan.standards",
        "watchtower_plan.task_companion_path_repair",
        "watchtower_plan.sync.command_index",
        "watchtower_plan.sync.repository_paths",
        "watchtower_plan.sync.route_index",
        "watchtower_core.validation.document_semantics",
        "watchtower_core.validation.registry",
        "watchtower_core.workflow_execution.initiative_packages",
        "watchtower_plan.validation.all",
        "watchtower_plan.validation.registry",
        "watchtower_plan.validation.targets",
        "watchtower_plan.query.common",
        "watchtower_plan.sync.tracking_common",
    ),
)
def test_retired_wrapper_modules_are_not_importable(module_name: str) -> None:
    sys.modules.pop(module_name, None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(module_name)


def test_plan_python_boundary_owners_remain_available() -> None:
    assert public_plan.PlanWorkspaceService.__module__ == "watchtower_plan.workspace.service"
    assert CommandQueryService.__module__ == "watchtower_core.query.commands"
    assert CommandIndexSyncService.__module__ == "watchtower_core.sync.command_index"
    assert ValidationAllService.__module__ == "watchtower_core.validation.all"
    assert RenderedSearchFilters.__module__ == "watchtower_core.query.rendered_search"
    assert RenderedTrackingSyncService.__module__ == "watchtower_core.sync.rendered_tracking"
    assert (
        resolve_pack_validation_suite_targets.__module__
        == "watchtower_core.validation.pack_targets"
    )
    assert InitiativeCloseoutService.__module__ == "watchtower_plan.closeout.initiative"
    assert (
        DocumentSemanticsValidationService.__module__
        == "watchtower_plan.validation.document_semantics"
    )


def test_plan_internal_modules_use_feature_owned_workspace_package() -> None:
    legacy_workspace_modules = {
        "watchtower_plan.plan_workspace",
        "watchtower_plan.artifact_index",
    }
    compatibility_shims = {
        "watchtower_plan/plan_workspace.py",
        "watchtower_plan/artifact_index.py",
    }
    offending_imports = [
        f"{relative_path}: {module_name}"
        for relative_path, module_name in _iter_import_modules(PLAN_PACKAGE_ROOT)
        if relative_path not in compatibility_shims and module_name in legacy_workspace_modules
    ]
    assert offending_imports == []


def test_plan_query_root_fails_closed_for_generic_query_exports() -> None:
    import watchtower_plan.query as public_plan_query

    with pytest.raises(AttributeError):
        _ = public_plan_query.CommandQueryService
    with pytest.raises(AttributeError):
        _ = public_plan_query.FoundationQueryService
    with pytest.raises(AttributeError):
        _ = public_plan_query.TraceabilityQueryService
