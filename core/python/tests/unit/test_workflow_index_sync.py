from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from textwrap import dedent

import pytest

import watchtower_core.sync.workflow_index as workflow_index_module
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync.workflow_index import (
    WorkflowIndexSyncService,
    build_workflow_document_context,
    load_workflow_document,
    validate_workflow_additional_load_section,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _workflow_entry_map(document: dict[str, object]) -> dict[str, dict[str, object]]:
    entries = document["entries"]
    assert isinstance(entries, list)
    return {
        entry["workflow_id"]: entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("workflow_id"), str)
    }


def _first_pack_workflow_entry(
    entries_by_id: dict[str, dict[str, object]],
    loader: ControlPlaneLoader,
    *,
    workflow_kind: str,
    subdir: str,
) -> dict[str, object] | None:
    workflows_root = loader.load_pack_settings().workspace_roots.workflows_root
    prefix = f"{workflows_root}/{subdir}/"
    for entry in entries_by_id.values():
        if entry["workflow_kind"] != workflow_kind:
            continue
        if not entry["doc_path"].startswith(prefix):
            continue
        return entry
    return None


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _append_workflow_metadata(
    repo_root: Path,
    workflow_id: str,
    *,
    phase_type: str = "execution",
    task_family: str = "workflow_testing",
    primary_risks: tuple[str, ...] = ("boundary_leak",),
    extra_trigger_tags: tuple[str, ...] = ("workflow", "test"),
) -> None:
    metadata_path = repo_root / "core/control_plane/registries/workflow_metadata_registry.json"
    metadata_document = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata_document["entries"].append(
        {
            "workflow_id": workflow_id,
            "phase_type": phase_type,
            "task_family": task_family,
            "primary_risks": list(primary_risks),
            "extra_trigger_tags": list(extra_trigger_tags),
        }
    )
    metadata_path.write_text(f"{json.dumps(metadata_document, indent=2)}\n", encoding="utf-8")


def test_workflow_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = WorkflowIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    entries_by_id = _workflow_entry_map(document)
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
        entry["workflow_id"] == "workflow.documentation_implementation_reconciliation"
        and "current" in entry["trigger_tags"]
        and "cli" in entry["trigger_tags"]
        and "behavior" in entry["trigger_tags"]
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
    assert any(
        entry["workflow_id"] == "workflow.workflow_system_review"
        and entry["workflow_kind"] == "module"
        and entry["phase_type"] == "review"
        and entry["task_family"] == "workflow_governance"
        and "workflows" in entry["trigger_tags"]
        and "routing" in entry["trigger_tags"]
        and "validator" in entry["trigger_tags"]
        for entry in entries
    )
    assert any(
        entry["workflow_id"] == "workflow.workflow_steward"
        and entry["workflow_kind"] == "role"
        and entry["phase_type"] == "review"
        and entry["composes_module_paths"] == [
            "core/workflows/modules/workflow_system_review.md"
        ]
        for entry in entries
    )
    github_task_sync = entries_by_id.get("workflow.github_task_sync")
    if github_task_sync is not None:
        assert github_task_sync["workflow_kind"] == "module"
        assert github_task_sync["phase_type"] == "execution"
        assert github_task_sync["task_family"] == "github_integration"
        assert github_task_sync["uses_internal_references"] is True
        assert "partial_update" in github_task_sync["primary_risks"]
        assert "sync" in github_task_sync["trigger_tags"]
        assert "workflow.task_lifecycle_management" in github_task_sync.get(
            "companion_workflow_ids",
            [],
        )
    task_phase_transition = entries_by_id.get("workflow.task_phase_transition")
    if task_phase_transition is not None:
        assert "successor" in task_phase_transition["trigger_tags"]
        assert "task" in task_phase_transition["trigger_tags"]
        assert "owner" in task_phase_transition["trigger_tags"]
    pack_module_entry = _first_pack_workflow_entry(
        entries_by_id,
        loader,
        workflow_kind="module",
        subdir="modules",
    )
    assert pack_module_entry is not None
    assert pack_module_entry["phase_type"]
    assert pack_module_entry["task_family"]
    assert pack_module_entry["uses_internal_references"] is True
    assert pack_module_entry["trigger_tags"]
    pack_role_entry = _first_pack_workflow_entry(
        entries_by_id,
        loader,
        workflow_kind="role",
        subdir="roles",
    )
    if pack_role_entry is not None:
        assert pack_role_entry["phase_type"]
        assert pack_role_entry["composes_module_paths"]


def test_workflow_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = WorkflowIndexSyncService(loader)
    output_path = tmp_path / "workflow_index.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.workflows"


def test_load_workflow_document_reuses_cached_pack_root_context(monkeypatch) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    call_counts = {"routing": 0, "module_roots": 0, "disallowed_tokens": 0}

    real_routing_paths = workflow_index_module.pack_routing_table_paths
    real_workflow_module_roots = workflow_index_module.pack_workflow_module_roots
    real_disallowed_tokens = workflow_index_module._shared_core_disallowed_pack_root_tokens

    def _wrap_routing_paths(*args, **kwargs):
        call_counts["routing"] += 1
        return real_routing_paths(*args, **kwargs)

    def _wrap_workflow_module_roots(*args, **kwargs):
        call_counts["module_roots"] += 1
        return real_workflow_module_roots(*args, **kwargs)

    def _wrap_disallowed_tokens(*args, **kwargs):
        call_counts["disallowed_tokens"] += 1
        return real_disallowed_tokens(*args, **kwargs)

    monkeypatch.setattr(
        workflow_index_module,
        "pack_routing_table_paths",
        _wrap_routing_paths,
    )
    monkeypatch.setattr(
        workflow_index_module,
        "pack_workflow_module_roots",
        _wrap_workflow_module_roots,
    )
    monkeypatch.setattr(
        workflow_index_module,
        "_shared_core_disallowed_pack_root_tokens",
        _wrap_disallowed_tokens,
    )

    context = build_workflow_document_context(loader)
    load_workflow_document(
        loader,
        "core/workflows/modules/workflow_system_review.md",
        context=context,
    )
    load_workflow_document(
        loader,
        "core/workflows/roles/workflow_steward.md",
        context=context,
    )

    assert call_counts == {
        "routing": 1,
        "module_roots": 1,
        "disallowed_tokens": 1,
    }


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


def test_workflow_index_sync_rejects_core_workflow_pack_owned_additional_load_path(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    workflow_path = repo_root / "core/workflows/modules/shared_validation.md"
    pack_doc_path = repo_root / "plan/docs/standards/example_standard.md"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    pack_doc_path.parent.mkdir(parents=True, exist_ok=True)
    pack_doc_path.write_text("# Example Standard\n", encoding="utf-8")
    workflow_path.write_text(
        dedent(
            """\
            # Shared Validation Workflow

            ## Purpose
            Use this workflow to validate one shared repository change.

            ## Use When
            - One shared change needs validation.

            ## Inputs
            - One scoped validation request.

            ## Additional Files to Load
            - [example_standard.md](/plan/docs/standards/example_standard.md): invalid pack-owned
              guidance.

            ## Workflow
            1. Validate the shared change.

            ## Data Structure
            - One shared validation record.

            ## Outputs
            - One validation result.

            ## Done When
            - The shared validation pass is complete.
            """
        ),
        encoding="utf-8",
    )
    _append_workflow_metadata(repo_root, "workflow.shared_validation")

    loader = ControlPlaneLoader(repo_root)
    with pytest.raises(
        ValueError,
        match=r"shared core workflow docs must keep 'Additional Files to Load' under core/",
    ):
        WorkflowIndexSyncService(loader).build_document()


def test_workflow_index_sync_rejects_core_workflow_pack_specific_coordination_language(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    workflow_path = repo_root / "core/workflows/modules/shared_validation.md"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(
        dedent(
            """\
            # Shared Validation Workflow

            ## Purpose
            Use this workflow to validate one shared repository change.

            ## Use When
            - One shared change needs validation.

            ## Inputs
            - Existing initiative context when present.

            ## Workflow
            1. Review the initiative tracker before validating the change.

            ## Data Structure
            - One shared validation record.

            ## Outputs
            - One validation result.

            ## Done When
            - The shared validation pass is complete.
            """
        ),
        encoding="utf-8",
    )
    _append_workflow_metadata(repo_root, "workflow.shared_validation")

    loader = ControlPlaneLoader(repo_root)
    with pytest.raises(
        ValueError,
        match=(
            r"shared core workflow docs must not require pack-specific "
            r"coordination language such as 'initiative'"
        ),
    ):
        WorkflowIndexSyncService(loader).build_document()


def test_workflow_index_sync_rejects_core_role_composing_pack_module(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    role_path = repo_root / "core/workflows/roles/shared_reviewer.md"
    pack_module_path = repo_root / "plan/workflows/modules/plan_specific_review.md"
    role_path.parent.mkdir(parents=True, exist_ok=True)
    pack_module_path.parent.mkdir(parents=True, exist_ok=True)
    role_path.write_text(
        dedent(
            """\
            # Shared Reviewer Role

            ## Purpose
            Use this role to apply one shared review lens.

            ## Use When
            - Running one shared review.

            ## Inputs
            - One scoped review request.

            ## Composes Modules
            - [plan_specific_review.md](/plan/workflows/modules/plan_specific_review.md): invalid
              pack-owned module.

            ## Workflow
            1. Apply the shared review lens.

            ## Data Structure
            - One shared review result.

            ## Outputs
            - One shared review output.

            ## Done When
            - The shared review lens has been applied.
            """
        ),
        encoding="utf-8",
    )
    pack_module_path.write_text(
        dedent(
            """\
            # Plan Specific Review Workflow

            ## Purpose
            Use this workflow to apply one pack-owned review path.

            ## Use When
            - Running one pack-owned review.

            ## Inputs
            - One scoped pack review request.

            ## Workflow
            1. Execute the pack-owned review procedure.

            ## Data Structure
            - One pack-owned review record.

            ## Outputs
            - One pack-owned review output.

            ## Done When
            - The pack-owned review is complete.
            """
        ),
        encoding="utf-8",
    )
    _append_workflow_metadata(
        repo_root,
        "workflow.shared_reviewer",
        phase_type="review",
        task_family="shared_review",
        primary_risks=("boundary_leak", "composition_drift"),
        extra_trigger_tags=("shared", "review"),
    )
    _append_workflow_metadata(
        repo_root,
        "workflow.plan_specific_review",
        phase_type="review",
        task_family="pack_review",
        primary_risks=("pack_coupling",),
        extra_trigger_tags=("plan", "review"),
    )

    loader = ControlPlaneLoader(repo_root)
    with pytest.raises(
        ValueError,
        match=r"shared core workflow roles must compose only modules under core/workflows/modules/",
    ):
        WorkflowIndexSyncService(loader).build_document()


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
