"""Typed models for planning and documentation index artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
            requirement_ids=tuple(document.get("requirement_ids", ())),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            linked_decision_ids=tuple(document.get("linked_decision_ids", ())),
            linked_design_ids=tuple(document.get("linked_design_ids", ())),
            linked_plan_ids=tuple(document.get("linked_plan_ids", ())),
            related_paths=tuple(document.get("related_paths", ())),
            internal_reference_paths=tuple(document.get("internal_reference_paths", ())),
            external_reference_urls=tuple(document.get("external_reference_urls", ())),
            tags=tuple(document.get("tags", ())),
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
        entries = tuple(PrdIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, prd_id: str) -> PrdIndexEntry:
        """Return a PRD-index entry by identifier."""
        for entry in self.entries:
            if entry.prd_id == prd_id:
                return entry
        raise KeyError(prd_id)


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
            linked_prd_ids=tuple(document.get("linked_prd_ids", ())),
            linked_design_ids=tuple(document.get("linked_design_ids", ())),
            linked_plan_ids=tuple(document.get("linked_plan_ids", ())),
            related_paths=tuple(document.get("related_paths", ())),
            internal_reference_paths=tuple(document.get("internal_reference_paths", ())),
            applied_reference_paths=tuple(document.get("applied_reference_paths", ())),
            external_reference_urls=tuple(document.get("external_reference_urls", ())),
            applied_external_reference_urls=tuple(
                document.get("applied_external_reference_urls", ())
            ),
            tags=tuple(document.get("tags", ())),
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
        entries = tuple(DecisionIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, decision_id: str) -> DecisionIndexEntry:
        """Return a decision-index entry by identifier."""
        for entry in self.entries:
            if entry.decision_id == decision_id:
                return entry
        raise KeyError(decision_id)


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
            source_paths=tuple(document.get("source_paths", ())),
            related_paths=tuple(document.get("related_paths", ())),
            internal_reference_paths=tuple(document.get("internal_reference_paths", ())),
            external_reference_urls=tuple(document.get("external_reference_urls", ())),
            tags=tuple(document.get("tags", ())),
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
        entries = tuple(
            DesignDocumentIndexEntry.from_document(entry) for entry in document["entries"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, document_id: str) -> DesignDocumentIndexEntry:
        """Return a design-document-index entry by identifier."""
        for entry in self.entries:
            if entry.document_id == document_id:
                return entry
        raise KeyError(document_id)


@dataclass(frozen=True, slots=True)
class ReferenceIndexEntry:
    """Reference-index entry."""

    reference_id: str
    title: str
    summary: str
    status: str
    doc_path: str
    updated_at: str
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
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            canonical_upstream_urls=tuple(document.get("canonical_upstream_urls", ())),
            cited_by_paths=tuple(document.get("cited_by_paths", ())),
            applied_by_paths=tuple(document.get("applied_by_paths", ())),
            related_paths=tuple(document.get("related_paths", ())),
            aliases=tuple(document.get("aliases", ())),
            tags=tuple(document.get("tags", ())),
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
        entries = tuple(ReferenceIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, reference_id: str) -> ReferenceIndexEntry:
        """Return a reference-index entry by identifier."""
        for entry in self.entries:
            if entry.reference_id == reference_id:
                return entry
        raise KeyError(reference_id)


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
            related_paths=tuple(document.get("related_paths", ())),
            reference_doc_paths=tuple(document.get("reference_doc_paths", ())),
            internal_reference_paths=tuple(document.get("internal_reference_paths", ())),
            external_reference_urls=tuple(document.get("external_reference_urls", ())),
            cited_by_paths=tuple(document.get("cited_by_paths", ())),
            applied_by_paths=tuple(document.get("applied_by_paths", ())),
            aliases=tuple(document.get("aliases", ())),
            tags=tuple(document.get("tags", ())),
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
        entries = tuple(FoundationIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, foundation_id: str) -> FoundationIndexEntry:
        """Return a foundation-index entry by identifier."""
        for entry in self.entries:
            if entry.foundation_id == foundation_id:
                return entry
        raise KeyError(foundation_id)


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
            applies_to=tuple(document.get("applies_to", ())),
            related_paths=tuple(document.get("related_paths", ())),
            reference_doc_paths=tuple(document.get("reference_doc_paths", ())),
            internal_reference_paths=tuple(document.get("internal_reference_paths", ())),
            applied_reference_paths=tuple(document.get("applied_reference_paths", ())),
            external_reference_urls=tuple(document.get("external_reference_urls", ())),
            applied_external_reference_urls=tuple(
                document.get("applied_external_reference_urls", ())
            ),
            operationalization_modes=tuple(document.get("operationalization_modes", ())),
            operationalization_paths=tuple(document.get("operationalization_paths", ())),
            tags=tuple(document.get("tags", ())),
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
        entries = tuple(StandardIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, standard_id: str) -> StandardIndexEntry:
        """Return a standard-index entry by identifier."""
        for entry in self.entries:
            if entry.standard_id == standard_id:
                return entry
        raise KeyError(standard_id)


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
            primary_risks=tuple(document.get("primary_risks", ())),
            trigger_tags=tuple(document.get("trigger_tags", ())),
            companion_workflow_ids=tuple(document.get("companion_workflow_ids", ())),
            related_paths=tuple(document.get("related_paths", ())),
            reference_doc_paths=tuple(document.get("reference_doc_paths", ())),
            internal_reference_paths=tuple(document.get("internal_reference_paths", ())),
            external_reference_urls=tuple(document.get("external_reference_urls", ())),
            aliases=tuple(document.get("aliases", ())),
            tags=tuple(document.get("tags", ())),
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
        entries = tuple(WorkflowIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, workflow_id: str) -> WorkflowIndexEntry:
        """Return a workflow-index entry by identifier."""
        for entry in self.entries:
            if entry.workflow_id == workflow_id:
                return entry
        raise KeyError(workflow_id)
