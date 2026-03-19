"""Residual WatchTowerPlan-specific orchestration surfaces."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "GovernedDocument",
    "InitiativePackageService",
    "PlanWorkspaceService",
    "ProjectWorkspaceService",
]

_EXPORT_MODULES = {
    "GovernedDocument": "watchtower_core.plan_runtime.governed_documents",
    "InitiativePackageService": "watchtower_core.plan_runtime.initiative_packages",
    "PlanWorkspaceService": "watchtower_core.plan_runtime.plan_workspace",
    "ProjectWorkspaceService": "watchtower_core.plan_runtime.project_workspace",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
