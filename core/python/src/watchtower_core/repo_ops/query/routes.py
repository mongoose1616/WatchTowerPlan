"""Deterministic route-preview helpers backed by governed route and workflow data."""

from __future__ import annotations

import re
from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import RouteIndexEntry, WorkflowIndexEntry
from watchtower_core.repo_ops.query.common import normalize_text

_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
_IGNORED_TOKENS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "when",
    "with",
}


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
        request_tokens = _normalized_tokens(normalized_request)
        matches: list[RoutePreviewMatch] = []

        for entry in entries:
            matched_keyword_values: list[str] = []
            score = 0

            for keyword in entry.trigger_keywords:
                keyword_score = _keyword_match_score(keyword, normalized_request, request_tokens)
                if keyword_score == 0:
                    continue
                score += keyword_score
                matched_keyword_values.append(keyword)

            score += _task_type_match_score(entry.task_type, normalized_request, request_tokens)
            if score == 0:
                continue

            matches.append(
                RoutePreviewMatch(
                    route_id=entry.route_id,
                    task_type=entry.task_type,
                    score=score,
                    matched_keywords=tuple(matched_keyword_values),
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


def _task_type_match_score(
    task_type: str,
    normalized_request: str,
    request_tokens: tuple[str, ...],
) -> int:
    normalized_task_type = normalize_text(task_type)
    if normalized_task_type in normalized_request:
        return 12

    task_tokens = _normalized_tokens(normalized_task_type)
    matched_count = _matched_token_count(request_tokens, task_tokens)
    if task_tokens and matched_count == len(task_tokens) and len(task_tokens) >= 2:
        return 8 + len(task_tokens)
    if matched_count >= 2:
        return 4 + matched_count
    return 0


def _keyword_match_score(
    keyword: str,
    normalized_request: str,
    request_tokens: tuple[str, ...],
) -> int:
    normalized_keyword = normalize_text(keyword)
    if normalized_keyword in normalized_request:
        return 18 + (3 * len(normalized_keyword.split()))

    keyword_tokens = _normalized_tokens(normalized_keyword)
    if not keyword_tokens:
        return 0

    matched_count = _matched_token_count(request_tokens, keyword_tokens)
    if len(keyword_tokens) == 1 and matched_count == 1:
        return 8
    if matched_count == len(keyword_tokens) and len(keyword_tokens) >= 2:
        return 10 + (2 * len(keyword_tokens))
    return 0


def _matched_token_count(
    request_tokens: tuple[str, ...],
    candidate_tokens: tuple[str, ...],
) -> int:
    return sum(
        1
        for candidate in candidate_tokens
        if any(_tokens_match(request, candidate) for request in request_tokens)
    )


def _tokens_match(request_token: str, candidate_token: str) -> bool:
    if request_token == candidate_token:
        return True
    if min(len(request_token), len(candidate_token)) >= 4 and (
        request_token.startswith(candidate_token) or candidate_token.startswith(request_token)
    ):
        return True
    common_prefix = len(_common_prefix(request_token, candidate_token))
    return common_prefix >= 4


def _common_prefix(left: str, right: str) -> str:
    prefix: list[str] = []
    for left_char, right_char in zip(left, right, strict=False):
        if left_char != right_char:
            break
        prefix.append(left_char)
    return "".join(prefix)


def _normalized_tokens(value: str) -> tuple[str, ...]:
    return tuple(
        token
        for token in _TOKEN_PATTERN.findall(normalize_text(value))
        if token not in _IGNORED_TOKENS
    )
