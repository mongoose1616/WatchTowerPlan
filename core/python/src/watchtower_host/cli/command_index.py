"""Host-owned rebuild helper for the command index."""

from __future__ import annotations

import json
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from importlib import import_module, invalidate_caches
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import CommandIndexEntry
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.documentation.command_semantics import (
    load_command_doc_source_surfaces,
)
from watchtower_core.sync.cache import (
    SyncCacheInputSpec,
    discover_pack_sync_cache_paths,
    module_relative_path,
    ordered_sync_cache_paths,
)

COMMAND_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/commands/command_index.json"


def _normalize_command_token(token: str) -> str:
    return token.replace("-", "_")


def _derived_tags(command: str, workspace: str) -> tuple[str, ...]:
    tags: list[str] = []
    if workspace == "core_python":
        tags.append("python")
    tags.append("cli")
    normalized_tokens = [_normalize_command_token(token) for token in command.split()[1:]]
    for token in normalized_tokens:
        for part in token.split("_"):
            if part and part not in tags:
                tags.append(part)
    return tuple(tags)


def _entry_to_document(entry: CommandIndexEntry) -> dict[str, object]:
    document: dict[str, object] = {
        "command_id": entry.command_id,
        "command": entry.command,
        "summary": entry.summary,
        "kind": entry.kind,
        "status": entry.status,
        "workspace": entry.workspace,
        "doc_path": entry.doc_path,
        "synopsis": entry.synopsis,
    }
    if entry.implementation_path is not None:
        document["implementation_path"] = entry.implementation_path
    if entry.package_entrypoint is not None:
        document["package_entrypoint"] = entry.package_entrypoint
    if entry.parent_command_id is not None:
        document["parent_command_id"] = entry.parent_command_id
    if entry.output_formats:
        document["output_formats"] = list(entry.output_formats)
    if entry.default_output_format is not None:
        document["default_output_format"] = entry.default_output_format
    if entry.aliases:
        document["aliases"] = list(entry.aliases)
    if entry.tags:
        document["tags"] = list(entry.tags)
    if entry.notes is not None:
        document["notes"] = entry.notes
    return document


@contextmanager
def _repo_local_watchtower_host_imports(repo_root: Path) -> Iterator[None]:
    source_root = (repo_root / "core" / "python" / "src").resolve()
    if not source_root.is_dir():
        raise ValueError(
            "Command-index rebuild requires a readable core/python source root under the "
            f"target repository: {source_root}"
        )

    saved_modules = {
        name: module
        for name, module in sys.modules.items()
        if name == "watchtower_host" or name.startswith("watchtower_host.")
    }
    original_sys_path = list(sys.path)
    original_dont_write_bytecode = sys.dont_write_bytecode
    for name in tuple(saved_modules):
        sys.modules.pop(name, None)

    invalidate_caches()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(source_root))
    try:
        yield
    finally:
        for name in tuple(sys.modules):
            if name == "watchtower_host" or name.startswith("watchtower_host."):
                sys.modules.pop(name, None)
        sys.path[:] = original_sys_path
        sys.dont_write_bytecode = original_dont_write_bytecode
        sys.modules.update(saved_modules)
        invalidate_caches()


def _iter_repo_local_host_command_parser_specs(
    repo_root: Path,
    loader: ControlPlaneLoader,
) -> tuple[Any, ...]:
    # Shared-core apply/bootstrap can replace target source files beneath an already-running
    # process. Reimport host CLI composition from the target repo root so the command index
    # reflects the target source tree rather than stale watchtower_host modules.
    with _repo_local_watchtower_host_imports(repo_root):
        introspection_module = import_module("watchtower_host.cli.introspection")
        iter_specs = getattr(introspection_module, "iter_host_command_parser_specs")
        return tuple(iter_specs(loader))


class CommandIndexSyncService:
    """Build and write the command index from host-composed CLI metadata."""

    OUTPUT_PATH = COMMAND_INDEX_ARTIFACT_PATH

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> CommandIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def sync_cache_inputs(self) -> SyncCacheInputSpec:
        return SyncCacheInputSpec(
            tracked_paths=ordered_sync_cache_paths(
                module_relative_path(self._repo_root, __file__),
                "core/docs/commands",
                "core/python/src/watchtower_host/cli",
                "core/python/src/watchtower_core/cli",
                "core/python/src/watchtower_core/documentation",
                "core/python/src/watchtower_core/pack_integration",
                discover_pack_sync_cache_paths(
                    self._loader,
                    include_command_docs=True,
                    include_python_sources=True,
                ),
            )
        )

    def build_document(self) -> dict[str, object]:
        existing_index = self._loader.load_command_index()
        existing_entries = {entry.command_id: entry for entry in existing_index.entries}
        derived_entries: dict[str, CommandIndexEntry] = {}
        for spec in _iter_repo_local_host_command_parser_specs(self._repo_root, self._loader):
            doc_path = self._repo_root / spec.doc_path
            if not doc_path.exists():
                raise ValueError(
                    "Registry-backed CLI command is missing its companion command doc: "
                    f"{spec.command} -> {spec.doc_path}"
                )
            table_source_surface, primary_source_surface = load_command_doc_source_surfaces(
                doc_path
            )
            resolved_implementation_path = spec.implementation_path
            if resolved_implementation_path is None:
                if table_source_surface != primary_source_surface:
                    raise ValueError(
                        "Companion command doc Source Surface section drifted from the "
                        "Command table Source Surface row while the registry-backed command "
                        "is unavailable: "
                        f"{spec.command} -> {spec.doc_path} "
                        f"(table={table_source_surface}, source={primary_source_surface})"
                    )
                resolved_implementation_path = table_source_surface
            elif table_source_surface != resolved_implementation_path:
                raise ValueError(
                    "Companion command doc Command table Source Surface drifted from the "
                    "registry-backed implementation path: "
                    f"{spec.command} -> {spec.doc_path} "
                    f"(doc={table_source_surface}, expected={resolved_implementation_path})"
                )
            if primary_source_surface != resolved_implementation_path:
                raise ValueError(
                    "Companion command doc Source Surface section drifted from the "
                    "registry-backed implementation path: "
                    f"{spec.command} -> {spec.doc_path} "
                    f"(doc={primary_source_surface}, expected={resolved_implementation_path})"
                )
            if not (self._repo_root / resolved_implementation_path).exists():
                raise ValueError(
                    "Registry-backed CLI command points to a missing implementation path: "
                    f"{spec.command} -> {resolved_implementation_path}"
                )

            current = existing_entries.get(spec.command_id)
            resolved_output_formats = spec.output_formats or (
                current.output_formats if current is not None else ()
            )
            resolved_default_output = spec.default_output_format
            if current is not None and current.default_output_format in resolved_output_formats:
                resolved_default_output = current.default_output_format
            if resolved_default_output is None and resolved_output_formats:
                resolved_default_output = (
                    "human" if "human" in resolved_output_formats else resolved_output_formats[0]
                )

            derived_entries[spec.command_id] = CommandIndexEntry(
                command_id=spec.command_id,
                command=spec.command,
                summary=spec.summary,
                kind=spec.kind,
                status=current.status if current is not None else "active",
                workspace=spec.workspace,
                doc_path=spec.doc_path,
                synopsis=spec.synopsis,
                implementation_path=resolved_implementation_path,
                package_entrypoint=spec.package_entrypoint,
                parent_command_id=spec.parent_command_id,
                output_formats=resolved_output_formats,
                default_output_format=resolved_default_output,
                aliases=current.aliases if current is not None else (),
                tags=current.tags
                if current is not None and current.tags
                else _derived_tags(
                    spec.command,
                    spec.workspace,
                ),
                notes=(
                    spec.notes
                    if spec.notes is not None
                    else (current.notes if current is not None else None)
                ),
            )

        self._validate_parent_links(derived_entries)

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:command-index:v1",
            "id": "index.commands",
            "title": "Command Index",
            "status": existing_index.status,
            "workspace": existing_index.workspace,
            "entries": [
                _entry_to_document(derived_entries[command_id])
                for command_id in sorted(derived_entries)
            ],
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated command index to disk."""
        target = destination or (self._repo_root / COMMAND_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _validate_parent_links(self, entries: dict[str, CommandIndexEntry]) -> None:
        known_ids = set(entries)
        for entry in entries.values():
            if entry.kind != "subcommand":
                continue
            if entry.parent_command_id is None:
                raise ValueError(f"Subcommand is missing its parent identifier: {entry.command_id}")
            if entry.parent_command_id not in known_ids:
                raise ValueError(
                    f"Subcommand points to a missing parent command: {entry.command_id} -> "
                    f"{entry.parent_command_id}"
                )


__all__ = ["COMMAND_INDEX_ARTIFACT_PATH", "CommandIndexSyncService"]
