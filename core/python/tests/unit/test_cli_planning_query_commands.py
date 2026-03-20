from __future__ import annotations

from pathlib import Path
from shutil import copytree

from tests.integration.fixture_repo_support import (
    InitiativeTaskSpec,
    bootstrap_packwide_initiative,
    materialize_plan_pack,
)
from tests.unit.cli_command_helpers import run_json_command
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.initiative_packages import InitiativePackageService
from watchtower_plan.plan_workspace import PlanWorkspaceService
from watchtower_plan.plan_task_state import update_task_document
from watchtower_plan.sync.coordination import CoordinationSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]
ACTIVE_TRACE_ID = "trace.example_live_query_active"
ACTIVE_INITIATIVE_ID = "initiative.example_live_query_active"
ACTIVE_TASK_ID = (
    "task.example_live_query_active."
    "seed_live_query_task_details"
)
DEPENDENCY_TASK_ID = (
    "task.example_live_query_active."
    "review_live_query_dependency_details"
)
COMPLETED_TRACE_ID = "trace.example_live_query_completed"
COMPLETED_INITIATIVE_SLUG = "example_live_query_completed"
COMPLETED_TASK_ID = "task.example_live_query_completed.seed_closed_query_task"
DISCREPANCY_TRACE_ID = "trace.plan_core_documentation_template_authority_foundation"
WATCHTOWER_PROJECT_ID = "project.watchtower"


def _build_live_query_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    materialize_plan_pack(repo_root, REPO_ROOT)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=ACTIVE_TRACE_ID,
        title="Example Live Query Active",
        summary="Fixture initiative for live query command coverage.",
        approve=True,
        task_specs=(
            InitiativeTaskSpec(
                title="Seed live query task details",
                summary="Provides one upstream dependency target for query coverage.",
                slug="seed_live_query_task_details",
                task_id=ACTIVE_TASK_ID,
                priority="high",
            ),
            InitiativeTaskSpec(
                title="Review live query dependency details",
                summary="Provides dependency detail coverage for task queries.",
                slug="review_live_query_dependency_details",
                task_id=DEPENDENCY_TASK_ID,
                priority="high",
                depends_on=(ACTIVE_TASK_ID,),
                blocked_by=(ACTIVE_TASK_ID,),
            ),
        ),
    )
    return repo_root


def _build_completed_query_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    materialize_plan_pack(repo_root, REPO_ROOT)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=COMPLETED_TRACE_ID,
        title="Example Live Query Completed",
        summary="Fixture initiative for completed-history query coverage.",
        approve=True,
        task_specs=(
            InitiativeTaskSpec(
                title="Seed closed query task",
                summary="Provides one completed task so the initiative can close cleanly.",
                slug="seed_closed_query_task",
                task_id=COMPLETED_TASK_ID,
                priority="high",
            ),
        ),
    )
    loader = ControlPlaneLoader(repo_root)
    update_task_document(
        loader,
        (
            f"plan/initiatives/{COMPLETED_INITIATIVE_SLUG}/.wt/tasks/"
            "seed_closed_query_task/task.json"
        ),
        updates={
            "task_status": "completed",
            "updated_at": "2026-03-19T10:55:00Z",
        },
    )
    PlanWorkspaceService(loader).sync(write=True)
    CoordinationSyncService(loader).run(write=True)
    InitiativePackageService(loader).close_packwide(
        COMPLETED_INITIATIVE_SLUG,
        initiative_status="completed",
        closure_reason="Fixture completed initiative for historical query coverage.",
        closed_at="2026-03-19T11:00:00Z",
        write=True,
    )
    return repo_root


def test_query_acceptance_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "acceptance",
            "--trace-id",
            "trace.governed_acceptance_example",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query acceptance"
    assert payload["status"] == "ok"
    assert any(
        entry["contract_id"]
        == "contract.acceptance.governed_acceptance_example"
        for entry in payload["results"]
    )


def test_query_evidence_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "evidence",
            "--trace-id",
            "trace.governed_acceptance_example",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query evidence"
    assert payload["status"] == "ok"
    assert any(
        entry["evidence_id"]
        == "evidence.governed_acceptance_example.validation_baseline"
        for entry in payload["results"]
    )


def test_query_tasks_supports_json_output(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_live_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
    result, payload = run_json_command(
        capsys,
        ["query", "tasks", "--trace-id", ACTIVE_TRACE_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query tasks"
    assert payload["status"] == "ok"
    entry = next(entry for entry in payload["results"] if entry["task_id"] == ACTIVE_TASK_ID)
    assert entry["status"] == "active"
    assert entry["task_status"] in {
        "planned",
        "ready",
        "in_progress",
        "in_review",
        "blocked",
        "completed",
        "cancelled",
    }
    assert entry["task_status"] != "active"
    assert all(entry["trace_id"] == ACTIVE_TRACE_ID for entry in payload["results"])


def test_query_tasks_supports_dependency_details_json_output(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_live_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "tasks",
            "--task-id",
            DEPENDENCY_TASK_ID,
            "--include-dependency-details",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query tasks"
    entry = payload["results"][0]
    assert entry["task_id"] == DEPENDENCY_TASK_ID
    assert "blocked_by_details" in entry
    assert "depends_on_details" in entry
    assert "reverse_dependency_details" in entry


def test_query_initiatives_supports_json_output(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_live_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
    result, payload = run_json_command(
        capsys,
        ["query", "initiatives", "--trace-id", ACTIVE_TRACE_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    assert payload["status"] == "ok"
    assert "default_initiative_status" not in payload
    assert any(
        entry["trace_id"] == ACTIVE_TRACE_ID for entry in payload["results"]
    )


def test_query_coordination_defaults_to_active_status(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_live_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
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
    assert any(entry["trace_id"] == ACTIVE_TRACE_ID for entry in payload["results"])


def test_query_coordination_supports_explicit_historical_lookup(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_completed_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "coordination",
            "--initiative-status",
            "completed",
            "--trace-id",
            COMPLETED_TRACE_ID,
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query coordination"
    assert payload["status"] == "ok"
    matched = next(
        entry for entry in payload["results"] if entry["trace_id"] == COMPLETED_TRACE_ID
    )
    assert matched["artifact_status"] == "active"
    assert matched["initiative_status"] == "completed"
    assert "status" not in matched


def test_query_readiness_supports_json_output(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_live_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
    result, payload = run_json_command(
        capsys,
        ["query", "readiness", "--initiative-id", ACTIVE_INITIATIVE_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query readiness"
    assert payload["status"] == "ok"
    assert any(
        entry["initiative_id"] == ACTIVE_INITIATIVE_ID for entry in payload["results"]
    )


def test_query_artifacts_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "artifacts", "--artifact-family", "artifact_index"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query artifacts"
    assert payload["status"] == "ok"
    assert any(
        entry["artifact_id"] == "index.artifacts" for entry in payload["results"]
    )


def test_query_discrepancies_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "discrepancies", "--trace-id", DISCREPANCY_TRACE_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query discrepancies"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 0
    if payload["results"]:
        assert all(entry["trace_id"] == DISCREPANCY_TRACE_ID for entry in payload["results"])


def test_query_projects_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "projects", "--project-id", WATCHTOWER_PROJECT_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query projects"
    assert payload["status"] == "ok"
    assert payload["results"][0]["project_id"] == WATCHTOWER_PROJECT_ID


def test_query_project_context_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["query", "project-context", "--project-slug", "watchtower"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query project-context"
    assert payload["status"] == "ok"
    assert payload["result"]["project_id"] == "project.watchtower"
    assert payload["result"]["pack_context"]["pack_id"] == "pack.plan"
    assert payload["result"]["initiative_root"] == "plan/projects/watchtower/initiatives"
    assert len(payload["result"]["repository_links"]) >= 1


def test_query_initiatives_uses_explicit_artifact_status_field(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_completed_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "initiatives",
            "--trace-id",
            COMPLETED_TRACE_ID,
            "--initiative-status",
            "completed",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    entry = next(
        item for item in payload["results"] if item["trace_id"] == COMPLETED_TRACE_ID
    )
    assert entry["artifact_status"] == "active"
    assert entry["initiative_status"] == "completed"
    assert "status" not in entry


def test_query_initiatives_defaults_to_active_status_when_filterless(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_live_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
    result, payload = run_json_command(capsys, ["query", "initiatives"])

    assert result == 0
    assert payload["command"] == "watchtower-core query initiatives"
    assert payload["status"] == "ok"
    assert payload["default_initiative_status"] == "active"
    assert payload["result_count"] >= 1
    assert all(entry["initiative_status"] == "active" for entry in payload["results"])


def test_query_initiatives_supports_closed_current_phase_history_lookup(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = _build_completed_query_repo(tmp_path)
    monkeypatch.chdir(repo_root / "core/python")
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
    assert any(entry["trace_id"] == COMPLETED_TRACE_ID for entry in payload["results"])
    assert all(entry["current_phase"] == "closed" for entry in payload["results"])


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
    assert payload["results"][0]["artifact_kind"] == "traceability_index"
    assert payload["results"][0]["preferred_command"] == "watchtower-core query trace"


def test_query_trace_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "trace",
            "--trace-id",
            "trace.governed_acceptance_example",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query trace"
    assert payload["status"] == "ok"
    assert payload["result"]["trace_id"] == "trace.governed_acceptance_example"
