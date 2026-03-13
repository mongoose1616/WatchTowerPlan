from __future__ import annotations

from tests.unit.cli_command_helpers import run_json_command


def test_query_paths_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "paths",
            "--surface-kind",
            "command_doc",
            "--limit",
            "2",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query paths"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert all(entry["surface_kind"] == "command_doc" for entry in payload["results"])


def test_query_paths_supports_retrieval_metadata_filters(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "paths",
            "--maturity",
            "authoritative",
            "--priority",
            "high",
            "--audience-hint",
            "shared",
            "--limit",
            "5",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query paths"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert all(entry["maturity"] == "authoritative" for entry in payload["results"])
    assert all(entry["priority"] == "high" for entry in payload["results"])
    assert all(entry["audience_hint"] == "shared" for entry in payload["results"])


def test_route_preview_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["route", "preview", "--task-type", "Repository Review"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core route preview"
    assert payload["status"] == "ok"
    assert payload["selected_route_count"] == 1
    assert payload["selected_routes"][0]["task_type"] == "Repository Review"
    assert any(
        workflow["workflow_id"] == "workflow.repository_review"
        for workflow in payload["selected_workflows"]
    )


def test_route_preview_matches_realistic_maintenance_request(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            (
                "review /external/repository/report and fix the valid issues with "
                "planning, tasks, validation, and commits"
            ),
        ],
    )

    task_types = {entry["task_type"] for entry in payload["selected_routes"]}
    workflow_ids = {entry["workflow_id"] for entry in payload["selected_workflows"]}
    assert result == 0
    assert payload["command"] == "watchtower-core route preview"
    assert payload["status"] == "ok"
    assert payload["selected_route_count"] >= 4
    assert "Repository Review" in task_types
    assert "Task Lifecycle Management" in task_types
    assert "Code Validation" in task_types
    assert "Commit Closeout" in task_types
    assert "Code Review" not in task_types
    assert "workflow.repository_review" in workflow_ids
    assert "workflow.task_lifecycle_management" in workflow_ids
    assert "workflow.code_validation" in workflow_ids
    assert "workflow.commit_closeout" in workflow_ids


def test_route_preview_matches_adjacent_boundary_prompts(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "reconcile command docs with current cli behavior",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Documentation-Implementation Reconciliation"
    }

    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "reconcile schema-backed indexes examples and validators for one artifact family",
        ],
    )

    assert result == 0
    assert {entry["task_type"] for entry in payload["selected_routes"]} == {
        "Governed Artifact Reconciliation"
    }


def test_route_preview_filters_low_signal_route_leakage_for_phase_handoffs(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "hand off this task from implementation to validation and create successor tasks",
        ],
    )

    task_types = {entry["task_type"] for entry in payload["selected_routes"]}
    assert result == 0
    assert task_types == {"Task Phase Transition"}
    assert "Code Validation" not in task_types


def test_route_preview_prefers_phase_transition_for_successor_task_boundaries(
    capsys,
) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "route",
            "preview",
            "--request",
            "move task to validation and create successor tasks",
        ],
    )

    task_types = {entry["task_type"] for entry in payload["selected_routes"]}
    assert result == 0
    assert task_types == {"Task Phase Transition"}
    assert "Task Lifecycle Management" not in task_types
