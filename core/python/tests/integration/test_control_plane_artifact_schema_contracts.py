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

    initiative_states = _allowed_states_for(
        REPO_ROOT / "plan/.wt/schemas/artifacts/initiative_state.schema.json",
        "lifecycle_stage",
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
