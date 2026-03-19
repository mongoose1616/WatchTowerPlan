"""Shared helpers for index-backed query services."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass
from typing import Any, Protocol

from watchtower_core.control_plane.models import InitiativeIndexEntry, PlanningCatalogEntry
from watchtower_core.query.common import normalize_optional_text, normalize_text, query_score


@dataclass(frozen=True, slots=True)
class RenderedSearchFilters:
    """Normalized filter inputs for trace-linked rendered-surface search."""

    query: str | None = None
    trace_id: str | None = None
    initiative_status: str | None = None
    current_phase: str | None = None
    owner: str | None = None
    blocked_only: bool = False
    limit: int | None = None


class RenderedSearchParamsLike(Protocol):
    """Common rendered-search parameter shape used across repo-local queries."""

    query: str | None
    trace_id: str | None
    initiative_status: str | None
    current_phase: str | None
    owner: str | None
    limit: int | None


class DataclassSearchAdapter[ParamsT, TargetParamsT, EntryT]:
    """Translate one query dataclass into the adjacent workspace search boundary."""

    def __init__(
        self,
        *,
        target_type: type[TargetParamsT],
        search: Callable[[TargetParamsT], tuple[EntryT, ...]],
    ) -> None:
        self._target_type = target_type
        self._search = search

    def search(self, params: ParamsT) -> tuple[EntryT, ...]:
        """Delegate one query through a differently typed workspace search contract."""

        return self._search(self._target_type(**asdict(params)))


def rendered_search_filters_from_params(
    params: RenderedSearchParamsLike,
    *,
    blocked_only: bool = False,
) -> RenderedSearchFilters:
    """Build one rendered-search filter set from a shared params contract."""

    return RenderedSearchFilters(
        query=params.query,
        trace_id=params.trace_id,
        initiative_status=params.initiative_status,
        current_phase=params.current_phase,
        owner=params.owner,
        blocked_only=blocked_only,
        limit=params.limit,
    )


def search_rendered_entries[EntryT](
    entries: Iterable[EntryT],
    filters: RenderedSearchFilters,
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
    """Apply shared rendered-surface search filters and deterministic ranking."""
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


def initiative_rendered_query_terms(entry: InitiativeIndexEntry) -> tuple[str, ...]:
    """Return deterministic searchable terms for compact initiative rendered surfaces."""
    return (
        entry.trace_id,
        entry.initiative_id or "",
        entry.slug or "",
        entry.title,
        entry.summary,
        entry.artifact_status,
        entry.initiative_status,
        entry.current_phase,
        entry.scope_type or "",
        entry.project_id or "",
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


def planning_catalog_rendered_query_terms(
    entry: PlanningCatalogEntry,
) -> tuple[str, ...]:
    """Return deterministic searchable terms for deep planning rendered surfaces."""
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
