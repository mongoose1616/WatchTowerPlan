"""Shared helpers for generated human-readable planning trackers."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader

ACTIVE_INITIATIVE_STATUS = "active"
TERMINAL_INITIATIVE_STATUSES = (
    "completed",
    "cancelled",
    "superseded",
    "abandoned",
)


def initiative_status_map(loader: ControlPlaneLoader) -> dict[str, str]:
    """Return initiative-status values keyed by trace ID."""
    index = loader.load_traceability_index()
    return {entry.trace_id: entry.initiative_status for entry in index.entries}


def terminal_initiative_status_counts_for_trace_ids(
    trace_ids: tuple[str, ...],
    trace_statuses: Mapping[str, str],
) -> tuple[tuple[str, int], ...]:
    """Return non-zero initiative terminal-status counts by unique trace ID."""
    counts = Counter()
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


def effective_updated_at(updated_at: str, closed_at: str | None = None) -> str:
    """Return the effective update timestamp, treating closeout as a state change."""
    if closed_at and closed_at > updated_at:
        return closed_at
    return updated_at


def markdown_repo_link(repo_root: Path, relative_path: str, *, label: str) -> str:
    """Return one repository-local Markdown link for a tracker cell."""
    return f"[{label}]({repo_root / relative_path})"


def render_markdown_table(
    headers: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
) -> tuple[str, ...]:
    """Render one Markdown table from headers and rows."""
    separator = tuple("---" for _ in headers)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return tuple(lines)


def render_bullet_summary(
    items: tuple[tuple[str, int], ...],
    *,
    empty_message: str,
) -> tuple[str, ...]:
    """Render one compact bullet summary from labeled integer counts."""
    if not items:
        return (empty_message,)
    return tuple(f"- `{label}`: {count}" for label, count in items)
