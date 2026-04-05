"""Public routing namespace for export-safe reusable route-selection surfaces."""

from __future__ import annotations

from watchtower_core.routing.engine import (
    AssistedWorkflowSuggestion,
    RoutePreviewMatch,
    RoutePreviewResult,
    RoutingEngine,
    RoutingSelection,
    ScoringConfig,
)
from watchtower_core.utils.module_exports import fail_closed_package_getattr

__all__ = [
    "AssistedWorkflowSuggestion",
    "RoutePreviewMatch",
    "RoutePreviewResult",
    "RoutingEngine",
    "RoutingSelection",
    "ScoringConfig",
]
__getattr__ = fail_closed_package_getattr(
    "watchtower_core.routing exports only reusable routing-engine surfaces."
)
