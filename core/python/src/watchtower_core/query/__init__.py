"""Public query namespace for export-safe generic query surfaces."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

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

_PLAN_DOMAIN_EXPORTS = {
    "AcceptanceContractQueryService",
    "ArtifactQueryService",
    "CoordinationQueryService",
    "DiscrepancyQueryService",
    "ValidationEvidenceQueryService",
    "FoundationQueryService",
    "InitiativeQueryService",
    "ProjectQueryService",
    "ReadinessQueryService",
    "ReferenceQueryService",
    "RepositoryPathQueryService",
    "StandardQueryService",
    "TaskQueryService",
    "TraceabilityQueryService",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
    blocked_messages=dict.fromkeys(
        _PLAN_DOMAIN_EXPORTS,
        "watchtower_core.query exposes only reusable generic query services. "
        "Import live planning or repo-local query services from "
        "watchtower_plan.query.",
    ),
)
