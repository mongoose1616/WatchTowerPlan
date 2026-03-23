from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.human_surface_policy import HumanSurfacePolicyHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> HumanSurfacePolicyHelper:
    return HumanSurfacePolicyHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_human_surface_policy_helper_matches_specific_roots() -> None:
    helper = _helper()

    assert (
        helper.policy_for_root("plan/initiatives/plan_entrypoint_cutover_proof").policy_id
        == "policy.human_surface.plan_initiative_root"
    )
    assert (
        helper.policy_for_root(
            "plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow"
        ).policy_id
        == "policy.human_surface.project_scoped_initiative_root"
    )
    assert helper.policy_for_root("plan/.wt").policy_id == "policy.human_surface.machine_root"
    assert helper.policy_for_root("core/workflows").policy_id == (
        "policy.human_surface.core_workflows_root"
    )


def test_human_surface_policy_helper_accepts_current_repo_roots() -> None:
    helper = _helper()

    assert helper.validate_repository(REPO_ROOT) == ()


def test_human_surface_policy_helper_reports_forbidden_machine_surface(
    tmp_path: Path,
) -> None:
    helper = _helper()
    repo_root = tmp_path / "repo"
    (repo_root / "plan" / ".wt").mkdir(parents=True)
    (repo_root / "plan" / ".wt" / "README.md").write_text("forbidden\n", encoding="utf-8")

    issues = helper.validate_root(repo_root, "plan/.wt")

    assert len(issues) == 1
    assert issues[0].issue_code == "forbidden_surface_present"
    assert issues[0].surface_path == "plan/.wt/README.md"
