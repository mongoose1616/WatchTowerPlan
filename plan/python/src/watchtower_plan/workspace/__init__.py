"""Feature-owned workspace services for the plan pack."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "ArtifactIndexService",
    "ArtifactIndexSyncResult",
    "PLAN_ARTIFACT_INDEX_PATH",
    "PLAN_COORDINATION_INDEX_PATH",
    "PLAN_PACK_SETTINGS_PATH",
    "PLAN_REVIEW_INDEX_PATH",
    "PLAN_TASK_INDEX_PATH",
    "PlanTaskIndexEntry",
    "PlanWorkspaceService",
    "search_artifact_entries",
]

_EXPORT_MODULES = {
    "ArtifactIndexService": "watchtower_plan.workspace.artifacts",
    "ArtifactIndexSyncResult": "watchtower_plan.workspace.artifacts",
    "PLAN_ARTIFACT_INDEX_PATH": "watchtower_plan.workspace.artifacts",
    "PLAN_COORDINATION_INDEX_PATH": "watchtower_plan.workspace.service",
    "PLAN_PACK_SETTINGS_PATH": "watchtower_plan.workspace.service",
    "PLAN_REVIEW_INDEX_PATH": "watchtower_plan.workspace.service",
    "PLAN_TASK_INDEX_PATH": "watchtower_plan.workspace.service",
    "PlanTaskIndexEntry": "watchtower_plan.workspace.service",
    "PlanWorkspaceService": "watchtower_plan.workspace.service",
    "search_artifact_entries": "watchtower_plan.workspace.artifacts",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
