"""Deterministic route-preview helpers backed by governed route and workflow data."""

from __future__ import annotations

import re
from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import RouteIndexEntry, WorkflowIndexEntry
from watchtower_core.repo_ops.query.common import normalize_text


@dataclass(frozen=True, slots=True)
class RoutePreviewMatch:
    """One matched route preview result."""

    route_id: str
    task_type: str
    score: int
    matched_keywords: tuple[str, ...]
    required_workflow_ids: tuple[str, ...]
    required_workflow_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RoutePreviewResult:
    """Route preview output."""

    selected_routes: tuple[RoutePreviewMatch, ...]
    selected_workflows: tuple[WorkflowIndexEntry, ...]
    warnings: tuple[str, ...] = ()


class RoutePreviewService:
    """Preview workflow-module routing for a request or explicit task type."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def preview(
        self,
        *,
        request_text: str | None = None,
        task_type: str | None = None,
    ) -> RoutePreviewResult:
        """Return the deterministic route preview for a request or one task type."""
        if bool(request_text) == bool(task_type):
            raise ValueError("route preview requires exactly one of request_text or task_type.")

        route_index = self._loader.load_route_index()
        workflow_index = self._loader.load_workflow_index()
        workflows_by_id = {entry.workflow_id: entry for entry in workflow_index.entries}

        if task_type is not None:
            normalized_task_type = normalize_text(task_type)
            matches = tuple(
                RoutePreviewMatch(
                    route_id=entry.route_id,
                    task_type=entry.task_type,
                    score=100,
                    matched_keywords=(),
                    required_workflow_ids=entry.required_workflow_ids,
                    required_workflow_paths=entry.required_workflow_paths,
                )
                for entry in route_index.entries
                if normalize_text(entry.task_type) == normalized_task_type
            )
            if not matches:
                known = ", ".join(entry.task_type for entry in route_index.entries)
                raise ValueError(
                    f"Unknown task type for route preview: {task_type}. Known task types: {known}"
                )
            return RoutePreviewResult(
                selected_routes=matches,
                selected_workflows=self._selected_workflows(matches, workflows_by_id),
            )

        selected_routes = self._score_routes(route_index.entries, request_text or "")
        warnings: list[str] = []
        if not selected_routes:
            warnings.append(
                "No route matched the request text exactly. Try --task-type for an explicit "
                "route or refine the request using routing-table terms."
            )
        elif len(selected_routes) > 1:
            warnings.append(
                "Multiple routes matched the request. The preview returned the merged workflow "
                "set for all positive matches."
            )
        return RoutePreviewResult(
            selected_routes=selected_routes,
            selected_workflows=self._selected_workflows(selected_routes, workflows_by_id),
            warnings=tuple(warnings),
        )

    def _score_routes(
        self,
        entries: tuple[RouteIndexEntry, ...],
        request_text: str,
    ) -> tuple[RoutePreviewMatch, ...]:
        normalized_request = normalize_text(request_text)
        request_tokens = set(re.findall(r"[a-z0-9]+", normalized_request))
        matches: list[RoutePreviewMatch] = []

        for entry in entries:
            matched_keywords = tuple(
                keyword
                for keyword in entry.trigger_keywords
                if normalize_text(keyword) in normalized_request
            )
            score = sum(10 + (3 * len(keyword.split())) for keyword in matched_keywords)
            task_type_match = normalize_text(entry.task_type) in normalized_request
            if task_type_match:
                score += 12
            if score == 0:
                continue

            task_tokens = set(re.findall(r"[a-z0-9]+", normalize_text(entry.task_type)))
            score += 2 * len(request_tokens.intersection(task_tokens))
            matches.append(
                RoutePreviewMatch(
                    route_id=entry.route_id,
                    task_type=entry.task_type,
                    score=score,
                    matched_keywords=matched_keywords,
                    required_workflow_ids=entry.required_workflow_ids,
                    required_workflow_paths=entry.required_workflow_paths,
                )
            )

        return tuple(sorted(matches, key=lambda item: (-item.score, item.task_type)))

    def _selected_workflows(
        self,
        matches: tuple[RoutePreviewMatch, ...],
        workflows_by_id: dict[str, WorkflowIndexEntry],
    ) -> tuple[WorkflowIndexEntry, ...]:
        selected_ids: list[str] = []
        for match in matches:
            for workflow_id in match.required_workflow_ids:
                if workflow_id not in selected_ids:
                    selected_ids.append(workflow_id)

        workflows: list[WorkflowIndexEntry] = []
        missing: list[str] = []
        for workflow_id in selected_ids:
            workflow = workflows_by_id.get(workflow_id)
            if workflow is None:
                missing.append(workflow_id)
                continue
            workflows.append(workflow)
        if missing:
            joined = ", ".join(missing)
            raise ValueError(f"Route preview referenced missing workflow-index entries: {joined}")
        return tuple(workflows)
