"""Deterministic rebuild helpers for the human-readable coordination tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import render_repo_link
from watchtower_core.sync.rendered_tracking import RenderedTrackingSyncService
from watchtower_plan.workspace.service import PlanWorkspaceService

COORDINATION_TRACKING_DOCUMENT_PATH = "plan/tracking/coordination_tracking.md"
INITIATIVE_TRACKING_DOCUMENT_PATH = "plan/tracking/initiative_tracking.md"
TASK_TRACKING_DOCUMENT_PATH = "plan/tracking/task_tracking.md"
COORDINATION_TRACKING_SURFACE_ID = "rendered.coordination_tracking"
ACTIVE_INITIATIVE_LIMIT = 5
ACTIONABLE_TASK_LIMIT = 5
RECENT_CLOSEOUT_LIMIT = 5


@dataclass(frozen=True, slots=True)
class CoordinationTrackingBuildResult:
    """Generated coordination-tracking document plus summary counts."""

    content: str
    coordination_entry_count: int
    active_initiative_count: int
    actionable_task_count: int
    recent_closed_count: int


class CoordinationTrackingSyncService(RenderedTrackingSyncService):
    """Build and write the human-readable coordination tracker."""

    DOCUMENT_PATH = COORDINATION_TRACKING_DOCUMENT_PATH
    SURFACE_ID = COORDINATION_TRACKING_SURFACE_ID

    def build_document(self) -> CoordinationTrackingBuildResult:
        coordination_index = PlanWorkspaceService(self._loader).load_coordination_index()
        active_entries = tuple(
            entry
            for entry in coordination_index.entries
            if entry.initiative_status == "active"
        )
        active_preview = active_entries[:ACTIVE_INITIATIVE_LIMIT]
        actionable_preview = coordination_index.actionable_tasks[:ACTIONABLE_TASK_LIMIT]
        recent_closed_preview = coordination_index.recent_closed_initiatives[
            :RECENT_CLOSEOUT_LIMIT
        ]
        content = self._render_tracking_document(
            {
                "current_state": (
                    {
                        "field": "Mode",
                        "value": f"`{coordination_index.coordination_mode}`",
                    },
                    {
                        "field": "Summary",
                        "value": coordination_index.summary,
                    },
                    {
                        "field": "Next",
                        "value": coordination_index.recommended_next_action,
                    },
                    {
                        "field": "Open First",
                        "value": render_repo_link(
                            coordination_index.recommended_surface_path,
                            label=coordination_index.recommended_surface_path,
                        ),
                    },
                    {
                        "field": "Companion Views",
                        "value": ", ".join(
                            (
                                render_repo_link(
                                    INITIATIVE_TRACKING_DOCUMENT_PATH,
                                    label="initiative_tracking.md",
                                ),
                                render_repo_link(
                                    TASK_TRACKING_DOCUMENT_PATH,
                                    label="task_tracking.md",
                                ),
                            )
                        ),
                    },
                ),
                "active_initiatives": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "current_phase": entry.current_phase,
                        "owners": (
                            ", ".join(entry.active_owners)
                            if entry.active_owners
                            else "unassigned"
                        ),
                        "next_surface_path": entry.next_surface_path,
                        "next_label": Path(entry.next_surface_path).name,
                        "next_action": entry.next_action,
                    }
                    for entry in active_preview
                ),
                "active_initiative_notes": (
                    (
                        f"_Showing {len(active_preview)} of "
                        f"{coordination_index.active_initiative_count} active initiatives. "
                        "Open initiative_tracking.md for the full family view._"
                    ),
                )
                if coordination_index.active_initiative_count > len(active_preview)
                else (),
                "actionable_tasks": tuple(
                    {
                        "task_id": entry.task_id,
                        "doc_path": entry.doc_path,
                        "trace_id": entry.trace_id,
                        "task_status": entry.task_status,
                        "priority": entry.priority,
                        "owner": entry.owner,
                    }
                    for entry in actionable_preview
                ),
                "actionable_task_notes": (
                    (
                        f"_Showing {len(actionable_preview)} of "
                        f"{coordination_index.actionable_task_count} actionable tasks. "
                        "Use task_tracking.md or query coordination --format json for more._"
                    ),
                )
                if coordination_index.actionable_task_count > len(actionable_preview)
                else (),
                "recent_closeouts": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "initiative_status": entry.initiative_status,
                        "closed_at": entry.closed_at,
                        "key_surface_path": entry.key_surface_path,
                        "key_label": Path(entry.key_surface_path).name,
                    }
                    for entry in recent_closed_preview
                ),
                "updated_at": coordination_index.updated_at,
            },
        )
        return CoordinationTrackingBuildResult(
            content=content,
            coordination_entry_count=len(coordination_index.entries),
            active_initiative_count=coordination_index.active_initiative_count,
            actionable_task_count=coordination_index.actionable_task_count,
            recent_closed_count=len(coordination_index.recent_closed_initiatives),
        )
