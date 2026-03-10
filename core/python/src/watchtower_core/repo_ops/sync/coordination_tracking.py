"""Deterministic rebuild helpers for the human-readable coordination tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import (
    markdown_repo_link,
    render_markdown_table,
)

COORDINATION_TRACKING_DOCUMENT_PATH = "docs/planning/coordination_tracking.md"
INITIATIVE_TRACKING_DOCUMENT_PATH = "docs/planning/initiatives/initiative_tracking.md"
TASK_TRACKING_DOCUMENT_PATH = "docs/planning/tasks/task_tracking.md"
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


class CoordinationTrackingSyncService:
    """Build and write the human-readable coordination tracker."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> CoordinationTrackingSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> CoordinationTrackingBuildResult:
        coordination_index = self._loader.load_coordination_index()
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

        current_state_rows = (
            ("Mode", f"`{coordination_index.coordination_mode}`"),
            ("Summary", coordination_index.summary),
            ("Next", coordination_index.recommended_next_action),
            (
                "Open First",
                markdown_repo_link(
                    self._repo_root,
                    coordination_index.recommended_surface_path,
                    label=coordination_index.recommended_surface_path,
                ),
            ),
            (
                "Companion Views",
                ", ".join(
                    [
                        markdown_repo_link(
                            self._repo_root,
                            INITIATIVE_TRACKING_DOCUMENT_PATH,
                            label="initiative_tracking.md",
                        ),
                        markdown_repo_link(
                            self._repo_root,
                            TASK_TRACKING_DOCUMENT_PATH,
                            label="task_tracking.md",
                        ),
                    ]
                ),
            ),
        )

        lines = ["# Coordination Tracking", "", "## Current State"]
        lines.extend(render_markdown_table(("Field", "Value"), current_state_rows))

        lines.extend(["", "## Active Initiatives"])
        if not active_preview:
            lines.append("_No active initiatives._")
        else:
            rows: list[tuple[str, ...]] = []
            for entry in active_preview:
                owners = ", ".join(entry.active_owners) if entry.active_owners else "unassigned"
                rows.append(
                    (
                        f"`{entry.trace_id}`",
                        f"`{entry.current_phase}`",
                        owners,
                        markdown_repo_link(
                            self._repo_root,
                            entry.next_surface_path,
                            label=Path(entry.next_surface_path).name,
                        ),
                        entry.next_action,
                    )
                )
            lines.extend(
                render_markdown_table(
                    ("Trace ID", "Phase", "Owners", "Next", "Action"),
                    tuple(rows),
                )
            )
            if coordination_index.active_initiative_count > len(active_preview):
                lines.extend(
                    [
                        "",
                        (
                            f"_Showing {len(active_preview)} of "
                            f"{coordination_index.active_initiative_count} active initiatives. "
                            "Open initiative_tracking.md for the full family view._"
                        ),
                    ]
                )

        lines.extend(["", "## Actionable Tasks"])
        if not actionable_preview:
            lines.append("_No actionable tasks._")
        else:
            rows = [
                (
                    markdown_repo_link(
                        self._repo_root,
                        entry.doc_path,
                        label=entry.task_id,
                    ),
                    f"`{entry.trace_id}`",
                    f"`{entry.task_status}`",
                    f"`{entry.priority}`",
                    f"`{entry.owner}`",
                )
                for entry in actionable_preview
            ]
            lines.extend(
                render_markdown_table(
                    ("Task", "Initiative", "Status", "Priority", "Owner"),
                    tuple(rows),
                )
            )
            if coordination_index.actionable_task_count > len(actionable_preview):
                lines.extend(
                    [
                        "",
                        (
                            f"_Showing {len(actionable_preview)} of "
                            f"{coordination_index.actionable_task_count} actionable tasks. "
                            "Use task_tracking.md or query coordination --format json for more._"
                        ),
                    ]
                )

        lines.extend(["", "## Recent Closeouts"])
        if not recent_closed_preview:
            lines.append("_No recent closeouts._")
        else:
            rows = [
                (
                    f"`{entry.trace_id}`",
                    f"`{entry.initiative_status}`",
                    f"`{entry.closed_at}`",
                    markdown_repo_link(
                        self._repo_root,
                        entry.key_surface_path,
                        label=Path(entry.key_surface_path).name,
                    ),
                )
                for entry in recent_closed_preview
            ]
            lines.extend(
                render_markdown_table(
                    ("Trace ID", "Status", "Closed At", "Key"),
                    tuple(rows),
                )
            )

        lines.extend(["", f"_Updated At: `{coordination_index.updated_at}`_", ""])
        return CoordinationTrackingBuildResult(
            content="\n".join(lines),
            coordination_entry_count=len(coordination_index.entries),
            active_initiative_count=coordination_index.active_initiative_count,
            actionable_task_count=coordination_index.actionable_task_count,
            recent_closed_count=len(coordination_index.recent_closed_initiatives),
        )

    def write_document(
        self,
        result: CoordinationTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write the generated coordination tracker to disk."""
        target = destination or (self._repo_root / COORDINATION_TRACKING_DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target
