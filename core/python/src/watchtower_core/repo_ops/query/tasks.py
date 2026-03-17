"""Repo-specific query helpers for local task records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.plan_workspace import PlanTaskIndexEntry, PlanWorkspaceService
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
        self._plan_workspace = PlanWorkspaceService(loader)
        self._reverse_dependency_map: dict[str, tuple[PlanTaskIndexEntry, ...]] | None = None

    def search(self, params: TaskSearchParams) -> tuple[PlanTaskIndexEntry, ...]:
        """Return task entries matching the requested filters."""
        entries = self._plan_workspace.load_task_entries()
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

        matches: list[tuple[int, PlanTaskIndexEntry]] = []
        for entry in entries:
            if selected_task_ids and entry.task_id.casefold() not in selected_task_ids:
                continue
            if trace_id is not None and entry.trace_id.casefold() != trace_id:
                continue
            if task_status is not None and entry.status.casefold() != task_status:
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
                    entry.trace_id,
                    entry.initiative_id,
                    entry.project_id or "",
                    entry.initiative_title,
                    entry.title,
                    entry.summary,
                    entry.status,
                    entry.priority,
                    entry.owner,
                    entry.task_kind,
                    *entry.related_ids,
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

    def get(self, task_id: str) -> PlanTaskIndexEntry:
        """Return one task entry by its stable task identifier."""
        for entry in self._plan_workspace.load_task_entries():
            if entry.task_id == task_id:
                return entry
        raise KeyError(task_id)

    def reverse_dependencies(self, task_id: str) -> tuple[PlanTaskIndexEntry, ...]:
        """Return task entries that depend on or are blocked by the given task."""
        return self.reverse_dependencies_for((task_id,)).get(task_id, ())

    def reverse_dependencies_for(
        self,
        task_ids: tuple[str, ...],
    ) -> dict[str, tuple[PlanTaskIndexEntry, ...]]:
        """Return reverse dependencies for each requested task identifier."""
        reverse_dependency_map = self._load_reverse_dependency_map()
        return {
            task_id: reverse_dependency_map.get(task_id.casefold(), ())
            for task_id in task_ids
        }

    def _load_reverse_dependency_map(self) -> dict[str, tuple[PlanTaskIndexEntry, ...]]:
        """Build one reverse-dependency map per service-backed query run."""
        if self._reverse_dependency_map is not None:
            return self._reverse_dependency_map

        matches: dict[str, list[PlanTaskIndexEntry]] = {}
        for entry in self._plan_workspace.load_task_entries():
            referenced_task_ids = {
                value.casefold() for value in (*entry.depends_on, *entry.blocked_by)
            }
            for referenced_task_id in referenced_task_ids:
                matches.setdefault(referenced_task_id, []).append(entry)

        self._reverse_dependency_map = {
            task_id: tuple(sorted(entries, key=lambda candidate: candidate.task_id))
            for task_id, entries in matches.items()
        }
        return self._reverse_dependency_map
