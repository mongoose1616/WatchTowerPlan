"""Repo-specific query helpers for live plan readiness state."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.plan_workspace import (
    PlanReadinessIndexEntry,
    PlanReadinessSearchParams,
    PlanWorkspaceService,
)


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


class ReadinessQueryService:
    """Search the live plan readiness index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._plan_workspace = PlanWorkspaceService(loader)

    def search(self, params: ReadinessSearchParams) -> tuple[PlanReadinessIndexEntry, ...]:
        """Return readiness entries matching the requested filters."""

        return self._plan_workspace.search_readiness(
            PlanReadinessSearchParams(
                query=params.query,
                initiative_id=params.initiative_id,
                project_id=params.project_id,
                trace_id=params.trace_id,
                lifecycle_stage=params.lifecycle_stage,
                review_status=params.review_status,
                ready_for_execution=params.ready_for_execution,
                blocked_only=params.blocked_only,
                limit=params.limit,
            )
        )

