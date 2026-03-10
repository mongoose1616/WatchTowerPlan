"""Deterministic rebuild helpers for the human-readable PRD tracker."""

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

PRD_TRACKING_DOCUMENT_PATH = "docs/planning/prds/prd_tracking.md"


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
        updated_at = latest_timestamp(tuple(entry.updated_at for entry in prd_index.entries))

        lines = ["# PRD Tracking", "", "## PRDs"]
        if not prd_index.entries:
            lines.append("_No PRDs._")
        else:
            rows: list[tuple[str, ...]] = []
            for entry in prd_index.entries:
                initiative_status = trace_statuses.get(entry.trace_id, "active")
                linked = "; ".join((*entry.linked_design_ids, *entry.linked_plan_ids)) or "-"
                rows.append(
                    (
                        f"`{entry.trace_id}`",
                        markdown_repo_link(
                            self._repo_root,
                            entry.doc_path,
                            label=entry.prd_id,
                        ),
                        f"`{initiative_status}`",
                        entry.summary,
                        linked,
                    )
                )
            lines.extend(
                render_markdown_table(
                    ("Trace ID", "PRD", "Status", "Summary", "Linked Designs and Plans"),
                    tuple(rows),
                )
            )
        lines.extend(["", f"_Updated At: `{updated_at}`_", ""])
        return PrdTrackingBuildResult(content="\n".join(lines), prd_count=len(prd_index.entries))

    def write_document(
        self,
        result: PrdTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write the generated PRD tracker to disk."""
        target = destination or (self._repo_root / PRD_TRACKING_DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target
