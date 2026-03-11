"""Runtime handlers for sync command families."""

from __future__ import annotations

from watchtower_core.cli.sync_document_handlers import (
    _run_sync_command_index,
    _run_sync_decision_index,
    _run_sync_design_document_index,
    _run_sync_document_command,
    _run_sync_foundation_index,
    _run_sync_initiative_index,
    _run_sync_planning_catalog,
    _run_sync_prd_index,
    _run_sync_reference_index,
    _run_sync_repository_paths,
    _run_sync_route_index,
    _run_sync_standard_index,
    _run_sync_task_index,
    _run_sync_traceability_index,
    _run_sync_workflow_index,
)
from watchtower_core.cli.sync_orchestration_handlers import (
    _run_sync_all,
    _run_sync_coordination,
    _run_sync_github_tasks,
)
from watchtower_core.cli.sync_tracking_handlers import (
    _run_sync_decision_tracking,
    _run_sync_design_tracking,
    _run_sync_initiative_tracking,
    _run_sync_prd_tracking,
    _run_sync_task_tracking,
)

__all__ = [
    "_run_sync_all",
    "_run_sync_command_index",
    "_run_sync_coordination",
    "_run_sync_decision_index",
    "_run_sync_decision_tracking",
    "_run_sync_design_document_index",
    "_run_sync_design_tracking",
    "_run_sync_document_command",
    "_run_sync_foundation_index",
    "_run_sync_github_tasks",
    "_run_sync_initiative_index",
    "_run_sync_initiative_tracking",
    "_run_sync_planning_catalog",
    "_run_sync_prd_index",
    "_run_sync_prd_tracking",
    "_run_sync_reference_index",
    "_run_sync_repository_paths",
    "_run_sync_route_index",
    "_run_sync_standard_index",
    "_run_sync_task_index",
    "_run_sync_task_tracking",
    "_run_sync_traceability_index",
    "_run_sync_workflow_index",
]
