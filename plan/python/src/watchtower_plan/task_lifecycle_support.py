"""Shared helpers for initiative-local live task lifecycle operations."""

from __future__ import annotations

from collections.abc import Iterable

from watchtower_core.control_plane.path_ids import PlanPathIdHelper

TASK_STATUS_CHOICES = (
    "planned",
    "ready",
    "in_progress",
    "blocked",
    "in_review",
    "completed",
    "cancelled",
)
TASK_KIND_CHOICES = (
    "feature",
    "bug",
    "chore",
    "documentation",
    "governance",
    "research",
    "validation",
)
TASK_PRIORITY_CHOICES = ("critical", "high", "medium", "low")


def normalize_required_string(value: str, *, label: str) -> str:
    """Validate and normalize one required non-empty string."""

    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{label} must be a non-empty string.")
    return normalized


def normalize_choice(value: str, allowed: tuple[str, ...], *, label: str) -> str:
    """Validate and normalize one required enum value."""

    normalized = normalize_required_string(value, label=label)
    if normalized not in allowed:
        joined = ", ".join(allowed)
        raise ValueError(f"{label} must be one of: {joined}")
    return normalized


def pick_choice(
    value: str | None,
    *,
    current: str,
    allowed: tuple[str, ...],
    label: str,
) -> str:
    """Return the current enum value or a normalized replacement."""

    if value is None:
        return current
    return normalize_choice(value, allowed, label=label)


def pick_string(value: str | None, *, current: str, label: str) -> str:
    """Return the current string or a normalized replacement."""

    if value is None:
        return current
    return normalize_required_string(value, label=label)


def normalize_list(values: Iterable[str]) -> tuple[str, ...]:
    """Normalize a list of unique non-empty strings while preserving order."""

    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        candidate = normalize_required_string(value, label="list item")
        if candidate in seen:
            continue
        seen.add(candidate)
        normalized.append(candidate)
    return tuple(normalized)


def apply_optional_list_field(
    front_matter: dict[str, object],
    key: str,
    *,
    values: tuple[str, ...] | None,
    clear: bool,
) -> bool:
    """Update or clear one optional list-valued field."""

    if clear:
        if key in front_matter:
            del front_matter[key]
            return True
        return False
    if values is None:
        return False
    normalized = normalize_list(values)
    if not normalized:
        if key in front_matter:
            del front_matter[key]
            return True
        return False
    existing_values = front_matter.get(key)
    current_values = tuple(existing_values) if isinstance(existing_values, list) else ()
    if current_values != normalized:
        front_matter[key] = list(normalized)
        return True
    return False


def slugify_file_stem(value: str) -> str:
    """Normalize one task title or file stem into a repo-safe filename."""

    return PlanPathIdHelper.slugify(value, label="task file stem")
