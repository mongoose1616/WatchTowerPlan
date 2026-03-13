"""Repo-specific query helpers for the coordination index."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import CoordinationIndex, InitiativeIndexEntry
from watchtower_core.repo_ops.query.common import (
    ProjectionSearchFilters,
    initiative_projection_query_terms,
    search_projection_entries,
)
from watchtower_core.repo_ops.query.initiatives import (
    InitiativeQueryService,
    InitiativeSearchParams,
)

CoordinationSearchParams = InitiativeSearchParams


@dataclass(frozen=True, slots=True)
class CoordinationQueryResult:
    """Coordination query results plus the underlying coordination snapshot."""

    index: CoordinationIndex
    entries: tuple[InitiativeIndexEntry, ...]


class CoordinationQueryService:
    """Search the coordination index with structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._initiative_service = InitiativeQueryService(loader)

    def search(self, params: CoordinationSearchParams) -> CoordinationQueryResult:
        """Return coordination entries matching the requested filters."""
        index = self._loader.load_coordination_index()
        if _delegates_to_initiative_history(params):
            return CoordinationQueryResult(
                index=index,
                entries=self._initiative_service.search(params),
            )
        entry_rank = {entry.trace_id: idx for idx, entry in enumerate(index.entries)}
        entries = search_projection_entries(
            index.entries,
            ProjectionSearchFilters(
                query=params.query,
                trace_id=params.trace_id,
                initiative_status=params.initiative_status,
                current_phase=params.current_phase,
                owner=params.owner,
                blocked_only=params.blocked_only,
                limit=params.limit,
            ),
            query_fields=initiative_projection_query_terms,
            sort_key=lambda entry: (entry_rank.get(entry.trace_id, 9999), entry.trace_id),
            trace_id=lambda entry: entry.trace_id,
            initiative_status=lambda entry: entry.initiative_status,
            current_phase=lambda entry: entry.current_phase,
            primary_owner=lambda entry: entry.primary_owner,
            active_owners=lambda entry: entry.active_owners,
            blocked_task_count=lambda entry: entry.blocked_task_count,
        )
        return CoordinationQueryResult(index=index, entries=entries)


def _delegates_to_initiative_history(params: CoordinationSearchParams) -> bool:
    """Keep the coordination snapshot compact by delegating explicit history lookups."""
    if params.initiative_status is None:
        return False
    return params.initiative_status.casefold() != "active"
