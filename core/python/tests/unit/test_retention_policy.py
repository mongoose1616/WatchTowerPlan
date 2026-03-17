from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.retention_policy import RetentionPolicyHelper

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> RetentionPolicyHelper:
    return RetentionPolicyHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_retention_policy_helper_matches_live_and_legacy_roots() -> None:
    helper = _helper()

    assert helper.policy_for_path("docs/planning").policy_id == (
        "policy.retention.legacy_docs_planning"
    )
    assert helper.policy_for_path("plan/.wt/indexes/initiative_index.json").policy_id == (
        "policy.retention.plan_machine_authority"
    )
    assert helper.policy_for_path(
        "plan/initiatives/plan_entrypoint_cutover_proof/summary.md"
    ).policy_id == "policy.retention.plan_packwide_initiative_archive"
    assert helper.policy_for_path(
        "plan/projects/watchtower/initiatives/watchtower_work_item_notes/summary.md"
    ).policy_id == "policy.retention.plan_project_initiative_archive"
    assert helper.policy_for_path(
        "core/control_plane/ledgers/purges/"
    ).policy_id == "policy.retention.trace_purge_ledgers"


def test_retention_policy_helper_exposes_current_and_clean_endstate_dispositions() -> None:
    helper = _helper()

    assert helper.current_disposition("docs/planning") == "legacy_ignored"
    assert (
        helper.clean_endstate_disposition("plan/initiatives/plan_entrypoint_cutover_proof")
        == "purge_when_eligible"
    )


def test_retention_policy_helper_accepts_current_repository_roots() -> None:
    helper = _helper()

    assert helper.validate_repository(REPO_ROOT) == ()
