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
        "current_status",
        "recent_events_or_changes",
        "active_tasks",
        "blockers",
        "next_actions",
        "evidence_or_validation_state",
    )
    assert entry.section_spec_schema_id == (
        "urn:watchtower:schema:interfaces:plan:documentation:initiative-progress-section-spec:v1"
    )
    assert helper.validate_contracts(REPO_ROOT) == ()


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


def test_template_catalog_helper_reports_section_spec_mismatch(tmp_path: Path) -> None:
    helper = _helper()
    shutil.copytree(REPO_ROOT / "plan/.wt/templates", tmp_path / "plan/.wt/templates")
    target = tmp_path / "plan/.wt/templates/initiatives/progress.md"
    target.write_text(
        target.read_text(encoding="utf-8").replace(
            "## Current Status",
            "## Broken Status",
            1,
        ),
        encoding="utf-8",
    )

    issues = helper.validate_contracts(tmp_path)

    assert any(issue.issue_code == "section_spec_mismatch" for issue in issues)


def test_core_template_catalog_loads_by_explicit_path_and_validates_contracts() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    catalog = loader.load_template_catalog(
        "core/control_plane/registries/template_catalog.json"
    )
    helper = TemplateCatalogHelper(catalog, schema_store=loader.schema_store)

    entry = helper.template("template.core.workflow.module")

    assert entry.section_spec_schema_id == (
        "urn:watchtower:schema:interfaces:documentation:workflow-module-section-spec:v1"
    )
    assert helper.validate_contracts(REPO_ROOT) == ()
