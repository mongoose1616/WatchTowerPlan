"""Deterministic rebuild helpers for the human-readable decision tracker."""

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

DECISION_TRACKING_DOCUMENT_PATH = "docs/planning/decisions/decision_tracking.md"
DECISION_TRACKING_SURFACE_ID = "rendered.decision_tracking"


@dataclass(frozen=True, slots=True)
class DecisionTrackingBuildResult:
    """Generated decision-tracking document plus document count."""

    content: str
    decision_count: int


class DecisionTrackingSyncService(RenderedTrackingSyncService):
    """Build and write the human-readable decision tracker from the decision index."""

    DOCUMENT_PATH = DECISION_TRACKING_DOCUMENT_PATH
    SURFACE_ID = DECISION_TRACKING_SURFACE_ID

    def build_document(self) -> DecisionTrackingBuildResult:
        decision_index = self._loader.load_decision_index()
        trace_statuses = initiative_status_map(self._loader)
        active_entries = active_entries_for_trace_status(
            decision_index.entries,
            trace_statuses,
        )
        terminal_entries = terminal_entries_for_trace_status(
            decision_index.entries,
            trace_statuses,
        )
        content = self._render_tracking_document(
            {
                "active_decisions": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "decision_id": entry.decision_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": initiative_status_for_trace_id(
                            entry.trace_id,
                            trace_statuses,
                        ),
                        "decision_status": entry.decision_status,
                        "summary": entry.summary,
                    }
                    for entry in active_entries
                ),
                "terminal_decisions": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "decision_id": entry.decision_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": initiative_status_for_trace_id(
                            entry.trace_id,
                            trace_statuses,
                        ),
                        "decision_status": entry.decision_status,
                        "summary": entry.summary,
                    }
                    for entry in terminal_entries
                ),
                "updated_at": latest_updated_at_for_entries(decision_index.entries),
            },
        )
        return DecisionTrackingBuildResult(
            content=content,
            decision_count=len(decision_index.entries),
        )
