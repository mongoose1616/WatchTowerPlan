"""Public query namespace for export-safe generic query surfaces."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "ArtifactFamilyPathResolution",
    "ArtifactFamilyQueryService",
    "ArtifactFamilySearchParams",
    "AuthorityMapQueryService",
    "AuthorityMapSearchParams",
    "CommandQueryService",
    "CommandSearchParams",
    "GovernanceSurfaceQueryService",
    "GovernanceSurfaceSearchParams",
    "RoutePreviewMatch",
    "RoutePreviewResult",
    "RoutePreviewService",
    "WorkflowQueryService",
    "WorkflowSearchParams",
]

_EXPORT_MODULES = {
    "ArtifactFamilyPathResolution": "watchtower_core.query.artifact_families",
    "ArtifactFamilyQueryService": "watchtower_core.query.artifact_families",
    "ArtifactFamilySearchParams": "watchtower_core.query.artifact_families",
    "AuthorityMapQueryService": "watchtower_core.query.authority",
    "AuthorityMapSearchParams": "watchtower_core.query.authority",
    "CommandQueryService": "watchtower_core.query.commands",
    "CommandSearchParams": "watchtower_core.query.commands",
    "GovernanceSurfaceQueryService": "watchtower_core.query.governance_surfaces",
    "GovernanceSurfaceSearchParams": "watchtower_core.query.governance_surfaces",
    "RoutePreviewMatch": "watchtower_core.query.routes",
    "RoutePreviewResult": "watchtower_core.query.routes",
    "RoutePreviewService": "watchtower_core.query.routes",
    "WorkflowQueryService": "watchtower_core.query.workflows",
    "WorkflowSearchParams": "watchtower_core.query.workflows",
}

_REPO_OPS_EXPORTS = {
    "AcceptanceContractQueryService",
    "ArtifactQueryService",
    "CoordinationQueryService",
    "DecisionQueryService",
    "DesignDocumentQueryService",
    "DiscrepancyQueryService",
    "ValidationEvidenceQueryService",
    "FoundationQueryService",
    "InitiativeQueryService",
    "PlanningCatalogQueryService",
    "PrdQueryService",
    "ProjectQueryService",
    "ReadinessQueryService",
    "ReferenceQueryService",
    "RepositoryPathQueryService",
    "StandardQueryService",
    "TaskQueryService",
    "TraceabilityQueryService",
}

def __getattr__(name: str) -> Any:
    if name in _REPO_OPS_EXPORTS:
        raise AttributeError(
            "watchtower_core.query exposes only reusable generic query services. "
            "Import live planning or repo-local query services from "
            "watchtower_core.repo_ops.query."
        )
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(import_module(module_name), name)
