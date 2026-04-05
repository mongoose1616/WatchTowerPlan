"""Path helpers for the local repository and control-plane surfaces."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.errors import RepoRootNotFoundError


def _find_repo_root(candidate: Path) -> Path | None:
    """Return the enclosing repo root for one starting path when present."""
    search_root = candidate if candidate.is_dir() else candidate.parent

    for parent in (search_root, *search_root.parents):
        if (parent / "core/control_plane").is_dir() and (parent / "core/python").is_dir():
            return parent
    return None


def discover_repo_root(
    start: Path | None = None,
    *,
    allow_package_checkout_fallback: bool = False,
) -> Path:
    """Discover the repository root from a starting path.

    By default the discovery must succeed from the caller's current worktree.
    The package-checkout fallback is opt-in because it can silently bind a
    long-lived process to the wrong repository checkout.
    """
    candidates: tuple[Path, ...]
    if start is not None:
        candidates = (start.resolve(),)
    else:
        candidates = (
            (Path.cwd().resolve(), Path(__file__).resolve())
            if allow_package_checkout_fallback
            else (Path.cwd().resolve(),)
        )
    for candidate in candidates:
        repo_root = _find_repo_root(candidate)
        if repo_root is not None:
            return repo_root

    raise RepoRootNotFoundError(
        "Could not discover the repository root from the current Python workspace."
    )


def control_plane_path(repo_root: Path, relative_path: str) -> Path:
    """Resolve a repository-relative control-plane path."""
    return repo_root / relative_path
