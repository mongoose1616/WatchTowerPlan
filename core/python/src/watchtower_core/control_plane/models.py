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
    def from_document(cls, document: dict[str, Any], repo_root: Path) -> SchemaCatalogRecord:
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
    def from_document(cls, document: dict[str, Any], repo_root: Path) -> SchemaCatalog:
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
    def from_document(cls, document: dict[str, Any]) -> RepositoryPathEntry:
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
class InitiativeIndexEntry:
    """Initiative-index entry."""

    trace_id: str
    title: str
    summary: str
    status: str
    initiative_status: str
    current_phase: str
    updated_at: str
    open_task_count: int
    blocked_task_count: int
    key_surface_path: str
    next_action: str
    next_surface_path: str
    primary_owner: str | None = None
    active_owners: tuple[str, ...] = ()
    active_task_ids: tuple[str, ...] = ()
    blocked_by_task_ids: tuple[str, ...] = ()
    prd_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    design_ids: tuple[str, ...] = ()
    plan_ids: tuple[str, ...] = ()
    task_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    acceptance_contract_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    closed_at: str | None = None
    closure_reason: str | None = None
    superseded_by_trace_id: str | None = None
    related_paths: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> InitiativeIndexEntry:
        return cls(
            trace_id=document["trace_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            initiative_status=document["initiative_status"],
            current_phase=document["current_phase"],
            updated_at=document["updated_at"],
            open_task_count=document["open_task_count"],
            blocked_task_count=document["blocked_task_count"],
            key_surface_path=document["key_surface_path"],
            next_action=document["next_action"],
            next_surface_path=document["next_surface_path"],
            primary_owner=document.get("primary_owner"),
            active_owners=tuple(document.get("active_owners", ())),
            active_task_ids=tuple(document.get("active_task_ids", ())),
            blocked_by_task_ids=tuple(document.get("blocked_by_task_ids", ())),
            prd_ids=tuple(document.get("prd_ids", ())),
            decision_ids=tuple(document.get("decision_ids", ())),
            design_ids=tuple(document.get("design_ids", ())),
            plan_ids=tuple(document.get("plan_ids", ())),
            task_ids=tuple(document.get("task_ids", ())),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            acceptance_contract_ids=tuple(document.get("acceptance_contract_ids", ())),
            evidence_ids=tuple(document.get("evidence_ids", ())),
            closed_at=document.get("closed_at"),
            closure_reason=document.get("closure_reason"),
            superseded_by_trace_id=document.get("superseded_by_trace_id"),
            related_paths=tuple(document.get("related_paths", ())),
            tags=tuple(document.get("tags", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class InitiativeIndex:
    """Typed initiative-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[InitiativeIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> InitiativeIndex:
        entries = tuple(InitiativeIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, trace_id: str) -> InitiativeIndexEntry:
        """Return an initiative-index entry by trace identifier."""
        for entry in self.entries:
            if entry.trace_id == trace_id:
                return entry
        raise KeyError(trace_id)


@dataclass(frozen=True, slots=True)
class StandardIndexEntry:
    """Standard-index entry."""

    standard_id: str
    category: str
    title: str
    summary: str
    status: str
    doc_path: str
    updated_at: str
    uses_internal_references: bool
    uses_external_references: bool
    related_paths: tuple[str, ...] = ()
    reference_doc_paths: tuple[str, ...] = ()
    internal_reference_paths: tuple[str, ...] = ()
    applied_reference_paths: tuple[str, ...] = ()
    external_reference_urls: tuple[str, ...] = ()
    applied_external_reference_urls: tuple[str, ...] = ()
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
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
            related_paths=tuple(document.get("related_paths", ())),
            reference_doc_paths=tuple(document.get("reference_doc_paths", ())),
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
            uses_internal_references=document["uses_internal_references"],
            uses_external_references=document["uses_external_references"],
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


@dataclass(frozen=True, slots=True)
class TaskIndexEntry:
    """Task-index entry."""

    task_id: str
    title: str
    summary: str
    status: str
    task_status: str
    task_kind: str
    priority: str
    owner: str
    doc_path: str
    updated_at: str
    trace_id: str | None = None
    blocked_by: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    applies_to: tuple[str, ...] = ()
    github_repository: str | None = None
    github_issue_number: int | None = None
    github_issue_node_id: str | None = None
    github_project_owner: str | None = None
    github_project_owner_type: str | None = None
    github_project_number: int | None = None
    github_project_item_id: str | None = None
    github_synced_at: str | None = None
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TaskIndexEntry:
        return cls(
            task_id=document["task_id"],
            trace_id=document.get("trace_id"),
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            task_status=document["task_status"],
            task_kind=document["task_kind"],
            priority=document["priority"],
            owner=document["owner"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            blocked_by=tuple(document.get("blocked_by", ())),
            depends_on=tuple(document.get("depends_on", ())),
            related_ids=tuple(document.get("related_ids", ())),
            applies_to=tuple(document.get("applies_to", ())),
            github_repository=document.get("github_repository"),
            github_issue_number=document.get("github_issue_number"),
            github_issue_node_id=document.get("github_issue_node_id"),
            github_project_owner=document.get("github_project_owner"),
            github_project_owner_type=document.get("github_project_owner_type"),
            github_project_number=document.get("github_project_number"),
            github_project_item_id=document.get("github_project_item_id"),
            github_synced_at=document.get("github_synced_at"),
            tags=tuple(document.get("tags", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class TaskIndex:
    """Typed task-index artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[TaskIndexEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TaskIndex:
        entries = tuple(TaskIndexEntry.from_document(entry) for entry in document["entries"])
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, task_id: str) -> TaskIndexEntry:
        """Return a task-index entry by identifier."""
        for entry in self.entries:
            if entry.task_id == task_id:
                return entry
        raise KeyError(task_id)


@dataclass(frozen=True, slots=True)
class TraceabilityEntry:
    """Traceability-index entry."""

    trace_id: str
    title: str
    summary: str
    status: str
    initiative_status: str
    updated_at: str
    closed_at: str | None = None
    closure_reason: str | None = None
    superseded_by_trace_id: str | None = None
    prd_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    design_ids: tuple[str, ...] = ()
    plan_ids: tuple[str, ...] = ()
    task_ids: tuple[str, ...] = ()
    requirement_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    acceptance_contract_ids: tuple[str, ...] = ()
    validator_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TraceabilityEntry:
        return cls(
            trace_id=document["trace_id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            initiative_status=document["initiative_status"],
            updated_at=document["updated_at"],
            closed_at=document.get("closed_at"),
            closure_reason=document.get("closure_reason"),
            superseded_by_trace_id=document.get("superseded_by_trace_id"),
            prd_ids=tuple(document.get("prd_ids", ())),
            decision_ids=tuple(document.get("decision_ids", ())),
            design_ids=tuple(document.get("design_ids", ())),
            plan_ids=tuple(document.get("plan_ids", ())),
            task_ids=tuple(document.get("task_ids", ())),
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
    def from_document(cls, document: dict[str, Any]) -> TraceabilityIndex:
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


@dataclass(frozen=True, slots=True)
class AcceptanceContractItem:
    """Acceptance-contract entry."""

    acceptance_id: str
    summary: str
    source_requirement_ids: tuple[str, ...] = ()
    required_validator_ids: tuple[str, ...] = ()
    validation_targets: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> AcceptanceContractItem:
        return cls(
            acceptance_id=document["acceptance_id"],
            summary=document["summary"],
            source_requirement_ids=tuple(document.get("source_requirement_ids", ())),
            required_validator_ids=tuple(document.get("required_validator_ids", ())),
            validation_targets=tuple(document.get("validation_targets", ())),
            related_paths=tuple(document.get("related_paths", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class AcceptanceContract:
    """Typed acceptance-contract artifact."""

    schema_id: str
    contract_id: str
    title: str
    status: str
    trace_id: str
    source_prd_id: str
    doc_path: str
    entries: tuple[AcceptanceContractItem, ...]

    @classmethod
    def from_document(
        cls,
        document: dict[str, Any],
        *,
        doc_path: str,
    ) -> AcceptanceContract:
        entries = tuple(
            AcceptanceContractItem.from_document(entry) for entry in document["entries"]
        )
        return cls(
            schema_id=document["$schema"],
            contract_id=document["id"],
            title=document["title"],
            status=document["status"],
            trace_id=document["trace_id"],
            source_prd_id=document["source_prd_id"],
            doc_path=doc_path,
            entries=entries,
        )


@dataclass(frozen=True, slots=True)
class ValidationEvidenceCheck:
    """Validation-evidence check entry."""

    check_id: str
    title: str
    result: str
    subject_paths: tuple[str, ...] = ()
    subject_ids: tuple[str, ...] = ()
    validator_id: str | None = None
    acceptance_ids: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidationEvidenceCheck:
        return cls(
            check_id=document["check_id"],
            title=document["title"],
            result=document["result"],
            subject_paths=tuple(document.get("subject_paths", ())),
            subject_ids=tuple(document.get("subject_ids", ())),
            validator_id=document.get("validator_id"),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ValidationEvidenceArtifact:
    """Typed validation-evidence artifact."""

    schema_id: str
    evidence_id: str
    title: str
    status: str
    trace_id: str
    overall_result: str
    recorded_at: str
    doc_path: str
    checks: tuple[ValidationEvidenceCheck, ...]
    source_prd_ids: tuple[str, ...] = ()
    source_decision_ids: tuple[str, ...] = ()
    source_design_ids: tuple[str, ...] = ()
    source_plan_ids: tuple[str, ...] = ()
    source_acceptance_contract_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(
        cls,
        document: dict[str, Any],
        *,
        doc_path: str,
    ) -> ValidationEvidenceArtifact:
        checks = tuple(
            ValidationEvidenceCheck.from_document(entry) for entry in document["checks"]
        )
        return cls(
            schema_id=document["$schema"],
            evidence_id=document["id"],
            title=document["title"],
            status=document["status"],
            trace_id=document["trace_id"],
            overall_result=document["overall_result"],
            recorded_at=document["recorded_at"],
            doc_path=doc_path,
            checks=checks,
            source_prd_ids=tuple(document.get("source_prd_ids", ())),
            source_decision_ids=tuple(document.get("source_decision_ids", ())),
            source_design_ids=tuple(document.get("source_design_ids", ())),
            source_plan_ids=tuple(document.get("source_plan_ids", ())),
            source_acceptance_contract_ids=tuple(
                document.get("source_acceptance_contract_ids", ())
            ),
            related_paths=tuple(document.get("related_paths", ())),
            notes=document.get("notes"),
        )
