"""Deterministic rebuild helpers for the human-readable task tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import render_rendered_surface
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import latest_timestamp
from watchtower_core.repo_ops.task_documents import (
    TERMINAL_TASK_STATUSES,
    TaskDocument,
    iter_task_documents,
)

TASK_TRACKING_DOCUMENT_PATH = "docs/planning/tasks/task_tracking.md"
TASK_TRACKING_SURFACE_ID = "rendered.task_tracking"

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
    "backlog": 4,
    "done": 5,
    "cancelled": 6,
}


@dataclass(frozen=True, slots=True)
class TaskTrackingBuildResult:
    """Generated task-tracking document plus task counts."""

    content: str
    task_count: int
    open_count: int
    closed_count: int


class TaskTrackingSyncService:
    """Build and write the human-readable task tracker from task documents."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> TaskTrackingSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

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
        recent_closed_tasks = sorted(
            closed_tasks,
            key=lambda task: (task.updated_at, task.task_id),
            reverse=True,
        )[:10]
        surface = self._loader.load_rendered_surface_registry().get(
            TASK_TRACKING_SURFACE_ID
        )
        content = render_rendered_surface(
            surface,
            {
                "open_tasks": tuple(_task_row(task) for task in open_tasks),
                "closed_task_counts": tuple(
                    {"label": label, "count": count}
                    for label, count in (
                        ("done", sum(task.task_status == "done" for task in closed_tasks)),
                        (
                            "cancelled",
                            sum(task.task_status == "cancelled" for task in closed_tasks),
                        ),
                    )
                    if count > 0
                ),
                "closed_task_notes": (
                    (
                        "Use `docs/planning/tasks/closed/archive/` for canonical "
                        "terminal task records, "
                        "`watchtower-core query tasks --task-status done --format json` "
                        "for completed-task lookup, or "
                        "`watchtower-core query tasks --task-status cancelled --format json` "
                        "for cancelled-task lookup.",
                    )
                    if closed_tasks
                    else ()
                ),
                "recently_closed_tasks": tuple(_task_row(task) for task in recent_closed_tasks),
                "include_blocked_by_column": any(
                    task.list_values("blocked_by") for task in (*open_tasks, *recent_closed_tasks)
                ),
                "updated_at": latest_timestamp(tuple(task.updated_at for task in tasks)),
            },
        )
        return TaskTrackingBuildResult(
            content=content,
            task_count=len(tasks),
            open_count=len(open_tasks),
            closed_count=len(closed_tasks),
        )

    def write_document(
        self,
        result: TaskTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write the generated task tracker to disk."""
        target = destination or (self._repo_root / TASK_TRACKING_DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target


def _sort_key(task: TaskDocument) -> tuple[int, int, str]:
    return (
        _TASK_STATUS_ORDER.get(task.task_status, 99),
        _STATUS_ORDER.get(task.priority, 99),
        task.task_id,
    )


def _task_row(task: TaskDocument) -> dict[str, str | None]:
    return {
        "task_id": task.task_id,
        "doc_path": task.relative_path,
        "task_status": task.task_status,
        "priority": task.priority,
        "owner": task.owner,
        "trace_id": task.trace_id,
        "summary": task.summary,
        "blocked_by": "; ".join(task.list_values("blocked_by")) or "-",
    }
