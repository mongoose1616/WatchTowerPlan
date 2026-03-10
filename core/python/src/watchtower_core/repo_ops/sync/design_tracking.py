"""Deterministic rebuild helpers for the human-readable design tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import initiative_status_map, latest_timestamp

DESIGN_TRACKING_DOCUMENT_PATH = "docs/planning/design/design_tracking.md"


@dataclass(frozen=True, slots=True)
class DesignTrackingBuildResult:
    """Generated design-tracking document plus family counts."""

    content: str
    feature_design_count: int
    implementation_plan_count: int


class DesignTrackingSyncService:
    """Build and write the human-readable design tracker from the design index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> DesignTrackingSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> DesignTrackingBuildResult:
        design_index = self._loader.load_design_document_index()
        trace_statuses = initiative_status_map(self._loader)
        updated_at = latest_timestamp(tuple(entry.updated_at for entry in design_index.entries))
        feature_designs = tuple(
            entry for entry in design_index.entries if entry.family == "feature_design"
        )
        implementation_plans = tuple(
            entry for entry in design_index.entries if entry.family == "implementation_plan"
        )

        lines = [
            "# Design Tracking",
            "",
            "## Summary",
            (
                "This document provides the human-readable tracking view for the "
                "current design documents under `docs/planning/design/`. Use it "
                "to see which feature designs exist, which implementation plans "
                "are active, and how those documents relate to one another."
            ),
            "",
            "## Feature Designs",
            "| Trace ID | Initiative Status | Path | Summary | Linked Plans | Notes |",
            "|---|---|---|---|---|---|",
        ]
        if not feature_designs:
            lines.append(
                "| `None` | `None` | `None` | No feature designs are currently "
                "tracked. | `None` | `None` |"
            )
        else:
            for entry in feature_designs:
                initiative_status = trace_statuses.get(entry.trace_id, "active")
                linked_plans = "; ".join(
                    path for path in entry.related_paths if "/design/implementation/" in path
                ) or "None"
                notes = entry.notes or "None"
                lines.append(
                    "| "
                    f"`{entry.trace_id}` | `{initiative_status}` | `{entry.doc_path}` | "
                    f"{entry.summary} | `{linked_plans}` | {notes} |"
                )

        lines.extend(
            [
                "",
                "## Implementation Plans",
                "| Trace ID | Initiative Status | Path | Summary | Source Designs | Notes |",
                "|---|---|---|---|---|---|",
            ]
        )
        if not implementation_plans:
            lines.append(
                "| `None` | `None` | `None` | No implementation plans are "
                "currently tracked. | `None` | `None` |"
            )
        else:
            for entry in implementation_plans:
                initiative_status = trace_statuses.get(entry.trace_id, "active")
                sources = "; ".join(entry.source_paths) or "None"
                notes = entry.notes or "None"
                lines.append(
                    "| "
                    f"`{entry.trace_id}` | `{initiative_status}` | `{entry.doc_path}` | "
                    f"{entry.summary} | `{sources}` | {notes} |"
                )

        lines.extend(
            [
                "",
                "## Update Rules",
                (
                    "- Rebuild this tracker in the same change set when a design "
                    "document or implementation plan is added, renamed, removed, "
                    "materially retargeted, or when a trace initiative changes "
                    "closeout state."
                ),
                (
                    "- Keep the machine-readable companion index at "
                    "[design_document_index.v1.json](/home/j/WatchTowerPlan/core/"
                    "control_plane/indexes/design_documents/design_document_index.v1.json) "
                    "aligned with this tracker."
                ),
                (
                    "- Treat the unified traceability index at "
                    "[traceability_index.v1.json](/home/j/WatchTowerPlan/core/"
                    "control_plane/indexes/traceability/traceability_index.v1.json) "
                    "as the source for initiative closeout status."
                ),
                "",
                "## References",
                "- [README.md](/home/j/WatchTowerPlan/docs/planning/design/README.md)",
                (
                    "- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/documentation/feature_design_md_standard.md)"
                ),
                (
                    "- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/"
                    "docs/standards/documentation/implementation_plan_md_standard.md)"
                ),
                (
                    "- [design_document_index_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/data_contracts/design_document_index_standard.md)"
                ),
                "",
                "## Updated At",
                f"- `{updated_at}`",
                "",
            ]
        )
        return DesignTrackingBuildResult(
            content="\n".join(lines),
            feature_design_count=len(feature_designs),
            implementation_plan_count=len(implementation_plans),
        )

    def write_document(
        self,
        result: DesignTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write the generated design tracker to disk."""
        target = destination or (self._repo_root / DESIGN_TRACKING_DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target
