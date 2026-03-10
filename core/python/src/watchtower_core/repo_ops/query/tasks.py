"""Repo-specific query helpers for local task records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import TaskIndexEntry
from watchtower_core.repo_ops.query.common import query_score


@dataclass(frozen=True, slots=True)
class TaskSearchParams:
    """Filter and ranking inputs for task lookup."""

    query: str | None = None
    task_ids: tuple[str, ...] = ()
    trace_id: str | None = None
    task_status: str | None = None
    priority: str | None = None
    owner: str | None = None
    task_kind: str | None = None
    blocked_only: bool = False
    blocked_by_task_id: str | None = None
    depends_on_task_id: str | None = None
    limit: int | None = None


class TaskQueryService:
    """Search the task index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(self, params: TaskSearchParams) -> tuple[TaskIndexEntry, ...]:
        """Return task entries matching the requested filters."""
        index = self._loader.load_task_index()
        selected_task_ids = {task_id.casefold() for task_id in params.task_ids}
        trace_id = params.trace_id.casefold() if params.trace_id is not None else None
        task_status = params.task_status.casefold() if params.task_status is not None else None
        priority = params.priority.casefold() if params.priority is not None else None
        owner = params.owner.casefold() if params.owner is not None else None
        task_kind = params.task_kind.casefold() if params.task_kind is not None else None
        blocked_by_task_id = (
            params.blocked_by_task_id.casefold()
            if params.blocked_by_task_id is not None
            else None
        )
        depends_on_task_id = (
            params.depends_on_task_id.casefold()
            if params.depends_on_task_id is not None
            else None
        )

        matches: list[tuple[int, TaskIndexEntry]] = []
        for entry in index.entries:
            if selected_task_ids and entry.task_id.casefold() not in selected_task_ids:
                continue
            if trace_id is not None and (entry.trace_id or "").casefold() != trace_id:
                continue
            if task_status is not None and entry.task_status.casefold() != task_status:
                continue
            if priority is not None and entry.priority.casefold() != priority:
                continue
            if owner is not None and entry.owner.casefold() != owner:
                continue
            if task_kind is not None and entry.task_kind.casefold() != task_kind:
                continue
            if params.blocked_only and not entry.blocked_by:
                continue
            if blocked_by_task_id is not None and blocked_by_task_id not in {
                value.casefold() for value in entry.blocked_by
            }:
                continue
            if depends_on_task_id is not None and depends_on_task_id not in {
                value.casefold() for value in entry.depends_on
            }:
                continue

            score = query_score(
                params.query,
                (
                    entry.task_id,
                    entry.trace_id or "",
                    entry.title,
                    entry.summary,
                    entry.task_status,
                    entry.priority,
                    entry.owner,
                    entry.task_kind,
                    *entry.related_ids,
                    *entry.applies_to,
                    *entry.tags,
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].task_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)

    def get(self, task_id: str) -> TaskIndexEntry:
        """Return one task entry by its stable task identifier."""
        return self._loader.load_task_index().get(task_id)

    def reverse_dependencies(self, task_id: str) -> tuple[TaskIndexEntry, ...]:
        """Return task entries that depend on or are blocked by the given task."""
        needle = task_id.casefold()
        matches = [
            entry
            for entry in self._loader.load_task_index().entries
            if needle in {value.casefold() for value in (*entry.depends_on, *entry.blocked_by)}
        ]
        matches.sort(key=lambda entry: entry.task_id)
        return tuple(matches)
