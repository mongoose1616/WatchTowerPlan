"""Repository-specific sync services."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "AllSyncResult",
    "AllSyncService",
    "COORDINATION_SYNC_GROUP",
    "COORDINATION_INDEX_ARTIFACT_PATH",
    "COORDINATION_TRACKING_DOCUMENT_PATH",
    "CoordinationSyncService",
    "CoordinationIndexSyncService",
    "CoordinationTrackingSyncService",
    "GitHubTaskSyncParams",
    "GitHubTaskSyncService",
    "INITIATIVE_INDEX_ARTIFACT_PATH",
    "INITIATIVE_TRACKING_DOCUMENT_PATH",
    "InitiativeIndexSyncService",
    "InitiativeTrackingSyncService",
    "SYNC_TARGET_SPECS",
    "sync_target_specs_for_group",
    "SyncTargetGroup",
    "SyncTargetSpec",
    "TASK_INDEX_ARTIFACT_PATH",
    "TASK_TRACKING_DOCUMENT_PATH",
    "TaskIndexSyncService",
    "TaskTrackingSyncService",
    "TRACEABILITY_INDEX_ARTIFACT_PATH",
    "TraceabilityIndexSyncService",
]

_EXPORT_MODULES = {
    "AllSyncResult": "watchtower_plan.sync.all",
    "AllSyncService": "watchtower_plan.sync.all",
    "COORDINATION_SYNC_GROUP": "watchtower_plan.sync.registry",
    "COORDINATION_INDEX_ARTIFACT_PATH": "watchtower_plan.sync.coordination_index",
    "COORDINATION_TRACKING_DOCUMENT_PATH": "watchtower_plan.sync.coordination_tracking",
    "CoordinationSyncService": "watchtower_plan.sync.coordination",
    "CoordinationIndexSyncService": "watchtower_plan.sync.coordination_index",
    "CoordinationTrackingSyncService": "watchtower_plan.sync.coordination_tracking",
    "GitHubTaskSyncParams": "watchtower_plan.sync.github_tasks",
    "GitHubTaskSyncService": "watchtower_plan.sync.github_tasks",
    "INITIATIVE_INDEX_ARTIFACT_PATH": "watchtower_plan.sync.initiative_index",
    "INITIATIVE_TRACKING_DOCUMENT_PATH": "watchtower_plan.sync.initiative_tracking",
    "InitiativeIndexSyncService": "watchtower_plan.sync.initiative_index",
    "InitiativeTrackingSyncService": "watchtower_plan.sync.initiative_tracking",
    "SYNC_TARGET_SPECS": "watchtower_plan.sync.registry",
    "sync_target_specs_for_group": "watchtower_plan.sync.registry",
    "SyncTargetGroup": "watchtower_plan.sync.registry",
    "SyncTargetSpec": "watchtower_plan.sync.registry",
    "TASK_INDEX_ARTIFACT_PATH": "watchtower_plan.sync.task_index",
    "TASK_TRACKING_DOCUMENT_PATH": "watchtower_plan.sync.task_tracking",
    "TaskIndexSyncService": "watchtower_plan.sync.task_index",
    "TaskTrackingSyncService": "watchtower_plan.sync.task_tracking",
    "TRACEABILITY_INDEX_ARTIFACT_PATH": "watchtower_plan.sync.traceability",
    "TraceabilityIndexSyncService": "watchtower_plan.sync.traceability",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
