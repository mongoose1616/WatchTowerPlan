"""Shared repo-path filtering helpers for sync and traceability services."""

from __future__ import annotations

from pathlib import Path, PurePosixPath


def path_exists(repo_root: Path, relative_path: str) -> bool:
    """Return whether one repo-relative path currently exists."""

    candidate = relative_path.rstrip("/")
    if not candidate:
        return False
    normalized = PurePosixPath(candidate)
    if normalized.is_absolute() or ".." in normalized.parts:
        return False
    return (repo_root / normalized).exists()


def add_existing_paths(repo_root: Path, destination: set[str], values: tuple[str, ...]) -> None:
    """Add existing repo-relative paths to a destination set."""

    for value in values:
        if path_exists(repo_root, value):
            destination.add(value)


def existing_paths(repo_root: Path, values: tuple[str, ...]) -> tuple[str, ...]:
    """Return the existing repo-relative paths from one ordered value set."""

    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen or not path_exists(repo_root, value):
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)
