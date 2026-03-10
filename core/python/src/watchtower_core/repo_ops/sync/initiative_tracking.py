"""Deterministic rebuild helpers for the human-readable initiative tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.initiative_index import PHASE_ORDER
from watchtower_core.repo_ops.sync.tracking_common import (
    latest_timestamp,
    markdown_repo_link,
    render_markdown_table,
)

INITIATIVE_TRACKING_DOCUMENT_PATH = "docs/planning/initiatives/initiative_tracking.md"


@dataclass(frozen=True, slots=True)
class InitiativeTrackingBuildResult:
    """Generated initiative-tracking document plus initiative counts."""

    content: str
    initiative_count: int
    active_count: int
    closed_count: int


class InitiativeTrackingSyncService:
    """Build and write the human-readable initiative tracker from the initiative index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> InitiativeTrackingSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> InitiativeTrackingBuildResult:
        initiative_index = self._loader.load_initiative_index()
        updated_at = latest_timestamp(tuple(entry.updated_at for entry in initiative_index.entries))
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

        lines = ["# Initiative Tracking", "", "## Active Initiatives"]
        if not active_entries:
            lines.append("_No active initiatives._")
        else:
            active_rows: list[tuple[str, ...]] = []
            for entry in active_entries:
                owners = ", ".join(entry.active_owners) if entry.active_owners else "unassigned"
                task_summary = f"`{entry.open_task_count}`"
                if entry.blocked_task_count:
                    task_summary = (
                        f"`{entry.open_task_count}` "
                        f"(`blocked={entry.blocked_task_count}`)"
                    )
                active_rows.append(
                    (
                        f"`{entry.trace_id}`",
                        f"`{entry.current_phase}`",
                        owners,
                        task_summary,
                        markdown_repo_link(
                            self._repo_root,
                            entry.key_surface_path,
                            label=Path(entry.key_surface_path).name,
                        ),
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
                    ("Trace ID", "Phase", "Owners", "Open Tasks", "Key", "Next", "Action"),
                    tuple(active_rows),
                )
            )

        lines.extend(["", "## Closed Initiatives"])
        if not closed_entries:
            lines.append("_No closed initiatives._")
        else:
            closed_rows: list[tuple[str, ...]] = []
            for entry in closed_entries:
                closure_reason = entry.closure_reason or "-"
                closed_rows.append(
                    (
                        f"`{entry.trace_id}`",
                        f"`{entry.initiative_status}`",
                        markdown_repo_link(
                            self._repo_root,
                            entry.key_surface_path,
                            label=Path(entry.key_surface_path).name,
                        ),
                        f"`{entry.closed_at}`" if entry.closed_at is not None else "-",
                        closure_reason,
                    )
                )
            lines.extend(
                render_markdown_table(
                    ("Trace ID", "Status", "Key", "Closed At", "Reason"),
                    tuple(closed_rows),
                )
            )
        lines.extend(["", f"_Updated At: `{updated_at}`_", ""])
        return InitiativeTrackingBuildResult(
            content="\n".join(lines),
            initiative_count=len(initiative_index.entries),
            active_count=len(active_entries),
            closed_count=len(closed_entries),
        )

    def write_document(
        self,
        result: InitiativeTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write the generated initiative tracker to disk."""
        target = destination or (self._repo_root / INITIATIVE_TRACKING_DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target
