from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from watchtower_core.control_plane import ControlPlaneLoader, PackContext
from watchtower_core.control_plane.models import (
    ArtifactFamilyRegistry,
    DocumentationFamilyRegistry,
    HumanSurfacePolicyRegistry,
    LifecycleStageRegistry,
    ProjectSurfacePolicyRegistry,
    PromotionPolicyRegistry,
    RetentionPolicyRegistry,
    ReviewStatusRegistry,
    SourceTypeRegistry,
    TemplateCatalog,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_pack_context_loads_declared_pack_surfaces() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context()

    assert isinstance(context, PackContext)
    assert context.pack_settings.pack_id == "pack.plan"
    assert context.workspace_roots.workspace_root == "plan"
    assert context.schema_catalog.get(
        "urn:watchtower:schema:interfaces:packs:pack-settings:v1"
    ).canonical_relative_path == (
        "core/control_plane/schemas/interfaces/packs/pack_settings.schema.json"
    )
    assert (
        context.governance_surface_map.get("routing_table").path
        == "core/workflows/ROUTING_TABLE.md"
    )
    assert context.status_registry.get("accepted").entry_status == "active"
    assert context.actor_registry.get("actor.codex").actor_type == "agent"
    assert "rendered_surface_registry" in context.registries
    assert "validator_registry" in context.registries
    assert "validation_suite_registry" in context.registries
    assert (
        context.validation_suite_registry.get("suite.plan.validation_baseline")
        .get_step("step.plan.artifacts")
        .step_kind
        == "artifact"
    )
    assert "coordination_index" not in context.indexes


def test_pack_context_exposes_loaded_surfaces_by_name() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context()
    surface = context.get_surface("path_pattern_registry")

    assert surface is context.path_pattern_registry


def test_pack_context_loads_cleaned_shared_status_vocabulary() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context()

    assert context.status_registry.get("blocked").allowed_families == ()
    assert context.status_registry.get("completed").entry_status == "active"
    assert context.status_registry.get("cancelled").entry_status == "active"


def test_pack_context_loads_required_surface_from_relocated_declared_path() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    base_settings = json.loads(
        (REPO_ROOT / "core/control_plane/manifests/pack_settings.json").read_text(encoding="utf-8")
    )

    with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
        tmp_path = Path(tmp_dir)
        relocated_status_path = tmp_path / "status_registry.json"
        shutil.copy2(
            REPO_ROOT / "core/control_plane/registries/status_registry.json",
            relocated_status_path,
        )

        custom_settings = dict(base_settings)
        custom_settings["surfaces"] = [dict(entry) for entry in base_settings["surfaces"]]
        for entry in custom_settings["surfaces"]:
            if entry["surface_name"] == "status_registry":
                entry["path"] = relocated_status_path.relative_to(REPO_ROOT).as_posix()
                break
        custom_settings_path = tmp_path / "pack_settings.json"
        custom_settings_path.write_text(
            f"{json.dumps(custom_settings, indent=2)}\n",
            encoding="utf-8",
        )

        context = loader.load_pack_context(custom_settings_path.relative_to(REPO_ROOT).as_posix())

    assert context.status_registry.get("accepted").entry_status == "active"


def test_pack_context_skips_missing_rebuildable_derived_surface_until_built() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    base_settings = json.loads(
        (REPO_ROOT / "core/control_plane/manifests/pack_settings.json").read_text(encoding="utf-8")
    )

    with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
        tmp_path = Path(tmp_dir)
        custom_settings = dict(base_settings)
        custom_settings["surfaces"] = [dict(entry) for entry in base_settings["surfaces"]]
        for entry in custom_settings["surfaces"]:
            if entry["surface_name"] == "route_index":
                entry["path"] = (
                    (tmp_path / "missing_route_index.json").relative_to(REPO_ROOT).as_posix()
                )
                break
        custom_settings_path = tmp_path / "pack_settings.json"
        custom_settings_path.write_text(
            f"{json.dumps(custom_settings, indent=2)}\n",
            encoding="utf-8",
        )

        context = loader.load_pack_context(custom_settings_path.relative_to(REPO_ROOT).as_posix())

    assert "route_index" not in context.indexes
    assert context.status_registry.get("accepted").entry_status == "active"


def test_plan_pack_context_loads_human_surface_policy_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context("plan/.wt/manifests/pack_settings.json")

    registry = context.registries["human_surface_policy_registry"]
    assert isinstance(registry, HumanSurfacePolicyRegistry)
    assert registry.get("policy.human_surface.plan_root").surfaces[2].relative_path == (
        "plan_overview.md"
    )


def test_plan_pack_context_loads_artifact_family_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context("plan/.wt/manifests/pack_settings.json")

    registry = context.registries["artifact_family_registry"]
    assert isinstance(registry, ArtifactFamilyRegistry)
    assert registry.get("deferred_item_record").status_field == "status"


def test_plan_pack_context_loads_documentation_family_and_template_catalog() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context("plan/.wt/manifests/pack_settings.json")

    documentation_registry = context.registries["documentation_family_registry"]
    template_catalog = context.registries["template_catalog"]

    assert isinstance(documentation_registry, DocumentationFamilyRegistry)
    assert documentation_registry.get("foundation").mirror_group_id == "mirror.foundations"
    assert documentation_registry.get("foundation").section_spec_schema_id == (
        "urn:watchtower:schema:interfaces:plan:documentation:foundation-section-spec:v1"
    )
    assert isinstance(template_catalog, TemplateCatalog)
    assert template_catalog.get("template.plan.rendered.project.summary").surface_id == (
        "rendered.project.summary"
    )
    assert template_catalog.get(
        "template.plan.rendered.project.summary"
    ).section_spec_schema_id == (
        "urn:watchtower:schema:interfaces:plan:documentation:project-summary-section-spec:v1"
    )


def test_plan_pack_context_loads_retention_policy_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context("plan/.wt/manifests/pack_settings.json")

    registry = context.registries["retention_policy_registry"]
    assert isinstance(registry, RetentionPolicyRegistry)
    assert registry.get("policy.retention.plan_promoted_guidance").current_disposition == (
        "authoritative"
    )


def test_plan_pack_context_loads_lifecycle_review_and_source_registries() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context("plan/.wt/manifests/pack_settings.json")

    lifecycle_registry = context.registries["lifecycle_stage_registry"]
    review_registry = context.registries["review_status_registry"]
    source_registry = context.registries["source_type_registry"]

    assert isinstance(lifecycle_registry, LifecycleStageRegistry)
    assert lifecycle_registry.get("closing").current_phase == "closeout"
    assert isinstance(review_registry, ReviewStatusRegistry)
    assert review_registry.get("approved").allows_execution is True
    assert isinstance(source_registry, SourceTypeRegistry)
    assert source_registry.get("promoted_guidance").source_class == "promoted_guidance"


def test_plan_pack_context_loads_promotion_policy_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context("plan/.wt/manifests/pack_settings.json")

    registry = context.registries["promotion_policy_registry"]
    assert isinstance(registry, PromotionPolicyRegistry)
    assert registry.get("policy.promotion.plan_pattern").target_root == "plan/docs/patterns"


def test_plan_pack_context_loads_project_surface_policy_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context("plan/.wt/manifests/pack_settings.json")

    registry = context.registries["project_surface_policy_registry"]
    assert isinstance(registry, ProjectSurfacePolicyRegistry)
    assert registry.get("policy.project_surface.project_root").surfaces[0].relative_path == ".wt"
