from __future__ import annotations

import pytest

from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.control_plane.path_ids import PlanPathIdHelper


def test_plan_path_id_helper_slugifies_and_validates_canonical_slugs() -> None:
    assert PlanPathIdHelper.slugify("Plan Path Helper") == "plan_path_helper"
    assert PlanPathIdHelper.normalize_slug("plan_path_helper") == "plan_path_helper"

    with pytest.raises(ValueError, match="canonical snake_case"):
        PlanPathIdHelper.normalize_slug("Plan Path Helper")


def test_plan_path_id_helper_derives_trace_and_initiative_identity() -> None:
    assert PlanPathIdHelper.trace_suffix("trace.example_path_helper") == "example_path_helper"
    assert (
        PlanPathIdHelper.initiative_slug(trace_id="trace.example_path_helper")
        == "example_path_helper"
    )
    assert (
        PlanPathIdHelper.canonical_initiative_id("example_path_helper")
        == "initiative.example_path_helper"
    )

    with pytest.raises(ValueError, match="trace stem derived from trace_id"):
        PlanPathIdHelper.initiative_slug(
            trace_id="trace.example_path_helper",
            initiative_slug="different_slug",
        )


def _workspace_paths() -> PackWorkspacePaths:
    return PackWorkspacePaths.from_pack_settings(
        type(
            "PackSettingsStub",
            (),
            {
                "pack_id": "pack.example",
                "default_validation_suite_id": "suite.example.validation_baseline",
                "workspace_roots": type(
                    "WorkspaceRootsStub",
                    (),
                    {
                        "workspace_root": "packs/example",
                        "machine_root": "packs/example/.wt",
                        "docs_root": "packs/example/docs",
                        "workflows_root": "packs/example/workflows",
                        "tracking_root": "packs/example/tracking",
                        "initiatives_root": "packs/example/initiatives",
                        "projects_root": "packs/example/projects",
                        "overview_path": "packs/example/overview.md",
                    },
                )(),
            },
        )(),
        pack_settings_path="packs/example/.wt/manifests/pack_settings.json",
    )


def test_pack_workspace_paths_build_packwide_and_project_scoped_locations() -> None:
    workspace_paths = _workspace_paths()
    packwide = workspace_paths.packwide_initiative_location(
        trace_id="trace.example_path_helper"
    )
    assert packwide.initiative_root_relative == "packs/example/initiatives/example_path_helper"
    assert (
        packwide.relative_path(".wt/initiative.json")
        == "packs/example/initiatives/example_path_helper/.wt/initiative.json"
    )
    assert packwide.discrepancy_namespace == "example_path_helper"

    project_scoped = workspace_paths.project_scoped_initiative_location(
        "watchtower",
        trace_id="trace.example_path_helper",
    )
    assert project_scoped.project_id == "project.watchtower"
    assert (
        project_scoped.initiative_root_relative
        == "packs/example/projects/watchtower/initiatives/example_path_helper"
    )
    assert project_scoped.discrepancy_namespace == "watchtower.example_path_helper"


def test_plan_path_id_helper_builds_canonical_companion_ids_and_project_paths() -> None:
    workspace_paths = _workspace_paths()
    assert (
        PlanPathIdHelper.canonical_project_id("watchtower") == "project.watchtower"
    )
    assert (
        PlanPathIdHelper.canonical_repository_id("watchtower", "implementation")
        == "repository.watchtower.implementation"
    )
    assert (
        PlanPathIdHelper.canonical_task_id(
            "example_path_helper",
            "add_path_and_id_helper",
        )
        == "task.example_path_helper.add_path_and_id_helper"
    )
    assert (
        PlanPathIdHelper.canonical_deferred_item_id(
            "example_path_helper",
            "needs_scope_follow_up",
        )
        == "deferred.example_path_helper.needs_scope_follow_up"
    )
    assert (
        PlanPathIdHelper.canonical_evidence_id(
            "example_path_helper",
            "bootstrap_validation_bundle",
        )
        == "evidence.example_path_helper.bootstrap_validation_bundle"
    )
    assert (
        workspace_paths.project_root_relative("watchtower")
        == "packs/example/projects/watchtower"
    )
    assert (
        workspace_paths.project_initiatives_root_relative("watchtower")
        == "packs/example/projects/watchtower/initiatives"
    )
