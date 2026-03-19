"""Deterministic rebuild helpers for the human-readable task tracker."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.repo_ops.sync.tracking_common import (
    RenderedTrackingSyncService,
    latest_updated_at_for_entries,
)
from watchtower_core.repo_ops.plan_task_state import PlanTaskStateDocument, iter_task_documents

TASK_TRACKING_DOCUMENT_PATH = "docs/planning/tasks/task_tracking.md"
TASK_TRACKING_SURFACE_ID = "rendered.task_tracking"
TERMINAL_TASK_STATUSES = {"completed", "cancelled"}

_STATUS_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}
_TASK_STATUS_ORDER = {
    "in_progress": 0,
    "blocked": 1,
    "in_review": 2,
    "ready": 3,
    "planned": 4,
    "completed": 5,
    "cancelled": 6,
}


@dataclass(frozen=True, slots=True)
class TaskTrackingBuildResult:
    """Generated task-tracking document plus task counts."""

    content: str
    task_count: int
    open_count: int
    closed_count: int


class TaskTrackingSyncService(RenderedTrackingSyncService):
    """Build and write the human-readable task tracker from live task state."""

    DOCUMENT_PATH = TASK_TRACKING_DOCUMENT_PATH
    SURFACE_ID = TASK_TRACKING_SURFACE_ID

    def build_document(self) -> TaskTrackingBuildResult:
        tasks = iter_task_documents(self._loader)
        open_tasks = sorted(
            (task for task in tasks if task.task_status not in TERMINAL_TASK_STATUSES),
            key=_sort_key,
        )
        closed_tasks = sorted(
            (task for task in tasks if task.task_status in TERMINAL_TASK_STATUSES),
            key=_sort_key,
        )
        content = self._render_tracking_document(
            {
                "open_tasks": tuple(_task_row(task) for task in open_tasks),
                "closed_task_counts": tuple(
                    {"label": label, "count": count}
                    for label, count in (
                        (
                            "completed",
                            sum(task.task_status == "completed" for task in closed_tasks),
                        ),
                        (
                            "cancelled",
                            sum(task.task_status == "cancelled" for task in closed_tasks),
                        ),
                    )
                    if count > 0
                ),
                "closed_tasks": tuple(_task_row(task) for task in closed_tasks),
                "include_blocked_by_column": any(
                    task.blocked_by for task in (*open_tasks, *closed_tasks)
                ),
                "updated_at": latest_updated_at_for_entries(tasks),
            },
        )
        return TaskTrackingBuildResult(
            content=content,
            task_count=len(tasks),
            open_count=len(open_tasks),
            closed_count=len(closed_tasks),
        )


def _sort_key(task: PlanTaskStateDocument) -> tuple[int, int, str]:
    return (
        _TASK_STATUS_ORDER.get(task.task_status, 99),
        _STATUS_ORDER.get(task.priority, 99),
        task.task_id,
    )


def _task_row(task: PlanTaskStateDocument) -> dict[str, str | None]:
    return {
        "task_id": task.task_id,
        "doc_path": task.relative_path,
        "task_status": task.task_status,
        "priority": task.priority,
        "owner": task.owner,
        "trace_id": task.trace_id,
        "summary": task.summary,
        "blocked_by": "; ".join(task.blocked_by) or "-",
    }
