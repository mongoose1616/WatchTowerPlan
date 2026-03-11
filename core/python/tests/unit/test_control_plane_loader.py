from __future__ import annotations

import json
from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.schemas import SchemaStore, SupplementalSchemaDocument

REPO_ROOT = Path(__file__).resolve().parents[4]


def write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def test_control_plane_loader_reads_validator_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    registry = loader.load_validator_registry()
    validator = registry.get("validator.documentation.reference_front_matter")

    assert registry.artifact_id == "registry.validators"
    assert validator.engine == "json_schema"
    assert validator.schema_ids == (
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
    )


def test_control_plane_loader_reads_authority_map() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    authority_map = loader.load_authority_map()
    entry = authority_map.get("authority.planning.deep_trace_context")

    assert authority_map.artifact_id == "registry.authority_map"
    assert entry.artifact_kind == "planning_catalog"
    assert entry.preferred_command == "watchtower-core query planning"
    assert "artifact_status" in entry.status_fields


def test_control_plane_loader_reads_workflow_metadata_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    registry = loader.load_workflow_metadata_registry()
    entry = registry.get("workflow.github_task_sync")

    assert registry.artifact_id == "registry.workflow_metadata"
    assert entry.phase_type == "execution"
    assert entry.task_family == "github_integration"
    assert "workflow.task_lifecycle_management" in entry.companion_workflow_ids


def test_control_plane_loader_reads_repository_path_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    index = loader.load_repository_path_index()
    entry = index.get("core/python/")

    assert index.coverage_mode == "entrypoints"
    assert entry.surface_kind == "python_workspace"
    assert entry.maturity == "supporting"
    assert entry.priority == "medium"
    assert entry.audience_hint == "shared"
    assert "core/python/AGENTS.md" in entry.related_paths


def test_control_plane_loader_reads_command_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    command_index = loader.load_command_index()
    doctor = command_index.get("command.watchtower_core.doctor")
    query_paths = command_index.get("command.watchtower_core.query.paths")
    query_foundations = command_index.get("command.watchtower_core.query.foundations")
    query_workflows = command_index.get("command.watchtower_core.query.workflows")
    query_standards = command_index.get("command.watchtower_core.query.standards")
    query_acceptance = command_index.get("command.watchtower_core.query.acceptance")
    query_coordination = command_index.get("command.watchtower_core.query.coordination")
    query_authority = command_index.get("command.watchtower_core.query.authority")
    query_evidence = command_index.get("command.watchtower_core.query.evidence")
    query_initiatives = command_index.get("command.watchtower_core.query.initiatives")
    query_trace = command_index.get("command.watchtower_core.query.trace")
    route_group = command_index.get("command.watchtower_core.route")
    route_preview = command_index.get("command.watchtower_core.route.preview")
    sync_initiative_index = command_index.get("command.watchtower_core.sync.initiative_index")
    sync_initiative_tracking = command_index.get(
        "command.watchtower_core.sync.initiative_tracking"
    )
    sync_coordination = command_index.get("command.watchtower_core.sync.coordination")
    sync_route_index = command_index.get("command.watchtower_core.sync.route_index")
    sync_standard_index = command_index.get("command.watchtower_core.sync.standard_index")
    sync_workflow_index = command_index.get("command.watchtower_core.sync.workflow_index")
    sync_traceability = command_index.get("command.watchtower_core.sync.traceability_index")
    sync_github_tasks = command_index.get("command.watchtower_core.sync.github_tasks")
    validate_all = command_index.get("command.watchtower_core.validate.all")
    validate_acceptance = command_index.get("command.watchtower_core.validate.acceptance")
    validate_front_matter = command_index.get("command.watchtower_core.validate.front_matter")
    validate_document_semantics = command_index.get(
        "command.watchtower_core.validate.document_semantics"
    )
    validate_artifact = command_index.get("command.watchtower_core.validate.artifact")

    assert command_index.get("command.watchtower_core").implementation_path == (
        "core/python/src/watchtower_core/cli/parser.py"
    )
    assert doctor.parent_command_id == "command.watchtower_core"
    assert doctor.doc_path == "docs/commands/core_python/watchtower_core_doctor.md"
    assert doctor.implementation_path == "core/python/src/watchtower_core/cli/doctor_family.py"
    assert route_group.parent_command_id == "command.watchtower_core"
    assert route_group.doc_path == "docs/commands/core_python/watchtower_core_route.md"
    assert (
        route_group.implementation_path
        == "core/python/src/watchtower_core/cli/route_family.py"
    )
    assert route_preview.parent_command_id == "command.watchtower_core.route"
    assert (
        route_preview.doc_path
        == "docs/commands/core_python/watchtower_core_route_preview.md"
    )
    assert (
        route_preview.implementation_path
        == "core/python/src/watchtower_core/cli/route_family.py"
    )
    assert query_paths.default_output_format == "human"
    assert query_paths.doc_path == "docs/commands/core_python/watchtower_core_query_paths.md"
    assert query_paths.implementation_path == "core/python/src/watchtower_core/cli/query_family.py"
    assert query_foundations.parent_command_id == "command.watchtower_core.query"
    assert (
        query_foundations.doc_path
        == "docs/commands/core_python/watchtower_core_query_foundations.md"
    )
    assert query_workflows.parent_command_id == "command.watchtower_core.query"
    assert (
        query_workflows.doc_path
        == "docs/commands/core_python/watchtower_core_query_workflows.md"
    )
    assert query_standards.parent_command_id == "command.watchtower_core.query"
    assert (
        query_standards.doc_path
        == "docs/commands/core_python/watchtower_core_query_standards.md"
    )
    assert query_coordination.parent_command_id == "command.watchtower_core.query"
    assert (
        query_coordination.doc_path
        == "docs/commands/core_python/watchtower_core_query_coordination.md"
    )
    assert (
        query_coordination.implementation_path
        == "core/python/src/watchtower_core/cli/query_family.py"
    )
    assert query_authority.parent_command_id == "command.watchtower_core.query"
    assert (
        query_authority.doc_path
        == "docs/commands/core_python/watchtower_core_query_authority.md"
    )
    assert query_acceptance.parent_command_id == "command.watchtower_core.query"
    assert (
        query_acceptance.doc_path
        == "docs/commands/core_python/watchtower_core_query_acceptance.md"
    )
    assert query_evidence.parent_command_id == "command.watchtower_core.query"
    assert (
        query_evidence.doc_path
        == "docs/commands/core_python/watchtower_core_query_evidence.md"
    )
    assert query_initiatives.parent_command_id == "command.watchtower_core.query"
    assert (
        query_initiatives.doc_path
        == "docs/commands/core_python/watchtower_core_query_initiatives.md"
    )
    query_references = command_index.get("command.watchtower_core.query.references")
    assert query_trace.parent_command_id == "command.watchtower_core.query"
    assert query_references.parent_command_id == "command.watchtower_core.query"
    assert (
        query_references.doc_path
        == "docs/commands/core_python/watchtower_core_query_references.md"
    )
    assert sync_traceability.parent_command_id == "command.watchtower_core.sync"
    sync_reference_index = command_index.get("command.watchtower_core.sync.reference_index")
    sync_foundation_index = command_index.get("command.watchtower_core.sync.foundation_index")
    assert sync_reference_index.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_reference_index.doc_path
        == "docs/commands/core_python/watchtower_core_sync_reference_index.md"
    )
    sync_all = command_index.get("command.watchtower_core.sync.all")
    assert sync_all.parent_command_id == "command.watchtower_core.sync"
    assert sync_all.doc_path == "docs/commands/core_python/watchtower_core_sync_all.md"
    assert sync_all.implementation_path == "core/python/src/watchtower_core/cli/sync_family.py"
    assert sync_coordination.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_coordination.doc_path
        == "docs/commands/core_python/watchtower_core_sync_coordination.md"
    )
    assert sync_route_index.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_route_index.doc_path
        == "docs/commands/core_python/watchtower_core_sync_route_index.md"
    )
    assert (
        sync_route_index.implementation_path
        == "core/python/src/watchtower_core/cli/sync_family.py"
    )
    assert sync_initiative_index.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_initiative_index.doc_path
        == "docs/commands/core_python/watchtower_core_sync_initiative_index.md"
    )
    assert sync_initiative_tracking.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_initiative_tracking.doc_path
        == "docs/commands/core_python/watchtower_core_sync_initiative_tracking.md"
    )
    assert sync_foundation_index.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_foundation_index.doc_path
        == "docs/commands/core_python/watchtower_core_sync_foundation_index.md"
    )
    assert sync_standard_index.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_standard_index.doc_path
        == "docs/commands/core_python/watchtower_core_sync_standard_index.md"
    )
    assert sync_workflow_index.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_workflow_index.doc_path
        == "docs/commands/core_python/watchtower_core_sync_workflow_index.md"
    )
    assert (
        sync_traceability.doc_path
        == "docs/commands/core_python/watchtower_core_sync_traceability_index.md"
    )
    assert sync_github_tasks.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_github_tasks.doc_path
        == "docs/commands/core_python/watchtower_core_sync_github_tasks.md"
    )
    assert validate_all.parent_command_id == "command.watchtower_core.validate"
    assert validate_all.doc_path == "docs/commands/core_python/watchtower_core_validate_all.md"
    assert (
        validate_all.implementation_path
        == "core/python/src/watchtower_core/cli/validate_family.py"
    )
    assert validate_acceptance.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_acceptance.doc_path
        == "docs/commands/core_python/watchtower_core_validate_acceptance.md"
    )
    assert validate_front_matter.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_front_matter.doc_path
        == "docs/commands/core_python/watchtower_core_validate_front_matter.md"
    )
    assert validate_document_semantics.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_document_semantics.doc_path
        == "docs/commands/core_python/watchtower_core_validate_document_semantics.md"
    )
    assert validate_artifact.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_artifact.doc_path
        == "docs/commands/core_python/watchtower_core_validate_artifact.md"
    )


def test_control_plane_loader_reads_route_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    route_index = loader.load_route_index()
    entry = route_index.get("route.code_review")

    assert route_index.artifact_id == "index.routes"
    assert entry.task_type == "Code Review"
    assert "workflow.code_review" in entry.required_workflow_ids
    assert "workflows/modules/code_review.md" in entry.required_workflow_paths


def test_control_plane_loader_reads_traceability_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    traceability_index = loader.load_traceability_index()
    trace = traceability_index.get("trace.core_python_foundation")

    assert trace.trace_id == "trace.core_python_foundation"
    assert "design.features.schema_resolution_and_index_search" in trace.design_ids


def test_control_plane_loader_reads_initiative_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    initiative_index = loader.load_initiative_index()
    coordination_index = loader.load_coordination_index()
    entry = initiative_index.get("trace.core_python_foundation")

    assert entry.trace_id == "trace.core_python_foundation"
    assert coordination_index.artifact_id == "index.coordination"
    assert entry.current_phase in {
        "prd",
        "design",
        "implementation_planning",
        "execution",
        "validation",
        "closeout",
        "closed",
    }
    assert isinstance(entry.active_task_summaries, tuple)
    assert entry.next_surface_path
    assert entry.key_surface_path


def test_control_plane_loader_reads_planning_indexes() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    prd_index = loader.load_prd_index()
    decision_index = loader.load_decision_index()
    design_index = loader.load_design_document_index()
    foundation_index = loader.load_foundation_index()
    standard_index = loader.load_standard_index()
    workflow_index = loader.load_workflow_index()

    prd = prd_index.get("prd.core_python_foundation")
    decision = decision_index.get("decision.core_python_workspace_root")
    design = design_index.get("design.features.python_validator_execution")
    foundation = foundation_index.get("foundation.engineering_design_principles")
    standard = standard_index.get("std.governance.github_collaboration")
    workflow = workflow_index.get("workflow.github_task_sync")

    assert prd.trace_id == "trace.core_python_foundation"
    assert "req.core_python_foundation.003" in prd.requirement_ids
    assert decision.decision_status == "accepted"
    assert "prd.core_python_foundation" in decision.linked_prd_ids
    assert design.family == "feature_design"
    assert design.trace_id == "trace.core_python_foundation"
    assert foundation.authority == "authoritative"
    assert foundation.doc_path == "docs/foundations/engineering_design_principles.md"
    assert prd.uses_internal_references is True
    assert decision.uses_internal_references is True
    assert design.uses_internal_references is True
    assert standard.category == "governance"
    assert standard.uses_external_references is True
    assert "docs/references/github_collaboration_reference.md" in standard.reference_doc_paths
    assert workflow.doc_path == "workflows/modules/github_task_sync.md"
    assert workflow.phase_type == "execution"
    assert workflow.task_family == "github_integration"
    assert workflow.uses_internal_references is True
    assert "partial_update" in workflow.primary_risks
    assert "sync" in workflow.trigger_tags
    assert "workflow.task_lifecycle_management" in workflow.companion_workflow_ids
    assert (
        "docs/standards/governance/github_task_sync_standard.md"
        in workflow.internal_reference_paths
    )


def test_control_plane_loader_accepts_supplemental_schema_documents() -> None:
    schema_id = "urn:watchtower:schema:external:loader-check:v1"
    loader = ControlPlaneLoader(
        REPO_ROOT,
        supplemental_schema_documents=(
            SupplementalSchemaDocument.from_document(
                {
                    "$id": schema_id,
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "properties": {"kind": {"const": "loader_check"}},
                    "required": ["kind"],
                    "additionalProperties": False,
                },
                source_label="external:loader-check",
            ),
        ),
    )

    loader.schema_store.validate_instance({"kind": "loader_check"}, schema_id=schema_id)
    assert loader.supplemental_schema_ids == (schema_id,)


def test_control_plane_loader_accepts_supplemental_schema_paths(tmp_path: Path) -> None:
    schema_path = tmp_path / "schemas" / "loader_path.v1.schema.json"
    schema_id = "urn:watchtower:schema:external:loader-path-check:v1"
    write_json(
        schema_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Loader Path Check",
            "description": "Schema loaded from a filesystem path.",
            "type": "object",
            "properties": {"kind": {"const": "loader_path_check"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )

    loader = ControlPlaneLoader(
        REPO_ROOT,
        supplemental_schema_paths=(schema_path,),
    )

    loader.schema_store.validate_instance({"kind": "loader_path_check"}, schema_id=schema_id)
    assert loader.supplemental_schema_ids == (schema_id,)


def test_control_plane_loader_rejects_supplemental_docs_with_explicit_schema_store() -> None:
    schema_store = SchemaStore.from_repo_root(REPO_ROOT)

    with pytest.raises(ValueError, match="supplemental schema documents or paths"):
        ControlPlaneLoader(
            REPO_ROOT,
            schema_store=schema_store,
            supplemental_schema_documents=(
                SupplementalSchemaDocument.from_document(
                    {
                        "$id": "urn:watchtower:schema:external:conflict:v1",
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "type": "object",
                    },
                    source_label="external:conflict",
                ),
            ),
        )


def test_control_plane_loader_rejects_supplemental_paths_with_explicit_schema_store() -> None:
    schema_store = SchemaStore.from_repo_root(REPO_ROOT)

    with pytest.raises(ValueError, match="supplemental schema documents or paths"):
        ControlPlaneLoader(
            REPO_ROOT,
            schema_store=schema_store,
            supplemental_schema_paths=("core/control_plane/schemas/interfaces/packs",),
        )


def test_control_plane_loader_reads_reference_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    reference_index = loader.load_reference_index()
    entry = reference_index.get("ref.github_collaboration")

    assert entry.doc_path == "docs/references/github_collaboration_reference.md"
    assert entry.uses_external_references is True
    assert "https://docs.github.com/en/rest/issues/issues" in entry.canonical_upstream_urls
    assert (
        "docs/standards/governance/github_collaboration_standard.md"
        in entry.applied_by_paths
    )


def test_control_plane_loader_reads_foundation_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    foundation_index = loader.load_foundation_index()
    entry = foundation_index.get("foundation.engineering_design_principles")

    assert entry.doc_path == "docs/foundations/engineering_design_principles.md"
    assert entry.authority == "authoritative"
    assert (
        "docs/standards/engineering/engineering_best_practices_standard.md"
        in entry.applied_by_paths
    )
