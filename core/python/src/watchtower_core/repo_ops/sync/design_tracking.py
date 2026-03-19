"""Deterministic rebuild helpers for the human-readable design tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.adapters import render_repo_link
from watchtower_core.repo_ops.sync.tracking_common import (
    RenderedTrackingSyncService,
    active_entries_for_trace_status,
    initiative_status_for_trace_id,
    initiative_status_map,
    latest_updated_at_for_entries,
    terminal_entries_for_trace_status,
)

DESIGN_TRACKING_DOCUMENT_PATH = "docs/planning/design/design_tracking.md"
DESIGN_TRACKING_SURFACE_ID = "rendered.design_tracking"


@dataclass(frozen=True, slots=True)
class DesignTrackingBuildResult:
    """Generated design-tracking document plus family counts."""

    content: str
    feature_design_count: int
    implementation_plan_count: int


class DesignTrackingSyncService(RenderedTrackingSyncService):
    """Build and write the human-readable design tracker from the design index."""

    DOCUMENT_PATH = DESIGN_TRACKING_DOCUMENT_PATH
    SURFACE_ID = DESIGN_TRACKING_SURFACE_ID

    def build_document(self) -> DesignTrackingBuildResult:
        design_index = self._loader.load_design_document_index()
        trace_statuses = initiative_status_map(self._loader)
        feature_designs = tuple(
            entry for entry in design_index.entries if entry.family == "feature_design"
        )
        implementation_plans = tuple(
            entry for entry in design_index.entries if entry.family == "implementation_plan"
        )
        active_feature_designs = active_entries_for_trace_status(
            feature_designs,
            trace_statuses,
        )
        terminal_feature_designs = terminal_entries_for_trace_status(
            feature_designs,
            trace_statuses,
        )
        active_implementation_plans = active_entries_for_trace_status(
            implementation_plans,
            trace_statuses,
        )
        terminal_implementation_plans = terminal_entries_for_trace_status(
            implementation_plans,
            trace_statuses,
        )
        content = self._render_tracking_document(
            {
                "active_feature_designs": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "document_id": entry.document_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": initiative_status_for_trace_id(
                            entry.trace_id,
                            trace_statuses,
                        ),
                        "summary": entry.summary,
                        "linked_plans": "; ".join(
                            render_repo_link(path, label=Path(path).name)
                            for path in entry.related_paths
                            if "/design/implementation/" in path
                        )
                        or "-",
                        "notes": entry.notes or "-",
                    }
                    for entry in active_feature_designs
                ),
                "include_feature_design_notes": any(entry.notes for entry in feature_designs),
                "active_implementation_plans": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "document_id": entry.document_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": initiative_status_for_trace_id(
                            entry.trace_id,
                            trace_statuses,
                        ),
                        "summary": entry.summary,
                        "sources": "; ".join(
                            render_repo_link(path, label=Path(path).name)
                            for path in entry.source_paths
                        )
                        or "-",
                        "notes": entry.notes or "-",
                    }
                    for entry in active_implementation_plans
                ),
                "include_implementation_plan_notes": any(
                    entry.notes for entry in implementation_plans
                ),
                "terminal_feature_designs": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "document_id": entry.document_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": initiative_status_for_trace_id(
                            entry.trace_id,
                            trace_statuses,
                        ),
                        "summary": entry.summary,
                        "linked_plans": "; ".join(
                            render_repo_link(path, label=Path(path).name)
                            for path in entry.related_paths
                            if "/design/implementation/" in path
                        )
                        or "-",
                        "notes": entry.notes or "-",
                    }
                    for entry in terminal_feature_designs
                ),
                "terminal_implementation_plans": tuple(
                    {
                        "trace_id": entry.trace_id,
                        "document_id": entry.document_id,
                        "doc_path": entry.doc_path,
                        "initiative_status": initiative_status_for_trace_id(
                            entry.trace_id,
                            trace_statuses,
                        ),
                        "summary": entry.summary,
                        "sources": "; ".join(
                            render_repo_link(path, label=Path(path).name)
                            for path in entry.source_paths
                        )
                        or "-",
                        "notes": entry.notes or "-",
                    }
                    for entry in terminal_implementation_plans
                ),
                "updated_at": latest_updated_at_for_entries(design_index.entries),
            },
        )
        return DesignTrackingBuildResult(
            content=content,
            feature_design_count=len(feature_designs),
            implementation_plan_count=len(implementation_plans),
        )
