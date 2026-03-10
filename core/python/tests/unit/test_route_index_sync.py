from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query.routes import RoutePreviewService
from watchtower_core.repo_ops.sync import RouteIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_route_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RouteIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["route_id"] == "route.repository_review"
        and entry["task_type"] == "Repository Review"
        and "workflow.repository_review" in entry["required_workflow_ids"]
        and "workflows/modules/repository_review.md" in entry["required_workflow_paths"]
        for entry in entries
    )


def test_route_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = RouteIndexSyncService(loader)
    output_path = tmp_path / "route_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.routes"


def test_route_preview_service_scores_request_text() -> None:
    service = RoutePreviewService(ControlPlaneLoader(REPO_ROOT))

    result = service.preview(request_text="review code and finalize commit")

    task_types = {match.task_type for match in result.selected_routes}
    workflow_ids = {workflow.workflow_id for workflow in result.selected_workflows}
    assert "Code Review" in task_types
    assert "Commit Closeout" in task_types
    assert "workflow.code_review" in workflow_ids
    assert "workflow.commit_closeout" in workflow_ids


def test_route_preview_service_supports_explicit_task_type() -> None:
    service = RoutePreviewService(ControlPlaneLoader(REPO_ROOT))

    result = service.preview(task_type="Repository Review")

    assert len(result.selected_routes) == 1
    assert result.selected_routes[0].task_type == "Repository Review"
    assert any(
        workflow.workflow_id == "workflow.repository_review"
        for workflow in result.selected_workflows
    )
