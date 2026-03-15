"""Private helpers for compact planning projection serialization."""

from __future__ import annotations

from collections.abc import Callable


def _sequence_payload(
    values: tuple[str, ...],
    *,
    compact: bool,
) -> list[str] | None:
    if compact and not values:
        return None
    return list(values)


def _assign_sequence(
    payload: dict[str, object],
    key: str,
    values: tuple[str, ...],
    *,
    compact: bool,
) -> None:
    rendered = _sequence_payload(values, compact=compact)
    if rendered is None:
        return
    payload[key] = rendered


def _assign_scalar(
    payload: dict[str, object],
    key: str,
    value: object,
    *,
    compact: bool,
) -> None:
    if compact and value is None:
        return
    payload[key] = value


def _assign_serialized_collection[TSerializable](
    payload: dict[str, object],
    key: str,
    values: tuple[TSerializable, ...],
    *,
    compact: bool,
    serializer: Callable[[TSerializable], dict[str, object]],
) -> None:
    if compact and not values:
        return
    payload[key] = [serializer(item) for item in values]
