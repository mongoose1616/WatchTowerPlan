from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_control_plane_loader_reads_validator_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    registry = loader.load_validator_registry()
    validator = registry.get("validator.documentation.reference_front_matter")

    assert registry.artifact_id == "registry.validators"
    assert validator.engine == "json_schema"
    assert validator.schema_ids == (
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
    )


def test_control_plane_loader_reads_repository_path_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    index = loader.load_repository_path_index()
    entry = index.get("core/python/")

    assert index.coverage_mode == "entrypoints"
    assert entry.surface_kind == "python_workspace"
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
    query_evidence = command_index.get("command.watchtower_core.query.evidence")
    query_trace = command_index.get("command.watchtower_core.query.trace")
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

    assert doctor.parent_command_id == "command.watchtower_core"
    assert doctor.doc_path == "docs/commands/core_python/watchtower_core_doctor.md"
    assert query_paths.default_output_format == "human"
    assert query_paths.doc_path == "docs/commands/core_python/watchtower_core_query_paths.md"
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


def test_control_plane_loader_reads_traceability_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    traceability_index = loader.load_traceability_index()
    trace = traceability_index.get("trace.core_python_foundation")

    assert trace.trace_id == "trace.core_python_foundation"
    assert "design.features.schema_resolution_and_index_search" in trace.design_ids


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
    assert workflow.uses_internal_references is True
    assert (
        "docs/standards/governance/github_task_sync_standard.md"
        in workflow.internal_reference_paths
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
