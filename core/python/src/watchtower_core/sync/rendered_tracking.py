"""Generic helpers for rendered tracking surfaces owned by hosted packs."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import ClassVar, Protocol

from watchtower_core.adapters import render_rendered_surface
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root

ACTIVE_INITIATIVE_STATUS = "active"
TERMINAL_INITIATIVE_STATUSES = (
    "completed",
    "cancelled",
    "superseded",
    "abandoned",
)


class RenderedTrackingBuildResult(Protocol):
    """Minimal build-result contract for shared tracker document writes."""

    content: str


class TraceTrackedEntry(Protocol):
    """Entry contract for helpers that reason about initiative trace state."""

    trace_id: str


class UpdatedEntry(Protocol):
    """Entry contract for helpers that derive an updated-at summary."""

    updated_at: str


class RenderedTrackingSyncService:
    """Shared bootstrap and write helpers for rendered tracking documents."""

    DOCUMENT_PATH: ClassVar[str]
    SURFACE_ID: ClassVar[str]

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None):
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def _render_tracking_document(self, context: Mapping[str, object]) -> str:
        surface = self._loader.load_rendered_surface_registry().get(self.SURFACE_ID)
        return render_rendered_surface(surface, context)

    def write_document(
        self,
        result: RenderedTrackingBuildResult,
        destination: Path | None = None,
    ) -> Path:
        """Write one generated tracking document to disk."""

        target = destination or (self._repo_root / self.DOCUMENT_PATH)
        target.write_text(result.content, encoding="utf-8")
        return target


def initiative_status_map(loader: ControlPlaneLoader) -> dict[str, str]:
    """Return initiative-status values keyed by trace ID."""

    index = loader.load_traceability_index()
    return {entry.trace_id: entry.initiative_status for entry in index.entries}


def terminal_initiative_status_counts_for_trace_ids(
    trace_ids: tuple[str, ...],
    trace_statuses: Mapping[str, str],
) -> tuple[tuple[str, int], ...]:
    """Return non-zero initiative terminal-status counts by unique trace ID."""

    counts: Counter[str] = Counter()
    seen_trace_ids: set[str] = set()

    for trace_id in trace_ids:
        if trace_id in seen_trace_ids:
            continue
        seen_trace_ids.add(trace_id)
        status = trace_statuses.get(trace_id, ACTIVE_INITIATIVE_STATUS)
        if status in TERMINAL_INITIATIVE_STATUSES:
            counts[status] += 1

    return tuple(
        (status, counts[status])
        for status in TERMINAL_INITIATIVE_STATUSES
        if counts[status] > 0
    )


def latest_timestamp(values: tuple[str, ...]) -> str:
    """Return the latest timestamp from a non-empty or empty timestamp tuple."""

    return max(values) if values else "None"


def initiative_status_for_trace_id(
    trace_id: str,
    trace_statuses: Mapping[str, str],
) -> str:
    """Return the effective initiative status for one trace ID."""

    return trace_statuses.get(trace_id, ACTIVE_INITIATIVE_STATUS)


def active_entries_for_trace_status[EntryT: TraceTrackedEntry](
    entries: Iterable[EntryT],
    trace_statuses: Mapping[str, str],
) -> tuple[EntryT, ...]:
    """Return entries whose initiatives are still active."""

    return tuple(
        entry
        for entry in entries
        if initiative_status_for_trace_id(entry.trace_id, trace_statuses)
        == ACTIVE_INITIATIVE_STATUS
    )


def terminal_entries_for_trace_status[EntryT: TraceTrackedEntry](
    entries: Iterable[EntryT],
    trace_statuses: Mapping[str, str],
) -> tuple[EntryT, ...]:
    """Return entries whose initiatives are no longer active."""

    return tuple(
        entry
        for entry in entries
        if initiative_status_for_trace_id(entry.trace_id, trace_statuses)
        != ACTIVE_INITIATIVE_STATUS
    )


def terminal_count_rows_for_entries(
    entries: Iterable[TraceTrackedEntry],
    trace_statuses: Mapping[str, str],
) -> tuple[dict[str, str | int], ...]:
    """Return rendered payload rows for terminal initiative counts."""

    return tuple(
        {"label": label, "count": count}
        for label, count in terminal_initiative_status_counts_for_trace_ids(
            tuple(entry.trace_id for entry in entries),
            trace_statuses,
        )
    )


def latest_updated_at_for_entries(entries: Iterable[UpdatedEntry]) -> str:
    """Return the latest updated-at value across a collection of entries."""

    return latest_timestamp(tuple(entry.updated_at for entry in entries))


def effective_updated_at(updated_at: str, closed_at: str | None = None) -> str:
    """Return the effective update timestamp, treating closeout as a state change."""

    if closed_at and closed_at > updated_at:
        return closed_at
    return updated_at


__all__ = [
    "ACTIVE_INITIATIVE_STATUS",
    "RenderedTrackingBuildResult",
    "RenderedTrackingSyncService",
    "TERMINAL_INITIATIVE_STATUSES",
    "TraceTrackedEntry",
    "UpdatedEntry",
    "active_entries_for_trace_status",
    "effective_updated_at",
    "initiative_status_for_trace_id",
    "initiative_status_map",
    "latest_timestamp",
    "latest_updated_at_for_entries",
    "terminal_count_rows_for_entries",
    "terminal_entries_for_trace_status",
    "terminal_initiative_status_counts_for_trace_ids",
]
