"""Search helpers for workspace index entries."""

from __future__ import annotations

from watchtower_core.query.common import (
    normalize_optional_text,
    normalize_text,
    query_score,
)

from watchtower_plan.workspace.constants import PRIORITY_ORDER
from watchtower_plan.workspace.models import (
    PlanCloseoutIndexEntry,
    PlanCloseoutSearchParams,
    PlanDiscrepancyIndexEntry,
    PlanDiscrepancySearchParams,
    PlanEvidenceIndexEntry,
    PlanEvidenceSearchParams,
    PlanReadinessIndexEntry,
    PlanReadinessSearchParams,
    PlanReviewIndexEntry,
    PlanReviewSearchParams,
    PlanTaskIndexEntry,
    PlanTaskSearchParams,
)
from watchtower_plan.workspace.support import task_status_order


def search_task_entries(
    entries: tuple[PlanTaskIndexEntry, ...],
    params: PlanTaskSearchParams,
) -> tuple[PlanTaskIndexEntry, ...]:
    initiative_id = normalize_optional_text(params.initiative_id)
    project_id = normalize_optional_text(params.project_id)
    trace_id = normalize_optional_text(params.trace_id)
    status = normalize_optional_text(params.status)
    priority = normalize_optional_text(params.priority)
    owner = normalize_optional_text(params.owner)
    matches: list[tuple[int, PlanTaskIndexEntry]] = []
    for entry in entries:
        if (
            initiative_id is not None
            and normalize_text(entry.initiative_id) != initiative_id
        ):
            continue
        if (
            project_id is not None
            and normalize_text(entry.project_id or "") != project_id
        ):
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if status is not None and normalize_text(entry.task_status) != status:
            continue
        if priority is not None and normalize_text(entry.priority) != priority:
            continue
        if owner is not None and normalize_text(entry.owner) != owner:
            continue
        if params.blocked_only and not entry.blocked_by:
            continue
        score = query_score(
            params.query,
            (
                entry.task_id,
                entry.initiative_id,
                entry.project_id or "",
                entry.trace_id,
                entry.initiative_title,
                entry.title,
                entry.summary,
                entry.task_status,
                entry.priority,
                entry.owner,
                entry.doc_path,
                *entry.blocked_by,
                *entry.depends_on,
                *entry.related_ids,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(
        key=lambda item: (
            -item[0],
            task_status_order(item[1].task_status),
            PRIORITY_ORDER.get(item[1].priority, 99),
            item[1].task_id,
        )
    )
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)


def search_readiness_entries(
    entries: tuple[PlanReadinessIndexEntry, ...],
    params: PlanReadinessSearchParams,
) -> tuple[PlanReadinessIndexEntry, ...]:
    initiative_id = normalize_optional_text(params.initiative_id)
    project_id = normalize_optional_text(params.project_id)
    trace_id = normalize_optional_text(params.trace_id)
    lifecycle_stage = normalize_optional_text(params.lifecycle_stage)
    review_status = normalize_optional_text(params.review_status)
    matches: list[tuple[int, PlanReadinessIndexEntry]] = []
    for entry in entries:
        if (
            initiative_id is not None
            and normalize_text(entry.initiative_id) != initiative_id
        ):
            continue
        if (
            project_id is not None
            and normalize_text(entry.project_id or "") != project_id
        ):
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if (
            lifecycle_stage is not None
            and normalize_text(entry.lifecycle_stage) != lifecycle_stage
        ):
            continue
        if (
            review_status is not None
            and normalize_text(entry.review_status) != review_status
        ):
            continue
        if (
            params.ready_for_execution is not None
            and entry.ready_for_execution != params.ready_for_execution
        ):
            continue
        if params.blocked_only and not entry.blocking_reasons:
            continue
        score = query_score(
            params.query,
            (
                entry.initiative_id,
                entry.project_id or "",
                entry.trace_id,
                entry.title,
                entry.initiative_root,
                entry.lifecycle_stage,
                entry.review_status,
                entry.approval_status,
                *entry.blocking_reasons,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1].initiative_id))
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)


def search_discrepancy_entries(
    entries: tuple[PlanDiscrepancyIndexEntry, ...],
    params: PlanDiscrepancySearchParams,
) -> tuple[PlanDiscrepancyIndexEntry, ...]:
    initiative_id = normalize_optional_text(params.initiative_id)
    project_id = normalize_optional_text(params.project_id)
    trace_id = normalize_optional_text(params.trace_id)
    category = normalize_optional_text(params.category)
    severity = normalize_optional_text(params.severity)
    status = normalize_optional_text(params.status)
    matches: list[tuple[int, PlanDiscrepancyIndexEntry]] = []
    for entry in entries:
        if (
            initiative_id is not None
            and normalize_text(entry.initiative_id) != initiative_id
        ):
            continue
        if (
            project_id is not None
            and normalize_text(entry.project_id or "") != project_id
        ):
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if category is not None and normalize_text(entry.category) != category:
            continue
        if severity is not None and normalize_text(entry.severity) != severity:
            continue
        if status is not None and normalize_text(entry.status) != status:
            continue
        if params.blocking_only and entry.gate_effect == "none":
            continue
        score = query_score(
            params.query,
            (
                entry.discrepancy_id,
                entry.initiative_id,
                entry.project_id or "",
                entry.trace_id,
                entry.title,
                entry.category,
                entry.severity,
                entry.gate_effect,
                entry.status,
                entry.summary,
                *entry.source_paths,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1].discrepancy_id))
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)


def search_evidence_entries(
    entries: tuple[PlanEvidenceIndexEntry, ...],
    params: PlanEvidenceSearchParams,
) -> tuple[PlanEvidenceIndexEntry, ...]:
    initiative_id = normalize_optional_text(params.initiative_id)
    project_id = normalize_optional_text(params.project_id)
    trace_id = normalize_optional_text(params.trace_id)
    status = normalize_optional_text(params.status)
    owner = normalize_optional_text(params.owner)
    target_phase = normalize_optional_text(params.target_phase)
    validation_type = normalize_optional_text(params.validation_type)
    acceptance_label = normalize_optional_text(params.acceptance_label)
    matches: list[tuple[int, PlanEvidenceIndexEntry]] = []
    for entry in entries:
        if (
            initiative_id is not None
            and normalize_text(entry.initiative_id) != initiative_id
        ):
            continue
        if (
            project_id is not None
            and normalize_text(entry.project_id or "") != project_id
        ):
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if status is not None and normalize_text(entry.status) != status:
            continue
        if owner is not None and owner not in {
            normalize_text(value) for value in entry.owners
        }:
            continue
        if target_phase is not None and target_phase not in {
            normalize_text(value) for value in entry.target_phases
        }:
            continue
        if validation_type is not None and validation_type not in {
            normalize_text(value) for value in entry.validation_types
        }:
            continue
        if acceptance_label is not None and acceptance_label not in {
            normalize_text(value) for value in entry.acceptance_labels
        }:
            continue
        score = query_score(
            params.query,
            (
                entry.evidence_id,
                entry.initiative_id,
                entry.project_id or "",
                entry.trace_id,
                entry.initiative_title,
                entry.title,
                entry.status,
                *entry.acceptance_labels,
                *entry.validation_types,
                *entry.owners,
                *entry.target_phases,
                *entry.expected_output_paths,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1].evidence_id))
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)


def search_closeout_entries(
    entries: tuple[PlanCloseoutIndexEntry, ...],
    params: PlanCloseoutSearchParams,
) -> tuple[PlanCloseoutIndexEntry, ...]:
    initiative_id = normalize_optional_text(params.initiative_id)
    project_id = normalize_optional_text(params.project_id)
    trace_id = normalize_optional_text(params.trace_id)
    status = normalize_optional_text(params.status)
    terminal_state = normalize_optional_text(params.terminal_state)
    matches: list[tuple[int, PlanCloseoutIndexEntry]] = []
    for entry in entries:
        if (
            initiative_id is not None
            and normalize_text(entry.initiative_id) != initiative_id
        ):
            continue
        if (
            project_id is not None
            and normalize_text(entry.project_id or "") != project_id
        ):
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if status is not None and normalize_text(entry.status) != status:
            continue
        if (
            terminal_state is not None
            and normalize_text(entry.terminal_state or "") != terminal_state
        ):
            continue
        if (
            params.promotion_review_required is not None
            and entry.promotion_review_required != params.promotion_review_required
        ):
            continue
        score = query_score(
            params.query,
            (
                entry.closeout_id,
                entry.initiative_id,
                entry.project_id or "",
                entry.trace_id,
                entry.initiative_title,
                entry.title,
                entry.status,
                entry.expected_outcome,
                entry.follow_up_handling,
                *entry.acceptance_ids,
                *entry.evidence_ids,
                *entry.terminal_state_options,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1].closeout_id))
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)


def search_review_entries(
    entries: tuple[PlanReviewIndexEntry, ...],
    params: PlanReviewSearchParams,
) -> tuple[PlanReviewIndexEntry, ...]:
    subject_kind = normalize_optional_text(params.subject_kind)
    initiative_id = normalize_optional_text(params.initiative_id)
    project_id = normalize_optional_text(params.project_id)
    trace_id = normalize_optional_text(params.trace_id)
    review_state = normalize_optional_text(params.review_state)
    review_ref = normalize_optional_text(params.review_ref)
    matches: list[tuple[int, PlanReviewIndexEntry]] = []
    for entry in entries:
        if (
            subject_kind is not None
            and normalize_text(entry.subject_kind) != subject_kind
        ):
            continue
        if (
            initiative_id is not None
            and normalize_text(entry.initiative_id) != initiative_id
        ):
            continue
        if (
            project_id is not None
            and normalize_text(entry.project_id or "") != project_id
        ):
            continue
        if trace_id is not None and normalize_text(entry.trace_id) != trace_id:
            continue
        if (
            review_state is not None
            and normalize_text(entry.review_state) != review_state
        ):
            continue
        if (
            params.ready_for_execution is not None
            and entry.ready_for_execution != params.ready_for_execution
        ):
            continue
        if review_ref is not None and review_ref not in {
            normalize_text(value) for value in entry.review_refs
        }:
            continue
        score = query_score(
            params.query,
            (
                entry.review_subject_id,
                entry.subject_kind,
                entry.initiative_id,
                entry.project_id or "",
                entry.trace_id,
                entry.initiative_title,
                entry.title,
                entry.review_state,
                entry.lifecycle_stage or "",
                *entry.review_refs,
                *entry.evidence_refs,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1].review_subject_id))
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)
