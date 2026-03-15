"""Private helpers for selecting and summarizing planning projection tasks."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.models import InitiativeActiveTaskSummary, TaskIndexEntry

TERMINAL_TASK_STATUSES = {"done", "cancelled"}
TASK_STATUS_ORDER = {
    "ready": 0,
    "in_progress": 1,
    "in_review": 2,
    "backlog": 3,
    "blocked": 4,
}
PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


@dataclass(frozen=True, slots=True)
class TracePlanningTaskSelection:
    """Derived task-selection data reused by planning projections."""

    active_owners: tuple[str, ...]
    primary_owner: str | None
    blocked_task_count: int
    active_task_ids: tuple[str, ...]
    active_task_summaries: tuple[InitiativeActiveTaskSummary, ...]
    blocked_by_task_ids: tuple[str, ...]


def build_trace_planning_task_selection(
    active_tasks: tuple[TaskIndexEntry, ...],
    task_lookup: dict[str, TaskIndexEntry],
) -> TracePlanningTaskSelection:
    """Derive the shared active-task selection view for one trace."""

    active_owners = tuple(sorted({entry.owner for entry in active_tasks}))
    primary_owner = active_owners[0] if len(active_owners) == 1 else None
    blocked_by_task_ids = tuple(
        sorted(
            {
                task_id
                for entry in active_tasks
                for task_id in (
                    *entry.blocked_by,
                    *_unresolved_dependency_ids(entry, task_lookup),
                )
            }
        )
    )
    blocked_task_count = sum(1 for entry in active_tasks if _task_is_blocked(entry, task_lookup))
    active_task_summaries = tuple(
        InitiativeActiveTaskSummary.from_document(item)
        for item in _build_active_task_summaries(active_tasks, task_lookup)
    )
    return TracePlanningTaskSelection(
        active_owners=active_owners,
        primary_owner=primary_owner,
        blocked_task_count=blocked_task_count,
        active_task_ids=tuple(entry.task_id for entry in active_tasks),
        active_task_summaries=active_task_summaries,
        blocked_by_task_ids=blocked_by_task_ids,
    )


def _build_active_task_summaries(
    active_tasks: tuple[TaskIndexEntry, ...],
    task_lookup: dict[str, TaskIndexEntry],
) -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []
    for entry in sorted(
        active_tasks,
        key=lambda item: _coordination_task_sort_key(item, task_lookup),
    ):
        summary: dict[str, object] = {
            "task_id": entry.task_id,
            "title": entry.title,
            "task_status": entry.task_status,
            "priority": entry.priority,
            "owner": entry.owner,
            "doc_path": entry.doc_path,
            "is_actionable": _task_is_actionable(entry, task_lookup),
        }
        if entry.blocked_by:
            summary["blocked_by"] = list(entry.blocked_by)
        if entry.depends_on:
            summary["depends_on"] = list(entry.depends_on)
        summaries.append(summary)
    return summaries


def _select_coordination_task(
    active_tasks: tuple[TaskIndexEntry, ...],
    task_lookup: dict[str, TaskIndexEntry],
) -> TaskIndexEntry | None:
    actionable_tasks = [
        entry for entry in active_tasks if _task_is_actionable(entry, task_lookup)
    ]
    if actionable_tasks:
        return sorted(
            actionable_tasks,
            key=lambda item: _coordination_task_sort_key(item, task_lookup),
        )[0]
    if not active_tasks:
        return None
    return sorted(
        active_tasks,
        key=lambda item: _blocked_task_sort_key(item, task_lookup),
    )[0]


def _coordination_task_sort_key(
    entry: TaskIndexEntry,
    task_lookup: dict[str, TaskIndexEntry],
) -> tuple[int, int, int, str]:
    return (
        0 if _task_is_actionable(entry, task_lookup) else 1,
        TASK_STATUS_ORDER.get(entry.task_status, 99),
        PRIORITY_ORDER.get(entry.priority, 99),
        entry.task_id,
    )


def _blocked_task_sort_key(
    entry: TaskIndexEntry,
    task_lookup: dict[str, TaskIndexEntry],
) -> tuple[int, int, int, str]:
    return (
        0 if _task_is_blocked(entry, task_lookup) else 1,
        PRIORITY_ORDER.get(entry.priority, 99),
        TASK_STATUS_ORDER.get(entry.task_status, 99),
        entry.task_id,
    )


def _task_is_actionable(
    entry: TaskIndexEntry,
    task_lookup: dict[str, TaskIndexEntry],
) -> bool:
    return not _task_is_blocked(entry, task_lookup)


def _task_is_blocked(
    entry: TaskIndexEntry,
    task_lookup: dict[str, TaskIndexEntry],
) -> bool:
    return (
        entry.task_status == "blocked"
        or bool(entry.blocked_by)
        or bool(_unresolved_dependency_ids(entry, task_lookup))
    )


def _unresolved_dependency_ids(
    entry: TaskIndexEntry,
    task_lookup: dict[str, TaskIndexEntry],
) -> tuple[str, ...]:
    unresolved: list[str] = []
    for dependency_id in entry.depends_on:
        dependency = task_lookup.get(dependency_id)
        if dependency is None or dependency.task_status not in TERMINAL_TASK_STATUSES:
            unresolved.append(dependency_id)
    return tuple(unresolved)
