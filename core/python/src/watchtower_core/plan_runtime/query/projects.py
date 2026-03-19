"""Repo-specific query helpers for live plan projects."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.plan_runtime.project_workspace import (
    PlanProjectIndexEntry,
    ProjectWorkspaceService,
)
from watchtower_core.plan_runtime.project_workspace import (
    PlanProjectSearchParams as WorkspacePlanProjectSearchParams,
)
from watchtower_core.plan_runtime.query.common import DataclassSearchAdapter


@dataclass(frozen=True, slots=True)
class ProjectSearchParams:
    """Filter and ranking inputs for live plan project lookup."""

    query: str | None = None
    project_id: str | None = None
    slug: str | None = None
    status: str | None = None
    repository_role: str | None = None
    limit: int | None = None


class ProjectQueryService(
    DataclassSearchAdapter[
        ProjectSearchParams,
        WorkspacePlanProjectSearchParams,
        PlanProjectIndexEntry,
    ]
):
    """Search the live plan project index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        project_workspace = ProjectWorkspaceService(loader)
        super().__init__(
            target_type=WorkspacePlanProjectSearchParams,
            search=project_workspace.search_projects,
        )
