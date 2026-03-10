from __future__ import annotations

from watchtower_core.control_plane.models import TaskIndexEntry
from watchtower_core.repo_ops.sync.initiative_index import (
    _build_active_task_summaries,
    _select_coordination_task,
    _task_is_blocked,
)


def _task(
    *,
    task_id: str,
    title: str,
    doc_path: str,
    task_status: str = "ready",
    priority: str = "high",
    depends_on: tuple[str, ...] = (),
    blocked_by: tuple[str, ...] = (),
) -> TaskIndexEntry:
    return TaskIndexEntry(
        task_id=task_id,
        title=title,
        summary=title,
        status="active",
        task_status=task_status,
        task_kind="feature",
        priority=priority,
        owner="repository_maintainer",
        doc_path=doc_path,
        updated_at="2026-03-10T18:10:36Z",
        trace_id="trace.preimplementation_repo_review_and_hardening",
        depends_on=depends_on,
        blocked_by=blocked_by,
    )


def test_select_coordination_task_prefers_actionable_dependency_root() -> None:
    machine_coordination = _task(
        task_id="task.preimplementation_repo_review_and_hardening.machine_coordination.001",
        title="Strengthen the machine coordination start-here surface",
        doc_path="docs/planning/tasks/open/preimplementation_machine_coordination.md",
    )
    core_modularity = _task(
        task_id="task.preimplementation_repo_review_and_hardening.core_modularity.001",
        title="Split core monoliths and add supplemental schema loading",
        doc_path="docs/planning/tasks/open/preimplementation_core_modularity.md",
        depends_on=(machine_coordination.task_id,),
    )
    active_tasks = (core_modularity, machine_coordination)
    task_lookup = {task.task_id: task for task in active_tasks}

    chosen = _select_coordination_task(active_tasks, task_lookup)

    assert chosen is not None
    assert chosen.task_id == machine_coordination.task_id


def test_active_task_summaries_mark_dependency_blocked_tasks() -> None:
    blocker = _task(
        task_id="task.example.blocker.001",
        title="Finish the prerequisite task",
        doc_path="docs/planning/tasks/open/example_blocker.md",
    )
    blocked = _task(
        task_id="task.example.blocked.001",
        title="Land the dependent task",
        doc_path="docs/planning/tasks/open/example_blocked.md",
        depends_on=(blocker.task_id,),
    )
    active_tasks = (blocked, blocker)
    task_lookup = {task.task_id: task for task in active_tasks}

    summaries = _build_active_task_summaries(active_tasks, task_lookup)

    blocker_summary = next(item for item in summaries if item["task_id"] == blocker.task_id)
    blocked_summary = next(item for item in summaries if item["task_id"] == blocked.task_id)

    assert blocker_summary["is_actionable"] is True
    assert blocked_summary["is_actionable"] is False
    assert blocked_summary["depends_on"] == [blocker.task_id]
    assert _task_is_blocked(blocked, task_lookup) is True
