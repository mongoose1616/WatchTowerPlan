"""Deterministic rebuild helpers for the human-readable PRD tracker."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.repo_ops.sync.tracking_common import (
    RenderedTrackingSyncService,
    active_entries_for_trace_status,
    initiative_status_for_trace_id,
    initiative_status_map,
    latest_updated_at_for_entries,
    terminal_entries_for_trace_status,
)

PRD_TRACKING_DOCUMENT_PATH = "docs/planning/prds/prd_tracking.md"
PRD_TRACKING_SURFACE_ID = "rendered.prd_tracking"


@dataclass(frozen=True, slots=True)
class PrdTrackingBuildResult:
    """Generated PRD-tracking document plus document count."""

    content: str
    prd_count: int


class PrdTrackingSyncService(RenderedTrackingSyncService):
    """Build and write the human-readable PRD tracker from the PRD index."""

    DOCUMENT_PATH = PRD_TRACKING_DOCUMENT_PATH
    SURFACE_ID = PRD_TRACKING_SURFACE_ID

    def build_document(self) -> PrdTrackingBuildResult:
        prd_index = self._loader.load_prd_index()
        trace_statuses = initiative_status_map(self._loader)
        active_entries = active_entries_for_trace_status(prd_index.entries, trace_statuses)
        terminal_entries = terminal_entries_for_trace_status(prd_index.entries, trace_statuses)
        content = self._render_tracking_document(
            {
                "active_prds": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "prd_id": entry.prd_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": initiative_status_for_trace_id(
                            entry.trace_id,
                            trace_statuses,
                        ),
                        "summary": entry.summary,
                        "linked_designs_and_plans": "; ".join(
                            (*entry.linked_design_ids, *entry.linked_plan_ids)
                        )
                        or "-",
                    }
                    for entry in active_entries
                ),
                "terminal_prds": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "prd_id": entry.prd_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": initiative_status_for_trace_id(
                            entry.trace_id,
                            trace_statuses,
                        ),
                        "summary": entry.summary,
                        "linked_designs_and_plans": "; ".join(
                            (*entry.linked_design_ids, *entry.linked_plan_ids)
                        )
                        or "-",
                    }
                    for entry in terminal_entries
                ),
                "updated_at": latest_updated_at_for_entries(prd_index.entries),
            },
        )
        return PrdTrackingBuildResult(content=content, prd_count=len(prd_index.entries))
