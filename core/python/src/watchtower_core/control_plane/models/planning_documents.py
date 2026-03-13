"""Typed models for PRD, decision, and design-document indexes."""

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
class PrdIndexEntry:
    """PRD-index entry."""

    trace_id: str
    prd_id: str
    title: str
    summary: str
    status: str
    doc_path: str
    updated_at: str
    uses_internal_references: bool
    uses_external_references: bool
    requirement_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    linked_decision_ids: tuple[str, ...] = ()
    linked_design_ids: tuple[str, ...] = ()
    linked_plan_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    internal_reference_paths: tuple[str, ...] = ()
    external_reference_urls: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PrdIndexEntry:
        return cls(
            trace_id=document["trace_id"],
            prd_id=document["prd_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            requirement_ids=tuple_field(document, "requirement_ids"),
            acceptance_ids=tuple_field(document, "acceptance_ids"),
            linked_decision_ids=tuple_field(document, "linked_decision_ids"),
            linked_design_ids=tuple_field(document, "linked_design_ids"),
            linked_plan_ids=tuple_field(document, "linked_plan_ids"),
            related_paths=tuple_field(document, "related_paths"),
            internal_reference_paths=tuple_field(document, "internal_reference_paths"),
            external_reference_urls=tuple_field(document, "external_reference_urls"),
            tags=tuple_field(document, "tags"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class PrdIndex:
    """Typed PRD-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[PrdIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PrdIndex:
        entries = load_entries(document, PrdIndexEntry.from_document)
        schema_id, artifact_id, title, status = index_metadata(document)
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=entries,
        )

    def get(self, prd_id: str) -> PrdIndexEntry:
        """Return a PRD-index entry by identifier."""

        return get_entry_by_attr(self.entries, attr_name="prd_id", value=prd_id)


@dataclass(frozen=True, slots=True)
class DecisionIndexEntry:
    """Decision-index entry."""

    trace_id: str
    decision_id: str
    title: str
    summary: str
    record_status: str
    decision_status: str
    doc_path: str
    updated_at: str
    uses_internal_references: bool
    uses_external_references: bool
    linked_prd_ids: tuple[str, ...] = ()
    linked_design_ids: tuple[str, ...] = ()
    linked_plan_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    internal_reference_paths: tuple[str, ...] = ()
    applied_reference_paths: tuple[str, ...] = ()
    external_reference_urls: tuple[str, ...] = ()
    applied_external_reference_urls: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> DecisionIndexEntry:
        return cls(
            trace_id=document["trace_id"],
            decision_id=document["decision_id"],
            title=document["title"],
            summary=document["summary"],
            record_status=document["record_status"],
            decision_status=document["decision_status"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            linked_prd_ids=tuple_field(document, "linked_prd_ids"),
            linked_design_ids=tuple_field(document, "linked_design_ids"),
            linked_plan_ids=tuple_field(document, "linked_plan_ids"),
            related_paths=tuple_field(document, "related_paths"),
            internal_reference_paths=tuple_field(document, "internal_reference_paths"),
            applied_reference_paths=tuple_field(document, "applied_reference_paths"),
            external_reference_urls=tuple_field(document, "external_reference_urls"),
            applied_external_reference_urls=tuple_field(
                document,
                "applied_external_reference_urls",
            ),
            tags=tuple_field(document, "tags"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class DecisionIndex:
    """Typed decision-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[DecisionIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> DecisionIndex:
        entries = load_entries(document, DecisionIndexEntry.from_document)
        schema_id, artifact_id, title, status = index_metadata(document)
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=entries,
        )

    def get(self, decision_id: str) -> DecisionIndexEntry:
        """Return a decision-index entry by identifier."""

        return get_entry_by_attr(self.entries, attr_name="decision_id", value=decision_id)


@dataclass(frozen=True, slots=True)
class DesignDocumentIndexEntry:
    """Design-document-index entry."""

    document_id: str
    trace_id: str
    family: str
    title: str
    summary: str
    status: str
    doc_path: str
    updated_at: str
    uses_internal_references: bool
    uses_external_references: bool
    source_paths: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    internal_reference_paths: tuple[str, ...] = ()
    external_reference_urls: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> DesignDocumentIndexEntry:
        return cls(
            document_id=document["document_id"],
            trace_id=document["trace_id"],
            family=document["family"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            source_paths=tuple_field(document, "source_paths"),
            related_paths=tuple_field(document, "related_paths"),
            internal_reference_paths=tuple_field(document, "internal_reference_paths"),
            external_reference_urls=tuple_field(document, "external_reference_urls"),
            tags=tuple_field(document, "tags"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class DesignDocumentIndex:
    """Typed design-document-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[DesignDocumentIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> DesignDocumentIndex:
        entries = load_entries(document, DesignDocumentIndexEntry.from_document)
        schema_id, artifact_id, title, status = index_metadata(document)
        return cls(
            schema_id=schema_id,
            artifact_id=artifact_id,
            title=title,
            status=status,
            entries=entries,
        )

    def get(self, document_id: str) -> DesignDocumentIndexEntry:
        """Return a design-document-index entry by identifier."""

        return get_entry_by_attr(self.entries, attr_name="document_id", value=document_id)
