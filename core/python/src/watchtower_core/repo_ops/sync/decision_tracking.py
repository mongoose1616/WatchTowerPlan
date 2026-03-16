"""Deterministic rebuild helpers for the human-readable decision tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import (
    ACTIVE_INITIATIVE_STATUS,
    initiative_status_map,
    latest_timestamp,
    markdown_repo_link,
    render_bullet_summary,
    render_markdown_table,
    terminal_initiative_status_counts_for_trace_ids,
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
        active_entries = tuple(
            entry
            for entry in decision_index.entries
            if trace_statuses.get(entry.trace_id, ACTIVE_INITIATIVE_STATUS)
            == ACTIVE_INITIATIVE_STATUS
        )
        terminal_counts = terminal_initiative_status_counts_for_trace_ids(
            tuple(entry.trace_id for entry in decision_index.entries),
            trace_statuses,
        )

        lines = ["# Decision Tracking", "", "## Active Decisions"]
        if not active_entries:
            lines.append(
                "_No active decisions. Use `watchtower-core query initiatives "
                "--initiative-status <status> --format json` for terminal trace browse "
                "or `watchtower-core query decisions --trace-id <trace_id>` for one known trace._"
            )
        else:
            rows: list[tuple[str, ...]] = []
            for entry in active_entries:
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
        lines.extend(
            [
                "",
                "## Terminal History",
                *render_bullet_summary(
                    terminal_counts,
                    empty_message="_No terminal decision traces._",
                ),
                "",
                "Use `watchtower-core query initiatives --initiative-status <status> "
                "--format json` for terminal trace browse, and "
                "`watchtower-core query decisions --trace-id <trace_id>` "
                "for one known decision trace.",
            ]
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
