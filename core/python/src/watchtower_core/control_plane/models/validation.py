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
    source_surface_path: str
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
            source_surface_path=document["source_surface_path"],
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
    source_surface_paths: tuple[str, ...] = ()
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
        checks = tuple(ValidationEvidenceCheck.from_document(entry) for entry in document["checks"])
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
            source_surface_paths=tuple(document.get("source_surface_paths", ())),
            source_acceptance_contract_ids=tuple(
                document.get("source_acceptance_contract_ids", ())
            ),
            related_paths=tuple(document.get("related_paths", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class EvidenceBundleEntry:
    """Evidence-bundle entry describing one expected validation or review output."""

    entry_id: str
    acceptance_label: str
    validation_type: str
    owner: str
    target_phase: str
    expected_output_paths: tuple[str, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> EvidenceBundleEntry:
        return cls(
            entry_id=document["entry_id"],
            acceptance_label=document["acceptance_label"],
            validation_type=document["validation_type"],
            owner=document["owner"],
            target_phase=document["target_phase"],
            expected_output_paths=tuple(document["expected_output_paths"]),
        )


@dataclass(frozen=True, slots=True)
class EvidenceBundleArtifact:
    """Typed evidence-bundle artifact for initiative-local validation bundles."""

    schema_id: str
    evidence_id: str
    initiative_id: str
    trace_id: str
    title: str
    status: str
    updated_at: str
    entries: tuple[EvidenceBundleEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> EvidenceBundleArtifact:
        return cls(
            schema_id=document["$schema"],
            evidence_id=document["id"],
            initiative_id=document["initiative_id"],
            trace_id=document["trace_id"],
            title=document["title"],
            status=document["status"],
            updated_at=document["updated_at"],
            entries=tuple(
                EvidenceBundleEntry.from_document(entry) for entry in document["entries"]
            ),
        )

    @property
    def entry_count(self) -> int:
        """Return the number of bundle entries."""

        return len(self.entries)

    @property
    def acceptance_labels(self) -> tuple[str, ...]:
        """Return the unique acceptance labels covered by the bundle."""

        return tuple(sorted({entry.acceptance_label for entry in self.entries}))

    @property
    def validation_types(self) -> tuple[str, ...]:
        """Return the unique validation or review types covered by the bundle."""

        return tuple(sorted({entry.validation_type for entry in self.entries}))

    @property
    def owners(self) -> tuple[str, ...]:
        """Return the unique owners responsible for the bundle entries."""

        return tuple(sorted({entry.owner for entry in self.entries}))

    @property
    def target_phases(self) -> tuple[str, ...]:
        """Return the unique target phases covered by the bundle."""

        return tuple(sorted({entry.target_phase for entry in self.entries}))

    @property
    def expected_output_paths(self) -> tuple[str, ...]:
        """Return the unique expected output paths referenced by the bundle."""

        return tuple(
            sorted({path for entry in self.entries for path in entry.expected_output_paths})
        )


@dataclass(frozen=True, slots=True)
class TracePurgeRecord:
    """Typed trace-purge record artifact."""

    schema_id: str
    record_id: str
    title: str
    status: str
    trace_id: str
    initiative_status: str
    closed_at: str
    purged_at: str
    closure_reason: str
    summary: str
    doc_path: str
    surviving_authority_paths: tuple[str, ...]
    purged_paths: tuple[str, ...]
    notes: str | None = None

    @classmethod
    def from_document(
        cls,
        document: dict[str, Any],
        *,
        doc_path: str,
    ) -> TracePurgeRecord:
        return cls(
            schema_id=document["$schema"],
            record_id=document["id"],
            title=document["title"],
            status=document["status"],
            trace_id=document["trace_id"],
            initiative_status=document["initiative_status"],
            closed_at=document["closed_at"],
            purged_at=document["purged_at"],
            closure_reason=document["closure_reason"],
            summary=document["summary"],
            doc_path=doc_path,
            surviving_authority_paths=tuple(document["surviving_authority_paths"]),
            purged_paths=tuple(document["purged_paths"]),
            notes=document.get("notes"),
        )
