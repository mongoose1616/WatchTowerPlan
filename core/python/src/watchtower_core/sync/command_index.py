"""Deterministic rebuild helpers for the command index."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.cli.introspection import iter_command_parser_specs
from watchtower_core.cli.parser import build_parser
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import CommandIndexEntry
from watchtower_core.control_plane.paths import discover_repo_root

COMMAND_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/commands/command_index.v1.json"


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


class CommandIndexSyncService:
    """Build and write the command index from registry-backed CLI metadata."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> CommandIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        existing_index = self._loader.load_command_index()
        existing_entries = {
            entry.command_id: entry
            for entry in existing_index.entries
        }
        derived_entries: dict[str, CommandIndexEntry] = {}
        for spec in iter_command_parser_specs(build_parser()):
            if not (self._repo_root / spec.doc_path).exists():
                raise ValueError(
                    "Registry-backed CLI command is missing its companion command doc: "
                    f"{spec.command} -> {spec.doc_path}"
                )
            if not (self._repo_root / spec.implementation_path).exists():
                raise ValueError(
                    "Registry-backed CLI command points to a missing implementation path: "
                    f"{spec.command} -> {spec.implementation_path}"
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
                implementation_path=spec.implementation_path,
                package_entrypoint=(
                    current.package_entrypoint
                    if current is not None and current.package_entrypoint is not None
                    else spec.package_entrypoint
                ),
                parent_command_id=spec.parent_command_id,
                output_formats=resolved_output_formats,
                default_output_format=resolved_default_output,
                aliases=current.aliases if current is not None else (),
                tags=current.tags if current is not None and current.tags else _derived_tags(
                    spec.command,
                    spec.workspace,
                ),
                notes=current.notes if current is not None else None,
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
