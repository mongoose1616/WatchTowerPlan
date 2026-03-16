"""Deterministic rebuild helpers for the human-readable decision tracker."""

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

DECISION_TRACKING_DOCUMENT_PATH = "docs/planning/decisions/decision_tracking.md"
DECISION_TRACKING_SURFACE_ID = "rendered.decision_tracking"


@dataclass(frozen=True, slots=True)
class DecisionTrackingBuildResult:
    """Generated decision-tracking document plus document count."""

    content: str
    decision_count: int


class DecisionTrackingSyncService:
    """Build and write the human-readable decision tracker from the decision index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> DecisionTrackingSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> DecisionTrackingBuildResult:
        decision_index = self._loader.load_decision_index()
        trace_statuses = initiative_status_map(self._loader)
        surface = self._loader.load_rendered_surface_registry().get(
            DECISION_TRACKING_SURFACE_ID
        )
        content = render_rendered_surface(
            surface,
            {
                "active_decisions": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "decision_id": entry.decision_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": trace_statuses.get(entry.trace_id, "active"),
                        "decision_status": entry.decision_status,
                        "summary": entry.summary,
                    }
                    for entry in decision_index.entries
                    if trace_statuses.get(entry.trace_id, ACTIVE_INITIATIVE_STATUS)
                    == ACTIVE_INITIATIVE_STATUS
                ),
                "terminal_counts": tuple(
                    {"label": label, "count": count}
                    for label, count in terminal_initiative_status_counts_for_trace_ids(
                        tuple(entry.trace_id for entry in decision_index.entries),
                        trace_statuses,
                    )
                ),
                "terminal_history_notes": (
                    "Use `watchtower-core query initiatives --initiative-status <status> "
                    "--format json` for terminal trace browse, and "
                    "`watchtower-core query decisions --trace-id <trace_id>` "
                    "for one known decision trace.",
                ),
                "updated_at": latest_timestamp(
                    tuple(entry.updated_at for entry in decision_index.entries)
                ),
            },
        )
        return DecisionTrackingBuildResult(
            content=content,
            decision_count=len(decision_index.entries),
        )

    def write_document(
        self,
        result: DecisionTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write the generated decision tracker to disk."""
        target = destination or (self._repo_root / DECISION_TRACKING_DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target
