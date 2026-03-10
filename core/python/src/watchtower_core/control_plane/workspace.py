"""Workspace and artifact IO abstractions for control-plane services."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Protocol

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.paths import discover_repo_root

CONTROL_PLANE_PREFIX = "core/control_plane"
PYTHON_WORKSPACE_PREFIX = "core/python"


def _normalize_relative_path(relative_path: str) -> str:
    path = PurePosixPath(relative_path)
    if path.is_absolute():
        raise ValueError(f"Workspace paths must be repository-relative: {relative_path}")
    if not path.parts or str(path) == ".":
        raise ValueError("Workspace paths must not be empty.")
    if any(part == ".." for part in path.parts):
        raise ValueError(f"Workspace paths must not escape the workspace: {relative_path}")
    return path.as_posix()


def _load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ArtifactLoadError(f"Could not load governed artifact at {label}") from exc

    if not isinstance(loaded, dict):
        raise ArtifactLoadError(f"Expected JSON object at {label}, found {type(loaded).__name__}")
    return loaded


@dataclass(frozen=True, slots=True)
class WorkspaceConfig:
    """Filesystem mapping for the repo root plus exportable core entrypoints."""

    repo_root: Path
    control_plane_root: Path
    python_workspace_root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "repo_root", self.repo_root.resolve())
        object.__setattr__(self, "control_plane_root", self.control_plane_root.resolve())
        object.__setattr__(self, "python_workspace_root", self.python_workspace_root.resolve())

    @classmethod
    def discover(cls, start: Path | None = None) -> WorkspaceConfig:
        """Discover the current repository layout from a starting path."""
        return cls.from_repo_root(discover_repo_root(start))

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> WorkspaceConfig:
        """Construct the default workspace mapping for the current repository shape."""
        resolved_root = discover_repo_root(repo_root)
        return cls(
            repo_root=resolved_root,
            control_plane_root=resolved_root / CONTROL_PLANE_PREFIX,
            python_workspace_root=resolved_root / PYTHON_WORKSPACE_PREFIX,
        )

    def resolve_path(self, relative_path: str) -> Path:
        """Resolve one repository-relative path through the current workspace mapping."""
        normalized = _normalize_relative_path(relative_path)
        if normalized == CONTROL_PLANE_PREFIX or normalized.startswith(f"{CONTROL_PLANE_PREFIX}/"):
            suffix = normalized.removeprefix(CONTROL_PLANE_PREFIX).lstrip("/")
            return self.control_plane_root if not suffix else self.control_plane_root / suffix
        if normalized == PYTHON_WORKSPACE_PREFIX or normalized.startswith(
            f"{PYTHON_WORKSPACE_PREFIX}/"
        ):
            suffix = normalized.removeprefix(PYTHON_WORKSPACE_PREFIX).lstrip("/")
            return self.python_workspace_root if not suffix else self.python_workspace_root / suffix
        return self.repo_root / normalized

    def logical_path_for(self, path: Path) -> str:
        """Return the repository-logical path for one resolved workspace path."""
        resolved_path = path.resolve()
        candidates = (
            (self.control_plane_root, CONTROL_PLANE_PREFIX),
            (self.python_workspace_root, PYTHON_WORKSPACE_PREFIX),
            (self.repo_root, ""),
        )
        for root, prefix in candidates:
            try:
                relative = resolved_path.relative_to(root).as_posix()
            except ValueError:
                continue
            if relative == ".":
                return prefix or "."
            return f"{prefix}/{relative}" if prefix else relative
        raise ValueError(f"Path is outside the configured workspace: {path}")


class ArtifactSource(Protocol):
    """Read-only access to governed artifacts through repository-logical paths."""

    def load_json_object(self, relative_path: str) -> dict[str, Any]:
        """Load one repository-logical JSON object."""

    def iter_json_objects(self, relative_directory: str) -> tuple[tuple[str, dict[str, Any]], ...]:
        """Load every direct JSON child under one repository-logical directory."""


class ArtifactStore(Protocol):
    """Write access to governed artifacts through repository-logical or explicit paths."""

    def write_json_object(self, relative_path: str, document: Mapping[str, Any]) -> Path:
        """Write one JSON object to a repository-logical destination."""

    def write_json_file(self, destination: Path, document: Mapping[str, Any]) -> Path:
        """Write one JSON object to an explicit filesystem path."""


@dataclass(frozen=True, slots=True)
class FileSystemArtifactIO:
    """Default filesystem-backed artifact source and store."""

    workspace_config: WorkspaceConfig

    def load_json_object(self, relative_path: str) -> dict[str, Any]:
        """Load one repository-logical JSON object from disk."""
        return _load_json_object(
            self.workspace_config.resolve_path(relative_path),
            label=relative_path,
        )

    def iter_json_objects(self, relative_directory: str) -> tuple[tuple[str, dict[str, Any]], ...]:
        """Load every direct JSON child under one repository-logical directory."""
        directory = self.workspace_config.resolve_path(relative_directory)
        documents: list[tuple[str, dict[str, Any]]] = []
        for path in sorted(directory.glob("*.json")):
            logical_path = self.workspace_config.logical_path_for(path)
            documents.append((logical_path, _load_json_object(path, label=logical_path)))
        return tuple(documents)

    def write_json_object(self, relative_path: str, document: Mapping[str, Any]) -> Path:
        """Write one JSON object to a repository-logical destination."""
        return self.write_json_file(self.workspace_config.resolve_path(relative_path), document)

    def write_json_file(self, destination: Path, document: Mapping[str, Any]) -> Path:
        """Write one JSON object to an explicit filesystem path."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(f"{json.dumps(dict(document), indent=2)}\n", encoding="utf-8")
        return destination
