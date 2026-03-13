"""Repo-specific query helpers for canonical planning-catalog records."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import PlanningCatalogEntry
from watchtower_core.repo_ops.query.common import (
    ProjectionSearchFilters,
    planning_catalog_query_terms,
    search_projection_entries,
)


@dataclass(frozen=True, slots=True)
class PlanningCatalogSearchParams:
    """Filter and ranking inputs for planning-catalog lookup."""

    query: str | None = None
    trace_id: str | None = None
    initiative_status: str | None = None
    current_phase: str | None = None
    owner: str | None = None
    limit: int | None = None


class PlanningCatalogQueryService:
    """Search the canonical planning catalog with simple structured filters."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(
        self,
        params: PlanningCatalogSearchParams,
    ) -> tuple[PlanningCatalogEntry, ...]:
        """Return planning-catalog entries matching the requested filters."""
        catalog = self._loader.load_planning_catalog()
        return search_projection_entries(
            catalog.entries,
            ProjectionSearchFilters(
                query=params.query,
                trace_id=params.trace_id,
                initiative_status=params.initiative_status,
                current_phase=params.current_phase,
                owner=params.owner,
                limit=params.limit,
            ),
            query_fields=planning_catalog_query_terms,
            sort_key=lambda entry: entry.trace_id,
            trace_id=lambda entry: entry.trace_id,
            initiative_status=lambda entry: entry.initiative_status,
            current_phase=lambda entry: entry.current_phase,
            primary_owner=lambda entry: entry.primary_owner,
            active_owners=lambda entry: entry.active_owners,
        )

    def get(self, trace_id: str) -> PlanningCatalogEntry:
        """Return one planning-catalog entry by its trace identifier."""
        return self._loader.load_planning_catalog().get(trace_id)
