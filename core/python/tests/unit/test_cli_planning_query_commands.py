from __future__ import annotations

from tests.unit.cli_command_helpers import run_json_command


def test_query_prds_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "prds", "--trace-id", "trace.core_python_foundation"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query prds"
    assert payload["status"] == "ok"
    assert any(entry["prd_id"] == "prd.core_python_foundation" for entry in payload["results"])


def test_query_decisions_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "decisions", "--decision-status", "accepted"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query decisions"
    assert payload["status"] == "ok"
    assert any(
        entry["decision_id"] == "decision.core_python_workspace_root"
        for entry in payload["results"]
    )


def test_query_designs_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "designs",
            "--family",
            "feature_design",
            "--trace-id",
            "trace.core_python_foundation",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query designs"
    assert payload["status"] == "ok"
    assert any(
        entry["document_id"] == "design.features.python_validator_execution"
        for entry in payload["results"]
    )


def test_query_acceptance_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "acceptance", "--trace-id", "trace.core_python_foundation"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query acceptance"
    assert payload["status"] == "ok"
    assert any(
        entry["contract_id"] == "contract.acceptance.core_python_foundation"
        for entry in payload["results"]
    )


def test_query_evidence_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "evidence", "--trace-id", "trace.core_python_foundation"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query evidence"
    assert payload["status"] == "ok"
    assert any(
        entry["evidence_id"] == "evidence.core_python_foundation.traceability_baseline"
        for entry in payload["results"]
    )


def test_query_tasks_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "tasks", "--trace-id", "trace.local_task_tracking"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query tasks"
    assert payload["status"] == "ok"
    assert any(
        entry["task_id"] == "task.local_task_tracking.github_sync.001"
        for entry in payload["results"]
    )


def test_query_tasks_supports_dependency_details_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "tasks",
            "--task-id",
            "task.local_task_tracking.github_sync.001",
            "--include-dependency-details",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query tasks"
    entry = payload["results"][0]
    assert entry["task_id"] == "task.local_task_tracking.github_sync.001"
    assert "blocked_by_details" in entry
    assert "depends_on_details" in entry
    assert "reverse_dependency_details" in entry


def test_query_initiatives_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "initiatives", "--trace-id", "trace.core_python_foundation"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    assert payload["status"] == "ok"
    assert "default_initiative_status" not in payload
    assert any(
        entry["trace_id"] == "trace.core_python_foundation" for entry in payload["results"]
    )


def test_query_coordination_defaults_to_active_status(capsys) -> None:
    result, payload = run_json_command(capsys, ["query", "coordination"])

    assert result == 0
    assert payload["command"] == "watchtower-core query coordination"
    assert payload["status"] == "ok"
    assert payload["default_initiative_status"] == "active"
    assert payload["coordination_mode"] in {
        "active_work",
        "blocked_work",
        "ready_for_bootstrap",
    }
    assert payload["recommended_next_action"]
    assert payload["recommended_surface_path"]
    assert "actionable_tasks" in payload
    assert "recent_closed_initiatives" in payload


def test_query_coordination_supports_explicit_historical_lookup(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "coordination",
            "--initiative-status",
            "completed",
            "--trace-id",
            "trace.core_python_foundation",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query coordination"
    assert payload["status"] == "ok"
    matched = next(
        entry for entry in payload["results"] if entry["trace_id"] == "trace.core_python_foundation"
    )
    assert matched["artifact_status"] == "active"
    assert matched["initiative_status"] == "completed"
    assert "status" not in matched


def test_query_planning_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "planning", "--trace-id", "trace.core_python_foundation"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query planning"
    assert payload["status"] == "ok"
    assert "default_initiative_status" not in payload
    assert payload["results"][0]["trace_id"] == "trace.core_python_foundation"
    assert "artifact_status" in payload["results"][0]
    assert "status" not in payload["results"][0]
    assert payload["results"][0]["coordination"]["current_phase"]


def test_query_planning_defaults_to_active_status_when_filterless(capsys) -> None:
    result, payload = run_json_command(capsys, ["query", "planning"])

    assert result == 0
    assert payload["command"] == "watchtower-core query planning"
    assert payload["status"] == "ok"
    assert payload["default_initiative_status"] == "active"
    assert all(entry["initiative_status"] == "active" for entry in payload["results"])


def test_query_initiatives_uses_explicit_artifact_status_field(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "initiatives",
            "--trace-id",
            "trace.core_python_foundation",
            "--initiative-status",
            "completed",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    entry = next(
        item for item in payload["results"] if item["trace_id"] == "trace.core_python_foundation"
    )
    assert entry["artifact_status"] == "active"
    assert entry["initiative_status"] == "completed"
    assert "status" not in entry


def test_query_initiatives_defaults_to_active_status_when_filterless(capsys) -> None:
    result, payload = run_json_command(capsys, ["query", "initiatives"])

    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    assert payload["status"] == "ok"
    assert payload["default_initiative_status"] == "active"
    assert all(entry["initiative_status"] == "active" for entry in payload["results"])


def test_query_initiatives_supports_closed_current_phase_history_lookup(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "initiatives",
            "--initiative-status",
            "completed",
            "--current-phase",
            "closed",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    assert payload["result_count"] > 0
    assert all(entry["current_phase"] == "closed" for entry in payload["results"])


def test_query_planning_supports_explicit_historical_lookup(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "planning",
            "--initiative-status",
            "completed",
            "--trace-id",
            "trace.core_python_foundation",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query planning"
    assert "default_initiative_status" not in payload
    entry = next(
        item for item in payload["results"] if item["trace_id"] == "trace.core_python_foundation"
    )
    assert entry["initiative_status"] == "completed"


def test_query_authority_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "authority",
            "--question-id",
            "authority.planning.deep_trace_context",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query authority"
    assert payload["status"] == "ok"
    assert payload["results"][0]["question_id"] == "authority.planning.deep_trace_context"
    assert payload["results"][0]["artifact_kind"] == "planning_catalog"
    assert payload["results"][0]["preferred_command"] == "watchtower-core query planning"


def test_query_trace_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "trace", "--trace-id", "trace.core_python_foundation"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query trace"
    assert payload["status"] == "ok"
    assert payload["result"]["trace_id"] == "trace.core_python_foundation"
