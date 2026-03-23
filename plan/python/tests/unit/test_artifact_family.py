from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.artifact_family import ArtifactFamilyHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> ArtifactFamilyHelper:
    return ArtifactFamilyHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_artifact_family_helper_resolves_live_family_rules() -> None:
    helper = _helper()

    assert helper.family("initiative_state").status_field == "lifecycle_stage"
    assert helper.family("task_index").canonical_schema_id == (
        "urn:watchtower:schema:artifacts:plan:task-summary-index:v1"
    )
    assert helper.family("deferred_item_record").allowed_status_values == (
        "open",
        "resolved",
    )


def test_artifact_family_helper_matches_pack_and_project_paths() -> None:
    helper = _helper()

    assert helper.family_for_path("plan/.wt/indexes/task_index.json").family_id == "task_index"
    assert (
        helper.family_for_path("plan/projects/watchtower/.wt/project.json").family_id
        == "project_record"
    )
    assert (
        helper.family_for_path(
            "plan/initiatives/example/.wt/deferred/deferred.example.pending.json"
        ).family_id
        == "deferred_item_record"
    )


def test_artifact_family_helper_reports_unclassified_paths() -> None:
    helper = _helper()

    issues = helper.validate_relative_path("plan/unknown/path.json")

    assert len(issues) == 1
    assert issues[0].issue_code == "unclassified_artifact_path"
