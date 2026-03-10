from __future__ import annotations

from pathlib import Path
from shutil import copytree
from textwrap import dedent

import pytest

from watchtower_core.closeout import InitiativeCloseoutService
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query import InitiativeQueryService, TaskQueryService, TaskSearchParams
from watchtower_core.sync.github_tasks import GitHubTaskSyncParams, GitHubTaskSyncService
from watchtower_core.sync.initiative_index import InitiativeIndexSyncService
from watchtower_core.sync.initiative_tracking import InitiativeTrackingSyncService
from watchtower_core.sync.task_index import TaskIndexSyncService
from watchtower_core.sync.task_tracking import TaskTrackingSyncService
from watchtower_core.sync.traceability import TraceabilityIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    copytree(REPO_ROOT / "docs", repo_root / "docs")
    return repo_root


def _write_task(
    repo_root: Path,
    *,
    relative_path: str,
    task_id: str,
    trace_id: str,
    title: str,
    summary: str,
    task_status: str,
    priority: str,
    updated_at: str,
    owner: str = "repository_maintainer",
    task_kind: str = "feature",
    applies_to: tuple[str, ...] = ("core/python/",),
    related_ids: tuple[str, ...] = ("prd.core_python_foundation",),
    depends_on: tuple[str, ...] = (),
    blocked_by: tuple[str, ...] = (),
) -> None:
    path = repo_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)

    front_matter_lines = [
        "---",
        f'id: "{task_id}"',
        f'trace_id: "{trace_id}"',
        f'title: "{title}"',
        f'summary: "{summary}"',
        'type: "task"',
        'status: "active"',
        f'task_status: "{task_status}"',
        f'task_kind: "{task_kind}"',
        f'priority: "{priority}"',
        f'owner: "{owner}"',
        f'updated_at: "{updated_at}"',
        'audience: "shared"',
        'authority: "authoritative"',
        "applies_to:",
        *[f'  - "{value}"' for value in applies_to],
        "related_ids:",
        *[f'  - "{value}"' for value in related_ids],
    ]
    if depends_on:
        front_matter_lines.extend(
            ["depends_on:", *[f'  - "{value}"' for value in depends_on]]
        )
    if blocked_by:
        front_matter_lines.extend(
            ["blocked_by:", *[f'  - "{value}"' for value in blocked_by]]
        )
    front_matter_lines.append("---")

    body = dedent(
        f"""\
        # {title}

        ## Summary
        {summary}

        ## Context
        - Added during end-to-end task workflow validation.
        - Exercises how task state feeds the helper-runtime surfaces.

        ## Scope
        - Publish a governed task record with explicit status and ownership.
        - Let the task feed task, traceability, and initiative projections.

        ## Done When
        - The task is visible through the rebuilt helper surfaces.
        - The task can influence initiative coordination behavior deterministically.

        ## Links
        - prd.core_python_foundation

        ## Updated At
        - `{updated_at}`
        """
    )
    path.write_text("\n".join(front_matter_lines) + "\n\n" + body, encoding="utf-8")


def _rebuild_task_management_surfaces(repo_root: Path) -> None:
    loader = ControlPlaneLoader(repo_root)

    task_index_service = TaskIndexSyncService(loader)
    task_index_service.write_document(task_index_service.build_document())

    task_tracking_service = TaskTrackingSyncService(loader)
    task_tracking_service.write_document(task_tracking_service.build_document())

    traceability_service = TraceabilityIndexSyncService(loader)
    traceability_service.write_document(traceability_service.build_document())

    initiative_index_service = InitiativeIndexSyncService(loader)
    initiative_index_service.write_document(initiative_index_service.build_document())

    initiative_tracking_service = InitiativeTrackingSyncService(loader)
    initiative_tracking_service.write_document(initiative_tracking_service.build_document())


def test_task_management_flow_updates_queries_trackers_and_initiative_views(
    tmp_path: Path,
) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    ready_task_id = "task.core_python_foundation.execution.001"
    blocked_task_id = "task.core_python_foundation.validation.001"

    _write_task(
        repo_root,
        relative_path="docs/planning/tasks/open/core_python_execution.md",
        task_id=ready_task_id,
        trace_id="trace.core_python_foundation",
        title="Execute core Python foundation work",
        summary="Executes the next bounded slice of the core Python foundation initiative.",
        task_status="ready",
        priority="high",
        updated_at="2026-03-10T12:00:00Z",
    )
    _write_task(
        repo_root,
        relative_path="docs/planning/tasks/open/core_python_validation.md",
        task_id=blocked_task_id,
        trace_id="trace.core_python_foundation",
        title="Validate the core Python foundation slice",
        summary="Validates the current core Python foundation slice after execution work lands.",
        task_status="blocked",
        priority="medium",
        updated_at="2026-03-10T12:05:00Z",
        depends_on=(ready_task_id,),
        blocked_by=(ready_task_id,),
    )

    _rebuild_task_management_surfaces(repo_root)

    loader = ControlPlaneLoader(repo_root)
    task_query = TaskQueryService(loader)
    task_entries = task_query.search(
        TaskSearchParams(trace_id="trace.core_python_foundation")
    )
    assert {entry.task_id for entry in task_entries} >= {ready_task_id, blocked_task_id}

    blocked_entries = task_query.search(
        TaskSearchParams(trace_id="trace.core_python_foundation", blocked_only=True)
    )
    assert [entry.task_id for entry in blocked_entries] == [blocked_task_id]

    reverse_dependencies = task_query.reverse_dependencies(ready_task_id)
    assert [entry.task_id for entry in reverse_dependencies] == [blocked_task_id]

    trace_entry = loader.load_traceability_index().get("trace.core_python_foundation")
    assert {ready_task_id, blocked_task_id}.issubset(set(trace_entry.task_ids))

    initiative_entry = InitiativeQueryService(loader).get("trace.core_python_foundation")
    assert initiative_entry.current_phase == "execution"
    assert initiative_entry.open_task_count == 2
    assert initiative_entry.blocked_task_count == 1
    assert initiative_entry.primary_owner == "repository_maintainer"
    assert {ready_task_id, blocked_task_id}.issubset(set(initiative_entry.active_task_ids))
    assert "Resolve blockers" in initiative_entry.next_action

    task_tracking = (repo_root / "docs/planning/tasks/task_tracking.md").read_text(
        encoding="utf-8"
    )
    assert ready_task_id in task_tracking
    assert blocked_task_id in task_tracking

    initiative_tracking = (
        repo_root / "docs/planning/initiatives/initiative_tracking.md"
    ).read_text(encoding="utf-8")
    assert "trace.core_python_foundation" in initiative_tracking
    assert "blocked=1" in initiative_tracking

    github_result = GitHubTaskSyncService(loader).sync(
        GitHubTaskSyncParams(
            repository="owner/repo",
            trace_id="trace.core_python_foundation",
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


def test_initiative_closeout_fails_closed_until_task_state_is_terminal(
    tmp_path: Path,
) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    task_id = "task.core_python_foundation.closeout.001"
    open_relative_path = "docs/planning/tasks/open/core_python_closeout.md"
    closed_relative_path = "docs/planning/tasks/closed/core_python_closeout.md"

    _write_task(
        repo_root,
        relative_path=open_relative_path,
        task_id=task_id,
        trace_id="trace.core_python_foundation",
        title="Close out the core Python foundation initiative",
        summary="Closes out the core Python foundation initiative after the final execution slice.",
        task_status="ready",
        priority="high",
        updated_at="2026-03-10T12:10:00Z",
    )

    unsynced_loader = ControlPlaneLoader(repo_root)
    task_index_service = TaskIndexSyncService(unsynced_loader)
    task_index_service.write_document(task_index_service.build_document())
    task_tracking_service = TaskTrackingSyncService(unsynced_loader)
    task_tracking_service.write_document(task_tracking_service.build_document())

    with pytest.raises(ValueError, match=task_id):
        InitiativeCloseoutService(ControlPlaneLoader(repo_root)).close(
            trace_id="trace.core_python_foundation",
            initiative_status="completed",
            closure_reason="Delivered and validated",
            write=False,
        )

    _rebuild_task_management_surfaces(repo_root)

    with pytest.raises(ValueError, match=task_id):
        InitiativeCloseoutService(ControlPlaneLoader(repo_root)).close(
            trace_id="trace.core_python_foundation",
            initiative_status="completed",
            closure_reason="Delivered and validated",
            write=False,
        )

    (repo_root / open_relative_path).unlink()
    _write_task(
        repo_root,
        relative_path=closed_relative_path,
        task_id=task_id,
        trace_id="trace.core_python_foundation",
        title="Close out the core Python foundation initiative",
        summary="Closes out the core Python foundation initiative after the final execution slice.",
        task_status="done",
        priority="high",
        updated_at="2026-03-10T12:20:00Z",
    )

    _rebuild_task_management_surfaces(repo_root)

    result = InitiativeCloseoutService(ControlPlaneLoader(repo_root)).close(
        trace_id="trace.core_python_foundation",
        initiative_status="completed",
        closure_reason="Delivered and validated",
        closed_at="2026-03-10T12:30:00Z",
        write=True,
    )
    assert result.wrote is True
    assert result.open_task_ids == ()
    assert result.traceability_output_path is not None
    assert result.initiative_index_output_path is not None
    assert result.initiative_tracking_output_path is not None

    loader = ControlPlaneLoader(repo_root)
    trace_entry = loader.load_traceability_index().get("trace.core_python_foundation")
    assert trace_entry.initiative_status == "completed"
    assert trace_entry.closed_at == "2026-03-10T12:30:00Z"
    assert trace_entry.closure_reason == "Delivered and validated"

    initiative_entry = loader.load_initiative_index().get("trace.core_python_foundation")
    assert initiative_entry.initiative_status == "completed"
    assert initiative_entry.current_phase == "closed"
    assert initiative_entry.open_task_count == 0
    assert initiative_entry.closed_at == "2026-03-10T12:30:00Z"

    initiative_tracking = (
        repo_root / "docs/planning/initiatives/initiative_tracking.md"
    ).read_text(encoding="utf-8")
    assert "| `trace.core_python_foundation` | `completed` |" in initiative_tracking
