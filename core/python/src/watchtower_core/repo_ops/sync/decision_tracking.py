"""Deterministic rebuild helpers for the human-readable decision tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import initiative_status_map, latest_timestamp

DECISION_TRACKING_DOCUMENT_PATH = "docs/planning/decisions/decision_tracking.md"


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
        updated_at = latest_timestamp(tuple(entry.updated_at for entry in decision_index.entries))

        lines = [
            "# Decision Tracking",
            "",
            "## Summary",
            (
                "This document provides the human-readable tracking view for "
                "durable decision records under `docs/planning/decisions/`."
            ),
            "",
            "## Current Decision Records",
            (
                "| Trace ID | Decision ID | Initiative Status | Path | Decision Status | Summary |"
            ),
            "|---|---|---|---|---|---|",
        ]
        if not decision_index.entries:
            lines.append(
                "| `None` | `None` | `None` | `None` | `None` | "
                "No decision records are currently tracked. |"
            )
        else:
            for entry in decision_index.entries:
                initiative_status = trace_statuses.get(entry.trace_id, "active")
                lines.append(
                    "| "
                    f"`{entry.trace_id}` | `{entry.decision_id}` | `{initiative_status}` | "
                    f"`{entry.doc_path}` | `{entry.decision_status}` | {entry.summary} |"
                )

        lines.extend(
            [
                "",
                "## Update Rules",
                (
                    "- Rebuild this tracker in the same change set when a decision "
                    "record is added, renamed, removed, materially retargeted, or "
                    "when a trace initiative changes closeout state."
                ),
                (
                    "- Keep the machine-readable companion index at "
                    "[decision_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/"
                    "indexes/decisions/decision_index.v1.json) aligned with this tracker."
                ),
                (
                    "- Treat the unified traceability index at "
                    "[traceability_index.v1.json](/home/j/WatchTowerPlan/core/"
                    "control_plane/indexes/traceability/traceability_index.v1.json) "
                    "as the source for initiative closeout status."
                ),
                "",
                "## References",
                "- [README.md](/home/j/WatchTowerPlan/docs/planning/decisions/README.md)",
                (
                    "- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/documentation/decision_record_md_standard.md)"
                ),
                (
                    "- [decision_index_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/data_contracts/decision_index_standard.md)"
                ),
                "",
                "## Updated At",
                f"- `{updated_at}`",
                "",
            ]
        )
        return DecisionTrackingBuildResult(
            content="\n".join(lines),
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
