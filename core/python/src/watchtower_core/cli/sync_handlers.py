"""Runtime handlers for sync command families."""

from __future__ import annotations

from watchtower_core.cli.sync_document_handlers import (
    DOCUMENT_SYNC_HANDLERS,
    _run_sync_document_command,
)
from watchtower_core.cli.sync_orchestration_handlers import ORCHESTRATION_SYNC_HANDLERS
from watchtower_core.cli.sync_tracking_handlers import TRACKING_SYNC_HANDLERS

SYNC_HANDLERS = {
    **ORCHESTRATION_SYNC_HANDLERS,
    **DOCUMENT_SYNC_HANDLERS,
    **TRACKING_SYNC_HANDLERS,
}

_SYNC_EXPORT_NAMES = {
    "_run_sync_all": "all",
    "_run_sync_command_index": "command_index",
    "_run_sync_coordination": "coordination",
    "_run_sync_decision_index": "decision_index",
    "_run_sync_decision_tracking": "decision_tracking",
    "_run_sync_design_document_index": "design_document_index",
    "_run_sync_design_tracking": "design_tracking",
    "_run_sync_foundation_index": "foundation_index",
    "_run_sync_github_tasks": "github_tasks",
    "_run_sync_initiative_index": "initiative_index",
    "_run_sync_initiative_tracking": "initiative_tracking",
    "_run_sync_planning_catalog": "planning_catalog",
    "_run_sync_prd_index": "prd_index",
    "_run_sync_prd_tracking": "prd_tracking",
    "_run_sync_reference_index": "reference_index",
    "_run_sync_repository_paths": "repository_paths",
    "_run_sync_route_index": "route_index",
    "_run_sync_standard_index": "standard_index",
    "_run_sync_task_index": "task_index",
    "_run_sync_task_tracking": "task_tracking",
    "_run_sync_traceability_index": "traceability_index",
    "_run_sync_workflow_index": "workflow_index",
}

globals().update({name: SYNC_HANDLERS[key] for name, key in _SYNC_EXPORT_NAMES.items()})

__all__ = [
    "SYNC_HANDLERS",
    "_run_sync_document_command",
    *_SYNC_EXPORT_NAMES,
]
