"""Deterministic rebuild helpers for the human-readable initiative tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import render_rendered_surface
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.initiative_index import PHASE_ORDER
from watchtower_core.repo_ops.sync.tracking_common import latest_timestamp

INITIATIVE_TRACKING_DOCUMENT_PATH = "docs/planning/initiatives/initiative_tracking.md"
INITIATIVE_TRACKING_SURFACE_ID = "rendered.initiative_tracking"


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
        surface = self._loader.load_rendered_surface_registry().get(
            INITIATIVE_TRACKING_SURFACE_ID
        )
        content = render_rendered_surface(
            surface,
            {
                "active_initiatives": tuple(
                    {
                        "trace_id": entry.trace_id,
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
                        "next_action": entry.next_action,
                    }
                    for entry in active_entries
                ),
                "closed_initiatives": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "initiative_status": entry.initiative_status,
                        "key_surface_path": entry.key_surface_path,
                        "key_label": Path(entry.key_surface_path).name,
                        "closed_at": entry.closed_at,
                        "closure_reason": entry.closure_reason or "-",
                    }
                    for entry in closed_entries
                ),
                "updated_at": latest_timestamp(
                    tuple(entry.updated_at for entry in initiative_index.entries)
                ),
            },
        )
        return InitiativeTrackingBuildResult(
            content=content,
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
