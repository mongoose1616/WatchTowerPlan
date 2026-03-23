from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane import ControlPlaneLoader
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
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def test_plan_pack_context_loads_human_surface_policy_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context(PLAN_PACK_SETTINGS_PATH)

    registry = context.registries["human_surface_policy_registry"]
    assert isinstance(registry, HumanSurfacePolicyRegistry)
    assert registry.get("policy.human_surface.plan_root").surfaces[2].relative_path == (
        "plan_overview.md"
    )


def test_plan_pack_context_loads_artifact_family_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context(PLAN_PACK_SETTINGS_PATH)

    registry = context.registries["artifact_family_registry"]
    assert isinstance(registry, ArtifactFamilyRegistry)
    assert registry.get("deferred_item_record").status_field == "status"


def test_plan_pack_context_loads_documentation_family_and_template_catalog() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context(PLAN_PACK_SETTINGS_PATH)

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

    context = loader.load_pack_context(PLAN_PACK_SETTINGS_PATH)

    registry = context.registries["retention_policy_registry"]
    assert isinstance(registry, RetentionPolicyRegistry)
    assert registry.get("policy.retention.plan_promoted_guidance").current_disposition == (
        "authoritative"
    )


def test_plan_pack_context_loads_lifecycle_review_and_source_registries() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context(PLAN_PACK_SETTINGS_PATH)

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

    context = loader.load_pack_context(PLAN_PACK_SETTINGS_PATH)

    registry = context.registries["promotion_policy_registry"]
    assert isinstance(registry, PromotionPolicyRegistry)
    assert registry.get("policy.promotion.plan_pattern").target_root == "plan/docs/patterns"


def test_plan_pack_context_loads_project_surface_policy_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context(PLAN_PACK_SETTINGS_PATH)

    registry = context.registries["project_surface_policy_registry"]
    assert isinstance(registry, ProjectSurfacePolicyRegistry)
    assert registry.get("policy.project_surface.project_root").surfaces[0].relative_path == ".wt"
