"""Public query namespace for export-safe generic query surfaces."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "AcceptanceContractQueryService",
    "AcceptanceContractSearchParams",
    "ArtifactFamilyPathResolution",
    "ArtifactFamilyQueryService",
    "ArtifactFamilySearchParams",
    "AuthorityMapQueryService",
    "AuthorityMapSearchParams",
    "CommandQueryService",
    "CommandSearchParams",
    "FoundationQueryService",
    "FoundationSearchParams",
    "GovernanceSurfaceQueryService",
    "GovernanceSurfaceSearchParams",
    "ReferenceQueryService",
    "ReferenceSearchParams",
    "RepositoryPathQueryService",
    "RepositoryPathSearchParams",
    "RoutePreviewMatch",
    "RoutePreviewResult",
    "RoutePreviewService",
    "StandardQueryService",
    "StandardSearchParams",
    "TraceabilityQueryService",
    "ValidationEvidenceQueryService",
    "ValidationEvidenceSearchParams",
    "WorkflowQueryService",
    "WorkflowSearchParams",
]

_EXPORT_MODULES = {
    "AcceptanceContractQueryService": "watchtower_core.query.acceptance",
    "AcceptanceContractSearchParams": "watchtower_core.query.acceptance",
    "ArtifactFamilyPathResolution": "watchtower_core.query.artifact_families",
    "ArtifactFamilyQueryService": "watchtower_core.query.artifact_families",
    "ArtifactFamilySearchParams": "watchtower_core.query.artifact_families",
    "AuthorityMapQueryService": "watchtower_core.query.authority",
    "AuthorityMapSearchParams": "watchtower_core.query.authority",
    "CommandQueryService": "watchtower_core.query.commands",
    "CommandSearchParams": "watchtower_core.query.commands",
    "FoundationQueryService": "watchtower_core.query.foundations",
    "FoundationSearchParams": "watchtower_core.query.foundations",
    "GovernanceSurfaceQueryService": "watchtower_core.query.governance_surfaces",
    "GovernanceSurfaceSearchParams": "watchtower_core.query.governance_surfaces",
    "ReferenceQueryService": "watchtower_core.query.references",
    "ReferenceSearchParams": "watchtower_core.query.references",
    "RepositoryPathQueryService": "watchtower_core.query.repository",
    "RepositoryPathSearchParams": "watchtower_core.query.repository",
    "RoutePreviewMatch": "watchtower_core.query.routes",
    "RoutePreviewResult": "watchtower_core.query.routes",
    "RoutePreviewService": "watchtower_core.query.routes",
    "StandardQueryService": "watchtower_core.query.standards",
    "StandardSearchParams": "watchtower_core.query.standards",
    "TraceabilityQueryService": "watchtower_core.query.traceability",
    "ValidationEvidenceQueryService": "watchtower_core.query.evidence",
    "ValidationEvidenceSearchParams": "watchtower_core.query.evidence",
    "WorkflowQueryService": "watchtower_core.query.workflows",
    "WorkflowSearchParams": "watchtower_core.query.workflows",
}

_PLAN_DOMAIN_EXPORTS = {
    "ArtifactQueryService",
    "CoordinationQueryService",
    "DiscrepancyQueryService",
    "InitiativeQueryService",
    "ProjectQueryService",
    "ReadinessQueryService",
    "TaskQueryService",
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
