"""Deterministic rebuild helpers for the human-readable PRD tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import render_rendered_surface
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import (
    ACTIVE_INITIATIVE_STATUS,
    initiative_status_map,
    latest_timestamp,
    terminal_initiative_status_counts_for_trace_ids,
)

PRD_TRACKING_DOCUMENT_PATH = "docs/planning/prds/prd_tracking.md"
PRD_TRACKING_SURFACE_ID = "rendered.prd_tracking"


@dataclass(frozen=True, slots=True)
class PrdTrackingBuildResult:
    """Generated PRD-tracking document plus document count."""

    content: str
    prd_count: int


class PrdTrackingSyncService:
    """Build and write the human-readable PRD tracker from the PRD index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> PrdTrackingSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> PrdTrackingBuildResult:
        prd_index = self._loader.load_prd_index()
        trace_statuses = initiative_status_map(self._loader)
        surface = self._loader.load_rendered_surface_registry().get(PRD_TRACKING_SURFACE_ID)
        content = render_rendered_surface(
            surface,
            {
                "active_prds": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "prd_id": entry.prd_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": trace_statuses.get(entry.trace_id, "active"),
                        "summary": entry.summary,
                        "linked_designs_and_plans": "; ".join(
                            (*entry.linked_design_ids, *entry.linked_plan_ids)
                        )
                        or "-",
                    }
                    for entry in prd_index.entries
                    if trace_statuses.get(entry.trace_id, ACTIVE_INITIATIVE_STATUS)
                    == ACTIVE_INITIATIVE_STATUS
                ),
                "terminal_counts": tuple(
                    {"label": label, "count": count}
                    for label, count in terminal_initiative_status_counts_for_trace_ids(
                        tuple(entry.trace_id for entry in prd_index.entries),
                        trace_statuses,
                    )
                ),
                "terminal_history_notes": (
                    "Use `watchtower-core query initiatives --initiative-status <status> "
                    "--format json` for terminal trace browse and "
                    "`watchtower-core query planning --trace-id <trace_id> --format json` "
                    "for the deep planning record behind one known PRD.",
                ),
                "updated_at": latest_timestamp(
                    tuple(entry.updated_at for entry in prd_index.entries)
                ),
            },
        )
        return PrdTrackingBuildResult(content=content, prd_count=len(prd_index.entries))

    def write_document(
        self,
        result: PrdTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write the generated PRD tracker to disk."""
        target = destination or (self._repo_root / PRD_TRACKING_DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target
