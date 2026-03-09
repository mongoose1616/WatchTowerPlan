"""UTC timestamp helpers shared across command and sync surfaces."""

from __future__ import annotations

from datetime import UTC, datetime


def utc_timestamp_now() -> str:
    """Return the current RFC 3339 UTC timestamp without fractional seconds."""
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
