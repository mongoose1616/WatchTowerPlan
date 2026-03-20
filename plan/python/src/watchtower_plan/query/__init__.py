"""Repository-specific query services."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "ArtifactQueryService",
    "ArtifactSearchParams",
    "CoordinationQueryResult",
    "CoordinationQueryService",
    "CoordinationSearchParams",
    "PlanCloseoutQueryService",
    "PlanCloseoutSearchParams",
    "DiscrepancyQueryService",
    "DiscrepancySearchParams",
    "PlanEvidenceQueryService",
    "PlanEvidenceSearchParams",
    "InitiativeQueryService",
    "InitiativeSearchParams",
    "ProjectQueryService",
    "ProjectSearchParams",
    "ReadinessQueryService",
    "ReadinessSearchParams",
    "PlanReviewQueryService",
    "PlanReviewSearchParams",
    "TaskQueryService",
    "TaskSearchParams",
]

_EXPORT_MODULES = {
    "ArtifactQueryService": "watchtower_plan.query.artifacts",
    "ArtifactSearchParams": "watchtower_plan.query.artifacts",
    "CoordinationQueryResult": "watchtower_plan.query.coordination",
    "CoordinationQueryService": "watchtower_plan.query.coordination",
    "CoordinationSearchParams": "watchtower_plan.query.coordination",
    "PlanCloseoutQueryService": "watchtower_plan.query.closeouts",
    "PlanCloseoutSearchParams": "watchtower_plan.query.closeouts",
    "DiscrepancyQueryService": "watchtower_plan.query.discrepancies",
    "DiscrepancySearchParams": "watchtower_plan.query.discrepancies",
    "PlanEvidenceQueryService": "watchtower_plan.query.plan_evidence",
    "PlanEvidenceSearchParams": "watchtower_plan.query.plan_evidence",
    "InitiativeQueryService": "watchtower_plan.query.initiatives",
    "InitiativeSearchParams": "watchtower_plan.query.initiatives",
    "ProjectQueryService": "watchtower_plan.query.projects",
    "ProjectSearchParams": "watchtower_plan.query.projects",
    "ReadinessQueryService": "watchtower_plan.query.readiness",
    "ReadinessSearchParams": "watchtower_plan.query.readiness",
    "PlanReviewQueryService": "watchtower_plan.query.reviews",
    "PlanReviewSearchParams": "watchtower_plan.query.reviews",
    "TaskQueryService": "watchtower_plan.query.tasks",
    "TaskSearchParams": "watchtower_plan.query.tasks",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
