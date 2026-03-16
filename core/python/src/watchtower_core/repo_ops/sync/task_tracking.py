"""Deterministic rebuild helpers for the human-readable task tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import (
    latest_timestamp,
    markdown_repo_link,
    render_markdown_table,
)
from watchtower_core.repo_ops.task_documents import (
    TERMINAL_TASK_STATUSES,
    TaskDocument,
    iter_task_documents,
)

TASK_TRACKING_DOCUMENT_PATH = "docs/planning/tasks/task_tracking.md"

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
        updated_at = latest_timestamp(tuple(task.updated_at for task in tasks))
        content = "\n".join(
            [
                "# Task Tracking",
                "",
                "## Open Tasks",
                _table_for_tasks(self._repo_root, open_tasks, empty_message="_No open tasks._"),
                "",
                "## Closed Task Summary",
                *_closed_task_summary(closed_tasks),
                "",
                "## Recently Closed Tasks",
                _table_for_tasks(
                    self._repo_root,
                    recent_closed_tasks,
                    empty_message="_No recently closed tasks._",
                ),
                "",
                f"_Updated At: `{updated_at}`_",
                "",
            ]
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


def _table_for_tasks(repo_root: Path, tasks: list[TaskDocument], *, empty_message: str) -> str:
    if not tasks:
        return empty_message

    include_blockers = any(task.list_values("blocked_by") for task in tasks)
    headers = ["Task", "Status", "Priority", "Owner", "Trace ID", "Summary"]
    if include_blockers:
        headers.append("Blocked By")
    rows: list[tuple[str, ...]] = []
    for task in tasks:
        row = [
            markdown_repo_link(
                repo_root,
                task.relative_path,
                label=task.task_id,
            ),
            f"`{task.task_status}`",
            f"`{task.priority}`",
            f"`{task.owner}`",
            f"`{task.trace_id}`" if task.trace_id is not None else "-",
            task.summary,
        ]
        if include_blockers:
            blocked_by = "; ".join(task.list_values("blocked_by")) or "-"
            row.append(blocked_by)
        rows.append(tuple(row))
    return "\n".join(render_markdown_table(tuple(headers), tuple(rows)))


def _closed_task_summary(closed_tasks: list[TaskDocument]) -> tuple[str, ...]:
    if not closed_tasks:
        return ("_No closed tasks._",)

    done_count = sum(task.task_status == "done" for task in closed_tasks)
    cancelled_count = sum(task.task_status == "cancelled" for task in closed_tasks)
    return (
        f"- `done`: {done_count}",
        f"- `cancelled`: {cancelled_count}",
        "",
        "Use `docs/planning/tasks/closed/archive/` for canonical terminal task records, "
        "`watchtower-core query tasks --task-status done --format json` "
        "for completed-task lookup, or "
        "`watchtower-core query tasks --task-status cancelled --format json` "
        "for cancelled-task lookup.",
    )
