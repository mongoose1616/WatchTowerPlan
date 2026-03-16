"""Deterministic rebuild helpers for the human-readable design tracker."""

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
        active_feature_designs = tuple(
            entry
            for entry in feature_designs
            if trace_statuses.get(entry.trace_id, ACTIVE_INITIATIVE_STATUS)
            == ACTIVE_INITIATIVE_STATUS
        )
        implementation_plans = tuple(
            entry for entry in design_index.entries if entry.family == "implementation_plan"
        )
        active_implementation_plans = tuple(
            entry
            for entry in implementation_plans
            if trace_statuses.get(entry.trace_id, ACTIVE_INITIATIVE_STATUS)
            == ACTIVE_INITIATIVE_STATUS
        )
        terminal_counts = terminal_initiative_status_counts_for_trace_ids(
            tuple(entry.trace_id for entry in design_index.entries),
            trace_statuses,
        )
        feature_design_has_notes = any(entry.notes for entry in feature_designs)
        implementation_plan_has_notes = any(entry.notes for entry in implementation_plans)

        lines = ["# Design Tracking", "", "## Active Feature Designs"]
        if not active_feature_designs:
            lines.append(
                "_No active feature designs. Use `watchtower-core query designs "
                "--trace-id <trace_id>` for one known trace or "
                "`watchtower-core query initiatives --initiative-status <status> "
                "--format json` for terminal trace browse._"
            )
        else:
            feature_rows: list[tuple[str, ...]] = []
            for entry in active_feature_designs:
                initiative_status = trace_statuses.get(entry.trace_id, "active")
                linked_plans = "; ".join(
                    markdown_repo_link(self._repo_root, path, label=Path(path).name)
                    for path in entry.related_paths
                    if "/design/implementation/" in path
                ) or "-"
                row = [
                    f"`{entry.trace_id}`",
                    markdown_repo_link(
                        self._repo_root,
                        entry.doc_path,
                        label=entry.document_id,
                    ),
                    f"`{initiative_status}`",
                    entry.summary,
                    linked_plans,
                ]
                if feature_design_has_notes:
                    row.append(entry.notes or "-")
                feature_rows.append(tuple(row))
            feature_headers = ["Trace ID", "Design", "Status", "Summary", "Linked Plans"]
            if feature_design_has_notes:
                feature_headers.append("Notes")
            lines.extend(render_markdown_table(tuple(feature_headers), tuple(feature_rows)))

        lines.extend(["", "## Active Implementation Plans"])
        if not active_implementation_plans:
            lines.append(
                "_No active implementation plans. Use `watchtower-core query designs "
                "--family implementation_plan --trace-id <trace_id>` for one known trace "
                "or `watchtower-core query initiatives --initiative-status <status> "
                "--format json` for terminal trace browse._"
            )
        else:
            implementation_rows: list[tuple[str, ...]] = []
            for entry in active_implementation_plans:
                initiative_status = trace_statuses.get(entry.trace_id, "active")
                sources = "; ".join(
                    markdown_repo_link(self._repo_root, path, label=Path(path).name)
                    for path in entry.source_paths
                ) or "-"
                row = [
                    f"`{entry.trace_id}`",
                    markdown_repo_link(
                        self._repo_root,
                        entry.doc_path,
                        label=entry.document_id,
                    ),
                    f"`{initiative_status}`",
                    entry.summary,
                    sources,
                ]
                if implementation_plan_has_notes:
                    row.append(entry.notes or "-")
                implementation_rows.append(tuple(row))
            implementation_headers = [
                "Trace ID",
                "Plan",
                "Status",
                "Summary",
                "Sources",
            ]
            if implementation_plan_has_notes:
                implementation_headers.append("Notes")
            lines.extend(
                render_markdown_table(
                    tuple(implementation_headers),
                    tuple(implementation_rows),
                )
            )

        lines.extend(
            [
                "",
                "## Terminal History",
                *render_bullet_summary(
                    terminal_counts,
                    empty_message="_No terminal design traces._",
                ),
                "",
                "Use `watchtower-core query initiatives --initiative-status <status> "
                "--format json` for terminal trace browse and "
                "`watchtower-core query designs --trace-id <trace_id>` for one known design trace.",
            ]
        )

        lines.extend(["", f"_Updated At: `{updated_at}`_", ""])
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
