"""Deterministic rebuild helpers for the human-readable PRD tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.tracking_common import initiative_status_map, latest_timestamp

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

        lines = [
            "# PRD Tracking",
            "",
            "## Summary",
            (
                "This document provides the human-readable tracking view for PRDs "
                "under `docs/planning/prds/`."
            ),
            "",
            "## Current PRDs",
            (
                "| Trace ID | PRD ID | Initiative Status | Path | Summary | "
                "Linked Designs and Plans |"
            ),
            "|---|---|---|---|---|---|",
        ]
        if not prd_index.entries:
            lines.append(
                "| `None` | `None` | `None` | `None` | No PRDs are currently tracked. | `None` |"
            )
        else:
            for entry in prd_index.entries:
                initiative_status = trace_statuses.get(entry.trace_id, "active")
                linked = "; ".join((*entry.linked_design_ids, *entry.linked_plan_ids)) or "None"
                lines.append(
                    "| "
                    f"`{entry.trace_id}` | `{entry.prd_id}` | `{initiative_status}` | "
                    f"`{entry.doc_path}` | {entry.summary} | `{linked}` |"
                )

        lines.extend(
            [
                "",
                "## Update Rules",
                (
                    "- Rebuild this tracker in the same change set when a PRD is "
                    "added, renamed, removed, materially retargeted, or when a "
                    "trace initiative changes closeout state."
                ),
                (
                    "- Keep the machine-readable companion index at "
                    "[prd_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/"
                    "indexes/prds/prd_index.v1.json) aligned with this tracker."
                ),
                (
                    "- Treat the unified traceability index at "
                    "[traceability_index.v1.json](/home/j/WatchTowerPlan/core/"
                    "control_plane/indexes/traceability/traceability_index.v1.json) "
                    "as the source for initiative closeout status."
                ),
                "",
                "## References",
                "- [README.md](/home/j/WatchTowerPlan/docs/planning/prds/README.md)",
                (
                    "- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/"
                    "documentation/prd_md_standard.md)"
                ),
                (
                    "- [prd_index_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/data_contracts/prd_index_standard.md)"
                ),
                "",
                "## Updated At",
                f"- `{updated_at}`",
                "",
            ]
        )
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
