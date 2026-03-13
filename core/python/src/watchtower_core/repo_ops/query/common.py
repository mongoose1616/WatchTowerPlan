"""Shared helpers for index-backed query services."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from watchtower_core.control_plane.models import InitiativeIndexEntry, PlanningCatalogEntry


@dataclass(frozen=True, slots=True)
class ProjectionSearchFilters:
    """Normalized filter inputs for trace-linked projection search."""

    query: str | None = None
    trace_id: str | None = None
    initiative_status: str | None = None
    current_phase: str | None = None
    owner: str | None = None
    blocked_only: bool = False
    limit: int | None = None


def normalize_text(value: str) -> str:
    """Normalize text for case-insensitive matching."""
    return value.casefold().strip()


def normalize_optional_text(value: str | None) -> str | None:
    """Normalize optional text for case-insensitive matching."""
    if value is None:
        return None
    return normalize_text(value)


def query_score(query: str | None, fields: Iterable[str]) -> int | None:
    """Return a simple relevance score or None when the query does not match."""
    if query is None:
        return 0

    tokens = [token for token in normalize_text(query).split() if token]
    if not tokens:
        return 0

    haystacks = [normalize_text(field) for field in fields if field]
    score = 0

    for token in tokens:
        token_score = 0
        for haystack in haystacks:
            if haystack == token:
                token_score = max(token_score, 12)
            elif haystack.startswith(token):
                token_score = max(token_score, 8)
            elif token in haystack:
                token_score = max(token_score, 4)
        if token_score == 0:
            return None
        score += token_score

    return score


def search_projection_entries[EntryT](
    entries: Iterable[EntryT],
    filters: ProjectionSearchFilters,
    *,
    query_fields: Callable[[EntryT], Iterable[str]],
    sort_key: Callable[[EntryT], Any],
    trace_id: Callable[[EntryT], str],
    initiative_status: Callable[[EntryT], str],
    current_phase: Callable[[EntryT], str],
    primary_owner: Callable[[EntryT], str | None],
    active_owners: Callable[[EntryT], Iterable[str]],
    blocked_task_count: Callable[[EntryT], int] | None = None,
) -> tuple[EntryT, ...]:
    """Apply shared projection search filters and deterministic ranking."""
    normalized_trace_id = normalize_optional_text(filters.trace_id)
    normalized_initiative_status = normalize_optional_text(filters.initiative_status)
    normalized_current_phase = normalize_optional_text(filters.current_phase)
    normalized_owner = normalize_optional_text(filters.owner)

    matches: list[tuple[int, Any, EntryT]] = []
    for entry in entries:
        if (
            normalized_trace_id is not None
            and normalize_text(trace_id(entry)) != normalized_trace_id
        ):
            continue
        if (
            normalized_initiative_status is not None
            and normalize_text(initiative_status(entry)) != normalized_initiative_status
        ):
            continue
        if (
            normalized_current_phase is not None
            and normalize_text(current_phase(entry)) != normalized_current_phase
        ):
            continue
        if normalized_owner is not None and not _owner_matches(
            normalized_owner,
            primary_owner=primary_owner(entry),
            active_owners=active_owners(entry),
        ):
            continue
        if filters.blocked_only:
            if blocked_task_count is None or blocked_task_count(entry) == 0:
                continue

        score = query_score(filters.query, query_fields(entry))
        if score is None:
            continue
        matches.append((score, sort_key(entry), entry))

    matches.sort(key=lambda item: (-item[0], item[1]))
    ordered_entries = [entry for _, _, entry in matches]
    if filters.limit is not None:
        ordered_entries = ordered_entries[: filters.limit]
    return tuple(ordered_entries)


def initiative_projection_query_terms(entry: InitiativeIndexEntry) -> tuple[str, ...]:
    """Return deterministic searchable terms for compact initiative projections."""
    return (
        entry.trace_id,
        entry.title,
        entry.summary,
        entry.artifact_status,
        entry.initiative_status,
        entry.current_phase,
        entry.primary_owner or "",
        entry.key_surface_path,
        entry.next_action,
        entry.next_surface_path,
        *entry.active_owners,
        *entry.active_task_ids,
        *(task.task_id for task in entry.active_task_summaries),
        *(task.title for task in entry.active_task_summaries),
        *(task.task_status for task in entry.active_task_summaries),
        *(task.priority for task in entry.active_task_summaries),
        *(task.owner for task in entry.active_task_summaries),
        *(task.doc_path for task in entry.active_task_summaries),
        *(blocker for task in entry.active_task_summaries for blocker in task.blocked_by),
        *(dependency for task in entry.active_task_summaries for dependency in task.depends_on),
        *entry.prd_ids,
        *entry.decision_ids,
        *entry.design_ids,
        *entry.plan_ids,
        *entry.acceptance_ids,
        *entry.acceptance_contract_ids,
        *entry.evidence_ids,
        *entry.related_paths,
        *entry.tags,
    )


def planning_catalog_query_terms(entry: PlanningCatalogEntry) -> tuple[str, ...]:
    """Return deterministic searchable terms for deep planning projections."""
    return (
        entry.trace_id,
        entry.title,
        entry.summary,
        entry.artifact_status,
        entry.initiative_status,
        entry.updated_at,
        entry.coordination.current_phase,
        entry.coordination.key_surface_path,
        entry.coordination.next_action,
        entry.coordination.next_surface_path,
        entry.coordination.primary_owner or "",
        *entry.coordination.active_owners,
        *entry.coordination.active_task_ids,
        *(task.task_id for task in entry.coordination.active_task_summaries),
        *(task.title for task in entry.coordination.active_task_summaries),
        *(item.prd_id for item in entry.prds),
        *(item.title for item in entry.prds),
        *(item.decision_id for item in entry.decisions),
        *(item.title for item in entry.decisions),
        *(item.document_id for item in entry.design_documents),
        *(item.title for item in entry.design_documents),
        *(item.task_id for item in entry.tasks),
        *(item.title for item in entry.tasks),
        *(item.contract_id for item in entry.acceptance_contracts),
        *(item.title for item in entry.acceptance_contracts),
        *(item.evidence_id for item in entry.validation_evidence),
        *(item.title for item in entry.validation_evidence),
        *entry.prd_ids,
        *entry.decision_ids,
        *entry.design_ids,
        *entry.plan_ids,
        *entry.task_ids,
        *entry.requirement_ids,
        *entry.acceptance_ids,
        *entry.acceptance_contract_ids,
        *entry.evidence_ids,
        *entry.validator_ids,
        *entry.related_paths,
        *entry.tags,
    )


def _owner_matches(
    normalized_owner: str,
    *,
    primary_owner: str | None,
    active_owners: Iterable[str],
) -> bool:
    owner_values = {normalize_text(value) for value in active_owners if value}
    if primary_owner is not None:
        owner_values.add(normalize_text(primary_owner))
    return normalized_owner in owner_values
