from __future__ import annotations

import importlib
import sys

import pytest

from watchtower_core.control_plane.models import (
    HumanSurfacePolicyRegistry,
    PackSettings,
    PrdIndex,
    RetentionPolicyRegistry,
    StatusRegistry,
    ValidationSuiteRegistry,
    WorkflowIndex,
)


def test_planning_module_reexports_split_typed_index_models() -> None:
    prd_index = PrdIndex.from_document(
        {
            "$schema": "urn:example:prd-index",
            "id": "index.prds",
            "title": "Example PRD Index",
            "status": "active",
            "entries": [
                {
                    "trace_id": "trace.example",
                    "prd_id": "prd.example",
                    "title": "Example PRD",
                    "summary": "Exercises the stable model export surface.",
                    "status": "active",
                    "doc_path": "docs/planning/prds/example.md",
                    "updated_at": "2026-03-13T18:03:07Z",
                    "uses_internal_references": False,
                    "uses_external_references": False,
                }
            ],
        }
    )
    workflow_index = WorkflowIndex.from_document(
        {
            "$schema": "urn:example:workflow-index",
            "id": "index.workflows",
            "title": "Example Workflow Index",
            "status": "active",
            "entries": [
                {
                    "workflow_id": "workflow.example",
                    "title": "Example Workflow",
                    "summary": "Exercises the stable model export surface.",
                    "status": "active",
                    "doc_path": "core/workflows/modules/example.md",
                    "uses_internal_references": True,
                    "uses_external_references": False,
                }
            ],
        }
    )

    assert prd_index.get("prd.example").trace_id == "trace.example"
    assert workflow_index.get("workflow.example").workflow_id == "workflow.example"
    assert workflow_index.get("workflow.example").phase_type == "shared"


def test_control_plane_models_export_pack_contract_types() -> None:
    pack_settings = PackSettings.from_document(
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
            "surface_name": "pack_settings",
            "contract_version": "v1",
            "description": "Example pack settings export test.",
            "updated_at": "2026-03-16T05:15:00Z",
            "pack_id": "pack.example",
            "surfaces": [
                {
                    "surface_name": "schema_catalog",
                    "surface_kind": "schema_collection",
                    "path": "core/control_plane/registries/schema_catalog.json",
                    "authority": "authoritative",
                    "visibility": "hidden",
                }
            ],
        }
    )
    status_registry = StatusRegistry.from_document(
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:status-registry:v1",
            "surface_name": "status_registry",
            "contract_version": "v1",
            "description": "Example status registry export test.",
            "updated_at": "2026-03-16T05:15:00Z",
            "statuses": [
                {
                    "value": "active",
                    "entry_status": "active",
                    "summary": "Active example.",
                }
            ],
        }
    )

    assert pack_settings.get("schema_catalog").surface_kind == "schema_collection"
    assert status_registry.get("active").summary == "Active example."


def test_control_plane_models_export_validation_suite_registry_types() -> None:
    registry = ValidationSuiteRegistry.from_document(
        {
            "$schema": (
                "urn:watchtower:schema:artifacts:registries:"
                "validation-suite-registry:v1"
            ),
            "id": "registry.validation_suites",
            "title": "Example Validation Suites",
            "status": "active",
            "suites": [
                {
                    "id": "suite.example.validation_baseline",
                    "title": "Example Validation Baseline",
                    "description": "Exercises the stable validation suite model export surface.",
                    "status": "active",
                    "steps": [
                        {
                            "id": "step.example.pack_contract",
                            "title": "Validate pack contract",
                            "description": "Example pack-contract step.",
                            "step_kind": "pack_contract",
                        }
                    ],
                }
            ],
        }
    )

    assert registry.get("suite.example.validation_baseline").get_step(
        "step.example.pack_contract"
    ).step_kind == "pack_contract"


def test_control_plane_models_export_human_surface_policy_registry_types() -> None:
    registry = HumanSurfacePolicyRegistry.from_document(
        {
            "$schema": "urn:watchtower:schema:artifacts:plan:human-surface-policy-registry:v1",
            "id": "registry.human_surface_policy",
            "title": "Example Human Surface Policy",
            "status": "active",
            "entries": [
                {
                    "policy_id": "policy.example.root",
                    "path_pattern": "plan",
                    "match_mode": "exact",
                    "root_kind": "domain_root",
                    "entry_status": "active",
                    "governing_surfaces": ["human_surface_policy_registry"],
                    "clarifying_rule": "Example root policy.",
                    "surfaces": [
                        {
                            "relative_path": "README.md",
                            "entity_shape": "file",
                            "surface_role": "readme",
                            "mode": "required",
                            "authorship_mode": "authored",
                        }
                    ],
                }
            ],
        }
    )

    assert registry.get("policy.example.root").surfaces[0].relative_path == "README.md"


def test_control_plane_models_export_retention_policy_registry_types() -> None:
    registry = RetentionPolicyRegistry.from_document(
        {
            "$schema": "urn:watchtower:schema:artifacts:plan:retention-policy-registry:v1",
            "id": "registry.retention_policy",
            "title": "Example Retention Policy",
            "status": "active",
            "entries": [
                {
                    "policy_id": "policy.retention.example",
                    "path_pattern": "docs/planning",
                    "match_mode": "exact",
                    "path_kind": "legacy_history_root",
                    "phase_qualifier": "legacy_only",
                    "entry_status": "active",
                    "current_disposition": "legacy_ignored",
                    "clean_endstate_disposition": "purge_when_eligible",
                    "operational_visibility": "hidden",
                    "purge_gate": "promotion_before_deletion",
                    "governing_surfaces": ["retention_policy_registry"],
                    "clarifying_rule": "Example retention rule.",
                    "surviving_authority_paths": ["plan/"],
                }
            ],
        }
    )

    assert registry.get("policy.retention.example").clean_endstate_disposition == (
        "purge_when_eligible"
    )


def test_retired_planning_reexport_module_is_not_importable() -> None:
    sys.modules.pop("watchtower_core.control_plane.models.planning", None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("watchtower_core.control_plane.models.planning")
