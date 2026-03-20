"""Residual WatchTowerPlan-specific orchestration surfaces."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "InitiativePackageService",
    "PlanWorkspaceService",
    "ProjectWorkspaceService",
]

_EXPORT_MODULES = {
    "InitiativePackageService": "watchtower_plan.initiatives",
    "PlanWorkspaceService": "watchtower_plan.plan_workspace",
    "ProjectWorkspaceService": "watchtower_plan.projects",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
