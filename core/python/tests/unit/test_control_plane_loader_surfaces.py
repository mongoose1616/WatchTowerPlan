from __future__ import annotations

import pytest

from tests.unit.control_plane_loader_test_support import REPO_ROOT
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    RenderedSurfaceRegistry,
    SchemaCatalog,
    ValidationSuiteRegistry,
    ValidatorRegistry,
)


def test_control_plane_loader_reads_validator_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    registry = loader.load_validator_registry()
    validator = registry.get("validator.documentation.reference_front_matter")
    pack_validator = registry.get("validator.plan.validation_bundle")

    assert registry.artifact_id == "registry.validators"
    assert validator.engine == "json_schema"
    assert validator.schema_ids == (
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
    )
    assert pack_validator.artifact_kind == "validation_bundle"
    assert pack_validator.applies_to == (
        "plan/initiatives/**/.wt/evidence/*.json",
        "plan/projects/**/initiatives/**/.wt/evidence/*.json",
    )


def test_control_plane_loader_declared_validator_registry_uses_merged_contract() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    relative_path = loader.load_pack_settings().get("validator_registry").path

    registry = loader.load_declared_surface(
        surface_name="validator_registry",
        relative_path=relative_path,
    )

    assert isinstance(registry, ValidatorRegistry)
    assert registry.get("validator.control_plane.pack_settings").artifact_kind == "pack_settings"
    assert registry.get("validator.plan.validation_bundle").artifact_kind == "validation_bundle"


def test_control_plane_loader_reads_validation_suite_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    registry = loader.load_validation_suite_registry()
    suite = registry.get("suite.plan.validation_baseline")

    assert isinstance(registry, ValidationSuiteRegistry)
    assert suite.get_step("step.plan.front_matter").step_kind == "front_matter"


def test_schema_catalog_get_by_subject_kind_returns_unique_match() -> None:
    loader = ControlPlaneLoader(
        REPO_ROOT,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )

    record = loader.load_schema_catalog().get_by_subject_kind("validation_bundle")

    assert record.schema_id == "urn:watchtower:schema:artifacts:plan:validation-bundle:v1"


def test_schema_catalog_get_by_subject_kind_rejects_ambiguous_match() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    with pytest.raises(ValueError, match="documentation_front_matter"):
        loader.load_schema_catalog().get_by_subject_kind("documentation_front_matter")


def test_control_plane_loader_reads_authority_map() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    authority_map = loader.load_authority_map()
    entry = authority_map.get("authority.planning.deep_trace_context")

    assert authority_map.artifact_id == "registry.authority_map"
    assert entry.artifact_kind == "traceability_index"
    assert entry.preferred_command == "watchtower-core plan query trace"
    assert "status" in entry.status_fields


def test_control_plane_loader_reads_rendered_surface_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    registry = loader.load_rendered_surface_registry()
    surface = registry.get("rendered.task_tracking")

    assert registry.artifact_id == "registry.rendered_surfaces"
    assert surface.output_path == "plan/tracking/task_tracking.md"
    assert surface.sections[-1].kind == "updated_at"


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
    query_group = command_index.get("command.watchtower_core.query")
    query_commands = command_index.get("command.watchtower_core.query.commands")
    query_paths = command_index.get("command.watchtower_core.query.paths")
    query_foundations = command_index.get("command.watchtower_core.query.foundations")
    query_workflows = command_index.get("command.watchtower_core.query.workflows")
    query_standards = command_index.get("command.watchtower_core.query.standards")
    query_acceptance = command_index.get("command.watchtower_core.query.acceptance")
    query_evidence = command_index.get("command.watchtower_core.query.evidence")
    query_references = command_index.get("command.watchtower_core.query.references")
    plan_query_group = command_index.get("command.watchtower_core.plan.query")
    plan_query_coordination = command_index.get("command.watchtower_core.plan.query.coordination")
    plan_query_authority = command_index.get("command.watchtower_core.plan.query.authority")
    plan_query_initiatives = command_index.get("command.watchtower_core.plan.query.initiatives")
    plan_query_trace = command_index.get("command.watchtower_core.plan.query.trace")
    plan_sync_group = command_index.get("command.watchtower_core.plan.sync")
    plan_sync_all = command_index.get("command.watchtower_core.plan.sync.all")
    plan_sync_coordination = command_index.get("command.watchtower_core.plan.sync.coordination")
    plan_sync_reference_index = command_index.get(
        "command.watchtower_core.plan.sync.reference_index"
    )
    plan_sync_foundation_index = command_index.get(
        "command.watchtower_core.plan.sync.foundation_index"
    )
    plan_sync_initiative_index = command_index.get(
        "command.watchtower_core.plan.sync.initiative_index"
    )
    plan_sync_initiative_tracking = command_index.get(
        "command.watchtower_core.plan.sync.initiative_tracking"
    )
    plan_sync_standard_index = command_index.get("command.watchtower_core.plan.sync.standard_index")
    plan_sync_workflow_index = command_index.get("command.watchtower_core.plan.sync.workflow_index")
    plan_sync_traceability = command_index.get(
        "command.watchtower_core.plan.sync.traceability_index"
    )
    plan_sync_github_tasks = command_index.get("command.watchtower_core.plan.sync.github_tasks")
    route_group = command_index.get("command.watchtower_core.route")
    route_preview = command_index.get("command.watchtower_core.route.preview")
    sync_route_index = command_index.get("command.watchtower_core.sync.route_index")
    validate_all = command_index.get("command.watchtower_core.validate.all")
    validate_acceptance = command_index.get("command.watchtower_core.validate.acceptance")
    validate_front_matter = command_index.get("command.watchtower_core.validate.front_matter")
    validate_document_semantics = command_index.get(
        "command.watchtower_core.validate.document_semantics"
    )
    validate_artifact = command_index.get("command.watchtower_core.validate.artifact")

    assert command_index.get("command.watchtower_core").implementation_path == (
        "core/python/src/watchtower_host/cli/parser.py"
    )
    assert (
        command_index.get("command.watchtower_core").package_entrypoint
        == "watchtower_host.cli.main:main"
    )
    assert doctor.parent_command_id == "command.watchtower_core"
    assert doctor.doc_path == "core/docs/commands/core_python/watchtower_core_doctor.md"
    assert doctor.implementation_path == "core/python/src/watchtower_host/cli/doctor_family.py"
    assert route_group.parent_command_id == "command.watchtower_core"
    assert route_group.doc_path == "core/docs/commands/core_python/watchtower_core_route.md"
    assert route_group.implementation_path == "core/python/src/watchtower_host/cli/route_family.py"
    assert route_preview.parent_command_id == "command.watchtower_core.route"
    assert (
        route_preview.doc_path == "core/docs/commands/core_python/watchtower_core_route_preview.md"
    )
    assert (
        route_preview.implementation_path == "core/python/src/watchtower_host/cli/route_family.py"
    )
    assert query_group.parent_command_id == "command.watchtower_core"
    assert query_group.doc_path == "core/docs/commands/core_python/watchtower_core_query.md"
    assert query_group.implementation_path == "core/python/src/watchtower_host/cli/query_family.py"
    assert query_commands.parent_command_id == "command.watchtower_core.query"
    assert (
        query_commands.doc_path
        == "core/docs/commands/core_python/watchtower_core_query_commands.md"
    )
    assert (
        query_commands.implementation_path
        == "core/python/src/watchtower_host/cli/query_discovery_family.py"
    )
    assert query_paths.default_output_format == "human"
    assert query_paths.doc_path == "core/docs/commands/core_python/watchtower_core_query_paths.md"
    assert (
        query_paths.implementation_path
        == "core/python/src/watchtower_host/cli/query_discovery_family.py"
    )
    assert query_foundations.parent_command_id == "command.watchtower_core.query"
    assert (
        query_foundations.doc_path
        == "core/docs/commands/core_python/watchtower_core_query_foundations.md"
    )
    assert (
        query_foundations.implementation_path
        == "core/python/src/watchtower_host/cli/query_knowledge_family.py"
    )
    assert query_workflows.parent_command_id == "command.watchtower_core.query"
    assert (
        query_workflows.doc_path
        == "core/docs/commands/core_python/watchtower_core_query_workflows.md"
    )
    assert (
        query_workflows.implementation_path
        == "core/python/src/watchtower_host/cli/query_knowledge_family.py"
    )
    assert query_standards.parent_command_id == "command.watchtower_core.query"
    assert (
        query_standards.doc_path
        == "core/docs/commands/core_python/watchtower_core_query_standards.md"
    )
    assert (
        query_standards.implementation_path
        == "core/python/src/watchtower_host/cli/query_knowledge_family.py"
    )
    assert plan_query_group.parent_command_id == "command.watchtower_core.plan"
    assert (
        plan_query_group.doc_path == "plan/docs/commands/core_python/watchtower_core_plan_query.md"
    )
    assert plan_query_group.implementation_path == "plan/python/src/watchtower_plan/cli/query.py"
    assert plan_query_coordination.parent_command_id == "command.watchtower_core.plan.query"
    assert (
        plan_query_coordination.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_query_coordination.md"
    )
    assert (
        plan_query_coordination.implementation_path
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert query_acceptance.parent_command_id == "command.watchtower_core.query"
    assert (
        query_acceptance.doc_path
        == "core/docs/commands/core_python/watchtower_core_query_acceptance.md"
    )
    assert (
        query_acceptance.implementation_path
        == "core/python/src/watchtower_host/cli/query_records_family.py"
    )
    assert query_evidence.parent_command_id == "command.watchtower_core.query"
    assert (
        query_evidence.doc_path
        == "core/docs/commands/core_python/watchtower_core_query_evidence.md"
    )
    assert (
        query_evidence.implementation_path
        == "core/python/src/watchtower_host/cli/query_records_family.py"
    )
    assert plan_query_authority.parent_command_id == "command.watchtower_core.plan.query"
    assert (
        plan_query_authority.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_query_authority.md"
    )
    assert (
        plan_query_authority.implementation_path == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert plan_query_initiatives.parent_command_id == "command.watchtower_core.plan.query"
    assert (
        plan_query_initiatives.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_query_initiatives.md"
    )
    assert (
        plan_query_initiatives.implementation_path == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert plan_query_trace.parent_command_id == "command.watchtower_core.plan.query"
    assert (
        plan_query_trace.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_query_trace.md"
    )
    assert plan_query_trace.implementation_path == "plan/python/src/watchtower_plan/cli/query.py"
    assert query_references.parent_command_id == "command.watchtower_core.query"
    assert (
        query_references.doc_path
        == "core/docs/commands/core_python/watchtower_core_query_references.md"
    )
    assert (
        query_references.implementation_path
        == "core/python/src/watchtower_host/cli/query_knowledge_family.py"
    )
    assert plan_sync_group.parent_command_id == "command.watchtower_core.plan"
    assert plan_sync_group.doc_path == "plan/docs/commands/core_python/watchtower_core_plan_sync.md"
    assert plan_sync_group.implementation_path == "plan/python/src/watchtower_plan/cli/sync.py"
    assert plan_sync_reference_index.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_reference_index.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_reference_index.md"
    )
    assert plan_sync_all.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_all.doc_path == "plan/docs/commands/core_python/watchtower_core_plan_sync_all.md"
    )
    assert plan_sync_all.implementation_path == "plan/python/src/watchtower_plan/cli/sync.py"
    assert plan_sync_coordination.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_coordination.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_coordination.md"
    )
    assert sync_route_index.parent_command_id == "command.watchtower_core.sync"
    assert (
        sync_route_index.doc_path
        == "core/docs/commands/core_python/watchtower_core_sync_route_index.md"
    )
    assert (
        sync_route_index.implementation_path == "core/python/src/watchtower_host/cli/sync_family.py"
    )
    assert (
        plan_sync_coordination.implementation_path == "plan/python/src/watchtower_plan/cli/sync.py"
    )
    assert plan_sync_initiative_index.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_initiative_index.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_initiative_index.md"
    )
    assert (
        plan_sync_initiative_index.implementation_path
        == "plan/python/src/watchtower_plan/cli/sync.py"
    )
    assert plan_sync_initiative_tracking.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_initiative_tracking.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_initiative_tracking.md"
    )
    assert plan_sync_foundation_index.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_foundation_index.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_foundation_index.md"
    )
    assert plan_sync_standard_index.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_standard_index.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_standard_index.md"
    )
    assert plan_sync_workflow_index.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_workflow_index.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_workflow_index.md"
    )
    assert (
        plan_sync_traceability.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_traceability_index.md"
    )
    assert plan_sync_traceability.parent_command_id == "command.watchtower_core.plan.sync"
    assert plan_sync_github_tasks.parent_command_id == "command.watchtower_core.plan.sync"
    assert (
        plan_sync_github_tasks.doc_path
        == "plan/docs/commands/core_python/watchtower_core_plan_sync_github_tasks.md"
    )
    assert validate_all.parent_command_id == "command.watchtower_core.validate"
    assert validate_all.doc_path == "core/docs/commands/core_python/watchtower_core_validate_all.md"
    assert (
        validate_all.implementation_path == "core/python/src/watchtower_host/cli/validate_family.py"
    )
    assert validate_acceptance.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_acceptance.doc_path
        == "core/docs/commands/core_python/watchtower_core_validate_acceptance.md"
    )
    assert validate_front_matter.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_front_matter.doc_path
        == "core/docs/commands/core_python/watchtower_core_validate_front_matter.md"
    )
    assert validate_document_semantics.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_document_semantics.doc_path
        == "core/docs/commands/core_python/watchtower_core_validate_document_semantics.md"
    )
    assert validate_artifact.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_artifact.doc_path
        == "core/docs/commands/core_python/watchtower_core_validate_artifact.md"
    )


def test_control_plane_loader_reads_route_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    route_index = loader.load_route_index()
    entry = route_index.get("route.code_review")

    assert route_index.artifact_id == "index.routes"
    assert entry.task_type == "Code Review"
    assert "workflow.code_review" in entry.required_workflow_ids
    assert "core/workflows/modules/code_review.md" in entry.required_workflow_paths


def test_control_plane_loader_reads_traceability_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    traceability_index = loader.load_traceability_index()
    trace = traceability_index.get("trace.governed_acceptance_example")

    assert trace.trace_id == "trace.governed_acceptance_example"
    assert trace.source_surface_paths


def test_control_plane_loader_reads_initiative_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    initiative_index = loader.load_initiative_index()
    coordination_index = loader.load_coordination_index()
    artifact_index = loader.load_artifact_index()

    assert initiative_index.artifact_id == "index.initiatives"
    assert coordination_index.artifact_id == "index.coordination"
    assert artifact_index.get("index.artifacts").artifact_family == "artifact_index"
    for entry in initiative_index.entries:
        assert entry.current_phase in {
            "capture",
            "execution",
            "closeout",
            "closed",
        }
        assert isinstance(entry.active_task_summaries, tuple)
        assert entry.next_surface_path
        assert entry.key_surface_path


def test_control_plane_loader_reads_governed_indexes() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    foundation_index = loader.load_foundation_index()
    standard_index = loader.load_standard_index()
    workflow_index = loader.load_workflow_index()
    task_index = loader.load_task_index()

    foundation = foundation_index.get("foundation.engineering_design_principles")
    standard = standard_index.get("std.governance.github_collaboration")
    workflow = workflow_index.get("workflow.github_task_sync")

    assert foundation.authority == "authoritative"
    assert foundation.doc_path == "core/docs/foundations/engineering_design_principles.md"
    assert standard.category == "governance"
    assert standard.owner == "repository_maintainer"
    assert ".github/" in standard.applies_to
    assert standard.uses_external_references is True
    assert "core/docs/references/github_collaboration_reference.md" in standard.reference_doc_paths
    assert "workflow" in standard.operationalization_modes
    assert ".github/" in standard.operationalization_paths
    assert workflow.doc_path == "plan/workflows/modules/github_task_sync.md"
    assert workflow.phase_type == "execution"
    assert workflow.task_family == "github_integration"
    assert workflow.uses_internal_references is True
    assert "partial_update" in workflow.primary_risks
    assert "sync" in workflow.trigger_tags
    assert "workflow.task_lifecycle_management" in workflow.companion_workflow_ids
    assert (
        "plan/docs/standards/governance/github_task_sync_standard.md"
        in workflow.internal_reference_paths
    )
    for task in task_index.entries:
        assert task.doc_path.endswith("/task.json")
        assert task.task_status in {
            "planned",
            "ready",
            "in_progress",
            "in_review",
            "blocked",
            "completed",
            "cancelled",
        }


def test_control_plane_loader_reads_reference_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    reference_index = loader.load_reference_index()
    entry = reference_index.get("ref.github_collaboration")

    assert entry.doc_path == "core/docs/references/github_collaboration_reference.md"
    assert entry.uses_external_references is True
    assert "https://docs.github.com/en/rest/issues/issues" in entry.canonical_upstream_urls
    assert (
        "plan/docs/standards/governance/github_collaboration_standard.md" in entry.applied_by_paths
    )


def test_control_plane_loader_reads_foundation_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    foundation_index = loader.load_foundation_index()
    entry = foundation_index.get("foundation.engineering_design_principles")

    assert entry.doc_path == "core/docs/foundations/engineering_design_principles.md"
    assert entry.authority == "authoritative"
    assert (
        "core/docs/standards/engineering/engineering_best_practices_standard.md"
        in entry.applied_by_paths
    )


def test_control_plane_loader_load_known_surface_materializes_schema_catalog() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    surface = loader.load_known_surface("core/control_plane/registries/schema_catalog.json")

    assert isinstance(surface, SchemaCatalog)
    assert surface.get("urn:watchtower:schema:interfaces:packs:pack-settings:v1").version == "v1"


def test_control_plane_loader_load_known_surface_materializes_rendered_surface_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    surface = loader.load_known_surface(
        "core/control_plane/registries/rendered_surface_registry.json"
    )

    assert isinstance(surface, RenderedSurfaceRegistry)
    assert surface.get("rendered.coordination_tracking").title == "Coordination Tracking"
