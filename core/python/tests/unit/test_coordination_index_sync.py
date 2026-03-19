from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from tests.integration.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_plan_runtime_pack,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.plan_runtime.initiative_packages import InitiativeTaskSpec
from watchtower_core.plan_runtime.plan_workspace import PlanWorkspaceService
from watchtower_core.plan_runtime.query.coordination import (
    CoordinationQueryService,
    CoordinationSearchParams,
)
from watchtower_core.plan_runtime.sync.coordination_index import CoordinationIndexSyncService
from watchtower_core.plan_runtime.task_lifecycle import TaskLifecycleService, TaskUpdateParams

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_control_plane_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    materialize_plan_runtime_pack(repo_root, REPO_ROOT)
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def _task_service(repo_root: Path) -> TaskLifecycleService:
    return TaskLifecycleService(ControlPlaneLoader(repo_root))


def _sync_plan_workspace(repo_root: Path) -> None:
    PlanWorkspaceService(ControlPlaneLoader(repo_root)).sync(write=True)


def _write_completed_initiative_state(
    repo_root: Path,
    *,
    initiative_slug: str,
    closed_at: str,
    closure_reason: str,
) -> None:
    state_path = repo_root / "plan" / "initiatives" / initiative_slug / ".wt" / "initiative.json"
    document = json.loads(state_path.read_text(encoding="utf-8"))
    document["status"] = "completed"
    document["lifecycle_stage"] = "completed"
    document["closed_at"] = closed_at
    document["closure_reason"] = closure_reason
    document["updated_at"] = closed_at
    state_path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def test_coordination_index_reports_active_work_when_actionable_tasks_exist(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_active",
        title="Example Active Initiative",
        summary="Exercises active coordination work selection.",
        task_specs=(
            InitiativeTaskSpec(
                title="Do the active work",
                summary="Carries the active work item.",
                slug="execution",
                task_id="task.example_active.execution.001",
                priority="high",
            ),
        ),
        approve=True,
    )

    _task_service(repo_root).update(
        TaskUpdateParams(
            task_id="task.example_active.execution.001",
            task_status="ready",
        ),
        write=True,
    )

    document = CoordinationIndexSyncService(ControlPlaneLoader(repo_root)).build_document()

    assert document["id"] == "index.coordination"
    assert document["coordination_mode"] == "active_work"
    assert document["active_initiative_count"] == 1
    assert document["actionable_task_count"] == 1
    assert document["recommended_surface_path"] == "plan/initiatives/example_active/plan.md"
    assert len(document["entries"]) == 1
    assert document["entries"][0]["trace_id"] == "trace.example_active"
    assert all(entry["initiative_status"] == "active" for entry in document["entries"])
    assert document["actionable_tasks"][0]["doc_path"] == (
        "plan/initiatives/example_active/.wt/tasks/execution/task.json"
    )
    assert isinstance(document["recent_closed_initiatives"], list)


def test_coordination_index_reports_ready_for_bootstrap_when_no_active_initiatives(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)

    document = CoordinationIndexSyncService(ControlPlaneLoader(repo_root)).build_document()

    assert document["coordination_mode"] == "ready_for_bootstrap"
    assert document["active_initiative_count"] == 0
    assert document["actionable_task_count"] == 0
    assert document["recommended_surface_path"] == "plan/plan_overview.md"
    assert document["entries"] == []
    assert document["recent_closed_initiatives"] == []


def test_coordination_index_reports_blocked_work_when_execution_has_only_blocked_tasks(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_blocked",
        title="Example Blocked Initiative",
        summary="Exercises blocked coordination work selection.",
        task_specs=(
            InitiativeTaskSpec(
                title="Wait on dependency resolution",
                summary="Blocks until a prerequisite resolves.",
                slug="execution",
                task_id="task.example_blocked.execution.001",
                priority="high",
            ),
        ),
        approve=True,
    )

    _task_service(repo_root).update(
        TaskUpdateParams(
            task_id="task.example_blocked.execution.001",
            task_status="blocked",
        ),
        write=True,
    )

    document = CoordinationIndexSyncService(ControlPlaneLoader(repo_root)).build_document()

    assert document["coordination_mode"] == "blocked_work"
    assert document["active_initiative_count"] == 1
    assert document["actionable_task_count"] == 0
    assert document["blocked_task_count"] == 1
    assert document["recommended_surface_path"] == "plan/initiatives/example_blocked/plan.md"
    assert len(document["entries"]) == 1
    assert all(entry["initiative_status"] == "active" for entry in document["entries"])


def test_coordination_query_uses_initiative_index_for_explicit_historical_lookup(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_active",
        title="Example Active Initiative",
        summary="Keeps one active initiative in the coordination slice.",
        task_specs=(
            InitiativeTaskSpec(
                title="Do the active work",
                summary="Carries the active work item.",
                slug="execution",
                task_id="task.example_active.execution.001",
                priority="high",
            ),
        ),
        approve=True,
    )
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_completed",
        title="Example Completed Initiative",
        summary="Provides one closed initiative for historical lookup coverage.",
        task_specs=(
            InitiativeTaskSpec(
                title="Finish the completed work",
                summary="Carries the historical work item.",
                slug="closeout",
                task_id="task.example_completed.closeout.001",
                priority="high",
            ),
        ),
        approve=True,
    )

    _task_service(repo_root).update(
        TaskUpdateParams(
            task_id="task.example_active.execution.001",
            task_status="ready",
        ),
        write=True,
    )
    _task_service(repo_root).update(
        TaskUpdateParams(
            task_id="task.example_completed.closeout.001",
            task_status="completed",
        ),
        write=True,
    )
    _write_completed_initiative_state(
        repo_root,
        initiative_slug="example_completed",
        closed_at="2026-03-10T20:00:00Z",
        closure_reason="Closed for historical lookup coverage.",
    )
    _sync_plan_workspace(repo_root)

    result = CoordinationQueryService(ControlPlaneLoader(repo_root)).search(
        CoordinationSearchParams(
            initiative_status="completed",
            trace_id="trace.example_completed",
        )
    )

    assert len(result.index.entries) == 1
    assert result.index.entries[0].trace_id == "trace.example_active"
    assert all(entry.initiative_status == "active" for entry in result.index.entries)
    assert len(result.entries) == 1
    assert result.entries[0].trace_id == "trace.example_completed"
    assert result.entries[0].initiative_status == "completed"
