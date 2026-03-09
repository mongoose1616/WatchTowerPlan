"""Deterministic rebuild helpers for the command index."""

from __future__ import annotations

import json
import re
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import CommandIndexEntry
from watchtower_core.control_plane.paths import discover_repo_root

COMMAND_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/commands/command_index.v1.json"
COMMAND_DOC_ROOT = "docs/commands"
CLI_MAIN_PATH = "core/python/src/watchtower_core/cli/main.py"
CLI_MAIN_ENTRYPOINT = "watchtower_core.cli.main:main"
SECTION_HEADING_PATTERN = re.compile(r"^## (?P<title>.+)$")
FORMAT_OPTION_PATTERN = re.compile(r"`--format <(?P<formats>[^>]+)>`")


def _extract_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_title: str | None = None
    for line in markdown.splitlines():
        match = SECTION_HEADING_PATTERN.match(line)
        if match is not None:
            current_title = match.group("title")
            sections[current_title] = []
            continue
        if current_title is not None:
            sections[current_title].append(line)
    return {
        title: "\n".join(lines).strip()
        for title, lines in sections.items()
    }


def _extract_first_paragraph(section: str) -> str:
    for block in section.split("\n\n"):
        candidate = block.strip()
        if candidate:
            return candidate.replace("\n", " ").strip()
    raise ValueError("Section is missing its expected paragraph content.")


def _parse_table(section: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 4:
            continue
        key = parts[1]
        value = parts[2]
        if key in {"Field", "---"} or not key or not value:
            continue
        rows[key] = value.strip("`")
    return rows


def _extract_first_code_block(section: str) -> str:
    lines = section.splitlines()
    in_block = False
    collected: list[str] = []
    for line in lines:
        if line.startswith("```"):
            if in_block:
                break
            in_block = True
            continue
        if in_block:
            collected.append(line)
    lines = [line.strip() for line in collected if line.strip()]
    if not lines:
        raise ValueError("Section is missing its expected fenced code block.")
    return lines[-1]


def _extract_output_formats(section: str) -> tuple[tuple[str, ...], str | None]:
    for line in section.splitlines():
        match = FORMAT_OPTION_PATTERN.search(line)
        if match is None:
            continue
        formats = tuple(
            item.strip()
            for item in match.group("formats").split("|")
            if item.strip()
        )
        if not formats:
            break
        default = "human" if "human" in formats else formats[0]
        return formats, default
    return (), None


def _normalize_command_token(token: str) -> str:
    return token.replace("-", "_")


def _command_id(command: str) -> str:
    tokens = [_normalize_command_token(token) for token in command.split()]
    return "command." + ".".join(tokens)


def _parent_command_id(command: str, kind: str) -> str | None:
    if kind != "subcommand":
        return None
    tokens = [_normalize_command_token(token) for token in command.split()]
    if len(tokens) < 2:
        raise ValueError(f"Subcommand is missing a parent command: {command}")
    return "command." + ".".join(tokens[:-1])


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


def _package_entrypoint(implementation_path: str | None) -> str | None:
    if implementation_path == CLI_MAIN_PATH:
        return CLI_MAIN_ENTRYPOINT
    return None


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
    """Build and write the command index from authored command docs."""

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

        command_doc_root = self._repo_root / COMMAND_DOC_ROOT
        for doc_path in sorted(command_doc_root.rglob("*.md")):
            if doc_path.name == "README.md":
                continue
            entry = self._parse_command_doc(doc_path, existing_entries)
            derived_entries[entry.command_id] = entry

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

    def _parse_command_doc(
        self,
        doc_path: Path,
        existing_entries: dict[str, CommandIndexEntry],
    ) -> CommandIndexEntry:
        relative_doc_path = doc_path.relative_to(self._repo_root).as_posix()
        sections = _extract_sections(doc_path.read_text(encoding="utf-8"))
        summary = _extract_first_paragraph(sections["Summary"])
        command_rows = _parse_table(sections["Command"])
        invocation = command_rows["Invocation"]
        kind = command_rows["Kind"]
        workspace = command_rows["Workspace"]
        implementation_path = command_rows.get("Source Surface")
        synopsis = _extract_first_code_block(sections["Synopsis"])
        output_formats, default_output_format = _extract_output_formats(
            sections["Arguments and Options"]
        )

        if implementation_path is not None and not (self._repo_root / implementation_path).exists():
            raise ValueError(
                f"Command doc points to a missing implementation path: {relative_doc_path} -> "
                f"{implementation_path}"
            )

        command_id = _command_id(invocation)
        current = existing_entries.get(command_id)
        resolved_output_formats = output_formats or (
            current.output_formats if current is not None else ()
        )
        resolved_default_output = default_output_format
        if current is not None and current.default_output_format in resolved_output_formats:
            resolved_default_output = current.default_output_format
        if resolved_default_output is None and resolved_output_formats:
            resolved_default_output = (
                "human" if "human" in resolved_output_formats else resolved_output_formats[0]
            )

        return CommandIndexEntry(
            command_id=command_id,
            command=invocation,
            summary=summary,
            kind=kind,
            status=current.status if current is not None else "active",
            workspace=workspace,
            doc_path=relative_doc_path,
            synopsis=synopsis,
            implementation_path=implementation_path,
            package_entrypoint=(
                current.package_entrypoint
                if current is not None and current.package_entrypoint is not None
                else _package_entrypoint(implementation_path)
            ),
            parent_command_id=_parent_command_id(invocation, kind),
            output_formats=resolved_output_formats,
            default_output_format=resolved_default_output,
            aliases=current.aliases if current is not None else (),
            tags=current.tags if current is not None and current.tags else _derived_tags(
                invocation,
                workspace,
            ),
            notes=current.notes if current is not None else None,
        )

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
