"""Path helpers for the local repository and control-plane surfaces."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.errors import RepoRootNotFoundError


def discover_repo_root(start: Path | None = None) -> Path:
    """Discover the repository root from a starting path."""
    candidate = start.resolve() if start is not None else Path(__file__).resolve()
    search_root = candidate if candidate.is_dir() else candidate.parent

    for parent in (search_root, *search_root.parents):
        if (parent / "core/control_plane").is_dir() and (parent / "core/python").is_dir():
            return parent

    raise RepoRootNotFoundError(
        "Could not discover the repository root from the current Python workspace."
    )


def control_plane_path(repo_root: Path, relative_path: str) -> Path:
    """Resolve a repository-relative control-plane path."""
    return repo_root / relative_path
