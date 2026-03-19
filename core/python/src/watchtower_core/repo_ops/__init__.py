"""Residual WatchTowerPlan-specific orchestration surfaces."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "InitiativePackageService",
    "PlanWorkspaceService",
    "PlanningDocument",
    "ProjectWorkspaceService",
    "TaskDocument",
]

_EXPORT_MODULES = {
    "InitiativePackageService": "watchtower_core.repo_ops.initiative_packages",
    "PlanWorkspaceService": "watchtower_core.repo_ops.plan_workspace",
    "PlanningDocument": "watchtower_core.repo_ops.planning_documents",
    "ProjectWorkspaceService": "watchtower_core.repo_ops.project_workspace",
    "TaskDocument": "watchtower_core.repo_ops.task_documents",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
