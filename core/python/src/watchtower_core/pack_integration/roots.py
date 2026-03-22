"""Helpers for discovering pack-owned workspace roots from hosted-pack contracts."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.errors import RepoRootNotFoundError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import PackWorkspaceRoots


def discover_pack_workspace_roots(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> tuple[PackWorkspaceRoots, ...]:
    """Return the declared workspace roots for hosted packs visible in one repository."""

    effective_loader: ControlPlaneLoader | None = loader
    if effective_loader is None or effective_loader.repo_root != repo_root:
        try:
            effective_loader = ControlPlaneLoader(repo_root)
        except RepoRootNotFoundError:
            effective_loader = None
    discovered_roots: list[PackWorkspaceRoots] = []
    seen_settings_paths: set[str] = set()
    seen_workspace_roots: set[str] = set()

    pack_registry = None
    if effective_loader is not None:
        try:
            pack_registry = effective_loader.load_pack_registry()
        except Exception:
            pack_registry = None

    if pack_registry is not None and effective_loader is not None:
        for entry in pack_registry.packs:
            seen_settings_paths.add(entry.pack_settings_path)
            try:
                pack_settings = effective_loader.load_pack_settings(entry.pack_settings_path)
            except Exception:
                continue
            workspace_roots = pack_settings.workspace_roots
            if workspace_roots.workspace_root in seen_workspace_roots:
                continue
            discovered_roots.append(workspace_roots)
            seen_workspace_roots.add(workspace_roots.workspace_root)

    if effective_loader is not None:
        for settings_path in _discovered_pack_settings_paths(repo_root):
            if settings_path in seen_settings_paths:
                continue
            try:
                pack_settings = effective_loader.load_pack_settings(settings_path)
            except Exception:
                continue
            workspace_roots = pack_settings.workspace_roots
            if workspace_roots.workspace_root in seen_workspace_roots:
                continue
            discovered_roots.append(workspace_roots)
            seen_workspace_roots.add(workspace_roots.workspace_root)

    return tuple(discovered_roots)


def pack_standard_doc_roots(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> tuple[str, ...]:
    """Return hosted-pack standard document roots, excluding reusable core."""

    declared_roots = tuple(
        f"{roots.docs_root}/standards"
        for roots in discover_pack_workspace_roots(repo_root, loader=loader)
    )
    return _ordered_existing_paths(
        repo_root,
        (*declared_roots, *_conventional_relative_paths(repo_root, "docs/standards")),
        exclude={"core/docs/standards"},
    )


def pack_workflow_module_roots(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> tuple[str, ...]:
    """Return hosted-pack workflow-module roots, excluding reusable core."""

    declared_roots = tuple(
        f"{roots.workflows_root}/modules"
        for roots in discover_pack_workspace_roots(repo_root, loader=loader)
    )
    return _ordered_existing_paths(
        repo_root,
        (*declared_roots, *_conventional_relative_paths(repo_root, "workflows/modules")),
        exclude={"core/workflows/modules"},
    )


def pack_routing_table_paths(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> tuple[str, ...]:
    """Return hosted-pack routing-table paths, excluding reusable core."""

    declared_paths = tuple(
        f"{roots.workflows_root}/ROUTING_TABLE.md"
        for roots in discover_pack_workspace_roots(repo_root, loader=loader)
    )
    return _ordered_existing_paths(
        repo_root,
        (
            *declared_paths,
            *_conventional_relative_paths(repo_root, "workflows/ROUTING_TABLE.md"),
        ),
        exclude={"core/workflows/ROUTING_TABLE.md"},
    )


def _discovered_pack_settings_paths(repo_root: Path) -> tuple[str, ...]:
    return tuple(
        sorted(
            path.relative_to(repo_root).as_posix()
            for path in repo_root.rglob("pack_settings.json")
            if path.as_posix().endswith("/.wt/manifests/pack_settings.json")
        )
    )


def _conventional_relative_paths(repo_root: Path, suffix: str) -> tuple[str, ...]:
    matches: list[str] = []
    for pattern in (f"*/{suffix}", f"packs/*/{suffix}"):
        matches.extend(
            path.relative_to(repo_root).as_posix() for path in sorted(repo_root.glob(pattern))
        )
    return tuple(matches)


def _ordered_existing_paths(
    repo_root: Path,
    candidates: tuple[str, ...],
    *,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    excluded = exclude or set()
    retained: list[str] = []
    seen: set[str] = set()
    for relative_path in candidates:
        if relative_path in excluded or relative_path in seen:
            continue
        if (repo_root / relative_path).exists():
            retained.append(relative_path)
            seen.add(relative_path)
    return tuple(retained)


__all__ = [
    "discover_pack_workspace_roots",
    "pack_routing_table_paths",
    "pack_standard_doc_roots",
    "pack_workflow_module_roots",
]
