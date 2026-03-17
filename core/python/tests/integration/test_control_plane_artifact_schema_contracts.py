from __future__ import annotations

from copy import deepcopy

import pytest
from jsonschema import ValidationError

from tests.integration.control_plane_artifact_helpers import (
    FRONT_MATTER_PATTERN,
    REPO_ROOT,
    load_front_matter,
    load_json_object,
)
from watchtower_core.control_plane import TemplateCatalogHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.schemas import SchemaStore
from watchtower_core.validation.artifact import ArtifactValidationService


def test_live_governed_json_artifacts_have_active_schema_validation_coverage() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = ArtifactValidationService(loader)
    target_roots = (
        REPO_ROOT / "core/control_plane/contracts/acceptance",
        REPO_ROOT / "core/control_plane/indexes/commands",
        REPO_ROOT / "core/control_plane/indexes/coordination",
        REPO_ROOT / "core/control_plane/indexes/decisions",
        REPO_ROOT / "core/control_plane/indexes/design_documents",
        REPO_ROOT / "core/control_plane/indexes/foundations",
        REPO_ROOT / "core/control_plane/indexes/initiatives",
        REPO_ROOT / "core/control_plane/indexes/planning",
        REPO_ROOT / "core/control_plane/indexes/prds",
        REPO_ROOT / "core/control_plane/indexes/references",
        REPO_ROOT / "core/control_plane/indexes/repository_paths",
        REPO_ROOT / "core/control_plane/indexes/routes",
        REPO_ROOT / "core/control_plane/indexes/standards",
        REPO_ROOT / "core/control_plane/indexes/tasks",
        REPO_ROOT / "core/control_plane/indexes/traceability",
        REPO_ROOT / "core/control_plane/indexes/workflows",
        REPO_ROOT / "core/control_plane/ledgers/migrations",
        REPO_ROOT / "core/control_plane/ledgers/releases",
        REPO_ROOT / "core/control_plane/ledgers/validation_evidence",
        REPO_ROOT / "core/control_plane/manifests",
        REPO_ROOT / "core/control_plane/registries",
    )

    for root in target_roots:
        for path in sorted(root.glob("*.json")):
            result = service.validate(path.relative_to(REPO_ROOT).as_posix())
            assert result.passed, f"{path} failed schema validation: {result.issues}"


def test_plan_pack_governed_json_artifacts_have_active_schema_validation_coverage() -> None:
    loader = ControlPlaneLoader(
        REPO_ROOT,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )
    service = ArtifactValidationService(loader)
    target_roots = (
        REPO_ROOT / "plan" / ".wt" / "manifests",
        REPO_ROOT / "plan" / ".wt" / "policies",
        REPO_ROOT / "plan" / ".wt" / "registries",
        REPO_ROOT / "plan" / ".wt" / "indexes",
    )

    for root in target_roots:
        for path in sorted(root.glob("*.json")):
            result = service.validate(path.relative_to(REPO_ROOT).as_posix())
            assert result.passed, f"{path} failed schema validation: {result.issues}"


def test_plan_rule_registries_cover_current_live_plan_family_contracts() -> None:
    relation_registry = load_json_object(
        REPO_ROOT / "plan/.wt/registries/relation_type_registry.json"
    )
    lifecycle_registry = load_json_object(
        REPO_ROOT / "plan/.wt/registries/lifecycle_stage_registry.json"
    )
    review_registry = load_json_object(
        REPO_ROOT / "plan/.wt/registries/review_status_registry.json"
    )
    source_registry = load_json_object(
        REPO_ROOT / "plan/.wt/registries/source_type_registry.json"
    )
    transition_rules = load_json_object(
        REPO_ROOT / "plan/.wt/policies/status_transition_rules.json"
    )

    relation_names = {entry["canonical_name"] for entry in relation_registry["entries"]}
    assert {
        "depends_on",
        "blocked_by",
        "related_to",
        "implements",
        "supersedes",
        "evidences",
        "derived_from",
        "covers",
    }.issubset(relation_names)

    transition_rules_by_family = {
        entry["family_id"]: entry for entry in transition_rules["entries"]
    }
    assert {
        "initiative_state",
        "task_state",
        "validation_bundle",
        "closeout_recap",
        "guidance_promotion_record",
        "discrepancy_record",
        "project_record",
    }.issubset(transition_rules_by_family)

    def _allowed_states_for(schema_path: Path, field_name: str) -> set[str]:
        schema = load_json_object(schema_path)
        return set(schema["properties"][field_name]["enum"])

    def _allowed_readiness_states(schema_path: Path, field_name: str) -> set[str]:
        schema = load_json_object(schema_path)
        return set(schema["$defs"]["readinessEntry"]["properties"][field_name]["enum"])

    initiative_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/initiative_state.schema.json",
        "lifecycle_stage",
    )
    review_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/initiative_state.schema.json",
        "review_status",
    )
    readiness_review_states = _allowed_readiness_states(
        REPO_ROOT / "plan/.wt/schemas/artifacts/readiness_index.schema.json",
        "review_status",
    )
    task_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/task_state.schema.json",
        "status",
    )
    validation_bundle_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/validation_bundle.schema.json",
        "status",
    )
    closeout_recap_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/closeout_recap.schema.json",
        "status",
    )
    promotion_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/guidance_promotion_record.schema.json",
        "status",
    )
    discrepancy_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/discrepancy_record.schema.json",
        "status",
    )
    project_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/project_record.schema.json",
        "status",
    )
    configured_lifecycle_states = {
        entry["value"] for entry in lifecycle_registry["entries"] if entry["entry_status"] == "active"
    }
    configured_review_states = {
        entry["value"] for entry in review_registry["entries"] if entry["entry_status"] == "active"
    }
    configured_source_types = {
        entry["value"] for entry in source_registry["entries"] if entry["entry_status"] == "active"
    }

    allowed_states_by_family = {
        "initiative_state": initiative_states,
        "task_state": task_states,
        "validation_bundle": validation_bundle_states,
        "closeout_recap": closeout_recap_states,
        "guidance_promotion_record": promotion_states,
        "discrepancy_record": discrepancy_states,
        "project_record": project_states,
    }

    for family_id, allowed_states in allowed_states_by_family.items():
        entry = transition_rules_by_family[family_id]
        configured_states = set(entry["initial_states"]) | set(entry["terminal_states"])
        configured_states |= {
            transition["from_state"] for transition in entry["transitions"]
        }
        configured_states |= {
            transition["to_state"] for transition in entry["transitions"]
        }
        assert configured_states.issubset(allowed_states), (
            f"{family_id} transition rules reference states outside the live schema: "
            f"{sorted(configured_states - allowed_states)}"
        )

    assert configured_lifecycle_states == initiative_states
    assert configured_review_states == review_states
    assert configured_review_states == readiness_review_states
    assert {
        "authored_input",
        "external_reference",
        "external_import",
        "generated_output",
        "derived_artifact",
    }.issubset(configured_source_types)


def test_plan_artifact_family_registry_covers_current_live_plan_families() -> None:
    registry = load_json_object(
        REPO_ROOT / "plan/.wt/registries/artifact_family_registry.json"
    )
    loader = ControlPlaneLoader(
        REPO_ROOT,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )

    catalog_schema_ids = {
        record.schema_id
        for record in loader.load_schema_catalog().records
    }
    families = {
        entry["family_id"]: entry
        for entry in registry["entries"]
    }

    assert {
        "initiative_state",
        "initiative_event_stream",
        "task_state",
        "task_event_stream",
        "deferred_item_record",
        "validation_bundle",
        "closeout_recap",
        "discrepancy_record",
        "guidance_promotion_record",
        "project_record",
        "project_repository_map",
        "initiative_index",
        "task_index",
        "readiness_index",
        "discrepancy_index",
        "promotion_index",
        "guidance_index",
        "coordination_index",
        "project_index",
    }.issubset(families)

    for family_id, entry in families.items():
        assert entry["canonical_schema_id"] in catalog_schema_ids, (
            f"{family_id} references a schema not published in the schema catalog"
        )
        assert entry["placement_roots"], f"{family_id} is missing placement roots"
        assert entry["derived_index_ids"], f"{family_id} is missing derived index participation"


def test_plan_documentation_family_and_template_catalog_cover_live_plan_surfaces() -> None:
    pack_loader = ControlPlaneLoader(
        REPO_ROOT,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )
    core_loader = ControlPlaneLoader(REPO_ROOT)

    documentation_registry = load_json_object(
        REPO_ROOT / "plan/.wt/registries/documentation_family_registry.json"
    )
    template_catalog = load_json_object(REPO_ROOT / "plan/.wt/registries/template_catalog.json")
    rendered_registry = load_json_object(
        REPO_ROOT / "core/control_plane/registries/rendered_surface_registry.json"
    )

    plan_schema_ids = {record.schema_id for record in pack_loader.load_schema_catalog().records}
    core_schema_ids = {record.schema_id for record in core_loader.load_schema_catalog().records}
    families = {entry["family_id"]: entry for entry in documentation_registry["entries"]}
    template_entries = {entry["template_id"]: entry for entry in template_catalog["entries"]}
    rendered_surface_ids = {entry["surface_id"] for entry in rendered_registry["surfaces"]}

    assert {
        "foundation",
        "standard",
        "reference",
        "decision_record",
        "pattern",
        "workflow",
    }.issubset(families)
    assert {
        "template.plan.guidance.foundation",
        "template.plan.guidance.standard",
        "template.plan.guidance.reference",
        "template.plan.guidance.decision_record",
        "template.plan.guidance.pattern",
        "template.plan.workflow.module",
        "template.plan.rendered.plan_overview",
        "template.plan.rendered.initiative.plan",
        "template.plan.rendered.initiative.progress",
        "template.plan.rendered.initiative.summary",
        "template.plan.rendered.project.project",
        "template.plan.rendered.project.repositories",
        "template.plan.rendered.project.summary",
    }.issubset(template_entries)
    assert {
        "rendered.plan.overview",
        "rendered.initiative.plan",
        "rendered.initiative.progress",
        "rendered.initiative.summary",
        "rendered.project.project",
        "rendered.project.repositories",
        "rendered.project.summary",
    }.issubset(rendered_surface_ids)

    assert "urn:watchtower:schema:artifacts:plan:documentation-family-registry:v1" in plan_schema_ids
    assert "urn:watchtower:schema:artifacts:plan:template-catalog:v1" in plan_schema_ids
    assert "urn:watchtower:schema:interfaces:documentation:pattern-front-matter:v1" in core_schema_ids
    assert "urn:watchtower:schema:interfaces:plan:documentation:initiative-plan-section-spec:v1" in plan_schema_ids
    assert "urn:watchtower:schema:interfaces:plan:documentation:project-summary-section-spec:v1" in plan_schema_ids

    for family_id, entry in families.items():
        assert entry["front_matter_base_schema_id"] in core_schema_ids
        assert entry["front_matter_schema_id"] in core_schema_ids
        assert entry["section_spec_schema_id"] in plan_schema_ids
        for template_id in entry["template_ids"]:
            assert template_id in template_entries, (
                f"{family_id} references missing template entry {template_id}"
            )

    for template_id, entry in template_entries.items():
        template_path = REPO_ROOT / entry["template_path"]
        assert template_path.is_file(), f"{template_id} points to a missing template file"
        family_id = entry.get("family_id")
        if isinstance(family_id, str):
            assert family_id in families, f"{template_id} references unknown family {family_id}"
        front_matter_schema_id = entry.get("front_matter_schema_id")
        if isinstance(front_matter_schema_id, str):
            assert front_matter_schema_id in core_schema_ids
        section_spec_schema_id = entry.get("section_spec_schema_id")
        if isinstance(section_spec_schema_id, str):
            assert section_spec_schema_id in plan_schema_ids
        required_rendered_surface_ids = entry.get("required_rendered_surface_ids", [])
        for rendered_surface_id in required_rendered_surface_ids:
            assert rendered_surface_id in rendered_surface_ids

    helper = TemplateCatalogHelper.from_loader(
        pack_loader,
        pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )
    assert helper.validate_contracts(REPO_ROOT) == ()


def test_core_documentation_family_and_template_catalog_cover_core_surfaces() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    documentation_registry = load_json_object(
        REPO_ROOT / "core/control_plane/registries/documentation_family_registry.json"
    )
    template_catalog = load_json_object(
        REPO_ROOT / "core/control_plane/registries/template_catalog.json"
    )
    schema_ids = {record.schema_id for record in loader.load_schema_catalog().records}
    families = {entry["family_id"]: entry for entry in documentation_registry["entries"]}
    template_entries = {entry["template_id"]: entry for entry in template_catalog["entries"]}

    assert {"foundation", "workflow"}.issubset(families)
    assert {
        "template.core.root.readme",
        "template.core.root.agents",
        "template.core.workflow.module",
        "template.core.guidance.foundation",
    }.issubset(template_entries)
    assert "urn:watchtower:schema:artifacts:documentation-family-registry:v1" in schema_ids
    assert "urn:watchtower:schema:artifacts:template-catalog:v1" in schema_ids
    assert "urn:watchtower:schema:interfaces:documentation:foundation-section-spec:v1" in schema_ids
    assert "urn:watchtower:schema:interfaces:documentation:workflow-module-section-spec:v1" in schema_ids

    for family_id, entry in families.items():
        assert entry["front_matter_base_schema_id"] in schema_ids
        assert entry["front_matter_schema_id"] in schema_ids
        assert entry["section_spec_schema_id"] in schema_ids
        for template_id in entry["template_ids"]:
            assert template_id in template_entries

    for template_id, entry in template_entries.items():
        template_path = REPO_ROOT / entry["template_path"]
        assert template_path.is_file(), f"{template_id} points to a missing template file"
        section_spec_schema_id = entry.get("section_spec_schema_id")
        if isinstance(section_spec_schema_id, str):
            assert section_spec_schema_id in schema_ids

    helper = TemplateCatalogHelper(
        loader.load_template_catalog("core/control_plane/registries/template_catalog.json"),
        schema_store=loader.schema_store,
    )
    assert helper.validate_contracts(REPO_ROOT) == ()


def test_initiative_index_rejects_missing_current_phase() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    initiative_index = load_json_object(
        REPO_ROOT / "core/control_plane/indexes/initiatives/initiative_index.json"
    )
    invalid_index = deepcopy(initiative_index)
    del invalid_index["entries"][0]["current_phase"]

    with pytest.raises(ValidationError):
        store.validate_instance(invalid_index)


def test_coordination_index_rejects_missing_coordination_mode() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    coordination_index = load_json_object(
        REPO_ROOT / "core/control_plane/indexes/coordination/coordination_index.json"
    )
    invalid_index = deepcopy(coordination_index)
    del invalid_index["coordination_mode"]

    with pytest.raises(ValidationError):
        store.validate_instance(invalid_index)


def test_live_governed_applies_to_directory_paths_are_canonical() -> None:
    markdown_roots = (
        REPO_ROOT / "docs/references",
        REPO_ROOT / "docs/foundations",
        REPO_ROOT / "docs/standards",
        REPO_ROOT / "docs/planning/prds",
        REPO_ROOT / "docs/planning/decisions",
        REPO_ROOT / "docs/planning/design/features",
        REPO_ROOT / "docs/planning/design/implementation",
        REPO_ROOT / "docs/planning/tasks/open",
        REPO_ROOT / "docs/planning/tasks/closed",
    )

    for root in markdown_roots:
        for path in sorted(root.rglob("*.md")):
            if path.name in {"README.md", "AGENTS.md"}:
                continue
            if FRONT_MATTER_PATTERN.search(path.read_text(encoding="utf-8")) is None:
                continue
            front_matter = load_front_matter(path)
            applies_to = front_matter.get("applies_to")
            if not isinstance(applies_to, list):
                continue
            for value in applies_to:
                assert isinstance(value, str)
                if "/" not in value or "*" in value or "<" in value:
                    continue
                target = REPO_ROOT / value.rstrip("/")
                assert target.exists(), f"{path} applies_to path does not exist: {value}"
                if target.is_dir():
                    assert value.endswith("/"), (
                        f"{path} directory applies_to path must end in '/': {value}"
                    )
                else:
                    assert not value.endswith("/"), (
                        f"{path} file applies_to path must not end in '/': {value}"
                    )

def test_planning_catalog_rejects_missing_coordination_section() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    planning_catalog = load_json_object(
        REPO_ROOT / "core/control_plane/indexes/planning/planning_catalog.json"
    )
    invalid_catalog = deepcopy(planning_catalog)
    del invalid_catalog["entries"][0]["coordination"]

    with pytest.raises(ValidationError):
        store.validate_instance(invalid_catalog)


def test_route_index_rejects_missing_required_workflow_ids() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    route_index = load_json_object(
        REPO_ROOT / "core/control_plane/indexes/routes/route_index.json"
    )
    invalid_index = deepcopy(route_index)
    del invalid_index["entries"][0]["required_workflow_ids"]

    with pytest.raises(ValidationError):
        store.validate_instance(invalid_index)


def test_authority_map_rejects_missing_preferred_command() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    authority_map = load_json_object(
        REPO_ROOT / "core/control_plane/registries/authority_map.json"
    )
    invalid_map = deepcopy(authority_map)
    del invalid_map["entries"][0]["preferred_command"]

    with pytest.raises(ValidationError):
        store.validate_instance(invalid_map)


def test_governed_document_front_matter_profiles_validate() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    governed_families = [
        (
            REPO_ROOT / "docs/references",
            {
                "AGENTS.md",
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/prds",
            {
                "README.md",
                "prd_tracking.md",
            },
            "urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/decisions",
            {
                "README.md",
                "decision_tracking.md",
            },
            "urn:watchtower:schema:interfaces:documentation:decision-record-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/design/features",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:feature-design-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/design/implementation",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:implementation-plan-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/tasks/open",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:task-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/tasks/closed",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:task-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/standards",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:standard-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/foundations",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:foundation-front-matter:v1",
        ),
    ]

    for directory, excluded_names, schema_id in governed_families:
        for path in sorted(directory.rglob("*.md")):
            if path.name in excluded_names:
                continue
            store.validate_instance(load_front_matter(path), schema_id=schema_id)


def test_utc_timestamp_fields_reject_offset_timestamps() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    prd_front_matter = load_front_matter(
        REPO_ROOT
        / "docs/planning/prds/post_rewrite_core_cleanup_and_surface_reduction.md"
    )
    prd_front_matter["updated_at"] = "2026-03-09T05:06:54-04:00"
    with pytest.raises(ValidationError):
        store.validate_instance(
            prd_front_matter,
            schema_id="urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
        )

    validation_evidence = load_json_object(
        REPO_ROOT
        / "core/control_plane/ledgers/validation_evidence/"
        "post_rewrite_core_cleanup_and_surface_reduction_planning_baseline.json"
    )
    validation_evidence["recorded_at"] = "2026-03-09T05:06:54+01:00"
    with pytest.raises(ValidationError):
        store.validate_instance(validation_evidence)
