"""Deterministic export-safe route-preview helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    RouteIndexEntry,
    RouteMergePolicyDefinition,
    RouteOverlayDefinition,
    WorkflowIndexEntry,
)
from watchtower_core.query.common import normalize_text
from watchtower_core.query.trusted_indexes import (
    load_trusted_route_index,
    load_trusted_workflow_index,
)

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
_TOKEN_ALIASES = {
    "artifacts": "artifact",
    "behaviors": "behavior",
    "commands": "command",
    "commits": "commit",
    "docs": "doc",
    "documentation": "doc",
    "examples": "example",
    "families": "family",
    "indices": "index",
    "indexes": "index",
    "links": "link",
    "paths": "path",
    "queries": "query",
    "references": "reference",
    "registries": "registry",
    "schemas": "schema",
    "surfaces": "surface",
    "tasks": "task",
    "trackers": "tracker",
    "validators": "validator",
    "workflows": "workflow",
}
_TASK_LIFECYCLE_GENERIC_KEYWORDS = {
    "create task",
    "create tasks",
    "create tracked tasks",
    "tasks",
}
_ASSISTED_FALLBACK_EXCLUDED_WORKFLOW_IDS = {
    "workflow.core",
    "workflow.current_state_inspection",
    "workflow.external_guidance_research",
    "workflow.internal_context_review",
    "workflow.task_handoff_review",
    "workflow.task_scope_definition",
}
_ASSISTED_FALLBACK_MIN_SCORE = 10
_ASSISTED_FALLBACK_LIMIT = 5


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
    assisted_module_suggestions: tuple[AssistedWorkflowSuggestion, ...] = ()


@dataclass(frozen=True, slots=True)
class AssistedWorkflowSuggestion:
    """Advisory workflow candidate for agent-assisted module loading."""

    workflow_id: str
    workflow_kind: str
    title: str
    doc_path: str
    phase_type: str
    task_family: str
    score: int
    matched_signals: tuple[str, ...]
    suggested_load_paths: tuple[str, ...]


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

        route_index = load_trusted_route_index(self._loader)
        workflow_index = load_trusted_workflow_index(self._loader)
        overlay_registry = self._loader.load_route_overlay_registry()
        merge_policy_registry = self._loader.load_route_merge_policy_registry()
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
                selected_workflows=self._selected_workflows(
                    matches,
                    workflows_by_id,
                    overlay_registry.entries,
                ),
                assisted_module_suggestions=(),
            )

        effective_request_text = request_text or ""
        scored_matches = self._scored_matches(route_index.entries, effective_request_text)
        selected_routes = _filter_selected_routes(scored_matches)
        selected_routes = _apply_route_overlays(
            selected_routes,
            scored_matches,
            route_index.entries,
            overlay_registry.entries,
            request_text=effective_request_text,
        )
        selected_routes = _apply_route_merge_policies(
            selected_routes,
            merge_policy_registry.entries,
            request_text=effective_request_text,
        )
        assisted_module_suggestions: tuple[AssistedWorkflowSuggestion, ...] = ()
        if not selected_routes:
            assisted_module_suggestions = _assisted_workflow_suggestions(
                request_text=effective_request_text,
                workflow_entries=workflow_index.entries,
            )

        warnings: list[str] = []
        if not selected_routes:
            warnings.append(
                "No route matched the request text exactly. Try --task-type for an explicit "
                "route or refine the request using routing-table terms."
            )
            if assisted_module_suggestions:
                warnings.append(
                    "Advisory workflow suggestions were included for agent-assisted module "
                    "loading. They do not override governed routing."
                )
        elif len(selected_routes) > 1:
            warnings.append(
                "Multiple routes matched the request. The preview returned the merged workflow "
                "set for all positive matches."
            )
        return RoutePreviewResult(
            selected_routes=selected_routes,
            selected_workflows=self._selected_workflows(
                selected_routes,
                workflows_by_id,
                overlay_registry.entries,
                request_text=effective_request_text,
            ),
            warnings=tuple(warnings),
            assisted_module_suggestions=assisted_module_suggestions,
        )

    def _scored_matches(
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

        filtered_matches = _apply_scoring_boundary_filters(matches, request_tokens=request_tokens)
        return _sorted_selected_matches(tuple(filtered_matches))

    def _selected_workflows(
        self,
        matches: tuple[RoutePreviewMatch, ...],
        workflows_by_id: dict[str, WorkflowIndexEntry],
        overlay_entries: tuple[RouteOverlayDefinition, ...],
        request_text: str = "",
    ) -> tuple[WorkflowIndexEntry, ...]:
        selected_ids: list[str] = []
        for match in matches:
            for workflow_id in match.required_workflow_ids:
                if workflow_id not in selected_ids:
                    selected_ids.append(workflow_id)

        for workflow_id in _overlay_workflow_ids(
            request_text=request_text,
            selected_routes=matches,
            overlay_entries=overlay_entries,
        ):
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
    if _phrase_in_request(normalized_task_type, normalized_request):
        return 12

    task_tokens = _normalized_tokens(normalized_task_type)
    matched_count = _matched_token_count(request_tokens, task_tokens)
    if task_tokens and matched_count == len(task_tokens) and len(task_tokens) >= 2:
        return 8 + len(task_tokens)
    return 0


def _keyword_match_score(
    keyword: str,
    normalized_request: str,
    request_tokens: tuple[str, ...],
) -> int:
    normalized_keyword = normalize_text(keyword)
    if _phrase_in_request(normalized_keyword, normalized_request):
        return 18 + (3 * len(normalized_keyword.split()))

    keyword_tokens = _normalized_tokens(normalized_keyword)
    if not keyword_tokens:
        return 0

    matched_count = _matched_token_count(request_tokens, keyword_tokens)
    if len(keyword_tokens) == 1 and matched_count == 1:
        return 8
    if matched_count == len(keyword_tokens) and len(keyword_tokens) >= 2:
        return 10 + (2 * len(keyword_tokens))
    if len(keyword_tokens) >= 4 and matched_count >= len(keyword_tokens) - 1:
        return 6 + (2 * matched_count)
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
    return request_token == candidate_token


def _filter_selected_routes(
    matches: tuple[RoutePreviewMatch, ...],
) -> tuple[RoutePreviewMatch, ...]:
    if len(matches) <= 1:
        return matches

    top_match = matches[0]
    minimum_secondary_score = max(12, _ceil_fraction(top_match.score, 1, 2))
    filtered = [top_match]
    filtered.extend(match for match in matches[1:] if match.score >= minimum_secondary_score)
    return tuple(filtered)


def _apply_scoring_boundary_filters(
    matches: list[RoutePreviewMatch],
    *,
    request_tokens: tuple[str, ...],
) -> list[RoutePreviewMatch]:
    if "successor" not in request_tokens:
        return matches
    return [
        match
        for match in matches
        if not (
            match.task_type == "Task Lifecycle Management"
            and set(match.matched_keywords).issubset(_TASK_LIFECYCLE_GENERIC_KEYWORDS)
        )
    ]


def _apply_route_overlays(
    matches: tuple[RoutePreviewMatch, ...],
    all_matches: tuple[RoutePreviewMatch, ...],
    route_entries: tuple[RouteIndexEntry, ...],
    overlay_entries: tuple[RouteOverlayDefinition, ...],
    *,
    request_text: str,
) -> tuple[RoutePreviewMatch, ...]:
    if not matches or not request_text:
        return matches

    selected_by_task_type = {match.task_type: match for match in matches}
    candidates_by_task_type = {match.task_type: match for match in all_matches}
    route_entries_by_task_type = {entry.task_type: entry for entry in route_entries}

    for overlay in overlay_entries:
        if overlay.entry_status != "active":
            continue
        if not _route_overlay_requested(request_text, overlay):
            continue
        if not overlay.attached_route_task_types and not overlay.retain_dominant_compatible_route:
            continue

        for task_type in overlay.attached_route_task_types:
            candidate = candidates_by_task_type.get(task_type)
            if candidate is None:
                candidate = _synthetic_overlay_route_match(
                    task_type,
                    route_entries_by_task_type.get(task_type),
                    overlay,
                    request_text=request_text,
                )
            if candidate is not None:
                selected_by_task_type.setdefault(task_type, candidate)
                candidates_by_task_type.setdefault(task_type, candidate)

        if (
            overlay.retain_dominant_compatible_route
            and not _selected_routes_include_supported_non_overlay_route(
                selected_by_task_type,
                overlay,
            )
        ):
            strongest_compatible = next(
                (
                    candidate
                    for candidate in all_matches
                    if candidate.task_type not in selected_by_task_type
                    and candidate.task_type not in overlay.attached_route_task_types
                    and candidate.score >= overlay.minimum_route_score
                    and _overlay_supports_task_type(overlay, candidate.task_type)
                ),
                None,
            )
            if strongest_compatible is not None:
                selected_by_task_type[strongest_compatible.task_type] = strongest_compatible

    return _sorted_selected_matches(tuple(selected_by_task_type.values()))


def _selected_routes_include_supported_non_overlay_route(
    selected_by_task_type: dict[str, RoutePreviewMatch],
    overlay: RouteOverlayDefinition,
) -> bool:
    if not selected_by_task_type:
        return False
    overlay_route_types = set(overlay.attached_route_task_types)
    return any(
        task_type not in overlay_route_types and _overlay_supports_task_type(overlay, task_type)
        for task_type in selected_by_task_type
    )


def _synthetic_overlay_route_match(
    task_type: str,
    route_entry: RouteIndexEntry | None,
    overlay: RouteOverlayDefinition,
    *,
    request_text: str,
) -> RoutePreviewMatch | None:
    if route_entry is None:
        return None
    matched_keywords = tuple(
        term for term in overlay.trigger_terms if _phrase_in_request(term, request_text)
    )
    score = max(overlay.minimum_route_score, 12 + (3 * len(matched_keywords)))
    return RoutePreviewMatch(
        route_id=route_entry.route_id,
        task_type=route_entry.task_type,
        score=score,
        matched_keywords=matched_keywords,
        required_workflow_ids=route_entry.required_workflow_ids,
        required_workflow_paths=route_entry.required_workflow_paths,
    )


def _apply_route_merge_policies(
    matches: tuple[RoutePreviewMatch, ...],
    policy_entries: tuple[RouteMergePolicyDefinition, ...],
    *,
    request_text: str,
) -> tuple[RoutePreviewMatch, ...]:
    filtered: tuple[RoutePreviewMatch, ...] = matches
    for policy in sorted(
        (entry for entry in policy_entries if entry.entry_status == "active"),
        key=lambda entry: (entry.priority, entry.rule_id),
    ):
        if not _route_merge_policy_applies(policy, filtered, request_text):
            continue
        filtered = tuple(
            match for match in filtered if match.task_type not in policy.suppress_task_types
        )
    return _sorted_selected_matches(filtered)


def _route_merge_policy_applies(
    policy: RouteMergePolicyDefinition,
    matches: tuple[RoutePreviewMatch, ...],
    request_text: str,
) -> bool:
    task_types = {match.task_type for match in matches}
    if policy.when_all_task_types_present and not set(policy.when_all_task_types_present).issubset(
        task_types
    ):
        return False
    if policy.when_any_task_types_present and not task_types.intersection(
        policy.when_any_task_types_present
    ):
        return False
    if policy.when_request_terms_present_any and not _request_matches_any(
        request_text,
        policy.when_request_terms_present_any,
    ):
        return False
    if policy.unless_request_terms_present_any and _request_matches_any(
        request_text,
        policy.unless_request_terms_present_any,
    ):
        return False
    return True


def _overlay_workflow_ids(
    *,
    request_text: str,
    selected_routes: tuple[RoutePreviewMatch, ...],
    overlay_entries: tuple[RouteOverlayDefinition, ...],
) -> tuple[str, ...]:
    if not request_text or not selected_routes:
        return ()

    overlay_ids: list[str] = []
    for overlay in overlay_entries:
        if overlay.entry_status != "active":
            continue
        if not overlay.attached_workflow_ids:
            continue
        if not _route_overlay_requested(request_text, overlay):
            continue
        if not any(
            _overlay_supports_task_type(overlay, route.task_type)
            for route in selected_routes
        ):
            continue
        for workflow_id in overlay.attached_workflow_ids:
            if workflow_id not in overlay_ids:
                overlay_ids.append(workflow_id)
    return tuple(overlay_ids)


def _route_overlay_requested(
    request_text: str,
    overlay: RouteOverlayDefinition,
) -> bool:
    request_terms = _normalized_phrase_text(request_text).split()
    if not request_terms:
        return False

    if overlay.trigger_mode == "anywhere":
        return any(_phrase_in_request(term, request_text) for term in overlay.trigger_terms)

    anchor_tokens = _normalized_tokens(" ".join(overlay.anchor_terms))
    anchor_positions = [
        index
        for index, term in enumerate(request_terms)
        if any(_tokens_match(term, anchor) for anchor in anchor_tokens)
    ]
    if not anchor_positions:
        return False

    for trigger_term in overlay.trigger_terms:
        trigger_terms = _normalized_phrase_text(trigger_term).split()
        if not trigger_terms:
            continue
        trigger_position = _phrase_term_index(request_terms, trigger_terms)
        if trigger_position is None:
            continue
        if any(trigger_position < anchor_position for anchor_position in anchor_positions):
            return True
    return False


def _overlay_supports_task_type(overlay: RouteOverlayDefinition, task_type: str) -> bool:
    if task_type in overlay.excluded_task_types:
        return False
    if overlay.compatible_task_types and task_type not in overlay.compatible_task_types:
        return False
    return True


def _request_matches_any(request_text: str, terms: tuple[str, ...]) -> bool:
    return any(_phrase_in_request(term, request_text) for term in terms)


def _phrase_term_index(
    request_terms: list[str],
    phrase_terms: list[str],
) -> int | None:
    if not phrase_terms or len(phrase_terms) > len(request_terms):
        return None

    limit = len(request_terms) - len(phrase_terms) + 1
    for index in range(limit):
        if request_terms[index : index + len(phrase_terms)] == phrase_terms:
            return index
    return None


def _phrase_in_request(phrase: str, request_text: str) -> bool:
    normalized_phrase = _normalized_phrase_text(phrase)
    normalized_request = _normalized_phrase_text(request_text)
    if not normalized_phrase or not normalized_request:
        return False
    return f" {normalized_phrase} " in f" {normalized_request} "


def _normalized_phrase_text(value: str) -> str:
    return " ".join(_TOKEN_PATTERN.findall(normalize_text(value)))


def _normalized_tokens(value: str) -> tuple[str, ...]:
    return tuple(
        canonical
        for token in _TOKEN_PATTERN.findall(normalize_text(value))
        if (canonical := _canonical_token(token)) not in _IGNORED_TOKENS
    )


def _canonical_token(token: str) -> str:
    return _TOKEN_ALIASES.get(token, token)


def _ceil_fraction(value: int, numerator: int, denominator: int) -> int:
    return (value * numerator + denominator - 1) // denominator


def _sorted_selected_matches(
    matches: tuple[RoutePreviewMatch, ...],
) -> tuple[RoutePreviewMatch, ...]:
    return tuple(sorted(matches, key=lambda item: (-item.score, item.task_type)))


def _assisted_workflow_suggestions(
    *,
    request_text: str,
    workflow_entries: tuple[WorkflowIndexEntry, ...],
) -> tuple[AssistedWorkflowSuggestion, ...]:
    normalized_request = normalize_text(request_text)
    request_tokens = _normalized_tokens(normalized_request)
    if not request_tokens:
        return ()

    suggestions: list[AssistedWorkflowSuggestion] = []
    for workflow in workflow_entries:
        if workflow.workflow_id in _ASSISTED_FALLBACK_EXCLUDED_WORKFLOW_IDS:
            continue

        score, matched_signals = _assisted_workflow_score(
            workflow,
            normalized_request=normalized_request,
            request_tokens=request_tokens,
        )
        if score < _ASSISTED_FALLBACK_MIN_SCORE:
            continue
        suggestions.append(
            AssistedWorkflowSuggestion(
                workflow_id=workflow.workflow_id,
                workflow_kind=workflow.workflow_kind,
                title=workflow.title,
                doc_path=workflow.doc_path,
                phase_type=workflow.phase_type,
                task_family=workflow.task_family,
                score=score,
                matched_signals=matched_signals,
                suggested_load_paths=_suggested_load_paths(workflow),
            )
        )

    return tuple(
        sorted(
            suggestions,
            key=lambda item: (-item.score, item.workflow_kind, item.workflow_id),
        )[:_ASSISTED_FALLBACK_LIMIT]
    )


def _assisted_workflow_score(
    workflow: WorkflowIndexEntry,
    *,
    normalized_request: str,
    request_tokens: tuple[str, ...],
) -> tuple[int, tuple[str, ...]]:
    score = 0
    matched_signals: list[str] = []
    seen_signals: set[str] = set()

    for label, bonus in _assisted_workflow_labels(workflow):
        label_score = _assisted_label_score(
            label,
            normalized_request=normalized_request,
            request_tokens=request_tokens,
        )
        if label_score == 0:
            continue
        score += label_score + bonus
        normalized_label = _normalized_phrase_text(label)
        if normalized_label and normalized_label not in seen_signals:
            seen_signals.add(normalized_label)
            matched_signals.append(normalized_label)

    return score, tuple(matched_signals)


def _assisted_workflow_labels(
    workflow: WorkflowIndexEntry,
) -> tuple[tuple[str, int], ...]:
    doc_stem = PurePosixPath(workflow.doc_path).stem.replace("_", " ")
    task_family = workflow.task_family.replace("_", " ")
    title = _trim_workflow_title_suffix(workflow.title)
    candidates = (
        (title, 4),
        (doc_stem, 3),
        (task_family, 2),
        (workflow.phase_type, 1),
    )

    labels: list[tuple[str, int]] = []
    seen_labels: set[str] = set()
    for label, bonus in candidates:
        normalized_label = _normalized_phrase_text(label)
        if not normalized_label or normalized_label in seen_labels:
            continue
        seen_labels.add(normalized_label)
        labels.append((label, bonus))
    return tuple(labels)


def _trim_workflow_title_suffix(title: str) -> str:
    normalized_title = normalize_text(title).strip()
    for suffix in (" workflow", " role"):
        if normalized_title.endswith(suffix):
            return normalized_title[: -len(suffix)].strip()
    return normalized_title


def _assisted_label_score(
    label: str,
    *,
    normalized_request: str,
    request_tokens: tuple[str, ...],
) -> int:
    phrase_score = _keyword_match_score(label, normalized_request, request_tokens)
    if phrase_score:
        return phrase_score

    label_tokens = _normalized_tokens(label)
    if not label_tokens:
        return 0

    overlap = _matched_token_count(request_tokens, label_tokens)
    if overlap == 0:
        return 0

    score = 4 * overlap
    if overlap == len(label_tokens) and len(label_tokens) >= 2:
        score += 6
    elif len(label_tokens) >= 3 and overlap >= len(label_tokens) - 1:
        score += 3
    return score


def _suggested_load_paths(workflow: WorkflowIndexEntry) -> tuple[str, ...]:
    load_paths = [workflow.doc_path, *workflow.composes_module_paths]
    return tuple(dict.fromkeys(load_paths))


__all__ = [
    "AssistedWorkflowSuggestion",
    "RoutePreviewMatch",
    "RoutePreviewResult",
    "RoutePreviewService",
]
