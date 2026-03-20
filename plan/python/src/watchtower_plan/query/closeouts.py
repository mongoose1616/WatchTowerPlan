"""Repo-specific query helpers for live plan closeout recaps."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query.common import DataclassSearchAdapter
from watchtower_plan.plan_workspace import (
    PlanCloseoutIndexEntry,
    PlanWorkspaceService,
)
from watchtower_plan.plan_workspace import (
    PlanCloseoutSearchParams as WorkspacePlanCloseoutSearchParams,
)


@dataclass(frozen=True, slots=True)
class PlanCloseoutSearchParams:
    """Filter and ranking inputs for live plan closeout lookup."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    status: str | None = None
    terminal_state: str | None = None
    promotion_review_required: bool | None = None
    limit: int | None = None


class PlanCloseoutQueryService(
    DataclassSearchAdapter[
        PlanCloseoutSearchParams,
        WorkspacePlanCloseoutSearchParams,
        PlanCloseoutIndexEntry,
    ]
):
    """Search the live plan closeout index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        plan_workspace = PlanWorkspaceService(loader)
        super().__init__(
            target_type=WorkspacePlanCloseoutSearchParams,
            search=plan_workspace.search_closeouts,
        )
