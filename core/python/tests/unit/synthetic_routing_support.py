"""Synthetic fixture builders for pure unit tests of the routing algorithm.

Provides factory functions that construct minimal in-memory control-plane
data so tests can exercise scoring, overlay attachment, and merge-policy
suppression without loading JSON from disk.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from watchtower_core.control_plane.loader import (
    ROUTE_INDEX_PATH,
    WORKFLOW_INDEX_PATH,
)
from watchtower_core.control_plane.models import (
    RouteIndex,
    RouteIndexEntry,
    WorkflowIndex,
    WorkflowIndexEntry,
)
from watchtower_core.control_plane.models.catalog_routing import (
    RouteMergePolicyDefinition,
    RouteMergePolicyRegistry,
    RouteOverlayDefinition,
    RouteOverlayRegistry,
)
from watchtower_core.query.routes import (
    RoutePreviewResult,
    RoutePreviewService,
    ScoringConfig,
)

_COUNTER = 0


def _next_id() -> int:
    global _COUNTER
    _COUNTER += 1
    return _COUNTER


# ---------------------------------------------------------------------------
# Minimal model builders
# ---------------------------------------------------------------------------


def make_route(
    task_type: str,
    *,
    keywords: tuple[str, ...] = (),
    route_id: str | None = None,
    workflow_ids: tuple[str, ...] | None = None,
    route_families: tuple[str, ...] = (),
) -> RouteIndexEntry:
    """Build a minimal route-index entry."""
    slug = task_type.lower().replace(" ", "_").replace("-", "_")
    return RouteIndexEntry(
        route_id=route_id or f"route.{slug}",
        task_type=task_type,
        trigger_keywords=keywords,
        required_workflow_ids=workflow_ids or (f"workflow.{slug}",),
        required_workflow_paths=(f"core/workflows/modules/{slug}.md",),
        route_families=route_families,
    )


def make_workflow(
    workflow_id: str,
    *,
    title: str | None = None,
    kind: str = "module",
) -> WorkflowIndexEntry:
    """Build a minimal workflow-index entry."""
    return WorkflowIndexEntry(
        workflow_id=workflow_id,
        workflow_kind=kind,
        title=title or workflow_id.replace("workflow.", "").replace("_", " ").title(),
        summary="synthetic",
        status="active",
        doc_path=f"core/workflows/modules/{workflow_id.replace('workflow.', '')}.md",
        uses_internal_references=False,
        uses_external_references=False,
    )


def make_overlay(
    overlay_id: str,
    *,
    trigger_terms: tuple[str, ...] = (),
    trigger_mode: str = "anywhere",
    anchor_terms: tuple[str, ...] = (),
    intent_kind: str = "workflow_modifier",
    compatible_task_types: tuple[str, ...] = (),
    compatible_route_families: tuple[str, ...] = (),
    excluded_task_types: tuple[str, ...] = (),
    attached_workflow_ids: tuple[str, ...] = (),
    attached_route_task_types: tuple[str, ...] = (),
    dominant_route_retention_mode: str = "none",
    exclude_attached_from_scoring: bool = False,
    suppresses_intent_ids: tuple[str, ...] = (),
    minimum_route_score: int = 0,
) -> RouteOverlayDefinition:
    """Build a minimal route-overlay definition."""
    return RouteOverlayDefinition(
        overlay_id=overlay_id,
        entry_status="active",
        title=overlay_id,
        intent_kind=intent_kind,
        trigger_terms=trigger_terms,
        trigger_mode=trigger_mode,
        anchor_terms=anchor_terms,
        compatible_task_types=compatible_task_types,
        compatible_route_families=compatible_route_families,
        excluded_task_types=excluded_task_types,
        attached_workflow_ids=attached_workflow_ids,
        attached_route_task_types=attached_route_task_types,
        dominant_route_retention_mode=dominant_route_retention_mode,
        exclude_attached_task_types_from_base_scoring=exclude_attached_from_scoring,
        suppresses_intent_ids=suppresses_intent_ids,
        minimum_route_score=minimum_route_score,
    )


def make_merge_policy(
    rule_id: str,
    *,
    priority: int = 10,
    suppress_task_types: tuple[str, ...] = (),
    when_all: tuple[str, ...] = (),
    when_any: tuple[str, ...] = (),
    when_terms: tuple[str, ...] = (),
    unless_terms: tuple[str, ...] = (),
) -> RouteMergePolicyDefinition:
    """Build a minimal merge-policy definition."""
    return RouteMergePolicyDefinition(
        rule_id=rule_id,
        entry_status="active",
        title=rule_id,
        priority=priority,
        suppress_task_types=suppress_task_types,
        when_all_task_types_present=when_all,
        when_any_task_types_present=when_any,
        when_request_terms_present_any=when_terms,
        unless_request_terms_present_any=unless_terms,
    )


# ---------------------------------------------------------------------------
# Synthetic control-plane assembly
# ---------------------------------------------------------------------------


def make_stub_loader(
    *,
    routes: tuple[RouteIndexEntry, ...] = (),
    workflows: tuple[WorkflowIndexEntry, ...] = (),
    overlays: tuple[RouteOverlayDefinition, ...] = (),
    merge_policies: tuple[RouteMergePolicyDefinition, ...] = (),
) -> MagicMock:
    """Build a stub ControlPlaneLoader that returns synthetic data.

    The stub satisfies the interface that RoutePreviewService.preview()
    needs: load_json_object (for trusted index loading), plus the typed
    overlay/merge-policy loaders.
    """
    route_index = RouteIndex(
        schema_id="urn:test:route-index:v1",
        artifact_id="index.routes",
        title="Test Route Index",
        status="active",
        entries=routes,
    )
    workflow_index = WorkflowIndex(
        schema_id="urn:test:workflow-index:v1",
        artifact_id="index.workflows",
        title="Test Workflow Index",
        status="active",
        entries=workflows,
    )
    overlay_registry = RouteOverlayRegistry(
        schema_id="urn:test:overlay-registry:v1",
        artifact_id="registry.route_overlays",
        title="Test Overlay Registry",
        status="active",
        entries=overlays,
    )
    merge_policy_registry = RouteMergePolicyRegistry(
        schema_id="urn:test:merge-policy-registry:v1",
        artifact_id="registry.route_merge_policies",
        title="Test Merge Policy Registry",
        status="active",
        entries=merge_policies,
    )

    # The trusted-index loader uses load_json_object, but we bypass it
    # by pre-populating the typed document cache directly.
    loader = MagicMock()
    loader._typed_document_cache = {
        f"__trusted_query_index__::{ROUTE_INDEX_PATH}": route_index,
        f"__trusted_query_index__::{WORKFLOW_INDEX_PATH}": workflow_index,
    }
    loader.load_route_overlay_registry.return_value = overlay_registry
    loader.load_route_merge_policy_registry.return_value = merge_policy_registry
    return loader


def synthetic_preview(
    request_text: str,
    *,
    routes: tuple[RouteIndexEntry, ...] = (),
    workflows: tuple[WorkflowIndexEntry, ...] = (),
    overlays: tuple[RouteOverlayDefinition, ...] = (),
    merge_policies: tuple[RouteMergePolicyDefinition, ...] = (),
    scoring_config: ScoringConfig | None = None,
) -> RoutePreviewResult:
    """Run route preview against synthetic in-memory data."""
    loader = make_stub_loader(
        routes=routes,
        workflows=workflows,
        overlays=overlays,
        merge_policies=merge_policies,
    )
    service = RoutePreviewService(loader, scoring_config=scoring_config)
    return service.preview(request_text=request_text)
