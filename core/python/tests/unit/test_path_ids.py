from __future__ import annotations

import pytest

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


def test_plan_path_id_helper_builds_packwide_and_project_scoped_locations() -> None:
    packwide = PlanPathIdHelper.packwide_initiative_location(trace_id="trace.example_path_helper")
    assert packwide.initiative_root_relative == "plan/initiatives/example_path_helper"
    assert packwide.relative_path(".wt/initiative.json") == (
        "plan/initiatives/example_path_helper/.wt/initiative.json"
    )
    assert packwide.discrepancy_namespace == "example_path_helper"

    project_scoped = PlanPathIdHelper.project_scoped_initiative_location(
        "watchtower",
        trace_id="trace.example_path_helper",
    )
    assert project_scoped.project_id == "project.watchtower"
    assert (
        project_scoped.initiative_root_relative
        == "plan/projects/watchtower/initiatives/example_path_helper"
    )
    assert project_scoped.discrepancy_namespace == "watchtower.example_path_helper"


def test_plan_path_id_helper_builds_canonical_companion_ids_and_project_paths() -> None:
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
        PlanPathIdHelper.project_root_relative("watchtower") == "plan/projects/watchtower"
    )
    assert (
        PlanPathIdHelper.project_initiatives_root_relative("watchtower")
        == "plan/projects/watchtower/initiatives"
    )
