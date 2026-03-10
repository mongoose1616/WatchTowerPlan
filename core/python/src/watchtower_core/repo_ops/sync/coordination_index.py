"""Deterministic rebuild helpers for the coordination index."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    CoordinationRecentInitiativeSummary,
    CoordinationTaskSummary,
    InitiativeIndexEntry,
)
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.initiative_index import PHASE_ORDER
from watchtower_core.repo_ops.sync.tracking_common import latest_timestamp

COORDINATION_INDEX_ARTIFACT_PATH = (
    "core/control_plane/indexes/coordination/coordination_index.v1.json"
)
PLANNING_README_PATH = "docs/planning/README.md"
RECENT_CLOSEOUT_LIMIT = 10
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
PHASE_FOCUS_ORDER = {
    "execution": 0,
    "validation": 1,
    "closeout": 2,
    "implementation_planning": 3,
    "design": 4,
    "prd": 5,
    "closed": 6,
}


class CoordinationIndexSyncService:
    """Build and write the coordination index from the initiative index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> CoordinationIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        initiative_index = self._loader.load_initiative_index()
        active_entries = tuple(
            sorted(
                (
                    entry
                    for entry in initiative_index.entries
                    if entry.initiative_status == "active"
                ),
                key=_active_initiative_sort_key,
            )
        )
        closed_entries = tuple(
            sorted(
                (
                    entry
                    for entry in initiative_index.entries
                    if entry.initiative_status != "active"
                ),
                key=_closed_initiative_sort_key,
                reverse=True,
            )
        )
        actionable_tasks = tuple(_collect_actionable_tasks(active_entries))
        blocked_task_count = sum(entry.blocked_task_count for entry in active_entries)
        coordination_mode = _coordination_mode(
            active_entries=active_entries,
            actionable_task_count=len(actionable_tasks),
        )
        summary, recommended_next_action, recommended_surface_path = (
            _coordination_recommendation(
                coordination_mode=coordination_mode,
                active_entries=active_entries,
            )
        )

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:coordination-index:v1",
            "id": "index.coordination",
            "title": "Coordination Index",
            "status": "active",
            "updated_at": latest_timestamp(
                tuple(entry.updated_at for entry in initiative_index.entries)
            ),
            "coordination_mode": coordination_mode,
            "summary": summary,
            "recommended_next_action": recommended_next_action,
            "recommended_surface_path": recommended_surface_path,
            "active_initiative_count": len(active_entries),
            "blocked_task_count": blocked_task_count,
            "actionable_task_count": len(actionable_tasks),
            "entries": [
                _serialize_dataclass(entry)
                for entry in (*active_entries, *closed_entries)
            ],
            "actionable_tasks": [
                _serialize_dataclass(entry)
                for entry in actionable_tasks
            ],
            "recent_closed_initiatives": [
                _serialize_dataclass(entry)
                for entry in _recent_closed_summaries(closed_entries)
            ],
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(
        self,
        document: dict[str, object],
        destination: Path | None = None,
    ) -> Path:
        """Write the generated coordination index to disk."""
        target = destination or (self._repo_root / COORDINATION_INDEX_ARTIFACT_PATH)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target


def _serialize_dataclass(
    value: InitiativeIndexEntry
    | CoordinationTaskSummary
    | CoordinationRecentInitiativeSummary,
) -> dict[str, object]:
    document = _prune_empty(json.loads(json.dumps(asdict(value))))
    assert isinstance(document, dict)
    return document


def _prune_empty(value: object) -> object | None:
    if isinstance(value, dict):
        pruned: dict[str, object] = {}
        for key, entry in value.items():
            pruned_entry = _prune_empty(entry)
            if pruned_entry is None:
                continue
            pruned[key] = pruned_entry
        return pruned
    if isinstance(value, list):
        pruned_list = [
            pruned_entry
            for entry in value
            if (pruned_entry := _prune_empty(entry)) is not None
        ]
        return pruned_list or None
    if value is None or value == {}:
        return None
    return value


def _active_initiative_sort_key(entry: InitiativeIndexEntry) -> tuple[int, int, int, int, str]:
    actionable_priorities = [
        PRIORITY_ORDER.get(task.priority, 99)
        for task in entry.active_task_summaries
        if task.is_actionable
    ]
    return (
        0 if any(task.is_actionable for task in entry.active_task_summaries) else 1,
        PHASE_FOCUS_ORDER.get(entry.current_phase, 99),
        min(actionable_priorities, default=99),
        PHASE_ORDER.get(entry.current_phase, 99),
        entry.trace_id,
    )


def _closed_initiative_sort_key(entry: InitiativeIndexEntry) -> tuple[str, str]:
    return (entry.closed_at or "", entry.trace_id)


def _collect_actionable_tasks(
    active_entries: tuple[InitiativeIndexEntry, ...],
) -> list[CoordinationTaskSummary]:
    tasks: list[CoordinationTaskSummary] = []
    for entry in active_entries:
        for task in entry.active_task_summaries:
            if not task.is_actionable:
                continue
            tasks.append(
                CoordinationTaskSummary(
                    trace_id=entry.trace_id,
                    initiative_title=entry.title,
                    task_id=task.task_id,
                    title=task.title,
                    task_status=task.task_status,
                    priority=task.priority,
                    owner=task.owner,
                    doc_path=task.doc_path,
                    is_actionable=task.is_actionable,
                    blocked_by=task.blocked_by,
                    depends_on=task.depends_on,
                )
            )
    return sorted(tasks, key=_coordination_task_sort_key)


def _coordination_task_sort_key(
    entry: CoordinationTaskSummary,
) -> tuple[int, int, str, str]:
    return (
        TASK_STATUS_ORDER.get(entry.task_status, 99),
        PRIORITY_ORDER.get(entry.priority, 99),
        entry.trace_id,
        entry.task_id,
    )


def _coordination_mode(
    *,
    active_entries: tuple[InitiativeIndexEntry, ...],
    actionable_task_count: int,
) -> str:
    if not active_entries:
        return "ready_for_bootstrap"
    if (
        actionable_task_count == 0
        and any(entry.current_phase == "execution" for entry in active_entries)
        and any(entry.blocked_task_count > 0 for entry in active_entries)
    ):
        return "blocked_work"
    return "active_work"


def _coordination_recommendation(
    *,
    coordination_mode: str,
    active_entries: tuple[InitiativeIndexEntry, ...],
) -> tuple[str, str, str]:
    if not active_entries:
        return (
            (
                "No active initiatives are open. The repository is ready for one new "
                "bounded initiative."
            ),
            (
                "Bootstrap a traced initiative with a PRD, supporting design and plan "
                "documents, and a bounded task set before starting new execution work."
            ),
            PLANNING_README_PATH,
        )

    focus_entry = active_entries[0]
    if coordination_mode == "blocked_work":
        return (
            (
                "Active initiatives exist, but the current execution path is blocked "
                "or waiting on unresolved dependencies."
            ),
            focus_entry.next_action,
            focus_entry.next_surface_path,
        )
    return (
        (
            "Active initiatives exist and the coordination surface points to the most "
            "actionable next work."
        ),
        focus_entry.next_action,
        focus_entry.next_surface_path,
    )


def _recent_closed_summaries(
    closed_entries: tuple[InitiativeIndexEntry, ...],
) -> tuple[CoordinationRecentInitiativeSummary, ...]:
    summaries = [
        CoordinationRecentInitiativeSummary(
            trace_id=entry.trace_id,
            title=entry.title,
            initiative_status=entry.initiative_status,
            closed_at=entry.closed_at or entry.updated_at,
            key_surface_path=entry.key_surface_path,
            closure_reason=entry.closure_reason,
        )
        for entry in closed_entries[:RECENT_CLOSEOUT_LIMIT]
    ]
    return tuple(summaries)
