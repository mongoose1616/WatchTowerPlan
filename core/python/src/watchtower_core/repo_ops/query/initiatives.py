"""Repo-specific query helpers for initiative coordination records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import InitiativeIndexEntry
from watchtower_core.repo_ops.plan_workspace import PlanWorkspaceService
from watchtower_core.repo_ops.query.common import (
    initiative_rendered_query_terms,
    rendered_search_filters_from_params,
    search_rendered_entries,
)


@dataclass(frozen=True, slots=True)
class InitiativeSearchParams:
    """Filter and ranking inputs for initiative lookup."""

    query: str | None = None
    trace_id: str | None = None
    initiative_status: str | None = None
    current_phase: str | None = None
    owner: str | None = None
    blocked_only: bool = False
    limit: int | None = None


class InitiativeQueryService:
    """Search the initiative index with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._plan_workspace = PlanWorkspaceService(loader)

    def search(self, params: InitiativeSearchParams) -> tuple[InitiativeIndexEntry, ...]:
        """Return initiative entries matching the requested filters."""
        return search_rendered_entries(
            self._plan_workspace.load_initiative_index().entries,
            rendered_search_filters_from_params(
                params,
                blocked_only=params.blocked_only,
            ),
            query_fields=initiative_rendered_query_terms,
            sort_key=lambda entry: entry.trace_id,
            trace_id=lambda entry: entry.trace_id,
            initiative_status=lambda entry: entry.initiative_status,
            current_phase=lambda entry: entry.current_phase,
            primary_owner=lambda entry: entry.primary_owner,
            active_owners=lambda entry: entry.active_owners,
            blocked_task_count=lambda entry: entry.blocked_task_count,
        )

    def get(self, trace_id: str) -> InitiativeIndexEntry:
        """Return one initiative entry by its trace identifier."""
        return self._plan_workspace.load_initiative_index().get(trace_id)
