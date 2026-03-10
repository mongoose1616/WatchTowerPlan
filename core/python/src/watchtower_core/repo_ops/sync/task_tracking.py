"""Deterministic rebuild helpers for the human-readable task tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
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
        updated_at = max((task.updated_at for task in tasks), default="None")
        content = "\n".join(
            [
                "# Task Tracking",
                "",
                "## Summary",
                (
                    "This document provides the human-readable tracking view for "
                    "local task records under `docs/planning/tasks/`. Rebuild it "
                    "from the governed task files instead of using it as the "
                    "primary task source of truth."
                ),
                "",
                "## Open Tasks",
                _table_for_tasks(open_tasks),
                "",
                "## Closed Tasks",
                _table_for_tasks(closed_tasks),
                "",
                "## Update Rules",
                (
                    "- Treat the task files under `docs/planning/tasks/open/` "
                    "and `docs/planning/tasks/closed/` as the authoritative "
                    "local task source."
                ),
                (
                    "- Rebuild this tracker in the same change set when task "
                    "files are added, removed, moved, or materially updated."
                ),
                (
                    "- Keep the machine-readable companion index at "
                    "[task_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/"
                    "indexes/tasks/task_index.v1.json) aligned with this tracker."
                ),
                "",
                "## References",
                "- [README.md](/home/j/WatchTowerPlan/docs/planning/tasks/README.md)",
                (
                    "- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/governance/task_tracking_standard.md)"
                ),
                (
                    "- [task_md_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/documentation/task_md_standard.md)"
                ),
                (
                    "- [task_index_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/data_contracts/task_index_standard.md)"
                ),
                "",
                "## Updated At",
                f"- `{updated_at}`",
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


def _table_for_tasks(tasks: list[TaskDocument]) -> str:
    lines = [
        "| Task ID | Task Status | Priority | Owner | Trace ID | Path | Summary | Blocked By |",
        "|---|---|---|---|---|---|---|---|",
    ]
    if not tasks:
        lines.append(
            "| `None` | `None` | `None` | `None` | `None` | `None` | "
            "No tasks in this class. | `None` |"
        )
        return "\n".join(lines)

    for task in tasks:
        trace_id = task.trace_id or "None"
        blocked_by = "; ".join(task.list_values("blocked_by")) or "None"
        lines.append(
            "| "
            f"`{task.task_id}` | `{task.task_status}` | `{task.priority}` | "
            f"`{task.owner}` | `{trace_id}` | `{task.relative_path}` | "
            f"{task.summary} | `{blocked_by}` |"
        )
    return "\n".join(lines)
