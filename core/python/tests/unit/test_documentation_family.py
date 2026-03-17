from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane import ControlPlaneLoader, DocumentationFamilyHelper

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> DocumentationFamilyHelper:
    return DocumentationFamilyHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_documentation_family_helper_exposes_foundation_mirror_contract() -> None:
    helper = _helper()

    foundation = helper.family("foundation")

    assert foundation.mirror_group_id == "mirror.foundations"
    assert foundation.required_mirror_roots == (
        "core/docs/foundations",
        "plan/docs/foundations",
    )
    assert foundation.template_ids == ("template.plan.guidance.foundation",)


def test_documentation_family_helper_validates_allowed_roots() -> None:
    helper = _helper()

    assert helper.allowed_in_root("workflow", "workflows/modules") is True

    issues = helper.validate_root("reference", "plan/docs/foundations")

    assert len(issues) == 1
    assert issues[0].issue_code == "root_not_allowed"

