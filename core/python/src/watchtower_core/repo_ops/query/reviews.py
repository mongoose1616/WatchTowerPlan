"""Repo-specific query helpers for live plan review state."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.plan_workspace import (
    PlanReviewIndexEntry,
    PlanWorkspaceService,
)
from watchtower_core.repo_ops.plan_workspace import (
    PlanReviewSearchParams as WorkspacePlanReviewSearchParams,
)
from watchtower_core.repo_ops.query.common import DataclassSearchAdapter


@dataclass(frozen=True, slots=True)
class PlanReviewSearchParams:
    """Filter and ranking inputs for live plan review lookup."""

    query: str | None = None
    subject_kind: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    review_state: str | None = None
    ready_for_execution: bool | None = None
    review_ref: str | None = None
    limit: int | None = None


class PlanReviewQueryService(
    DataclassSearchAdapter[
        PlanReviewSearchParams,
        WorkspacePlanReviewSearchParams,
        PlanReviewIndexEntry,
    ]
):
    """Search the live plan review index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        plan_workspace = PlanWorkspaceService(loader)
        super().__init__(
            target_type=WorkspacePlanReviewSearchParams,
            search=plan_workspace.search_reviews,
        )
