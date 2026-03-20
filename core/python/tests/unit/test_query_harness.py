from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query import (
    ArtifactFamilyQueryService,
    ArtifactFamilySearchParams,
    AuthorityMapQueryService,
    AuthorityMapSearchParams,
    CommandQueryService,
    CommandSearchParams,
    GovernanceSurfaceQueryService,
    GovernanceSurfaceSearchParams,
    RoutePreviewService,
    WorkflowQueryService,
    WorkflowSearchParams,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def test_public_query_services_cover_generic_governed_surfaces() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    command_matches = CommandQueryService(loader).search(
        CommandSearchParams(query="coordination", limit=5)
    )
    assert any(
        entry.command_id == "command.watchtower_core.plan.query.coordination"
        for entry in command_matches
    )

    workflow_matches = WorkflowQueryService(loader).search(
        WorkflowSearchParams(query="validation", limit=10)
    )
    assert any(
        entry.doc_path == "core/workflows/modules/code_validation.md"
        for entry in workflow_matches
    )

    authority_matches = AuthorityMapQueryService(loader).search(
        AuthorityMapSearchParams(question_id="authority.governance.workflow_routing")
    )
    assert authority_matches[0].canonical_path == "core/control_plane/indexes/routes/route_index.json"


def test_public_query_services_cover_pack_surface_and_artifact_family_queries() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    surface_matches = GovernanceSurfaceQueryService(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    ).search(
        GovernanceSurfaceSearchParams(
            surface_name="artifact_index",
        )
    )
    assert surface_matches[0].path == "plan/.wt/indexes/artifact_index.json"
    assert surface_matches[0].rebuildable is True
    assert surface_matches[0].declaration_sources == ("pack_settings",)

    artifact_service = ArtifactFamilyQueryService(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )
    family_matches = artifact_service.search(
        ArtifactFamilySearchParams(relative_path="plan/.wt/indexes/artifact_index.json")
    )
    assert family_matches[0].family_id == "artifact_index"

    resolution = artifact_service.resolve_path("plan/projects/watchtower/.wt/project.json")
    assert resolution.best_match is not None
    assert resolution.best_match.family_id == "project_record"
    assert resolution.issues == ()


def test_public_route_preview_service_resolves_workflow_paths() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    preview = RoutePreviewService(loader).preview(task_type="Code Implementation")

    assert preview.selected_routes
    assert any(
        workflow.doc_path == "core/workflows/modules/code_implementation.md"
        for workflow in preview.selected_workflows
    )
