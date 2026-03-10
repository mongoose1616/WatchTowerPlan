"""Deterministic rebuild helpers for the human-readable decision tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import (
    initiative_status_map,
    latest_timestamp,
    markdown_repo_link,
    render_markdown_table,
)

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

        lines = ["# Decision Tracking", "", "## Decisions"]
        if not decision_index.entries:
            lines.append("_No decision records._")
        else:
            rows: list[tuple[str, ...]] = []
            for entry in decision_index.entries:
                initiative_status = trace_statuses.get(entry.trace_id, "active")
                rows.append(
                    (
                        f"`{entry.trace_id}`",
                        markdown_repo_link(
                            self._repo_root,
                            entry.doc_path,
                            label=entry.decision_id,
                        ),
                        f"`{initiative_status}`",
                        f"`{entry.decision_status}`",
                        entry.summary,
                    )
                )
            lines.extend(
                render_markdown_table(
                    ("Trace ID", "Decision", "Status", "Outcome", "Summary"),
                    tuple(rows),
                )
            )
        lines.extend(["", f"_Updated At: `{updated_at}`_", ""])
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
