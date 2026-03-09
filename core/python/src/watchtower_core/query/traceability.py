"""Index-backed query helpers for traceability records."""

from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import TraceabilityEntry


class TraceabilityQueryService:
    """Resolve traceability entries by trace identifier."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def get(self, trace_id: str) -> TraceabilityEntry:
        """Return the traceability entry for the requested trace identifier."""
        index = self._loader.load_traceability_index()
        return index.get(trace_id)
