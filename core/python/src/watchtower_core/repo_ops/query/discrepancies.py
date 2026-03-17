"""Repo-specific query helpers for live plan discrepancies."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.plan_workspace import (
    PlanDiscrepancyIndexEntry,
    PlanDiscrepancySearchParams,
    PlanWorkspaceService,
)


@dataclass(frozen=True, slots=True)
class DiscrepancySearchParams:
    """Filter and ranking inputs for live plan discrepancy lookup."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    category: str | None = None
    severity: str | None = None
    status: str | None = None
    blocking_only: bool = False
    limit: int | None = None


class DiscrepancyQueryService:
    """Search the live plan discrepancy index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._plan_workspace = PlanWorkspaceService(loader)

    def search(
        self,
        params: DiscrepancySearchParams,
    ) -> tuple[PlanDiscrepancyIndexEntry, ...]:
        """Return discrepancy entries matching the requested filters."""

        return self._plan_workspace.search_discrepancies(
            PlanDiscrepancySearchParams(
                query=params.query,
                initiative_id=params.initiative_id,
                project_id=params.project_id,
                trace_id=params.trace_id,
                category=params.category,
                severity=params.severity,
                status=params.status,
                blocking_only=params.blocking_only,
                limit=params.limit,
            )
        )

