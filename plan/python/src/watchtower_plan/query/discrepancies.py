"""Repo-specific query helpers for live plan discrepancies."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.plan_workspace import (
    PlanDiscrepancyIndexEntry,
    PlanDiscrepancySearchParams,
    PlanWorkspaceService,
)
from watchtower_plan.query.common import DataclassSearchAdapter


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


class DiscrepancyQueryService(
    DataclassSearchAdapter[
        DiscrepancySearchParams,
        PlanDiscrepancySearchParams,
        PlanDiscrepancyIndexEntry,
    ]
):
    """Search the live plan discrepancy index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        plan_workspace = PlanWorkspaceService(loader)
        super().__init__(
            target_type=PlanDiscrepancySearchParams,
            search=plan_workspace.search_discrepancies,
        )
