from __future__ import annotations

import json
import shutil
from pathlib import Path

from watchtower_core.control_plane import ControlPlaneLoader, TemplateCatalogHelper
from watchtower_core.control_plane.models import TemplateCatalog

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> TemplateCatalogHelper:
    return TemplateCatalogHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_template_catalog_helper_resolves_rendered_initiative_templates() -> None:
    helper = _helper()

    entry = helper.template("template.plan.rendered.initiative.progress")

    assert entry.surface_id == "rendered.initiative.progress"
    assert entry.required_section_ids == (
        "gate_state",
        "task_status",
        "discrepancies",
    )
    assert helper.validate_paths(REPO_ROOT) == ()


def test_template_catalog_helper_reports_missing_template_path(tmp_path: Path) -> None:
    document = json.loads(
        (REPO_ROOT / "plan/.wt/registries/template_catalog.json").read_text(encoding="utf-8")
    )
    document["entries"][0]["template_path"] = "plan/.wt/templates/roots/missing.md"
    helper = TemplateCatalogHelper(TemplateCatalog.from_document(document))
    shutil.copytree(REPO_ROOT / "plan/.wt/templates", tmp_path / "plan/.wt/templates")

    issues = helper.validate_paths(tmp_path)

    assert len(issues) == 1
    assert issues[0].issue_code == "template_missing"
