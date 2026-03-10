"""Typed models for navigation and repository index artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RepositoryPathEntry:
    """Repository path-index entry."""

    path: str
    kind: str
    surface_kind: str
    summary: str
    parent_path: str
    maturity: str = "supporting"
    priority: str = "medium"
    audience_hint: str = "shared"
    aliases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RepositoryPathEntry:
        return cls(
            path=document["path"],
            kind=document["kind"],
            surface_kind=document["surface_kind"],
            summary=document["summary"],
            parent_path=document["parent_path"],
            maturity=document.get("maturity", "supporting"),
            priority=document.get("priority", "medium"),
            audience_hint=document.get("audience_hint", "shared"),
            aliases=tuple(document.get("aliases", ())),
            tags=tuple(document.get("tags", ())),
            related_paths=tuple(document.get("related_paths", ())),
        )


@dataclass(frozen=True, slots=True)
class RepositoryPathIndex:
    """Typed repository-path-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    coverage_mode: str
    root_path: str
    entries: tuple[RepositoryPathEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RepositoryPathIndex:
        entries = tuple(RepositoryPathEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            coverage_mode=document["coverage_mode"],
            root_path=document["root_path"],
            entries=entries,
        )

    def get(self, path: str) -> RepositoryPathEntry:
        """Return a path-index entry by repository-relative path."""
        for entry in self.entries:
            if entry.path == path:
                return entry
        raise KeyError(path)


@dataclass(frozen=True, slots=True)
class CommandIndexEntry:
    """Command-index entry."""

    command_id: str
    command: str
    summary: str
    kind: str
    status: str
    workspace: str
    doc_path: str
    synopsis: str
    implementation_path: str | None = None
    package_entrypoint: str | None = None
    parent_command_id: str | None = None
    output_formats: tuple[str, ...] = ()
    default_output_format: str | None = None
    aliases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> CommandIndexEntry:
        return cls(
            command_id=document["command_id"],
            command=document["command"],
            summary=document["summary"],
            kind=document["kind"],
            status=document["status"],
            workspace=document["workspace"],
            doc_path=document["doc_path"],
            synopsis=document["synopsis"],
            implementation_path=document.get("implementation_path"),
            package_entrypoint=document.get("package_entrypoint"),
            parent_command_id=document.get("parent_command_id"),
            output_formats=tuple(document.get("output_formats", ())),
            default_output_format=document.get("default_output_format"),
            aliases=tuple(document.get("aliases", ())),
            tags=tuple(document.get("tags", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class CommandIndex:
    """Typed command-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    workspace: str
    entries: tuple[CommandIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> CommandIndex:
        entries = tuple(CommandIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            workspace=document["workspace"],
            entries=entries,
        )

    def get(self, command_id: str) -> CommandIndexEntry:
        """Return a command-index entry by identifier."""
        for entry in self.entries:
            if entry.command_id == command_id:
                return entry
        raise KeyError(command_id)
