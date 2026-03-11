"""Typed models for the canonical planning-catalog artifact."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from watchtower_core.control_plane.models.coordination import InitiativeActiveTaskSummary


@dataclass(frozen=True, slots=True)
class PlanningCoordinationSection:
    """Per-trace coordination section embedded in one planning-catalog entry."""

    current_phase: str
    key_surface_path: str
    next_action: str
    next_surface_path: str
    open_task_count: int
    blocked_task_count: int
    primary_owner: str | None = None
    active_owners: tuple[str, ...] = ()
    active_task_ids: tuple[str, ...] = ()
    active_task_summaries: tuple[InitiativeActiveTaskSummary, ...] = ()
    blocked_by_task_ids: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningCoordinationSection:
        return cls(
            current_phase=document["current_phase"],
            key_surface_path=document["key_surface_path"],
            next_action=document["next_action"],
            next_surface_path=document["next_surface_path"],
            open_task_count=document["open_task_count"],
            blocked_task_count=document["blocked_task_count"],
            primary_owner=document.get("primary_owner"),
            active_owners=tuple(document.get("active_owners", ())),
            active_task_ids=tuple(document.get("active_task_ids", ())),
            active_task_summaries=tuple(
                InitiativeActiveTaskSummary.from_document(entry)
                for entry in document.get("active_task_summaries", ())
            ),
            blocked_by_task_ids=tuple(document.get("blocked_by_task_ids", ())),
        )


@dataclass(frozen=True, slots=True)
class PlanningPrdSummary:
    """Compact PRD summary embedded in the planning catalog."""

    prd_id: str
    title: str
    summary: str
    artifact_status: str
    doc_path: str
    updated_at: str
    requirement_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    linked_decision_ids: tuple[str, ...] = ()
    linked_design_ids: tuple[str, ...] = ()
    linked_plan_ids: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningPrdSummary:
        return cls(
            prd_id=document["prd_id"],
            title=document["title"],
            summary=document["summary"],
            artifact_status=document["artifact_status"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            requirement_ids=tuple(document.get("requirement_ids", ())),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            linked_decision_ids=tuple(document.get("linked_decision_ids", ())),
            linked_design_ids=tuple(document.get("linked_design_ids", ())),
            linked_plan_ids=tuple(document.get("linked_plan_ids", ())),
        )


@dataclass(frozen=True, slots=True)
class PlanningDecisionSummary:
    """Compact decision summary embedded in the planning catalog."""

    decision_id: str
    title: str
    summary: str
    record_status: str
    decision_status: str
    doc_path: str
    updated_at: str
    linked_prd_ids: tuple[str, ...] = ()
    linked_design_ids: tuple[str, ...] = ()
    linked_plan_ids: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningDecisionSummary:
        return cls(
            decision_id=document["decision_id"],
            title=document["title"],
            summary=document["summary"],
            record_status=document["record_status"],
            decision_status=document["decision_status"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            linked_prd_ids=tuple(document.get("linked_prd_ids", ())),
            linked_design_ids=tuple(document.get("linked_design_ids", ())),
            linked_plan_ids=tuple(document.get("linked_plan_ids", ())),
        )


@dataclass(frozen=True, slots=True)
class PlanningDesignDocumentSummary:
    """Compact design-document summary embedded in the planning catalog."""

    document_id: str
    family: str
    title: str
    summary: str
    artifact_status: str
    doc_path: str
    updated_at: str
    source_paths: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningDesignDocumentSummary:
        return cls(
            document_id=document["document_id"],
            family=document["family"],
            title=document["title"],
            summary=document["summary"],
            artifact_status=document["artifact_status"],
            doc_path=document["doc_path"],
            updated_at=document["updated_at"],
            source_paths=tuple(document.get("source_paths", ())),
        )


@dataclass(frozen=True, slots=True)
class PlanningTaskSummary:
    """Compact task summary embedded in the planning catalog."""

    task_id: str
    title: str
    summary: str
    artifact_status: str
    task_status: str
    task_kind: str
    priority: str
    owner: str
    doc_path: str
    updated_at: str
    blocked_by: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    applies_to: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningTaskSummary:
        return cls(
            task_id=document["task_id"],
            title=document["title"],
            summary=document["summary"],
            artifact_status=document["artifact_status"],
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
        )


@dataclass(frozen=True, slots=True)
class PlanningAcceptanceContractSummary:
    """Compact acceptance-contract summary embedded in the planning catalog."""

    contract_id: str
    title: str
    artifact_status: str
    source_prd_id: str
    doc_path: str
    acceptance_ids: tuple[str, ...] = ()
    required_validator_ids: tuple[str, ...] = ()
    validation_targets: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningAcceptanceContractSummary:
        return cls(
            contract_id=document["contract_id"],
            title=document["title"],
            artifact_status=document["artifact_status"],
            source_prd_id=document["source_prd_id"],
            doc_path=document["doc_path"],
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            required_validator_ids=tuple(document.get("required_validator_ids", ())),
            validation_targets=tuple(document.get("validation_targets", ())),
            related_paths=tuple(document.get("related_paths", ())),
        )


@dataclass(frozen=True, slots=True)
class PlanningValidationEvidenceSummary:
    """Compact validation-evidence summary embedded in the planning catalog."""

    evidence_id: str
    title: str
    artifact_status: str
    overall_result: str
    recorded_at: str
    doc_path: str
    check_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    validator_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningValidationEvidenceSummary:
        return cls(
            evidence_id=document["evidence_id"],
            title=document["title"],
            artifact_status=document["artifact_status"],
            overall_result=document["overall_result"],
            recorded_at=document["recorded_at"],
            doc_path=document["doc_path"],
            check_ids=tuple(document.get("check_ids", ())),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            validator_ids=tuple(document.get("validator_ids", ())),
            related_paths=tuple(document.get("related_paths", ())),
        )


@dataclass(frozen=True, slots=True)
class PlanningCatalogEntry:
    """One canonical planning-catalog entry."""

    trace_id: str
    title: str
    summary: str
    artifact_status: str
    initiative_status: str
    updated_at: str
    coordination: PlanningCoordinationSection
    prds: tuple[PlanningPrdSummary, ...] = ()
    decisions: tuple[PlanningDecisionSummary, ...] = ()
    design_documents: tuple[PlanningDesignDocumentSummary, ...] = ()
    tasks: tuple[PlanningTaskSummary, ...] = ()
    acceptance_contracts: tuple[PlanningAcceptanceContractSummary, ...] = ()
    validation_evidence: tuple[PlanningValidationEvidenceSummary, ...] = ()
    prd_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    design_ids: tuple[str, ...] = ()
    plan_ids: tuple[str, ...] = ()
    task_ids: tuple[str, ...] = ()
    requirement_ids: tuple[str, ...] = ()
    acceptance_ids: tuple[str, ...] = ()
    acceptance_contract_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    validator_ids: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    notes: str | None = None
    closed_at: str | None = None
    closure_reason: str | None = None
    superseded_by_trace_id: str | None = None

    @property
    def current_phase(self) -> str:
        """Expose the coordination current phase for filtering."""
        return self.coordination.current_phase

    @property
    def primary_owner(self) -> str | None:
        """Expose the coordination primary owner for filtering."""
        return self.coordination.primary_owner

    @property
    def active_owners(self) -> tuple[str, ...]:
        """Expose the current active owners for filtering."""
        return self.coordination.active_owners

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningCatalogEntry:
        return cls(
            trace_id=document["trace_id"],
            title=document["title"],
            summary=document["summary"],
            artifact_status=document["artifact_status"],
            initiative_status=document["initiative_status"],
            updated_at=document["updated_at"],
            coordination=PlanningCoordinationSection.from_document(
                document["coordination"]
            ),
            prds=tuple(
                PlanningPrdSummary.from_document(entry)
                for entry in document.get("prds", ())
            ),
            decisions=tuple(
                PlanningDecisionSummary.from_document(entry)
                for entry in document.get("decisions", ())
            ),
            design_documents=tuple(
                PlanningDesignDocumentSummary.from_document(entry)
                for entry in document.get("design_documents", ())
            ),
            tasks=tuple(
                PlanningTaskSummary.from_document(entry)
                for entry in document.get("tasks", ())
            ),
            acceptance_contracts=tuple(
                PlanningAcceptanceContractSummary.from_document(entry)
                for entry in document.get("acceptance_contracts", ())
            ),
            validation_evidence=tuple(
                PlanningValidationEvidenceSummary.from_document(entry)
                for entry in document.get("validation_evidence", ())
            ),
            prd_ids=tuple(document.get("prd_ids", ())),
            decision_ids=tuple(document.get("decision_ids", ())),
            design_ids=tuple(document.get("design_ids", ())),
            plan_ids=tuple(document.get("plan_ids", ())),
            task_ids=tuple(document.get("task_ids", ())),
            requirement_ids=tuple(document.get("requirement_ids", ())),
            acceptance_ids=tuple(document.get("acceptance_ids", ())),
            acceptance_contract_ids=tuple(document.get("acceptance_contract_ids", ())),
            evidence_ids=tuple(document.get("evidence_ids", ())),
            validator_ids=tuple(document.get("validator_ids", ())),
            related_paths=tuple(document.get("related_paths", ())),
            tags=tuple(document.get("tags", ())),
            notes=document.get("notes"),
            closed_at=document.get("closed_at"),
            closure_reason=document.get("closure_reason"),
            superseded_by_trace_id=document.get("superseded_by_trace_id"),
        )


@dataclass(frozen=True, slots=True)
class PlanningCatalog:
    """Typed planning-catalog artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[PlanningCatalogEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PlanningCatalog:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(
                PlanningCatalogEntry.from_document(entry)
                for entry in document["entries"]
            ),
        )

    def get(self, trace_id: str) -> PlanningCatalogEntry:
        """Return a planning-catalog entry by trace identifier."""
        for entry in self.entries:
            if entry.trace_id == trace_id:
                return entry
        raise KeyError(trace_id)
