"""Shared serializers for initiative and planning projection payloads."""

from __future__ import annotations

from watchtower_core.control_plane.models import (
    InitiativeActiveTaskSummary,
    InitiativeIndexEntry,
    PlanningAcceptanceContractSummary,
    PlanningCatalogEntry,
    PlanningCoordinationSection,
    PlanningDecisionSummary,
    PlanningDesignDocumentSummary,
    PlanningPrdSummary,
    PlanningTaskSummary,
    PlanningValidationEvidenceSummary,
)


def _sequence_payload(
    values: tuple[str, ...],
    *,
    compact: bool,
) -> list[str] | None:
    if compact and not values:
        return None
    return list(values)


def _assign_sequence(
    payload: dict[str, object],
    key: str,
    values: tuple[str, ...],
    *,
    compact: bool,
) -> None:
    rendered = _sequence_payload(values, compact=compact)
    if rendered is None:
        return
    payload[key] = rendered


def _assign_scalar(
    payload: dict[str, object],
    key: str,
    value: object,
    *,
    compact: bool,
) -> None:
    if compact and value is None:
        return
    payload[key] = value


def serialize_active_task_summary(
    task: InitiativeActiveTaskSummary,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "task_id": task.task_id,
        "title": task.title,
        "task_status": task.task_status,
        "priority": task.priority,
        "owner": task.owner,
        "doc_path": task.doc_path,
        "is_actionable": task.is_actionable,
    }
    _assign_sequence(payload, "blocked_by", task.blocked_by, compact=compact)
    _assign_sequence(payload, "depends_on", task.depends_on, compact=compact)
    return payload


def serialize_coordination_section(
    entry: InitiativeIndexEntry | PlanningCoordinationSection,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "current_phase": entry.current_phase,
        "key_surface_path": entry.key_surface_path,
        "next_action": entry.next_action,
        "next_surface_path": entry.next_surface_path,
        "open_task_count": entry.open_task_count,
        "blocked_task_count": entry.blocked_task_count,
    }
    _assign_scalar(payload, "primary_owner", entry.primary_owner, compact=compact)
    _assign_sequence(payload, "active_owners", entry.active_owners, compact=compact)
    _assign_sequence(payload, "active_task_ids", entry.active_task_ids, compact=compact)
    if compact:
        if entry.active_task_summaries:
            payload["active_task_summaries"] = [
                serialize_active_task_summary(task, compact=True)
                for task in entry.active_task_summaries
            ]
    else:
        payload["active_task_summaries"] = [
            serialize_active_task_summary(task, compact=False)
            for task in entry.active_task_summaries
        ]
    _assign_sequence(
        payload,
        "blocked_by_task_ids",
        entry.blocked_by_task_ids,
        compact=compact,
    )
    return payload


def serialize_initiative_entry(
    entry: InitiativeIndexEntry,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "trace_id": entry.trace_id,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.artifact_status,
        "initiative_status": entry.initiative_status,
        "current_phase": entry.current_phase,
        "updated_at": entry.updated_at,
        "open_task_count": entry.open_task_count,
        "blocked_task_count": entry.blocked_task_count,
        "key_surface_path": entry.key_surface_path,
        "next_action": entry.next_action,
        "next_surface_path": entry.next_surface_path,
    }
    _assign_scalar(payload, "primary_owner", entry.primary_owner, compact=compact)
    _assign_sequence(payload, "active_owners", entry.active_owners, compact=compact)
    _assign_sequence(payload, "active_task_ids", entry.active_task_ids, compact=compact)
    if compact:
        if entry.active_task_summaries:
            payload["active_task_summaries"] = [
                serialize_active_task_summary(task, compact=True)
                for task in entry.active_task_summaries
            ]
    else:
        payload["active_task_summaries"] = [
            serialize_active_task_summary(task, compact=False)
            for task in entry.active_task_summaries
        ]
    _assign_sequence(
        payload,
        "blocked_by_task_ids",
        entry.blocked_by_task_ids,
        compact=compact,
    )
    _assign_sequence(payload, "prd_ids", entry.prd_ids, compact=compact)
    _assign_sequence(payload, "decision_ids", entry.decision_ids, compact=compact)
    _assign_sequence(payload, "design_ids", entry.design_ids, compact=compact)
    _assign_sequence(payload, "plan_ids", entry.plan_ids, compact=compact)
    _assign_sequence(payload, "task_ids", entry.task_ids, compact=compact)
    _assign_sequence(payload, "acceptance_ids", entry.acceptance_ids, compact=compact)
    _assign_sequence(
        payload,
        "acceptance_contract_ids",
        entry.acceptance_contract_ids,
        compact=compact,
    )
    _assign_sequence(payload, "evidence_ids", entry.evidence_ids, compact=compact)
    _assign_scalar(payload, "closed_at", entry.closed_at, compact=compact)
    _assign_scalar(payload, "closure_reason", entry.closure_reason, compact=compact)
    _assign_scalar(
        payload,
        "superseded_by_trace_id",
        entry.superseded_by_trace_id,
        compact=compact,
    )
    _assign_sequence(payload, "related_paths", entry.related_paths, compact=compact)
    _assign_sequence(payload, "tags", entry.tags, compact=compact)
    _assign_scalar(payload, "notes", entry.notes, compact=compact)
    return payload


def serialize_planning_prd_summary(
    entry: PlanningPrdSummary,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "prd_id": entry.prd_id,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.artifact_status,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    _assign_sequence(payload, "requirement_ids", entry.requirement_ids, compact=compact)
    _assign_sequence(payload, "acceptance_ids", entry.acceptance_ids, compact=compact)
    _assign_sequence(
        payload,
        "linked_decision_ids",
        entry.linked_decision_ids,
        compact=compact,
    )
    _assign_sequence(
        payload,
        "linked_design_ids",
        entry.linked_design_ids,
        compact=compact,
    )
    _assign_sequence(payload, "linked_plan_ids", entry.linked_plan_ids, compact=compact)
    return payload


def serialize_planning_decision_summary(
    entry: PlanningDecisionSummary,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "decision_id": entry.decision_id,
        "title": entry.title,
        "summary": entry.summary,
        "record_status": entry.record_status,
        "decision_status": entry.decision_status,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    _assign_sequence(payload, "linked_prd_ids", entry.linked_prd_ids, compact=compact)
    _assign_sequence(
        payload,
        "linked_design_ids",
        entry.linked_design_ids,
        compact=compact,
    )
    _assign_sequence(payload, "linked_plan_ids", entry.linked_plan_ids, compact=compact)
    return payload


def serialize_planning_design_document_summary(
    entry: PlanningDesignDocumentSummary,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "document_id": entry.document_id,
        "family": entry.family,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.artifact_status,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    _assign_sequence(payload, "source_paths", entry.source_paths, compact=compact)
    return payload


def serialize_planning_task_summary(
    entry: PlanningTaskSummary,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "task_id": entry.task_id,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.artifact_status,
        "task_status": entry.task_status,
        "task_kind": entry.task_kind,
        "priority": entry.priority,
        "owner": entry.owner,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
    }
    _assign_sequence(payload, "blocked_by", entry.blocked_by, compact=compact)
    _assign_sequence(payload, "depends_on", entry.depends_on, compact=compact)
    _assign_sequence(payload, "related_ids", entry.related_ids, compact=compact)
    _assign_sequence(payload, "applies_to", entry.applies_to, compact=compact)
    return payload


def serialize_planning_acceptance_contract_summary(
    entry: PlanningAcceptanceContractSummary,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "contract_id": entry.contract_id,
        "title": entry.title,
        "artifact_status": entry.artifact_status,
        "source_prd_id": entry.source_prd_id,
        "doc_path": entry.doc_path,
    }
    _assign_sequence(payload, "acceptance_ids", entry.acceptance_ids, compact=compact)
    _assign_sequence(
        payload,
        "required_validator_ids",
        entry.required_validator_ids,
        compact=compact,
    )
    _assign_sequence(
        payload,
        "validation_targets",
        entry.validation_targets,
        compact=compact,
    )
    _assign_sequence(payload, "related_paths", entry.related_paths, compact=compact)
    return payload


def serialize_planning_validation_evidence_summary(
    entry: PlanningValidationEvidenceSummary,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "evidence_id": entry.evidence_id,
        "title": entry.title,
        "artifact_status": entry.artifact_status,
        "overall_result": entry.overall_result,
        "recorded_at": entry.recorded_at,
        "doc_path": entry.doc_path,
    }
    _assign_sequence(payload, "check_ids", entry.check_ids, compact=compact)
    _assign_sequence(payload, "acceptance_ids", entry.acceptance_ids, compact=compact)
    _assign_sequence(payload, "validator_ids", entry.validator_ids, compact=compact)
    _assign_sequence(payload, "related_paths", entry.related_paths, compact=compact)
    return payload


def serialize_planning_catalog_entry(
    entry: PlanningCatalogEntry,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "trace_id": entry.trace_id,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.artifact_status,
        "initiative_status": entry.initiative_status,
        "updated_at": entry.updated_at,
        "coordination": serialize_coordination_section(
            entry.coordination,
            compact=compact,
        ),
    }
    if compact:
        if entry.prds:
            payload["prds"] = [
                serialize_planning_prd_summary(item, compact=True)
                for item in entry.prds
            ]
        if entry.decisions:
            payload["decisions"] = [
                serialize_planning_decision_summary(item, compact=True)
                for item in entry.decisions
            ]
        if entry.design_documents:
            payload["design_documents"] = [
                serialize_planning_design_document_summary(item, compact=True)
                for item in entry.design_documents
            ]
        if entry.tasks:
            payload["tasks"] = [
                serialize_planning_task_summary(item, compact=True)
                for item in entry.tasks
            ]
        if entry.acceptance_contracts:
            payload["acceptance_contracts"] = [
                serialize_planning_acceptance_contract_summary(item, compact=True)
                for item in entry.acceptance_contracts
            ]
        if entry.validation_evidence:
            payload["validation_evidence"] = [
                serialize_planning_validation_evidence_summary(item, compact=True)
                for item in entry.validation_evidence
            ]
    else:
        payload["prds"] = [
            serialize_planning_prd_summary(item, compact=False) for item in entry.prds
        ]
        payload["decisions"] = [
            serialize_planning_decision_summary(item, compact=False)
            for item in entry.decisions
        ]
        payload["design_documents"] = [
            serialize_planning_design_document_summary(item, compact=False)
            for item in entry.design_documents
        ]
        payload["tasks"] = [
            serialize_planning_task_summary(item, compact=False) for item in entry.tasks
        ]
        payload["acceptance_contracts"] = [
            serialize_planning_acceptance_contract_summary(item, compact=False)
            for item in entry.acceptance_contracts
        ]
        payload["validation_evidence"] = [
            serialize_planning_validation_evidence_summary(item, compact=False)
            for item in entry.validation_evidence
        ]
    _assign_sequence(payload, "prd_ids", entry.prd_ids, compact=compact)
    _assign_sequence(payload, "decision_ids", entry.decision_ids, compact=compact)
    _assign_sequence(payload, "design_ids", entry.design_ids, compact=compact)
    _assign_sequence(payload, "plan_ids", entry.plan_ids, compact=compact)
    _assign_sequence(payload, "task_ids", entry.task_ids, compact=compact)
    _assign_sequence(payload, "requirement_ids", entry.requirement_ids, compact=compact)
    _assign_sequence(payload, "acceptance_ids", entry.acceptance_ids, compact=compact)
    _assign_sequence(
        payload,
        "acceptance_contract_ids",
        entry.acceptance_contract_ids,
        compact=compact,
    )
    _assign_sequence(payload, "evidence_ids", entry.evidence_ids, compact=compact)
    _assign_sequence(payload, "validator_ids", entry.validator_ids, compact=compact)
    _assign_sequence(payload, "related_paths", entry.related_paths, compact=compact)
    _assign_sequence(payload, "tags", entry.tags, compact=compact)
    _assign_scalar(payload, "notes", entry.notes, compact=compact)
    _assign_scalar(payload, "closed_at", entry.closed_at, compact=compact)
    _assign_scalar(payload, "closure_reason", entry.closure_reason, compact=compact)
    _assign_scalar(
        payload,
        "superseded_by_trace_id",
        entry.superseded_by_trace_id,
        compact=compact,
    )
    return payload
