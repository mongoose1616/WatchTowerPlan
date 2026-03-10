"""Typed models for acceptance and validation evidence artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
