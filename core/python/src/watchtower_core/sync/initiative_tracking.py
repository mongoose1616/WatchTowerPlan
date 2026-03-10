"""Deterministic rebuild helpers for the human-readable initiative tracker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.sync.initiative_index import PHASE_ORDER
from watchtower_core.sync.tracking_common import latest_timestamp

INITIATIVE_TRACKING_DOCUMENT_PATH = "docs/planning/initiatives/initiative_tracking.md"


@dataclass(frozen=True, slots=True)
class InitiativeTrackingBuildResult:
    """Generated initiative-tracking document plus initiative counts."""

    content: str
    initiative_count: int
    active_count: int
    closed_count: int


class InitiativeTrackingSyncService:
    """Build and write the human-readable initiative tracker from the initiative index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> InitiativeTrackingSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> InitiativeTrackingBuildResult:
        initiative_index = self._loader.load_initiative_index()
        updated_at = latest_timestamp(tuple(entry.updated_at for entry in initiative_index.entries))
        active_entries = tuple(
            sorted(
                (
                    entry
                    for entry in initiative_index.entries
                    if entry.initiative_status == "active"
                ),
                key=lambda entry: (PHASE_ORDER.get(entry.current_phase, 999), entry.trace_id),
            )
        )
        closed_entries = tuple(
            sorted(
                (
                    entry
                    for entry in initiative_index.entries
                    if entry.initiative_status != "active"
                ),
                key=lambda entry: (entry.closed_at or entry.updated_at, entry.trace_id),
                reverse=True,
            )
        )

        lines = [
            "# Initiative Tracking",
            "",
            "## Summary",
            (
                "This document provides the human-readable start-here view for traced "
                "initiatives across PRDs, decisions, designs, implementation plans, tasks, "
                "validation, and closeout. Use it when the main question is what phase an "
                "initiative is in, who is currently working on it, and what should happen next."
            ),
            "",
            "## Active Initiatives",
            "| Trace ID | Phase | Owners | Open Tasks | Key Surface | Next Surface | Next Action |",
            "|---|---|---|---|---|---|---|",
        ]
        if not active_entries:
            lines.append(
                "| `None` | `None` | `None` | `0` | `None` | `None` | "
                "No active initiatives are currently tracked. |"
            )
        else:
            for entry in active_entries:
                owners = ", ".join(entry.active_owners) if entry.active_owners else "unassigned"
                task_summary = f"`{entry.open_task_count}`"
                if entry.blocked_task_count:
                    task_summary = (
                        f"`{entry.open_task_count}` "
                        f"(`blocked={entry.blocked_task_count}`)"
                    )
                lines.append(
                    "| "
                    f"`{entry.trace_id}` | `{entry.current_phase}` | {owners} | {task_summary} | "
                    f"`{entry.key_surface_path}` | "
                    f"`{entry.next_surface_path}` | {entry.next_action} |"
                )

        lines.extend(
            [
                "",
                "## Closed Initiatives",
                "| Trace ID | Initiative Status | Key Surface | Closed At | Closure Reason |",
                "|---|---|---|---|---|",
            ]
        )
        if not closed_entries:
            lines.append(
                "| `None` | `None` | `None` | `None` | "
                "No closed initiatives are currently tracked. |"
            )
        else:
            for entry in closed_entries:
                closure_reason = entry.closure_reason or "None"
                closed_at = entry.closed_at or "None"
                lines.append(
                    "| "
                    f"`{entry.trace_id}` | `{entry.initiative_status}` | "
                    f"`{entry.key_surface_path}` | "
                    f"`{closed_at}` | {closure_reason} |"
                )

        lines.extend(
            [
                "",
                "## Update Rules",
                (
                    "- Treat the unified traceability index, family-specific planning indexes, "
                    "and task index as the authoritative source surfaces for this tracker."
                ),
                (
                    "- Rebuild this tracker in the same change set when traced planning, task, "
                    "validation, or closeout state changes materially."
                ),
                (
                    "- Use this tracker as the start-here cross-family initiative view, and use "
                    "the PRD, decision, design, and task trackers as local family views."
                ),
                (
                    "- Keep the machine-readable companion index at "
                    "[initiative_index.v1.json]"
                    "(/home/j/WatchTowerPlan/core/control_plane/indexes/initiatives/"
                    "initiative_index.v1.json) "
                    "aligned with this tracker."
                ),
                "",
                "## References",
                "- [README.md](/home/j/WatchTowerPlan/docs/planning/initiatives/README.md)",
                (
                    "- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/governance/initiative_tracking_standard.md)"
                ),
                (
                    "- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/"
                    "standards/data_contracts/initiative_index_standard.md)"
                ),
                (
                    "- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/"
                    "governance/traceability_standard.md)"
                ),
                (
                    "- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/"
                    "governance/task_tracking_standard.md)"
                ),
                "",
                "## Updated At",
                f"- `{updated_at}`",
                "",
            ]
        )
        return InitiativeTrackingBuildResult(
            content="\n".join(lines),
            initiative_count=len(initiative_index.entries),
            active_count=len(active_entries),
            closed_count=len(closed_entries),
        )

    def write_document(
        self,
        result: InitiativeTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write the generated initiative tracker to disk."""
        target = destination or (self._repo_root / INITIATIVE_TRACKING_DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target
