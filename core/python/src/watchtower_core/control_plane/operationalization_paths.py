"""Reusable repository-path matching helpers for operationalization entries."""

from __future__ import annotations

from glob import has_magic
from pathlib import Path, PurePosixPath


def operationalization_path_matches(
    requested_path: str,
    indexed_path: str,
    repo_root: Path,
) -> bool:
    """Return whether one concrete path matches one indexed operationalization entry."""

    normalized_requested = requested_path.casefold()
    normalized_indexed = indexed_path.casefold()
    if normalized_requested == normalized_indexed:
        return True
    if operationalization_path_is_glob(indexed_path):
        return PurePosixPath(normalized_requested).match(normalized_indexed)
    if operationalization_path_is_directory(indexed_path, repo_root):
        directory_prefix = (
            normalized_indexed if normalized_indexed.endswith("/") else f"{normalized_indexed}/"
        )
        return normalized_requested.startswith(directory_prefix)
    return False


def operationalization_path_is_glob(indexed_path: str) -> bool:
    """Return whether one indexed operationalization entry is a glob pattern."""

    return has_magic(indexed_path)


def operationalization_path_is_directory(indexed_path: str, repo_root: Path) -> bool:
    """Return whether one indexed operationalization entry resolves to a directory."""

    if operationalization_path_is_glob(indexed_path):
        return False
    candidate = indexed_path[:-1] if indexed_path.endswith("/") else indexed_path
    resolved = repo_root / Path(candidate)
    return indexed_path.endswith("/") or resolved.is_dir()


__all__ = [
    "operationalization_path_is_directory",
    "operationalization_path_is_glob",
    "operationalization_path_matches",
]
