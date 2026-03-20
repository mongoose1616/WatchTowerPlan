"""Residual WatchTowerPlan-specific orchestration surfaces."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "InitiativePackageService",
    "PlanWorkspaceService",
    "ProjectWorkspaceService",
]

_EXPORT_MODULES = {
    "InitiativePackageService": "watchtower_plan.initiative_packages",
    "PlanWorkspaceService": "watchtower_plan.plan_workspace",
    "ProjectWorkspaceService": "watchtower_plan.project_workspace",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
