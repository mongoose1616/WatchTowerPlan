"""Deterministic rebuild helpers for the human-readable initiative tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import render_repo_link
from watchtower_core.sync.rendered_tracking import (
    RenderedTrackingSyncService,
    latest_updated_at_for_entries,
)
from watchtower_plan.workspace.service import PlanWorkspaceService
from watchtower_plan.sync.initiative_index import PHASE_ORDER

INITIATIVE_TRACKING_DOCUMENT_PATH = "plan/tracking/initiative_tracking.md"
INITIATIVE_TRACKING_SURFACE_ID = "rendered.initiative_tracking"


@dataclass(frozen=True, slots=True)
class InitiativeTrackingBuildResult:
    """Generated initiative-tracking document plus initiative counts."""

    content: str
    initiative_count: int
    active_count: int
    closed_count: int


class InitiativeTrackingSyncService(RenderedTrackingSyncService):
    """Build and write the human-readable initiative tracker from the initiative index."""

    DOCUMENT_PATH = INITIATIVE_TRACKING_DOCUMENT_PATH
    SURFACE_ID = INITIATIVE_TRACKING_SURFACE_ID

    def build_document(self) -> InitiativeTrackingBuildResult:
        initiative_index = PlanWorkspaceService(self._loader).load_initiative_index()
        active_entries = tuple(
            sorted(
                (
                    entry
                    for entry in initiative_index.entries
                    if entry.initiative_status == "active"
                ),
                key=lambda entry: (PHASE_ORDER.get(entry.current_phase, 999), entry.trace_id),
            )
        )
        closed_entries = tuple(
            sorted(
                (
                    entry
                    for entry in initiative_index.entries
                    if entry.initiative_status != "active"
                ),
                key=lambda entry: (entry.closed_at or entry.updated_at, entry.trace_id),
                reverse=True,
            )
        )
        content = self._render_tracking_document(
            {
                "active_initiatives": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "title": entry.title,
                        "current_phase": entry.current_phase,
                        "owners": (
                            ", ".join(entry.active_owners)
                            if entry.active_owners
                            else "unassigned"
                        ),
                        "open_tasks": (
                            f"`{entry.open_task_count}` "
                            f"(`blocked={entry.blocked_task_count}`)"
                            if entry.blocked_task_count
                            else f"`{entry.open_task_count}`"
                        ),
                        "key_surface_path": entry.key_surface_path,
                        "key_label": Path(entry.key_surface_path).name,
                        "next_surface_path": entry.next_surface_path,
                        "next_label": Path(entry.next_surface_path).name,
                        "active_tasks": " <br> ".join(
                            (
                                f"{render_repo_link(task.doc_path, label=task.task_id)} "
                                f"(`{task.task_status}`)"
                            )
                            for task in entry.active_task_summaries
                        )
                        or "-",
                        "next_action": entry.next_action,
                    }
                    for entry in active_entries
                ),
                "closed_initiatives": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "title": entry.title,
                        "initiative_status": entry.initiative_status,
                        "key_surface_path": entry.key_surface_path,
                        "key_label": Path(entry.key_surface_path).name,
                        "closed_at": entry.closed_at,
                        "closure_reason": entry.closure_reason or "-",
                    }
                    for entry in closed_entries
                ),
                "updated_at": latest_updated_at_for_entries(initiative_index.entries),
            },
        )
        return InitiativeTrackingBuildResult(
            content=content,
            initiative_count=len(initiative_index.entries),
            active_count=len(active_entries),
            closed_count=len(closed_entries),
        )
