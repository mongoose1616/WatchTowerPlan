"""Helpers for discovering pack-owned workspace roots from hosted-pack contracts."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.errors import RepoRootNotFoundError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import PackWorkspaceRoots
from watchtower_core.control_plane.pack_settings_discovery import (
    discover_pack_settings_paths,
)
from watchtower_core.pack_integration.discovery_errors import (
    RECOVERABLE_PACK_DISCOVERY_EXCEPTIONS,
)


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

    can_load_pack_registry = effective_loader is not None and hasattr(
        effective_loader, "load_pack_registry"
    )
    can_load_pack_settings = effective_loader is not None and hasattr(
        effective_loader, "load_pack_settings"
    )

    pack_registry = None
    if can_load_pack_registry:
        assert effective_loader is not None
        try:
            pack_registry = effective_loader.load_pack_registry()
        except RECOVERABLE_PACK_DISCOVERY_EXCEPTIONS:
            pack_registry = None

    if pack_registry is not None and can_load_pack_settings:
        assert effective_loader is not None
        for entry in pack_registry.packs:
            seen_settings_paths.add(entry.pack_settings_path)
            try:
                pack_settings = effective_loader.load_pack_settings(entry.pack_settings_path)
            except RECOVERABLE_PACK_DISCOVERY_EXCEPTIONS:
                continue
            workspace_roots = pack_settings.workspace_roots
            if workspace_roots.workspace_root in seen_workspace_roots:
                continue
            discovered_roots.append(workspace_roots)
            seen_workspace_roots.add(workspace_roots.workspace_root)

    if can_load_pack_settings:
        assert effective_loader is not None
        for settings_path in discover_pack_settings_paths(repo_root):
            if settings_path in seen_settings_paths:
                continue
            try:
                pack_settings = effective_loader.load_pack_settings(settings_path)
            except RECOVERABLE_PACK_DISCOVERY_EXCEPTIONS:
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


def pack_reference_doc_roots(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> tuple[str, ...]:
    """Return hosted-pack reference document roots, excluding reusable core."""

    declared_roots = tuple(
        f"{roots.docs_root}/references"
        for roots in discover_pack_workspace_roots(repo_root, loader=loader)
    )
    return _ordered_existing_paths(
        repo_root,
        (*declared_roots, *_conventional_relative_paths(repo_root, "docs/references")),
        exclude={"core/docs/references"},
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


def pack_workflow_role_roots(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> tuple[str, ...]:
    """Return hosted-pack workflow-role roots, excluding reusable core."""

    declared_roots = tuple(
        f"{roots.workflows_root}/roles"
        for roots in discover_pack_workspace_roots(repo_root, loader=loader)
    )
    return _ordered_existing_paths(
        repo_root,
        (*declared_roots, *_conventional_relative_paths(repo_root, "workflows/roles")),
        exclude={"core/workflows/roles"},
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


def pack_workflow_root_slug_map(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader | None = None,
) -> dict[str, str]:
    """Return pack workflow roots mapped to their hosted-pack slug."""

    effective_loader: ControlPlaneLoader | None = loader
    if effective_loader is None or effective_loader.repo_root != repo_root:
        try:
            effective_loader = ControlPlaneLoader(repo_root)
        except RepoRootNotFoundError:
            effective_loader = None
    if effective_loader is None or not hasattr(effective_loader, "load_pack_settings"):
        return {}

    root_slug_map: dict[str, str] = {}
    for settings_path in discover_pack_settings_paths(repo_root):
        try:
            pack_settings = effective_loader.load_pack_settings(settings_path)
        except RECOVERABLE_PACK_DISCOVERY_EXCEPTIONS:
            continue
        pack_slug = _pack_slug_from_pack_id(pack_settings.pack_id)
        workflows_root = pack_settings.workspace_roots.workflows_root
        root_slug_map[f"{workflows_root}/modules"] = pack_slug
        root_slug_map[f"{workflows_root}/roles"] = pack_slug
    return root_slug_map


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
def _pack_slug_from_pack_id(pack_id: str) -> str:
    if pack_id.startswith("pack.") and len(pack_id) > len("pack."):
        return pack_id.split(".", 1)[1]
    return pack_id.replace(".", "_")


__all__ = [
    "discover_pack_workspace_roots",
    "pack_reference_doc_roots",
    "pack_routing_table_paths",
    "pack_standard_doc_roots",
    "pack_workflow_root_slug_map",
    "pack_workflow_module_roots",
    "pack_workflow_role_roots",
]
