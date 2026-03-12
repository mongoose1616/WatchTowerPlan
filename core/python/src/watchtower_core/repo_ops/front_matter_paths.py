"""Shared helpers for canonical path-valued front-matter metadata."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from watchtower_core.adapters import normalize_repo_path_reference

_DIRECTORY_APPLIES_TO_ERROR = (
    "directory applies_to paths must use repo-relative directory paths ending in '/'"
)
_FILE_APPLIES_TO_ERROR = "file applies_to paths must not end with '/'"
_PATH_APPLIES_TO_ERROR = "path-valued applies_to entries must use canonical repo-relative paths"


def normalize_front_matter_applies_to(
    front_matter: Mapping[str, Any],
    *,
    relative_path: str,
    repo_root: Path,
) -> tuple[str, ...]:
    """Return canonical applies_to values for one governed front-matter document."""
    value = front_matter.get("applies_to")
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(f"{relative_path} front matter key applies_to must be a YAML list.")
    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{relative_path} front matter key applies_to must contain only strings."
            )
        items.append(item.strip())
    return normalize_governed_applies_to_values(
        items,
        origin=relative_path,
        repo_root=repo_root,
        enforce_canonical=True,
    )


def normalize_governed_applies_to_values(
    values: Iterable[str],
    *,
    origin: str,
    repo_root: Path,
    enforce_canonical: bool = False,
) -> tuple[str, ...]:
    """Return canonical applies_to values, optionally rejecting non-canonical input."""
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        candidate = value.strip()
        if not candidate:
            raise ValueError(f"{origin} applies_to entries must be non-empty strings.")
        canonical = _canonicalize_applies_to_value(candidate, origin=origin, repo_root=repo_root)
        if enforce_canonical and canonical != candidate:
            _raise_noncanonical_applies_to_value(
                origin=origin,
                authored=candidate,
                canonical=canonical,
                repo_root=repo_root,
            )
        if canonical in seen:
            continue
        seen.add(canonical)
        ordered.append(canonical)
    return tuple(ordered)


def applies_to_path_values(
    applies_to: Iterable[str],
    *,
    relative_path: str,
) -> tuple[str, ...]:
    """Return path-like applies_to values that are not the current document path."""
    return tuple(
        value
        for value in applies_to
        if "/" in value and value != relative_path
    )


def _canonicalize_applies_to_value(
    value: str,
    *,
    origin: str,
    repo_root: Path,
) -> str:
    if "/" not in value:
        return value

    normalized = normalize_repo_path_reference(value, repo_root)
    if normalized is None:
        raise ValueError(f"{origin} {_PATH_APPLIES_TO_ERROR}: {value}")

    resolved = repo_root / Path(normalized.rstrip("/"))
    if not resolved.exists():
        raise ValueError(f"{origin} {_PATH_APPLIES_TO_ERROR}: {value}")
    if resolved.is_dir():
        return normalized if normalized.endswith("/") else f"{normalized}/"
    return normalized.rstrip("/")


def _raise_noncanonical_applies_to_value(
    *,
    origin: str,
    authored: str,
    canonical: str,
    repo_root: Path,
) -> None:
    resolved = repo_root / Path(canonical.rstrip("/"))
    if resolved.is_dir() and authored.rstrip("/") == canonical.rstrip("/"):
        raise ValueError(f"{origin} {_DIRECTORY_APPLIES_TO_ERROR}: {authored}")
    if resolved.is_file() and authored.rstrip("/") == canonical and authored.endswith("/"):
        raise ValueError(f"{origin} {_FILE_APPLIES_TO_ERROR}: {authored}")
    raise ValueError(f"{origin} {_PATH_APPLIES_TO_ERROR}: {authored}")
