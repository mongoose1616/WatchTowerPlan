"""Typed models for references, foundations, standards, and workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from watchtower_core.control_plane.models._index_helpers import (
    get_entry_by_attr,
    index_metadata,
    load_entries,
    tuple_field,
)


@dataclass(frozen=True, slots=True)
class ReferenceIndexEntry:
    """Reference-index entry."""

    reference_id: str
    title: str
    summary: str
    status: str
    doc_path: str
    updated_at: str
    repository_status: str
    uses_internal_references: bool
    uses_external_references: bool
    canonical_upstream_urls: tuple[str, ...] = ()
    cited_by_paths: tuple[str, ...] = ()
    applied_by_paths: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ReferenceIndexEntry:
        return cls(
            reference_id=document["reference_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            repository_status=document["repository_status"],
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            canonical_upstream_urls=tuple_field(document, "canonical_upstream_urls"),
            cited_by_paths=tuple_field(document, "cited_by_paths"),
            applied_by_paths=tuple_field(document, "applied_by_paths"),
            related_paths=tuple_field(document, "related_paths"),
            aliases=tuple_field(document, "aliases"),
            tags=tuple_field(document, "tags"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ReferenceIndex:
    """Typed reference-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[ReferenceIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ReferenceIndex:
        entries = load_entries(document, ReferenceIndexEntry.from_document)
        schema_id, artifact_id, title, status = index_metadata(document)
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=entries,
        )

    def get(self, reference_id: str) -> ReferenceIndexEntry:
        """Return a reference-index entry by identifier."""

        return get_entry_by_attr(self.entries, attr_name="reference_id", value=reference_id)


@dataclass(frozen=True, slots=True)
class FoundationIndexEntry:
    """Foundation-index entry."""

    foundation_id: str
    title: str
    summary: str
    status: str
    audience: str
    authority: str
    doc_path: str
    updated_at: str
    uses_internal_references: bool
    uses_external_references: bool
    related_paths: tuple[str, ...] = ()
    reference_doc_paths: tuple[str, ...] = ()
    internal_reference_paths: tuple[str, ...] = ()
    external_reference_urls: tuple[str, ...] = ()
    cited_by_paths: tuple[str, ...] = ()
    applied_by_paths: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> FoundationIndexEntry:
        return cls(
            foundation_id=document["foundation_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            audience=document["audience"],
            authority=document["authority"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            related_paths=tuple_field(document, "related_paths"),
            reference_doc_paths=tuple_field(document, "reference_doc_paths"),
            internal_reference_paths=tuple_field(document, "internal_reference_paths"),
            external_reference_urls=tuple_field(document, "external_reference_urls"),
            cited_by_paths=tuple_field(document, "cited_by_paths"),
            applied_by_paths=tuple_field(document, "applied_by_paths"),
            aliases=tuple_field(document, "aliases"),
            tags=tuple_field(document, "tags"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class FoundationIndex:
    """Typed foundation-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[FoundationIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> FoundationIndex:
        entries = load_entries(document, FoundationIndexEntry.from_document)
        schema_id, artifact_id, title, status = index_metadata(document)
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=entries,
        )

    def get(self, foundation_id: str) -> FoundationIndexEntry:
        """Return a foundation-index entry by identifier."""

        return get_entry_by_attr(self.entries, attr_name="foundation_id", value=foundation_id)


@dataclass(frozen=True, slots=True)
class StandardIndexEntry:
    """Standard-index entry."""

    standard_id: str
    category: str
    title: str
    summary: str
    status: str
    owner: str
    doc_path: str
    updated_at: str
    uses_internal_references: bool
    uses_external_references: bool
    applies_to: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    reference_doc_paths: tuple[str, ...] = ()
    internal_reference_paths: tuple[str, ...] = ()
    applied_reference_paths: tuple[str, ...] = ()
    external_reference_urls: tuple[str, ...] = ()
    applied_external_reference_urls: tuple[str, ...] = ()
    operationalization_modes: tuple[str, ...] = ()
    operationalization_paths: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> StandardIndexEntry:
        return cls(
            standard_id=document["standard_id"],
            category=document["category"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            owner=document["owner"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            applies_to=tuple_field(document, "applies_to"),
            related_paths=tuple_field(document, "related_paths"),
            reference_doc_paths=tuple_field(document, "reference_doc_paths"),
            internal_reference_paths=tuple_field(document, "internal_reference_paths"),
            applied_reference_paths=tuple_field(document, "applied_reference_paths"),
            external_reference_urls=tuple_field(document, "external_reference_urls"),
            applied_external_reference_urls=tuple_field(
                document,
                "applied_external_reference_urls",
            ),
            operationalization_modes=tuple_field(document, "operationalization_modes"),
            operationalization_paths=tuple_field(document, "operationalization_paths"),
            tags=tuple_field(document, "tags"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class StandardIndex:
    """Typed standard-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[StandardIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> StandardIndex:
        entries = load_entries(document, StandardIndexEntry.from_document)
        schema_id, artifact_id, title, status = index_metadata(document)
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=entries,
        )

    def get(self, standard_id: str) -> StandardIndexEntry:
        """Return a standard-index entry by identifier."""

        return get_entry_by_attr(self.entries, attr_name="standard_id", value=standard_id)


@dataclass(frozen=True, slots=True)
class WorkflowIndexEntry:
    """Workflow-index entry."""

    workflow_id: str
    title: str
    summary: str
    status: str
    doc_path: str
    uses_internal_references: bool
    uses_external_references: bool
    phase_type: str = "shared"
    task_family: str = "workflow"
    primary_risks: tuple[str, ...] = ()
    trigger_tags: tuple[str, ...] = ()
    companion_workflow_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    reference_doc_paths: tuple[str, ...] = ()
    internal_reference_paths: tuple[str, ...] = ()
    external_reference_urls: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> WorkflowIndexEntry:
        return cls(
            workflow_id=document["workflow_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            doc_path=document["doc_path"],
            phase_type=document.get("phase_type", "shared"),
            task_family=document.get("task_family", "workflow"),
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            primary_risks=tuple_field(document, "primary_risks"),
            trigger_tags=tuple_field(document, "trigger_tags"),
            companion_workflow_ids=tuple_field(document, "companion_workflow_ids"),
            related_paths=tuple_field(document, "related_paths"),
            reference_doc_paths=tuple_field(document, "reference_doc_paths"),
            internal_reference_paths=tuple_field(document, "internal_reference_paths"),
            external_reference_urls=tuple_field(document, "external_reference_urls"),
            aliases=tuple_field(document, "aliases"),
            tags=tuple_field(document, "tags"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class WorkflowIndex:
    """Typed workflow-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[WorkflowIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> WorkflowIndex:
        entries = load_entries(document, WorkflowIndexEntry.from_document)
        schema_id, artifact_id, title, status = index_metadata(document)
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=entries,
        )

    def get(self, workflow_id: str) -> WorkflowIndexEntry:
        """Return a workflow-index entry by identifier."""

        return get_entry_by_attr(self.entries, attr_name="workflow_id", value=workflow_id)
