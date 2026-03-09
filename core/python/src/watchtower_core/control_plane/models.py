"""Typed models for governed control-plane artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class SchemaCatalogRecord:
    """Catalog entry for a published schema."""

    schema_id: str
    title: str
    description: str
    status: str
    schema_family: str
    subject_kind: str
    version: str
    canonical_relative_path: str
    canonical_path: Path
    aliases: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any], repo_root: Path) -> "SchemaCatalogRecord":
        return cls(
            schema_id=document["schema_id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            schema_family=document["schema_family"],
            subject_kind=document["subject_kind"],
            version=document["version"],
            canonical_relative_path=document["canonical_path"],
            canonical_path=repo_root / document["canonical_path"],
            aliases=tuple(document.get("aliases", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class SchemaCatalog:
    """Typed schema-catalog artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    records: tuple[SchemaCatalogRecord, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any], repo_root: Path) -> "SchemaCatalog":
        records = tuple(
            SchemaCatalogRecord.from_document(record, repo_root) for record in document["schemas"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            records=records,
        )

    def get(self, schema_id: str) -> SchemaCatalogRecord:
        """Return a catalog record by schema identifier."""
        for record in self.records:
            if record.schema_id == schema_id:
                return record
        raise KeyError(schema_id)


@dataclass(frozen=True, slots=True)
class ValidatorDefinition:
    """Validator registry entry."""

    validator_id: str
    title: str
    description: str
    status: str
    engine: str
    artifact_kind: str
    applies_to: tuple[str, ...]
    schema_ids: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "ValidatorDefinition":
        return cls(
            validator_id=document["id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            engine=document["engine"],
            artifact_kind=document["artifact_kind"],
            applies_to=tuple(document["applies_to"]),
            schema_ids=tuple(document.get("schema_ids", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ValidatorRegistry:
    """Typed validator-registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    validators: tuple[ValidatorDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "ValidatorRegistry":
        validators = tuple(
            ValidatorDefinition.from_document(entry) for entry in document["validators"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            validators=validators,
        )

    def get(self, validator_id: str) -> ValidatorDefinition:
        """Return a validator definition by identifier."""
        for entry in self.validators:
            if entry.validator_id == validator_id:
                return entry
        raise KeyError(validator_id)


@dataclass(frozen=True, slots=True)
class RepositoryPathEntry:
    """Repository path-index entry."""

    path: str
    kind: str
    surface_kind: str
    summary: str
    parent_path: str
    aliases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "RepositoryPathEntry":
        return cls(
            path=document["path"],
            kind=document["kind"],
            surface_kind=document["surface_kind"],
            summary=document["summary"],
            parent_path=document["parent_path"],
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
    def from_document(cls, document: dict[str, Any]) -> "RepositoryPathIndex":
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
    def from_document(cls, document: dict[str, Any]) -> "CommandIndexEntry":
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
    def from_document(cls, document: dict[str, Any]) -> "CommandIndex":
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


@dataclass(frozen=True, slots=True)
class TraceabilityEntry:
    """Traceability-index entry."""

    trace_id: str
    title: str
    summary: str
    status: str
    updated_at: str
    prd_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    design_ids: tuple[str, ...] = ()
    plan_ids: tuple[str, ...] = ()
    requirement_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    acceptance_contract_ids: tuple[str, ...] = ()
    validator_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "TraceabilityEntry":
        return cls(
            trace_id=document["trace_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            updated_at=document["updated_at"],
            prd_ids=tuple(document.get("prd_ids", ())),
            decision_ids=tuple(document.get("decision_ids", ())),
            design_ids=tuple(document.get("design_ids", ())),
            plan_ids=tuple(document.get("plan_ids", ())),
            requirement_ids=tuple(document.get("requirement_ids", ())),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            acceptance_contract_ids=tuple(document.get("acceptance_contract_ids", ())),
            validator_ids=tuple(document.get("validator_ids", ())),
            evidence_ids=tuple(document.get("evidence_ids", ())),
            related_paths=tuple(document.get("related_paths", ())),
            tags=tuple(document.get("tags", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class TraceabilityIndex:
    """Typed traceability-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[TraceabilityEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "TraceabilityIndex":
        entries = tuple(TraceabilityEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, trace_id: str) -> TraceabilityEntry:
        """Return a traceability entry by trace identifier."""
        for entry in self.entries:
            if entry.trace_id == trace_id:
                return entry
        raise KeyError(trace_id)
