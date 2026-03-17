"""Repo-specific query helpers for live plan projects."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.project_workspace import (
    PlanProjectIndexEntry,
    PlanProjectSearchParams,
    ProjectWorkspaceService,
)


@dataclass(frozen=True, slots=True)
class ProjectSearchParams:
    """Filter and ranking inputs for live plan project lookup."""

    query: str | None = None
    project_id: str | None = None
    slug: str | None = None
    status: str | None = None
    repository_role: str | None = None
    limit: int | None = None


class ProjectQueryService:
    """Search the live plan project index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._project_workspace = ProjectWorkspaceService(loader)

    def search(self, params: ProjectSearchParams) -> tuple[PlanProjectIndexEntry, ...]:
        """Return project entries matching the requested filters."""

        return self._project_workspace.search_projects(
            PlanProjectSearchParams(
                query=params.query,
                project_id=params.project_id,
                slug=params.slug,
                status=params.status,
                repository_role=params.repository_role,
                limit=params.limit,
            )
        )

