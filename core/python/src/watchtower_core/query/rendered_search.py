"""Generic rendered-surface query helpers used by hosted packs."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any, Protocol

from watchtower_core.control_plane.models import InitiativeIndexEntry
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
    """Common rendered-search parameter shape used across hosted packs."""

    @property
    def query(self) -> str | None: ...

    @property
    def trace_id(self) -> str | None: ...

    @property
    def initiative_status(self) -> str | None: ...

    @property
    def current_phase(self) -> str | None: ...

    @property
    def owner(self) -> str | None: ...

    @property
    def limit(self) -> int | None: ...


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
        *entry.source_surface_paths,
        *entry.acceptance_ids,
        *entry.acceptance_contract_ids,
        *entry.evidence_ids,
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


__all__ = [
    "RenderedSearchFilters",
    "RenderedSearchParamsLike",
    "initiative_rendered_query_terms",
    "rendered_search_filters_from_params",
    "search_rendered_entries",
]
