from __future__ import annotations

import importlib
import sys

import pytest

from watchtower_core.control_plane.models import (
    FoundationIndex,
    HumanSurfacePolicyRegistry,
    PackRegistry,
    PackRuntimeManifest,
    PackSettings,
    RetentionPolicyRegistry,
    StatusRegistry,
    TaskIndex,
    ValidationSuiteRegistry,
    WorkflowIndex,
)


def test_control_plane_models_export_live_index_models() -> None:
    foundation_index = FoundationIndex.from_document(
        {
            "$schema": "urn:example:foundation-index",
            "id": "index.foundations",
            "title": "Example Foundation Index",
            "status": "active",
            "entries": [
                {
                    "foundation_id": "foundation.example",
                    "title": "Example Foundation",
                    "summary": "Exercises the stable foundation model export surface.",
                    "status": "active",
                    "audience": "shared",
                    "authority": "authoritative",
                    "doc_path": "core/docs/foundations/example.md",
                    "updated_at": "2026-03-13T18:03:07Z",
                    "uses_internal_references": False,
                    "uses_external_references": False,
                }
            ],
        }
    )
    task_index = TaskIndex.from_document(
        {
            "$schema": "urn:example:task-index",
            "id": "index.plan_tasks",
            "title": "Example Task Index",
            "status": "active",
            "entries": [
                {
                    "task_id": "task.example",
                    "initiative_id": "initiative.example",
                    "trace_id": "trace.example",
                    "initiative_title": "Example Initiative",
                    "title": "Example Task",
                    "summary": "Exercises the stable live task model export surface.",
                    "status": "active",
                    "task_status": "planned",
                    "task_kind": "feature",
                    "priority": "high",
                    "owner": "repository_maintainer",
                    "doc_path": "plan/initiatives/example/.wt/tasks/example/task.json",
                    "updated_at": "2026-03-13T18:03:07Z",
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

    assert foundation_index.get("foundation.example").doc_path == "core/docs/foundations/example.md"
    assert task_index.get("task.example").trace_id == "trace.example"
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
            "workspace_roots": {
                "workspace_root": "packs/example",
                "machine_root": "packs/example/.wt",
                "docs_root": "packs/example/docs",
                "workflows_root": "packs/example/workflows",
                "tracking_root": "packs/example/tracking",
                "initiatives_root": "packs/example/initiatives",
                "projects_root": "packs/example/projects",
                "domain_roots": {
                    "initiatives": "packs/example/initiatives",
                    "projects": "packs/example/projects",
                    "reviews": "packs/example/reviews"
                },
                "overview_path": "packs/example/overview.md",
            },
            "default_validation_suite_id": "suite.example.validation_baseline",
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
    assert pack_settings.workspace_roots.machine_root == "packs/example/.wt"
    assert pack_settings.default_validation_suite_id == "suite.example.validation_baseline"
    assert status_registry.get("active").summary == "Active example."

    pack_registry = PackRegistry.from_document(
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:pack-registry:v1",
            "id": "registry.packs",
            "title": "Example Pack Registry",
            "status": "active",
            "packs": [
                {
                    "pack_id": "pack.example",
                    "pack_slug": "example",
                    "command_namespace": "example",
                    "pack_settings_path": "packs/example/.wt/manifests/pack_settings.json",
                    "pack_runtime_manifest_path": (
                        "packs/example/.wt/manifests/pack_runtime_manifest.json"
                    ),
                    "python_distribution": "watchtower-example",
                    "python_package": "watchtower_example",
                    "default_repo_pack": True,
                }
            ],
        }
    )
    runtime_manifest = PackRuntimeManifest.from_document(
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-runtime-manifest:v1",
            "surface_name": "pack_runtime_manifest",
            "contract_version": "v1",
            "description": "Example runtime manifest export test.",
            "updated_at": "2026-03-20T22:10:00Z",
            "pack_id": "pack.example",
            "pack_slug": "example",
            "command_namespace": "example",
            "python_distribution": "watchtower-example",
            "python_package": "watchtower_example",
            "integration_module": "watchtower_example.integration",
            "declared_capabilities": [
                "command_registration",
                "query_runtime",
                "sync_targets",
                "validation_provider",
            ],
            "required_validation_suite_ids": ["suite.example.validation_baseline"],
            "owned_roots": {
                "workspace_root": "packs/example",
                "machine_root": "packs/example/.wt",
                "docs_root": "packs/example/docs",
                "workflows_root": "packs/example/workflows",
                "tracking_root": "packs/example/tracking",
                "python_root": "packs/example/python",
                "domain_roots": {
                    "reviews": "packs/example/reviews"
                }
            },
        }
    )

    assert pack_registry.default_pack().pack_slug == "example"
    assert runtime_manifest.owned_roots.python_root == "packs/example/python"
    assert pack_settings.workspace_roots.domain_root_map()["reviews"] == "packs/example/reviews"
    assert runtime_manifest.owned_roots.domain_root_map()["reviews"] == "packs/example/reviews"


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
                    "path_pattern": "plan/initiatives/*",
                    "match_mode": "glob",
                    "path_kind": "initiative_archive_root",
                    "phase_qualifier": "terminal_only",
                    "entry_status": "active",
                    "current_disposition": "purge_when_eligible",
                    "clean_endstate_disposition": "purge_when_eligible",
                    "operational_visibility": "hidden",
                    "purge_gate": "promotion_before_deletion",
                    "governing_surfaces": ["retention_policy_registry"],
                    "clarifying_rule": "Example retention rule.",
                    "surviving_authority_paths": ["plan/docs/", "core/control_plane/ledgers/purges/"],
                }
            ],
        }
    )

    assert registry.get("policy.retention.example").clean_endstate_disposition == (
        "purge_when_eligible"
    )


def test_retired_planning_reexport_modules_are_not_importable() -> None:
    catalog_module = "watchtower_core.control_plane.models." + "_".join(("planning", "catalog"))
    documents_module = "watchtower_core.control_plane.models." + "_".join(
        ("planning", "documents")
    )
    sys.modules.pop("watchtower_core.control_plane.models.planning", None)
    sys.modules.pop(catalog_module, None)
    sys.modules.pop(documents_module, None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("watchtower_core.control_plane.models.planning")
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(catalog_module)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(documents_module)
