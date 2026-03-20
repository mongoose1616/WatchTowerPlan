from __future__ import annotations

from pathlib import Path
from shutil import copytree

import pytest

from tests.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_acceptance_and_evidence_paths,
    materialize_governed_applies_to_targets,
    materialize_plan_pack,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.initiative_packages import InitiativePackageService
from watchtower_plan.query import (
    CoordinationSearchParams,
    CoordinationQueryService,
    InitiativeQueryService,
    TaskQueryService,
    TaskSearchParams,
)
from watchtower_plan.sync.github_tasks import GitHubTaskSyncParams, GitHubTaskSyncService
from watchtower_plan.task_lifecycle import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskUpdateParams,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "core" / "docs", repo_root / "core" / "docs")
    (repo_root / "core" / "python").mkdir(parents=True)
    materialize_plan_pack(repo_root, REPO_ROOT)
    materialize_governed_applies_to_targets(repo_root)
    materialize_acceptance_and_evidence_paths(repo_root, REPO_ROOT)
    return repo_root


def test_task_management_flow_updates_queries_trackers_and_initiative_views(
    tmp_path: Path,
) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.task_workflow_e2e_foundation"
    ready_task_id = "task.task_workflow_e2e_foundation.execute_foundation_work"
    blocked_task_id = "task.task_workflow_e2e_foundation.validate_foundation_work"

    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title="Task Workflow E2E Foundation",
        summary="Bootstraps the live initiative package for end-to-end task workflow coverage.",
        approve=True,
    )
    lifecycle = TaskLifecycleService(ControlPlaneLoader(repo_root))
    lifecycle.create(
        TaskCreateParams(
            task_id=ready_task_id,
            trace_id=trace_id,
            title="Execute foundation work",
            summary="Executes the next bounded slice of the live foundation initiative.",
            task_status="ready",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Publish the next live foundation slice.",),
            done_when_items=("The execution slice is ready for validation.",),
            related_ids=("initiative.task_workflow_e2e_foundation",),
        ),
        write=True,
    )
    lifecycle.create(
        TaskCreateParams(
            task_id=blocked_task_id,
            trace_id=trace_id,
            title="Validate foundation work",
            summary="Validates the current foundation slice after execution work lands.",
            task_status="blocked",
            task_kind="validation",
            priority="medium",
            owner="repository_maintainer",
            scope_items=("Validate the live execution slice.",),
            done_when_items=("The validation slice is unblocked and completed.",),
            related_ids=("initiative.task_workflow_e2e_foundation",),
            depends_on=(ready_task_id,),
            blocked_by=(ready_task_id,),
        ),
        write=True,
    )

    loader = ControlPlaneLoader(repo_root)
    task_query = TaskQueryService(loader)
    task_entries = task_query.search(TaskSearchParams(trace_id=trace_id))
    assert {entry.task_id for entry in task_entries} >= {ready_task_id, blocked_task_id}

    blocked_entries = task_query.search(TaskSearchParams(trace_id=trace_id, blocked_only=True))
    assert [entry.task_id for entry in blocked_entries] == [blocked_task_id]

    reverse_dependencies = task_query.reverse_dependencies(ready_task_id)
    assert [entry.task_id for entry in reverse_dependencies] == [blocked_task_id]

    trace_entry = loader.load_traceability_index().get(trace_id)
    assert {ready_task_id, blocked_task_id}.issubset(set(trace_entry.task_ids))

    initiative_entry = InitiativeQueryService(loader).get(trace_id)
    assert initiative_entry.blocked_task_count == 1
    assert initiative_entry.primary_owner == "repository_maintainer"
    assert {ready_task_id, blocked_task_id}.issubset(set(initiative_entry.active_task_ids))
    assert "ready task" in initiative_entry.next_action

    lifecycle.update(
        TaskUpdateParams(task_id=ready_task_id, task_status="in_progress"),
        write=True,
    )

    refreshed_loader = ControlPlaneLoader(repo_root)
    refreshed_initiative_entry = InitiativeQueryService(refreshed_loader).get(trace_id)
    assert (
        refreshed_initiative_entry.next_action
        == "Advance the current in-progress task set and keep initiative-local task state current."
    )

    coordination_result = CoordinationQueryService(refreshed_loader).search(
        CoordinationSearchParams()
    )
    assert coordination_result.index.actionable_task_count == 0
    assert (
        coordination_result.index.recommended_next_action
        == "Advance the current in-progress task set and keep initiative-local task state current."
    )

    task_tracking = (repo_root / "plan/tracking/task_tracking.md").read_text(
        encoding="utf-8"
    )
    assert ready_task_id in task_tracking
    assert blocked_task_id in task_tracking
    assert "plan/initiatives/task_workflow_e2e_foundation/.wt/tasks/" in task_tracking

    initiative_tracking = (
        repo_root / "plan/tracking/initiative_tracking.md"
    ).read_text(encoding="utf-8")
    assert trace_id in initiative_tracking

    github_result = GitHubTaskSyncService(loader).sync(
        GitHubTaskSyncParams(
            repository="owner/repo",
            trace_id=trace_id,
            blocked_only=True,
        ),
        write=False,
    )
    assert github_result.wrote is False
    assert github_result.synced_task_count == 0
    assert len(github_result.records) == 1
    record = github_result.records[0]
    assert record.task_id == blocked_task_id
    assert record.success is True
    assert record.issue_action == "create_issue"
    assert "status:blocked" in record.labels
    assert "blocked" in record.labels


def test_packwide_initiative_closeout_requires_terminal_live_tasks(
    tmp_path: Path,
) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.task_workflow_e2e_closeout"
    initiative_slug = "task_workflow_e2e_closeout"
    seed_task_id = f"task.{initiative_slug}.seed_bootstrap"
    closeout_task_id = f"task.{initiative_slug}.closeout_validation"

    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title="Task Workflow E2E Closeout",
        summary="Bootstraps the live initiative package for closeout validation.",
        approve=True,
    )
    loader = ControlPlaneLoader(repo_root)
    lifecycle = TaskLifecycleService(loader)
    lifecycle.create(
        TaskCreateParams(
            task_id=closeout_task_id,
            trace_id=trace_id,
            title="Validate closeout readiness",
            summary="Tracks the final validation slice before terminal initiative closeout.",
            task_status="ready",
            task_kind="validation",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Validate the final initiative slice before closeout.",),
            done_when_items=("Every initiative-local task is terminal.",),
        ),
        write=True,
    )

    service = InitiativePackageService(loader)
    with pytest.raises(ValueError, match="completed or cancelled"):
        service.close_packwide(
            initiative_slug,
            initiative_status="completed",
            closure_reason="Delivered and validated the bounded end-to-end workflow slice.",
            write=False,
        )

    lifecycle.update(
        TaskUpdateParams(task_id=seed_task_id, task_status="completed"),
        write=True,
    )
    lifecycle.update(
        TaskUpdateParams(task_id=closeout_task_id, task_status="completed"),
        write=True,
    )

    result = service.close_packwide(
        initiative_slug,
        initiative_status="completed",
        closure_reason="Delivered and validated the bounded end-to-end workflow slice.",
        closed_at="2026-03-18T18:00:00Z",
        write=True,
    )

    assert result.wrote is True
    assert result.initiative_status == "completed"

    refreshed_loader = ControlPlaneLoader(repo_root)
    initiative_entry = InitiativeQueryService(refreshed_loader).get(trace_id)
    assert initiative_entry.initiative_status == "completed"
    assert initiative_entry.open_task_count == 0
    assert initiative_entry.current_phase == "closed"
    assert initiative_entry.next_action == "No further default action. Initiative is completed."
    assert initiative_entry.next_surface_path == f"plan/initiatives/{initiative_slug}/summary.md"

    task_entries = TaskQueryService(refreshed_loader).search(TaskSearchParams(trace_id=trace_id))
    task_status_by_id = {entry.task_id: entry.task_status for entry in task_entries}
    assert task_status_by_id[seed_task_id] == "completed"
    assert task_status_by_id[closeout_task_id] == "completed"
