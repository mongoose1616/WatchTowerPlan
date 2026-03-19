"""Reusable routing-engine surface over governed route selection."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query.routes import RoutePreviewMatch, RoutePreviewResult, RoutePreviewService

RoutingSelection = RoutePreviewResult


class RoutingEngine:
    """Select governed routes through a stable reusable runtime API."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._service = RoutePreviewService(loader)

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> RoutingEngine:
        """Build one routing engine from a repository root."""

        return cls(ControlPlaneLoader(repo_root))

    def select(
        self,
        *,
        request_text: str | None = None,
        task_type: str | None = None,
    ) -> RoutePreviewResult:
        """Select the governed routes for request text or one explicit task type."""

        return self._service.preview(request_text=request_text, task_type=task_type)

    def select_for_request(self, request_text: str) -> RoutePreviewResult:
        """Select governed routes for one request string."""

        return self.select(request_text=request_text)

    def select_for_task_type(self, task_type: str) -> RoutePreviewResult:
        """Select the governed route set for one explicit task type."""

        return self.select(task_type=task_type)


__all__ = [
    "RoutePreviewMatch",
    "RoutePreviewResult",
    "RoutingEngine",
    "RoutingSelection",
]
