from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane import (
    ControlPlaneLoader,
    DocumentationFamilyHelper,
    PromotionPolicyHelper,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _policy_helper() -> PromotionPolicyHelper:
    return PromotionPolicyHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_promotion_policy_helper_resolves_pattern_policy_for_implementation_slice() -> None:
    helper = _policy_helper()

    policy = helper.resolve(
        source_artifact_kind="implementation_slice",
        target_family="pattern",
    )

    assert policy.policy_id == "policy.promotion.plan_pattern"
    assert policy.target_root == "plan/docs/patterns"
    assert policy.required_review_path == "repository_maintainer_review"


def test_promotion_policy_helper_validates_alignment_against_documentation_family_rules() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    policy_helper = PromotionPolicyHelper.from_loader(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )
    documentation_helper = DocumentationFamilyHelper.from_loader(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )

    assert policy_helper.validate_alignment(documentation_helper) == ()
