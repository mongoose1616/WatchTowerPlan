from __future__ import annotations

import json
from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import WorkflowIndexSyncService
from watchtower_core.repo_ops.sync.workflow_index import validate_workflow_additional_load_section

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_workflow_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = WorkflowIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["workflow_id"] == "workflow.github_task_sync"
        and entry["phase_type"] == "execution"
        and entry["task_family"] == "github_integration"
        and entry["uses_internal_references"] is True
        and "partial_update" in entry["primary_risks"]
        and "sync" in entry["trigger_tags"]
        and "workflow.task_lifecycle_management" in entry.get("companion_workflow_ids", [])
        and "docs/standards/governance/github_task_sync_standard.md"
        in entry.get("internal_reference_paths", [])
        for entry in entries
    )


def test_workflow_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = WorkflowIndexSyncService(loader)
    output_path = tmp_path / "workflow_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.workflows"


def test_validate_workflow_additional_load_section_accepts_task_specific_files() -> None:
    section = (
        "- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/"
        "prd_md_standard.md): defines the required PRD structure for the output.\n"
    )

    result = validate_workflow_additional_load_section(
        "workflows/modules/prd_generation.md",
        section,
        repo_root=REPO_ROOT,
    )

    assert result == ("docs/standards/documentation/prd_md_standard.md",)


def test_validate_workflow_additional_load_section_rejects_routing_baseline_files() -> None:
    section = "- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): already loaded.\n"

    with pytest.raises(ValueError, match="routing-baseline files"):
        validate_workflow_additional_load_section(
            "workflows/modules/code_validation.md",
            section,
            repo_root=REPO_ROOT,
        )


def test_validate_workflow_additional_load_section_accepts_document_relative_files(
    tmp_path: Path,
) -> None:
    workflow_path = tmp_path / "repo" / "workflows/modules/example_workflow.md"
    load_target = tmp_path / "repo" / "docs/references/example_reference.md"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    load_target.parent.mkdir(parents=True, exist_ok=True)
    load_target.write_text("# Example reference\n", encoding="utf-8")
    section = (
        "- [example_reference.md](../../docs/references/example_reference.md): "
        "task-specific governed reference.\n"
    )

    result = validate_workflow_additional_load_section(
        "workflows/modules/example_workflow.md",
        section,
        repo_root=tmp_path / "repo",
        source_path=workflow_path,
    )

    assert result == ("docs/references/example_reference.md",)
