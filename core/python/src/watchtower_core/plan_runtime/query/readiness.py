"""Repo-specific query helpers for live plan readiness state."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.plan_runtime.plan_workspace import (
    PlanReadinessIndexEntry,
    PlanReadinessSearchParams,
    PlanWorkspaceService,
)
from watchtower_core.plan_runtime.query.common import DataclassSearchAdapter


@dataclass(frozen=True, slots=True)
class ReadinessSearchParams:
    """Filter and ranking inputs for live plan readiness lookup."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    lifecycle_stage: str | None = None
    review_status: str | None = None
    ready_for_execution: bool | None = None
    blocked_only: bool = False
    limit: int | None = None


class ReadinessQueryService(
    DataclassSearchAdapter[
        ReadinessSearchParams,
        PlanReadinessSearchParams,
        PlanReadinessIndexEntry,
    ]
):
    """Search the live plan readiness index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        plan_workspace = PlanWorkspaceService(loader)
        super().__init__(
            target_type=PlanReadinessSearchParams,
            search=plan_workspace.search_readiness,
        )
