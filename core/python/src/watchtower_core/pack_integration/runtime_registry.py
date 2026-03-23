"""Runtime-only hosted-pack registry helpers for copy-forward bootstrap mode."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, cast

from watchtower_core.control_plane.models import (
    PackRegistryEntry,
    PackRuntimeManifest,
    PackSettings,
)
from watchtower_core.control_plane.pack_settings_discovery import discover_pack_settings_paths

_RUNTIME_VIEW_CACHE_KEY = "pack_registry_runtime_view"


@dataclass(frozen=True, slots=True)
class PackRegistryRuntimeView:
    """Effective hosted-pack view used by runtime composition."""

    entries: tuple[PackRegistryEntry, ...]
    invalid_entries: tuple[PackRegistryEntry, ...] = ()
    invalid_authored_entries: tuple[tuple[str, str], ...] = ()

    def get_by_pack_id(self, pack_id: str) -> PackRegistryEntry:
        for entry in self.entries:
            if entry.pack_id == pack_id:
                return entry
        raise KeyError(pack_id)

    def get_by_pack_slug(self, pack_slug: str) -> PackRegistryEntry:
        for entry in self.entries:
            if entry.pack_slug == pack_slug:
                return entry
        invalid_message = self.invalid_entry_message(pack_slug)
        if invalid_message is not None:
            raise ValueError(invalid_message)
        raise KeyError(pack_slug)

    def get_by_command_namespace(self, command_namespace: str) -> PackRegistryEntry:
        for entry in self.entries:
            if entry.command_namespace == command_namespace:
                return entry
        invalid_message = self.invalid_entry_message(command_namespace)
        if invalid_message is not None:
            raise ValueError(invalid_message)
        raise KeyError(command_namespace)

    def default_pack(self) -> PackRegistryEntry:
        default_entries = tuple(entry for entry in self.entries if entry.default_repo_pack)
        if len(default_entries) == 1:
            return default_entries[0]
        if len(self.entries) == 1:
            return self.entries[0]
        if not self.entries:
            raise ValueError("No usable hosted packs are available in the current repository.")
        raise ValueError(
            "Could not resolve one default hosted pack from the current runtime view. "
            "Run watchtower-core pack list --format json to inspect the usable packs."
        )

    def invalid_entry_message(self, key: str) -> str | None:
        for slug_or_namespace, message in self.invalid_authored_entries:
            if slug_or_namespace == key:
                return message
        return None


def load_pack_registry_runtime_view(loader: Any) -> PackRegistryRuntimeView:
    """Return the effective runtime hosted-pack view for one repository."""

    cached = loader._typed_document_cache.get(_RUNTIME_VIEW_CACHE_KEY)
    if cached is not None:
        return cast(PackRegistryRuntimeView, cached)

    authored_registry = loader.load_pack_registry()
    entries: list[PackRegistryEntry] = []
    invalid_typed_entries: list[PackRegistryEntry] = []
    invalid_entries: list[tuple[str, str]] = []
    seen_pack_ids: set[str] = set()
    seen_slugs: set[str] = set()
    seen_namespaces: set[str] = set()
    seen_settings_paths: set[str] = set()
    try:
        active_pack_settings_path = loader.activate_pack_settings()
    except Exception:
        active_pack_settings_path = None

    for entry in authored_registry.packs:
        error_message = _authored_entry_error(loader, entry)
        if error_message is not None:
            invalid_typed_entries.append(entry)
            invalid_entries.extend(
                (
                    (entry.pack_slug, error_message),
                    (entry.command_namespace, error_message),
                )
            )
            continue
        entries.append(entry)
        seen_pack_ids.add(entry.pack_id)
        seen_slugs.add(entry.pack_slug)
        seen_namespaces.add(entry.command_namespace)
        seen_settings_paths.add(entry.pack_settings_path)

    discovered_entries: list[PackRegistryEntry] = []
    for settings_path in discover_pack_settings_paths(loader.repo_root):
        if settings_path in seen_settings_paths:
            continue
        try:
            pack_loader = loader.derive(active_pack_settings_path=settings_path)
            pack_loader.activate_pack_settings()
            pack_settings = pack_loader.load_pack_settings()
            runtime_manifest = pack_loader.load_pack_runtime_manifest()
        except Exception:
            continue
        if (
            pack_settings.pack_id in seen_pack_ids
            or runtime_manifest.pack_slug in seen_slugs
            or runtime_manifest.command_namespace in seen_namespaces
        ):
            continue
        discovered_entry = synthesize_pack_registry_entry(
            pack_settings_path=settings_path,
            pack_settings=pack_settings,
            runtime_manifest=runtime_manifest,
        )
        discovered_entries.append(discovered_entry)
        seen_pack_ids.add(discovered_entry.pack_id)
        seen_slugs.add(discovered_entry.pack_slug)
        seen_namespaces.add(discovered_entry.command_namespace)
        seen_settings_paths.add(discovered_entry.pack_settings_path)

    entries.extend(discovered_entries)
    if entries and not any(entry.default_repo_pack for entry in entries):
        if active_pack_settings_path is not None:
            entries = [
                replace(
                    entry,
                    default_repo_pack=entry.pack_settings_path == active_pack_settings_path,
                )
                for entry in entries
            ]

    runtime_view = PackRegistryRuntimeView(
        entries=tuple(
            sorted(
                entries,
                key=lambda entry: (not entry.default_repo_pack, entry.pack_slug.casefold()),
            )
        ),
        invalid_entries=tuple(invalid_typed_entries),
        invalid_authored_entries=tuple(invalid_entries),
    )
    loader._typed_document_cache[_RUNTIME_VIEW_CACHE_KEY] = runtime_view
    return runtime_view


def effective_pack_registry_entries(loader: Any) -> tuple[PackRegistryEntry, ...]:
    """Return the usable hosted-pack entries for runtime composition."""

    return load_pack_registry_runtime_view(loader).entries


def resolve_runtime_pack_registry_entry(
    loader: Any,
    pack_slug: str | None,
) -> PackRegistryEntry:
    """Resolve one pack slug through the effective runtime view."""

    runtime_view = load_pack_registry_runtime_view(loader)
    if pack_slug is None:
        return runtime_view.default_pack()
    return runtime_view.get_by_pack_slug(pack_slug)


def find_runtime_pack_registry_entry_by_namespace(
    loader: Any,
    command_namespace: str,
) -> PackRegistryEntry | None:
    """Resolve one command namespace through the effective runtime view."""

    try:
        return load_pack_registry_runtime_view(loader).get_by_command_namespace(command_namespace)
    except (KeyError, ValueError):
        return None


def synthesize_pack_registry_entry(
    *,
    pack_settings_path: str,
    pack_settings: PackSettings,
    runtime_manifest: PackRuntimeManifest,
) -> PackRegistryEntry:
    """Build one runtime-only hosted-pack entry from valid manifests."""

    return PackRegistryEntry(
        pack_id=pack_settings.pack_id,
        pack_slug=runtime_manifest.pack_slug,
        command_namespace=runtime_manifest.command_namespace,
        pack_settings_path=pack_settings_path,
        pack_runtime_manifest_path=_default_runtime_manifest_path(pack_settings_path),
        python_distribution=runtime_manifest.python_distribution,
        python_package=runtime_manifest.python_package,
        default_repo_pack=False,
        notes=(
            "Runtime-only bootstrap-mode entry discovered from local pack manifests. "
            "Run watchtower-core pack bootstrap to persist shared registry and workspace wiring."
        ),
    )


def _authored_entry_error(loader: Any, entry: PackRegistryEntry) -> str | None:
    entry_loader = loader.derive(active_pack_settings_path=None)
    try:
        entry_loader.load_pack_settings(entry.pack_settings_path)
    except Exception as exc:
        return (
            f"Hosted-pack registry entry for {entry.pack_slug!r} is unusable because its "
            f"pack settings path could not be loaded: {entry.pack_settings_path} ({exc})"
        )
    try:
        entry_loader.load_pack_runtime_manifest(pack_settings_path=entry.pack_settings_path)
    except Exception as exc:
        return (
            f"Hosted-pack registry entry for {entry.pack_slug!r} is unusable because its "
            "runtime manifest could not be loaded from the declared pack settings path: "
            f"{entry.pack_settings_path} ({exc})"
        )
    return None


def _default_runtime_manifest_path(pack_settings_path: str) -> str:
    return f"{pack_settings_path.rsplit('/', maxsplit=1)[0]}/pack_runtime_manifest.json"


__all__ = [
    "PackRegistryRuntimeView",
    "effective_pack_registry_entries",
    "find_runtime_pack_registry_entry_by_namespace",
    "load_pack_registry_runtime_view",
    "resolve_runtime_pack_registry_entry",
    "synthesize_pack_registry_entry",
]
