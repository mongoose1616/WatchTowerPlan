"""Deterministic rebuild helpers for the canonical planning catalog."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    DecisionIndexEntry,
    DesignDocumentIndexEntry,
    InitiativeIndexEntry,
    PlanningAcceptanceContractSummary,
    PlanningCatalogEntry,
    PlanningCoordinationSection,
    PlanningDecisionSummary,
    PlanningDesignDocumentSummary,
    PlanningPrdSummary,
    PlanningTaskSummary,
    PlanningValidationEvidenceSummary,
    PrdIndexEntry,
    TaskIndexEntry,
    TraceabilityEntry,
    ValidationEvidenceArtifact,
)
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.repo_ops.planning_projection_serialization import (
    serialize_planning_catalog_entry,
)
from watchtower_core.repo_ops.sync.tracking_common import latest_timestamp

PLANNING_CATALOG_ARTIFACT_PATH = (
    "core/control_plane/indexes/planning/planning_catalog.v1.json"
)


class PlanningCatalogSyncService:
    """Build and write the canonical planning catalog from trace-linked sources."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> PlanningCatalogSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        traceability_index = self._loader.load_traceability_index()
        initiative_lookup = {
            entry.trace_id: entry for entry in self._loader.load_initiative_index().entries
        }
        prd_entries = _group_by_trace(self._loader.load_prd_index().entries)
        decision_entries = _group_by_trace(self._loader.load_decision_index().entries)
        design_entries = _group_by_trace(self._loader.load_design_document_index().entries)
        task_entries = _group_by_trace(self._loader.load_task_index().entries)
        acceptance_contracts = _group_by_trace(self._loader.load_acceptance_contracts())
        validation_evidence = _group_by_trace(
            self._loader.load_validation_evidence_artifacts()
        )

        entries = [
            self._build_entry(
                trace_entry=trace_entry,
                initiative_entry=initiative_lookup.get(trace_entry.trace_id),
                prd_entries=prd_entries.get(trace_entry.trace_id, ()),
                decision_entries=decision_entries.get(trace_entry.trace_id, ()),
                design_entries=design_entries.get(trace_entry.trace_id, ()),
                task_entries=task_entries.get(trace_entry.trace_id, ()),
                acceptance_contracts=acceptance_contracts.get(trace_entry.trace_id, ()),
                validation_evidence=validation_evidence.get(trace_entry.trace_id, ()),
            )
            for trace_entry in traceability_index.entries
        ]

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:planning-catalog:v1",
            "id": "index.planning_catalog",
            "title": "Planning Catalog",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(
        self,
        document: dict[str, object],
        destination: Path | None = None,
    ) -> Path:
        """Write the generated planning catalog to disk."""
        target = destination or (self._repo_root / PLANNING_CATALOG_ARTIFACT_PATH)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _build_entry(
        self,
        *,
        trace_entry: TraceabilityEntry,
        initiative_entry: InitiativeIndexEntry | None,
        prd_entries: tuple[PrdIndexEntry, ...],
        decision_entries: tuple[DecisionIndexEntry, ...],
        design_entries: tuple[DesignDocumentIndexEntry, ...],
        task_entries: tuple[TaskIndexEntry, ...],
        acceptance_contracts: tuple[AcceptanceContract, ...],
        validation_evidence: tuple[ValidationEvidenceArtifact, ...],
    ) -> dict[str, object]:
        if initiative_entry is None:
            raise ValueError(
                "Planning catalog could not resolve an initiative entry for "
                f"{trace_entry.trace_id}."
            )

        validator_ids = tuple(
            sorted(
                {
                    *trace_entry.validator_ids,
                    *(
                        validator_id
                        for contract in acceptance_contracts
                        for validator_id in _contract_validator_ids(contract)
                    ),
                    *(
                        validator_id
                        for evidence in validation_evidence
                        for validator_id in _evidence_validator_ids(evidence)
                    ),
                }
            )
        )
        related_paths = tuple(
            sorted(
                {
                    *trace_entry.related_paths,
                    initiative_entry.key_surface_path,
                    initiative_entry.next_surface_path,
                    *(entry.doc_path for entry in prd_entries),
                    *(entry.doc_path for entry in decision_entries),
                    *(entry.doc_path for entry in design_entries),
                    *(entry.doc_path for entry in task_entries),
                    *(entry.doc_path for entry in acceptance_contracts),
                    *(entry.doc_path for entry in validation_evidence),
                    *(
                        path
                        for contract in acceptance_contracts
                        for path in _contract_related_paths(contract)
                    ),
                    *(
                        path
                        for evidence in validation_evidence
                        for path in evidence.related_paths
                    ),
                    *(
                        path
                        for task_entry in task_entries
                        for path in task_entry.applies_to
                    ),
                }
            )
        )
        tags = tuple(
            sorted(
                {
                    *trace_entry.tags,
                    *(entry.family for entry in design_entries),
                    *(
                        task_entry.task_kind
                        for task_entry in task_entries
                    ),
                }
            )
        )
        updated_at = latest_timestamp(
            (
                trace_entry.updated_at,
                initiative_entry.updated_at,
                *(entry.updated_at for entry in prd_entries),
                *(entry.updated_at for entry in decision_entries),
                *(entry.updated_at for entry in design_entries),
                *(entry.updated_at for entry in task_entries),
                *(entry.recorded_at for entry in validation_evidence),
            )
        )

        coordination = PlanningCoordinationSection(
            current_phase=initiative_entry.current_phase,
            key_surface_path=initiative_entry.key_surface_path,
            next_action=initiative_entry.next_action,
            next_surface_path=initiative_entry.next_surface_path,
            open_task_count=initiative_entry.open_task_count,
            blocked_task_count=initiative_entry.blocked_task_count,
            primary_owner=initiative_entry.primary_owner,
            active_owners=initiative_entry.active_owners,
            active_task_ids=initiative_entry.active_task_ids,
            active_task_summaries=initiative_entry.active_task_summaries,
            blocked_by_task_ids=initiative_entry.blocked_by_task_ids,
        )
        planning_entry = PlanningCatalogEntry(
            trace_id=trace_entry.trace_id,
            title=trace_entry.title,
            summary=trace_entry.summary,
            artifact_status=trace_entry.status,
            initiative_status=trace_entry.initiative_status,
            updated_at=updated_at,
            coordination=coordination,
            prds=tuple(_planning_prd_summary(item) for item in prd_entries),
            decisions=tuple(_planning_decision_summary(item) for item in decision_entries),
            design_documents=tuple(
                _planning_design_summary(item) for item in design_entries
            ),
            tasks=tuple(_planning_task_summary(item) for item in task_entries),
            acceptance_contracts=tuple(
                _planning_acceptance_contract_summary(item)
                for item in acceptance_contracts
            ),
            validation_evidence=tuple(
                _planning_validation_evidence_summary(item)
                for item in validation_evidence
            ),
            prd_ids=trace_entry.prd_ids,
            decision_ids=trace_entry.decision_ids,
            design_ids=trace_entry.design_ids,
            plan_ids=trace_entry.plan_ids,
            task_ids=trace_entry.task_ids,
            requirement_ids=trace_entry.requirement_ids,
            acceptance_ids=trace_entry.acceptance_ids,
            acceptance_contract_ids=trace_entry.acceptance_contract_ids,
            evidence_ids=trace_entry.evidence_ids,
            validator_ids=validator_ids,
            related_paths=related_paths,
            tags=tags,
            notes=trace_entry.notes,
            closed_at=trace_entry.closed_at,
            closure_reason=trace_entry.closure_reason,
            superseded_by_trace_id=trace_entry.superseded_by_trace_id,
        )
        return serialize_planning_catalog_entry(planning_entry, compact=True)


def _group_by_trace[T: object](
    entries: tuple[T, ...],
) -> dict[str, tuple[T, ...]]:
    grouped: dict[str, list[T]] = {}
    for entry in entries:
        trace_id = getattr(entry, "trace_id", None)
        if not isinstance(trace_id, str) or not trace_id:
            continue
        grouped.setdefault(trace_id, []).append(entry)
    return {trace_id: tuple(values) for trace_id, values in grouped.items()}


def _planning_prd_summary(entry: PrdIndexEntry) -> PlanningPrdSummary:
    return PlanningPrdSummary(
        prd_id=entry.prd_id,
        title=entry.title,
        summary=entry.summary,
        artifact_status=entry.status,
        doc_path=entry.doc_path,
        updated_at=entry.updated_at,
        requirement_ids=entry.requirement_ids,
        acceptance_ids=entry.acceptance_ids,
        linked_decision_ids=entry.linked_decision_ids,
        linked_design_ids=entry.linked_design_ids,
        linked_plan_ids=entry.linked_plan_ids,
    )


def _planning_decision_summary(entry: DecisionIndexEntry) -> PlanningDecisionSummary:
    return PlanningDecisionSummary(
        decision_id=entry.decision_id,
        title=entry.title,
        summary=entry.summary,
        record_status=entry.record_status,
        decision_status=entry.decision_status,
        doc_path=entry.doc_path,
        updated_at=entry.updated_at,
        linked_prd_ids=entry.linked_prd_ids,
        linked_design_ids=entry.linked_design_ids,
        linked_plan_ids=entry.linked_plan_ids,
    )


def _planning_design_summary(
    entry: DesignDocumentIndexEntry,
) -> PlanningDesignDocumentSummary:
    return PlanningDesignDocumentSummary(
        document_id=entry.document_id,
        family=entry.family,
        title=entry.title,
        summary=entry.summary,
        artifact_status=entry.status,
        doc_path=entry.doc_path,
        updated_at=entry.updated_at,
        source_paths=entry.source_paths,
    )


def _planning_task_summary(entry: TaskIndexEntry) -> PlanningTaskSummary:
    return PlanningTaskSummary(
        task_id=entry.task_id,
        title=entry.title,
        summary=entry.summary,
        artifact_status=entry.status,
        task_status=entry.task_status,
        task_kind=entry.task_kind,
        priority=entry.priority,
        owner=entry.owner,
        doc_path=entry.doc_path,
        updated_at=entry.updated_at,
        blocked_by=entry.blocked_by,
        depends_on=entry.depends_on,
        related_ids=entry.related_ids,
        applies_to=entry.applies_to,
    )


def _planning_acceptance_contract_summary(
    entry: AcceptanceContract,
) -> PlanningAcceptanceContractSummary:
    return PlanningAcceptanceContractSummary(
        contract_id=entry.contract_id,
        title=entry.title,
        artifact_status=entry.status,
        source_prd_id=entry.source_prd_id,
        doc_path=entry.doc_path,
        acceptance_ids=tuple(item.acceptance_id for item in entry.entries),
        required_validator_ids=_contract_validator_ids(entry),
        validation_targets=tuple(
            sorted(
                {
                    target
                    for item in entry.entries
                    for target in item.validation_targets
                }
            )
        ),
        related_paths=tuple(
            sorted(
                {
                    path
                    for item in entry.entries
                    for path in item.related_paths
                }
            )
        ),
    )


def _contract_related_paths(entry: AcceptanceContract) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                path
                for item in entry.entries
                for path in item.related_paths
            }
        )
    )


def _contract_validator_ids(entry: AcceptanceContract) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                validator_id
                for item in entry.entries
                for validator_id in item.required_validator_ids
            }
        )
    )


def _planning_validation_evidence_summary(
    entry: ValidationEvidenceArtifact,
) -> PlanningValidationEvidenceSummary:
    return PlanningValidationEvidenceSummary(
        evidence_id=entry.evidence_id,
        title=entry.title,
        artifact_status=entry.status,
        overall_result=entry.overall_result,
        recorded_at=entry.recorded_at,
        doc_path=entry.doc_path,
        check_ids=tuple(check.check_id for check in entry.checks),
        acceptance_ids=tuple(
            sorted(
                {
                    acceptance_id
                    for check in entry.checks
                    for acceptance_id in check.acceptance_ids
                }
            )
        ),
        validator_ids=_evidence_validator_ids(entry),
        related_paths=entry.related_paths,
    )


def _evidence_validator_ids(entry: ValidationEvidenceArtifact) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                check.validator_id
                for check in entry.checks
                if check.validator_id is not None
            }
        )
    )
