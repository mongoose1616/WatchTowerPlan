"""Reusable repository-path matching helpers for operationalization entries."""

from __future__ import annotations

from glob import has_magic
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.pack_settings_discovery import discover_pack_settings_paths

_PACK_PLACEHOLDER_TOKENS = ("<pack>", "<pack-root>")


def operationalization_path_matches(
    requested_path: str,
    indexed_path: str,
    repo_root: Path,
) -> bool:
    """Return whether one concrete path matches one indexed operationalization entry."""

    if operationalization_path_has_pack_placeholder(indexed_path):
        return any(
            _operationalization_path_matches_expanded(
                requested_path,
                candidate,
                repo_root,
            )
            for candidate in expand_pack_placeholder_operationalization_paths(
                indexed_path,
                repo_root,
            )
        )
    return _operationalization_path_matches_expanded(requested_path, indexed_path, repo_root)


def _operationalization_path_matches_expanded(
    requested_path: str,
    indexed_path: str,
    repo_root: Path,
) -> bool:
    """Return whether one concrete path matches one concrete indexed entry."""

    normalized_requested = requested_path.casefold()
    normalized_indexed = indexed_path.casefold()
    if normalized_requested == normalized_indexed:
        return True
    if operationalization_path_is_glob(indexed_path):
        if PurePosixPath(normalized_requested).match(normalized_indexed):
            return True
        if normalized_indexed.endswith("/"):
            return any(
                PurePosixPath(candidate).match(normalized_indexed)
                for candidate in _requested_directory_prefixes(normalized_requested)
            )
        return False
    if operationalization_path_is_directory(indexed_path, repo_root):
        directory_prefix = (
            normalized_indexed if normalized_indexed.endswith("/") else f"{normalized_indexed}/"
        )
        return normalized_requested.startswith(directory_prefix)
    return False


def _requested_directory_prefixes(requested_path: str) -> tuple[str, ...]:
    """Return directory prefixes for one requested path, deepest first."""

    stripped = requested_path.rstrip("/")
    if not stripped:
        return ()

    parts = PurePosixPath(stripped).parts
    if not parts:
        return ()

    if requested_path.endswith("/"):
        start = len(parts)
    else:
        start = len(parts) - 1
    if start <= 0:
        return ()

    return tuple(
        f"{PurePosixPath(*parts[:count]).as_posix()}/"
        for count in range(start, 0, -1)
    )


def operationalization_path_is_glob(indexed_path: str) -> bool:
    """Return whether one indexed operationalization entry is a glob pattern."""

    return has_magic(indexed_path)


def operationalization_path_has_pack_placeholder(indexed_path: str) -> bool:
    """Return whether one indexed operationalization entry uses a hosted-pack placeholder."""

    return any(token in indexed_path for token in _PACK_PLACEHOLDER_TOKENS)


def expand_pack_placeholder_operationalization_paths(
    indexed_path: str,
    repo_root: Path,
) -> tuple[str, ...]:
    """Expand one hosted-pack placeholder path into concrete current-repo pack paths."""

    if not operationalization_path_has_pack_placeholder(indexed_path):
        return (indexed_path,)

    expanded: list[str] = []
    seen: set[str] = set()
    for settings_path in discover_pack_settings_paths(repo_root):
        pack_root = Path(settings_path).parents[2].as_posix()
        candidate = indexed_path
        for token in _PACK_PLACEHOLDER_TOKENS:
            candidate = candidate.replace(token, pack_root)
        if candidate in seen:
            continue
        expanded.append(candidate)
        seen.add(candidate)
    return tuple(expanded)


def operationalization_path_is_directory(indexed_path: str, repo_root: Path) -> bool:
    """Return whether one indexed operationalization entry resolves to a directory."""

    if operationalization_path_is_glob(indexed_path):
        return False
    candidate = indexed_path[:-1] if indexed_path.endswith("/") else indexed_path
    resolved = repo_root / Path(candidate)
    return indexed_path.endswith("/") or resolved.is_dir()


__all__ = [
    "expand_pack_placeholder_operationalization_paths",
    "operationalization_path_has_pack_placeholder",
    "operationalization_path_is_directory",
    "operationalization_path_is_glob",
    "operationalization_path_matches",
]
