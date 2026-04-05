"""Generic NDJSON event stream engine for governed append-only event records."""

from __future__ import annotations

from watchtower_core.event_stream.engine import (
    EventStreamConfig,
    NdjsonEventStream,
)

__all__ = [
    "EventStreamConfig",
    "NdjsonEventStream",
]
