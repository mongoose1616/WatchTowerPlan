"""Deterministic rebuild helpers for the human-readable design tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import render_rendered_surface, render_repo_link
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.sync.tracking_common import (
    ACTIVE_INITIATIVE_STATUS,
    initiative_status_map,
    latest_timestamp,
    terminal_initiative_status_counts_for_trace_ids,
)

DESIGN_TRACKING_DOCUMENT_PATH = "docs/planning/design/design_tracking.md"
DESIGN_TRACKING_SURFACE_ID = "rendered.design_tracking"


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
        feature_designs = tuple(
            entry for entry in design_index.entries if entry.family == "feature_design"
        )
        implementation_plans = tuple(
            entry for entry in design_index.entries if entry.family == "implementation_plan"
        )
        surface = self._loader.load_rendered_surface_registry().get(
            DESIGN_TRACKING_SURFACE_ID
        )
        content = render_rendered_surface(
            surface,
            {
                "active_feature_designs": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "document_id": entry.document_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": trace_statuses.get(entry.trace_id, "active"),
                        "summary": entry.summary,
                        "linked_plans": "; ".join(
                            render_repo_link(path, label=Path(path).name)
                            for path in entry.related_paths
                            if "/design/implementation/" in path
                        )
                        or "-",
                        "notes": entry.notes or "-",
                    }
                    for entry in feature_designs
                    if trace_statuses.get(entry.trace_id, ACTIVE_INITIATIVE_STATUS)
                    == ACTIVE_INITIATIVE_STATUS
                ),
                "include_feature_design_notes": any(entry.notes for entry in feature_designs),
                "active_implementation_plans": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "document_id": entry.document_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": trace_statuses.get(entry.trace_id, "active"),
                        "summary": entry.summary,
                        "sources": "; ".join(
                            render_repo_link(path, label=Path(path).name)
                            for path in entry.source_paths
                        )
                        or "-",
                        "notes": entry.notes or "-",
                    }
                    for entry in implementation_plans
                    if trace_statuses.get(entry.trace_id, ACTIVE_INITIATIVE_STATUS)
                    == ACTIVE_INITIATIVE_STATUS
                ),
                "include_implementation_plan_notes": any(
                    entry.notes for entry in implementation_plans
                ),
                "terminal_counts": tuple(
                    {"label": label, "count": count}
                    for label, count in terminal_initiative_status_counts_for_trace_ids(
                        tuple(entry.trace_id for entry in design_index.entries),
                        trace_statuses,
                    )
                ),
                "terminal_history_notes": (
                    "Use `watchtower-core query initiatives --initiative-status <status> "
                    "--format json` for terminal trace browse and "
                    "`watchtower-core query designs --trace-id <trace_id>` "
                    "for one known design trace.",
                ),
                "updated_at": latest_timestamp(
                    tuple(entry.updated_at for entry in design_index.entries)
                ),
            },
        )
        return DesignTrackingBuildResult(
            content=content,
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
