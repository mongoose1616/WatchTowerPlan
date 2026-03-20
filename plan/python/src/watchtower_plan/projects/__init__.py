"""Feature-owned project services for the plan pack."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "PLAN_PACK_SETTINGS_PATH",
    "PLAN_PROJECT_INDEX_PATH",
    "DerivedProjectSurfaceIssue",
    "PlanProjectIndexEntry",
    "PlanProjectSearchParams",
    "ProjectBootstrapParams",
    "ProjectBootstrapResult",
    "ProjectContext",
    "ProjectMachineValidationResult",
    "ProjectRepositoryLink",
    "ProjectRepositoryLinkSpec",
    "ProjectValidationResult",
    "ProjectWorkspaceService",
    "ProjectWorkspaceSyncResult",
    "load_project_context",
    "validate_project_machine_state",
]

_EXPORT_MODULES = {
    "PLAN_PACK_SETTINGS_PATH": "watchtower_plan.projects.context",
    "PLAN_PROJECT_INDEX_PATH": "watchtower_plan.projects.workspace",
    "DerivedProjectSurfaceIssue": "watchtower_plan.projects.workspace",
    "PlanProjectIndexEntry": "watchtower_plan.projects.workspace",
    "PlanProjectSearchParams": "watchtower_plan.projects.workspace",
    "ProjectBootstrapParams": "watchtower_plan.projects.workspace",
    "ProjectBootstrapResult": "watchtower_plan.projects.workspace",
    "ProjectContext": "watchtower_plan.projects.context",
    "ProjectMachineValidationResult": "watchtower_plan.projects.context",
    "ProjectRepositoryLink": "watchtower_plan.projects.context",
    "ProjectRepositoryLinkSpec": "watchtower_plan.projects.workspace",
    "ProjectValidationResult": "watchtower_plan.projects.workspace",
    "ProjectWorkspaceService": "watchtower_plan.projects.workspace",
    "ProjectWorkspaceSyncResult": "watchtower_plan.projects.workspace",
    "load_project_context": "watchtower_plan.projects.context",
    "validate_project_machine_state": "watchtower_plan.projects.context",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
