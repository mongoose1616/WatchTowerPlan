"""Shared helpers for generated human-readable planning trackers."""

from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader


def initiative_status_map(loader: ControlPlaneLoader) -> dict[str, str]:
    """Return initiative-status values keyed by trace ID."""
    index = loader.load_traceability_index()
    return {entry.trace_id: entry.initiative_status for entry in index.entries}


def latest_timestamp(values: tuple[str, ...]) -> str:
    """Return the latest timestamp from a non-empty or empty timestamp tuple."""
    return max(values) if values else "None"
