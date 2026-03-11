"""Typed models for schema catalog and registry artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.workspace import WorkspaceConfig


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
    def from_document(
        cls,
        document: dict[str, Any],
        workspace_config: WorkspaceConfig,
    ) -> SchemaCatalogRecord:
        return cls(
            schema_id=document["schema_id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            schema_family=document["schema_family"],
            subject_kind=document["subject_kind"],
            version=document["version"],
            canonical_relative_path=document["canonical_path"],
            canonical_path=workspace_config.resolve_path(document["canonical_path"]),
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
    def from_document(
        cls,
        document: dict[str, Any],
        workspace_config: WorkspaceConfig,
    ) -> SchemaCatalog:
        records = tuple(
            SchemaCatalogRecord.from_document(record, workspace_config)
            for record in document["schemas"]
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
    def from_document(cls, document: dict[str, Any]) -> ValidatorDefinition:
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
    def from_document(cls, document: dict[str, Any]) -> ValidatorRegistry:
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
class AuthorityMapEntry:
    """Authority-map registry entry."""

    question_id: str
    domain: str
    question: str
    status: str
    artifact_kind: str
    canonical_path: str
    preferred_command: str
    fallback_paths: tuple[str, ...]
    preferred_human_path: str | None = None
    status_fields: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> AuthorityMapEntry:
        return cls(
            question_id=document["question_id"],
            domain=document["domain"],
            question=document["question"],
            status=document["status"],
            artifact_kind=document["artifact_kind"],
            canonical_path=document["canonical_path"],
            preferred_command=document["preferred_command"],
            fallback_paths=tuple(document["fallback_paths"]),
            preferred_human_path=document.get("preferred_human_path"),
            status_fields=tuple(document.get("status_fields", ())),
            aliases=tuple(document.get("aliases", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class AuthorityMap:
    """Typed authority-map registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[AuthorityMapEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> AuthorityMap:
        entries = tuple(
            AuthorityMapEntry.from_document(entry) for entry in document["entries"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, question_id: str) -> AuthorityMapEntry:
        """Return one authority-map entry by identifier."""
        for entry in self.entries:
            if entry.question_id == question_id:
                return entry
        raise KeyError(question_id)


@dataclass(frozen=True, slots=True)
class WorkflowMetadataDefinition:
    """Workflow metadata registry entry."""

    workflow_id: str
    phase_type: str
    task_family: str
    primary_risks: tuple[str, ...]
    extra_trigger_tags: tuple[str, ...] = ()
    companion_workflow_ids: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> WorkflowMetadataDefinition:
        return cls(
            workflow_id=document["workflow_id"],
            phase_type=document["phase_type"],
            task_family=document["task_family"],
            primary_risks=tuple(document["primary_risks"]),
            extra_trigger_tags=tuple(document.get("extra_trigger_tags", ())),
            companion_workflow_ids=tuple(document.get("companion_workflow_ids", ())),
        )


@dataclass(frozen=True, slots=True)
class WorkflowMetadataRegistry:
    """Typed workflow-metadata registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[WorkflowMetadataDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> WorkflowMetadataRegistry:
        entries = tuple(
            WorkflowMetadataDefinition.from_document(entry)
            for entry in document["entries"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, workflow_id: str) -> WorkflowMetadataDefinition:
        """Return one workflow metadata entry by workflow identifier."""
        for entry in self.entries:
            if entry.workflow_id == workflow_id:
                return entry
        raise KeyError(workflow_id)
