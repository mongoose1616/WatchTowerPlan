from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync.workflow_index import (
    WorkflowIndexSyncService,
    validate_workflow_additional_load_section,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def test_workflow_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = WorkflowIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["workflow_id"] == "workflow.documentation_review"
        and entry["workflow_kind"] == "module"
        and entry["phase_type"] == "review"
        and entry["task_family"] == "documentation_review"
        and "review" in entry["trigger_tags"]
        and "workflow.documentation_refresh" in entry.get("companion_workflow_ids", [])
        and "workflow.documentation_implementation_reconciliation"
        in entry.get("companion_workflow_ids", [])
        for entry in entries
    )
    assert any(
        entry["workflow_id"] == "workflow.github_task_sync"
        and entry["workflow_kind"] == "module"
        and entry["phase_type"] == "execution"
        and entry["task_family"] == "github_integration"
        and entry["uses_internal_references"] is True
        and "partial_update" in entry["primary_risks"]
        and "sync" in entry["trigger_tags"]
        and "workflow.task_lifecycle_management" in entry.get("companion_workflow_ids", [])
        for entry in entries
    )
    assert any(
        entry["workflow_id"] == "workflow.documentation_implementation_reconciliation"
        and "current" in entry["trigger_tags"]
        and "cli" in entry["trigger_tags"]
        and "behavior" in entry["trigger_tags"]
        for entry in entries
    )
    assert any(
        entry["workflow_id"] == "workflow.task_phase_transition"
        and "successor" in entry["trigger_tags"]
        and "task" in entry["trigger_tags"]
        and "owner" in entry["trigger_tags"]
        for entry in entries
    )
    assert any(
        entry["workflow_id"] == "workflow.test_suite_optimization"
        and entry["workflow_kind"] == "module"
        and entry["doc_path"] == "core/workflows/modules/test_suite_optimization.md"
        and "test" in entry["trigger_tags"]
        and "runtime" in entry["trigger_tags"]
        for entry in entries
    )


def test_workflow_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = WorkflowIndexSyncService(loader)
    output_path = tmp_path / "workflow_index.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.workflows"


def test_validate_workflow_additional_load_section_accepts_task_specific_files() -> None:
    section = (
        "- [compact_document_authoring_standard.md]("
        "/core/docs/standards/documentation/compact_document_authoring_standard.md): "
        "defines the compact authored-document structure for live initiative outputs.\n"
    )

    result = validate_workflow_additional_load_section(
        "packs/example/workflows/modules/initiative_brief_authoring.md",
        section,
        repo_root=REPO_ROOT,
    )

    assert result == ("core/docs/standards/documentation/compact_document_authoring_standard.md",)


def test_validate_workflow_additional_load_section_rejects_routing_baseline_files() -> None:
    section = "- [AGENTS.md](/AGENTS.md): already loaded.\n"

    with pytest.raises(ValueError, match="routing-baseline files"):
        validate_workflow_additional_load_section(
            "core/workflows/modules/code_validation.md",
            section,
            repo_root=REPO_ROOT,
        )


def test_validate_workflow_additional_load_section_rejects_generic_workflow_standards() -> None:
    section = (
        "- [routing_and_context_loading_standard.md](/core/docs/standards/workflows/"
        "routing_and_context_loading_standard.md): generic workflow baseline.\n"
    )

    with pytest.raises(ValueError, match="routing-baseline files"):
        validate_workflow_additional_load_section(
            "core/workflows/modules/code_validation.md",
            section,
            repo_root=REPO_ROOT,
        )


def test_validate_workflow_additional_load_section_accepts_document_relative_files(
    tmp_path: Path,
) -> None:
    workflow_path = tmp_path / "repo" / "core/workflows/modules/example_workflow.md"
    load_target = tmp_path / "repo" / "core/docs/references/example_reference.md"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    load_target.parent.mkdir(parents=True, exist_ok=True)
    load_target.write_text("# Example reference\n", encoding="utf-8")
    section = (
        "- [example_reference.md](../../../core/docs/references/example_reference.md): "
        "task-specific governed reference.\n"
    )

    result = validate_workflow_additional_load_section(
        "core/workflows/modules/example_workflow.md",
        section,
        repo_root=tmp_path / "repo",
        source_path=workflow_path,
    )

    assert result == ("core/docs/references/example_reference.md",)


def test_workflow_index_sync_rejects_heading_after_list_without_blank_line(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    workflow_path = repo_root / "core/workflows/modules/code_validation.md"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(
        dedent(
            """\
            # Code Validation Workflow

            ## Purpose
            Use this workflow to test blank-line heading separation for workflow sync.

            ## Use When
            - Validating workflow sync behavior.

            ## Inputs
            - One example request.
            ## Workflow
            1. Run the workflow sync check.

            ## Data Structure
            - One workflow fixture.

            ## Outputs
            - One validation result.

            ## Done When
            - Workflow index sync rejects the invalid spacing.
            """
        ),
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    service = WorkflowIndexSyncService(loader)

    with pytest.raises(ValueError, match="separated from the preceding list by a blank line"):
        service.build_document()


def test_workflow_index_sync_includes_role_root_documents(tmp_path: Path) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    module_path = repo_root / "core/workflows/modules/review_execution_baseline.md"
    role_path = repo_root / "core/workflows/roles/architecture_reviewer.md"
    module_path.parent.mkdir(parents=True, exist_ok=True)
    role_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.write_text(
        dedent(
            """\
            # Review Execution Baseline Workflow

            ## Purpose
            Use this workflow to provide one reusable review baseline.

            ## Use When
            - Running one substantive review.

            ## Inputs
            - One scoped review request.

            ## Workflow
            1. Execute the shared baseline review procedure.

            ## Data Structure
            - One baseline review plan.

            ## Outputs
            - One reusable review baseline result.

            ## Done When
            - The shared review baseline has been applied.
            """
        ),
        encoding="utf-8",
    )
    role_path.write_text(
        dedent(
            """\
            # Architecture Reviewer Role

            ## Purpose
            Use this role to apply one architecture-focused review lens.

            ## Use When
            - Reviewing architecture boundaries for one target.

            ## Inputs
            - One scoped review request.

            ## Composes Modules
            - [review_execution_baseline.md](../modules/review_execution_baseline.md): baseline.
              Applies it under an architecture-specific lens.

            ## Workflow
            1. Reuse the shared review baseline and inspect the relevant design surfaces.

            ## Data Structure
            - One set of architecture-focused findings.

            ## Outputs
            - One architecture review result.

            ## Done When
            - The architecture review posture has been applied to the scoped target.
            """
        ),
        encoding="utf-8",
    )

    metadata_path = repo_root / "core/control_plane/registries/workflow_metadata_registry.json"
    metadata_document = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata_document["entries"].append(
        {
            "workflow_id": "workflow.review_execution_baseline",
            "phase_type": "review",
            "task_family": "review_execution",
            "primary_risks": ["review_gap"],
            "extra_trigger_tags": ["review", "baseline"],
        }
    )
    metadata_document["entries"].append(
        {
            "workflow_id": "workflow.architecture_reviewer",
            "phase_type": "review",
            "task_family": "architecture_review",
            "primary_risks": ["architecture_blind_spot"],
            "extra_trigger_tags": ["architecture", "review"],
        }
    )
    metadata_path.write_text(f"{json.dumps(metadata_document, indent=2)}\n", encoding="utf-8")

    loader = ControlPlaneLoader(repo_root)
    document = WorkflowIndexSyncService(loader).build_document()
    entries = document["entries"]
    assert any(
        entry["workflow_id"] == "workflow.architecture_reviewer"
        and entry["workflow_kind"] == "role"
        and entry["composes_module_paths"] == [
            "core/workflows/modules/review_execution_baseline.md"
        ]
        for entry in entries
    )


def test_workflow_index_sync_rejects_role_without_composes_modules(tmp_path: Path) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    role_path = repo_root / "core/workflows/roles/architecture_reviewer.md"
    role_path.parent.mkdir(parents=True, exist_ok=True)
    role_path.write_text(
        dedent(
            """\
            # Architecture Reviewer Role

            ## Purpose
            Use this role to apply one architecture-focused review lens.

            ## Use When
            - Reviewing architecture boundaries for one target.

            ## Inputs
            - One scoped review request.

            ## Workflow
            1. Reuse the shared review baseline and inspect the relevant design surfaces.

            ## Data Structure
            - One set of architecture-focused findings.

            ## Outputs
            - One architecture review result.

            ## Done When
            - The architecture review posture has been applied to the scoped target.
            """
        ),
        encoding="utf-8",
    )

    metadata_path = repo_root / "core/control_plane/registries/workflow_metadata_registry.json"
    metadata_document = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata_document["entries"].append(
        {
            "workflow_id": "workflow.architecture_reviewer",
            "phase_type": "review",
            "task_family": "architecture_review",
            "primary_risks": ["architecture_blind_spot"],
            "extra_trigger_tags": ["architecture", "review"],
        }
    )
    metadata_path.write_text(f"{json.dumps(metadata_document, indent=2)}\n", encoding="utf-8")

    loader = ControlPlaneLoader(repo_root)
    with pytest.raises(ValueError, match="is missing required sections: Composes Modules"):
        WorkflowIndexSyncService(loader).build_document()


def test_workflow_index_sync_rejects_composes_modules_on_module_files(tmp_path: Path) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    module_path = repo_root / "core/workflows/modules/review_execution_baseline.md"
    module_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.write_text(
        dedent(
            """\
            # Review Execution Baseline Workflow

            ## Purpose
            Use this workflow to provide one reusable review baseline.

            ## Use When
            - Running one substantive review.

            ## Inputs
            - One scoped review request.

            ## Composes Modules
            - [core.md](./core.md): this should be invalid on workflow modules.

            ## Workflow
            1. Execute the shared baseline review procedure.

            ## Data Structure
            - One baseline review plan.

            ## Outputs
            - One reusable review baseline result.

            ## Done When
            - The shared review baseline has been applied.
            """
        ),
        encoding="utf-8",
    )
    core_module_path = repo_root / "core/workflows/modules/core.md"
    core_module_path.write_text(
        dedent(
            """\
            # Core Workflow

            ## Purpose
            Use this workflow to provide one shared routed baseline.

            ## Use When
            - Running one routed task.

            ## Inputs
            - One routed task request.

            ## Workflow
            1. Load the routed baseline.

            ## Data Structure
            - One baseline context record.

            ## Outputs
            - One routed baseline.

            ## Done When
            - The routed baseline is active.
            """
        ),
        encoding="utf-8",
    )

    metadata_path = repo_root / "core/control_plane/registries/workflow_metadata_registry.json"
    metadata_document = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata_document["entries"].extend(
        [
            {
                "workflow_id": "workflow.review_execution_baseline",
                "phase_type": "review",
                "task_family": "review_execution",
                "primary_risks": ["review_gap"],
                "extra_trigger_tags": ["review", "baseline"],
            },
            {
                "workflow_id": "workflow.core",
                "phase_type": "shared",
                "task_family": "routing_baseline",
                "primary_risks": ["context_gap"],
                "extra_trigger_tags": ["core", "baseline"],
            },
        ]
    )
    metadata_path.write_text(f"{json.dumps(metadata_document, indent=2)}\n", encoding="utf-8")

    loader = ControlPlaneLoader(repo_root)
    with pytest.raises(
        ValueError,
        match="must not define section 'Composes Modules' outside workflow role roots",
    ):
        WorkflowIndexSyncService(loader).build_document()
