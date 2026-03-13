from __future__ import annotations

from watchtower_core.control_plane.models.planning import PrdIndex, WorkflowIndex


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
                    "summary": "Exercises the compatibility import surface.",
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
                    "summary": "Exercises the compatibility import surface.",
                    "status": "active",
                    "doc_path": "workflows/modules/example.md",
                    "uses_internal_references": True,
                    "uses_external_references": False,
                }
            ],
        }
    )

    assert prd_index.get("prd.example").trace_id == "trace.example"
    assert workflow_index.get("workflow.example").workflow_id == "workflow.example"
    assert workflow_index.get("workflow.example").phase_type == "shared"
