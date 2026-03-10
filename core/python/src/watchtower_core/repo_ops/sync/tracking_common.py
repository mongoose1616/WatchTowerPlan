"""Shared helpers for generated human-readable planning trackers."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader


def initiative_status_map(loader: ControlPlaneLoader) -> dict[str, str]:
    """Return initiative-status values keyed by trace ID."""
    index = loader.load_traceability_index()
    return {entry.trace_id: entry.initiative_status for entry in index.entries}


def latest_timestamp(values: tuple[str, ...]) -> str:
    """Return the latest timestamp from a non-empty or empty timestamp tuple."""
    return max(values) if values else "None"


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
