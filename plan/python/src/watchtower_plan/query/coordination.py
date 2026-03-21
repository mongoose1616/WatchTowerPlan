"""Repo-specific query helpers for the coordination index."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import CoordinationIndex, InitiativeIndexEntry
from watchtower_core.query.rendered_search import rendered_search_filters_from_params
from watchtower_plan.workspace.service import PlanWorkspaceService
from watchtower_plan.query.initiatives import (
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
        self._plan_workspace = PlanWorkspaceService(loader)
        self._initiative_service = InitiativeQueryService(loader)

    def search(self, params: CoordinationSearchParams) -> CoordinationQueryResult:
        """Return coordination entries matching the requested filters."""
        index = self._plan_workspace.load_coordination_index()
        if _delegates_to_initiative_history(params):
            return CoordinationQueryResult(
                index=index,
                entries=self._initiative_service.search(params),
            )
        entries = self._plan_workspace.search_coordination(
            rendered_search_filters_from_params(
                params,
                blocked_only=params.blocked_only,
            )
        )
        return CoordinationQueryResult(index=index, entries=entries)


def _delegates_to_initiative_history(params: CoordinationSearchParams) -> bool:
    """Keep the coordination snapshot compact by delegating explicit history lookups."""
    if params.initiative_status is None:
        return False
    return params.initiative_status.casefold() != "active"
