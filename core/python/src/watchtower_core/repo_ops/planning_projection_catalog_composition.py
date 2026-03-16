"""Private helpers for composing planning catalog entries from one snapshot."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.models import (
    AcceptanceContract,
    DecisionIndexEntry,
    DesignDocumentIndexEntry,
    PlanningAcceptanceContractSummary,
    PlanningCatalogEntry,
    PlanningDecisionSummary,
    PlanningDesignDocumentSummary,
    PlanningPrdSummary,
    PlanningTaskSummary,
    PlanningValidationEvidenceSummary,
    PrdIndexEntry,
    TaskIndexEntry,
    ValidationEvidenceArtifact,
)
from watchtower_core.repo_ops.planning_projection_snapshot import (
    TracePlanningCoordinationSnapshot,
    TracePlanningProjectionSnapshot,
)
from watchtower_core.repo_ops.sync.tracking_common import (
    effective_updated_at,
    latest_timestamp,
)


@dataclass(frozen=True, slots=True)
class TracePlanningCatalogAggregation:
    """Catalog-only aggregated metadata derived from one planning snapshot."""

    validator_ids: tuple[str, ...]
    related_paths: tuple[str, ...]
    tags: tuple[str, ...]
    updated_at: str


def build_trace_planning_catalog_aggregation(
    snapshot: TracePlanningProjectionSnapshot,
    coordination: TracePlanningCoordinationSnapshot,
) -> TracePlanningCatalogAggregation:
    """Aggregate catalog-only metadata that should stay out of the sync entrypoint."""

    trace_entry = snapshot.trace_entry
    initiative_updated_at = effective_updated_at(trace_entry.updated_at, trace_entry.closed_at)

    return TracePlanningCatalogAggregation(
        validator_ids=tuple(
            sorted(
                {
                    *trace_entry.validator_ids,
                    *(
                        validator_id
                        for contract in snapshot.acceptance_contracts
                        for validator_id in _contract_validator_ids(contract)
                    ),
                    *(
                        validator_id
                        for evidence in snapshot.validation_evidence
                        for validator_id in _evidence_validator_ids(evidence)
                    ),
                }
            )
        ),
        related_paths=tuple(
            sorted(
                {
                    *trace_entry.related_paths,
                    coordination.key_surface_path,
                    coordination.next_surface_path,
                    *(entry.doc_path for entry in snapshot.prd_entries),
                    *(entry.doc_path for entry in snapshot.decision_entries),
                    *(entry.doc_path for entry in snapshot.design_entries),
                    *(entry.doc_path for entry in snapshot.task_entries),
                    *(entry.doc_path for entry in snapshot.acceptance_contracts),
                    *(entry.doc_path for entry in snapshot.validation_evidence),
                    *(
                        path
                        for contract in snapshot.acceptance_contracts
                        for path in _contract_related_paths(contract)
                    ),
                    *(
                        path
                        for evidence in snapshot.validation_evidence
                        for path in evidence.related_paths
                    ),
                    *(
                        path
                        for task_entry in snapshot.task_entries
                        for path in task_entry.applies_to
                    ),
                }
            )
        ),
        tags=tuple(
            sorted(
                {
                    *trace_entry.tags,
                    *(entry.family for entry in snapshot.design_entries),
                    *(task_entry.task_kind for task_entry in snapshot.task_entries),
                }
            )
        ),
        updated_at=latest_timestamp(
            (
                trace_entry.updated_at,
                initiative_updated_at,
                *(entry.updated_at for entry in snapshot.prd_entries),
                *(entry.updated_at for entry in snapshot.decision_entries),
                *(entry.updated_at for entry in snapshot.design_entries),
                *(entry.updated_at for entry in snapshot.task_entries),
                *(entry.recorded_at for entry in snapshot.validation_evidence),
            )
        ),
    )


def build_trace_planning_catalog_entry(
    snapshot: TracePlanningProjectionSnapshot,
    coordination: TracePlanningCoordinationSnapshot,
) -> PlanningCatalogEntry:
    """Compose the full typed planning catalog entry for one trace snapshot."""

    trace_entry = snapshot.trace_entry
    aggregation = build_trace_planning_catalog_aggregation(snapshot, coordination)

    return PlanningCatalogEntry(
        trace_id=trace_entry.trace_id,
        title=trace_entry.title,
        summary=trace_entry.summary,
        artifact_status=trace_entry.status,
        initiative_status=trace_entry.initiative_status,
        updated_at=aggregation.updated_at,
        coordination=coordination.to_planning_coordination_section(),
        prds=tuple(_planning_prd_summary(item) for item in snapshot.prd_entries),
        decisions=tuple(
            _planning_decision_summary(item) for item in snapshot.decision_entries
        ),
        design_documents=tuple(
            _planning_design_summary(item) for item in snapshot.design_entries
        ),
        tasks=tuple(_planning_task_summary(item) for item in snapshot.task_entries),
        acceptance_contracts=tuple(
            _planning_acceptance_contract_summary(item)
            for item in snapshot.acceptance_contracts
        ),
        validation_evidence=tuple(
            _planning_validation_evidence_summary(item)
            for item in snapshot.validation_evidence
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
        validator_ids=aggregation.validator_ids,
        related_paths=aggregation.related_paths,
        tags=aggregation.tags,
        notes=trace_entry.notes,
        closed_at=trace_entry.closed_at,
        closure_reason=trace_entry.closure_reason,
        superseded_by_trace_id=trace_entry.superseded_by_trace_id,
    )


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
        related_paths=_contract_related_paths(entry),
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
