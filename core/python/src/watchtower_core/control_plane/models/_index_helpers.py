"""Private explicit helpers for typed control-plane index models."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast


def tuple_field(document: dict[str, Any], key: str) -> tuple[str, ...]:
    """Return one optional tuple-of-string field from a raw document."""

    values = document.get(key, ())
    return tuple(cast(tuple[str, ...] | list[str], values))


def load_entries[TEntry](
    document: dict[str, Any],
    entry_builder: Callable[[dict[str, Any]], TEntry],
) -> tuple[TEntry, ...]:
    """Materialize typed index entries from one raw governed artifact."""

    raw_entries = cast(tuple[dict[str, Any], ...] | list[dict[str, Any]], document["entries"])
    return tuple(entry_builder(entry) for entry in raw_entries)


def index_metadata(document: dict[str, Any]) -> tuple[str, str, str, str]:
    """Return the shared top-level metadata carried by typed index artifacts."""

    return (
        cast(str, document["$schema"]),
        cast(str, document["id"]),
        cast(str, document["title"]),
        cast(str, document["status"]),
    )


def get_entry_by_attr[TEntry](
    entries: tuple[TEntry, ...],
    *,
    attr_name: str,
    value: str,
) -> TEntry:
    """Return one typed entry by a stable identifier attribute."""

    for entry in entries:
        if getattr(entry, attr_name) == value:
            return entry
    raise KeyError(value)
