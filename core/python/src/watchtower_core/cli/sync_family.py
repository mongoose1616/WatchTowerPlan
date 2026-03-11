"""Sync command-family registration."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _run_help
from watchtower_core.cli.sync_family_documents import register_document_sync_commands
from watchtower_core.cli.sync_family_special import (
    build_sync_subparsers,
    register_special_sync_commands,
)
from watchtower_core.cli.sync_family_tracking import register_tracking_sync_commands
from watchtower_core.cli.sync_handlers import (
    _run_sync_all,
    _run_sync_command_index,
    _run_sync_coordination,
    _run_sync_decision_index,
    _run_sync_decision_tracking,
    _run_sync_design_document_index,
    _run_sync_design_tracking,
    _run_sync_foundation_index,
    _run_sync_github_tasks,
    _run_sync_initiative_index,
    _run_sync_initiative_tracking,
    _run_sync_planning_catalog,
    _run_sync_prd_index,
    _run_sync_prd_tracking,
    _run_sync_reference_index,
    _run_sync_repository_paths,
    _run_sync_route_index,
    _run_sync_standard_index,
    _run_sync_task_index,
    _run_sync_task_tracking,
    _run_sync_traceability_index,
    _run_sync_workflow_index,
)


def register_sync_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the sync command family and its subcommands."""

    handlers = {
        "all": _run_sync_all,
        "command_index": _run_sync_command_index,
        "coordination": _run_sync_coordination,
        "decision_index": _run_sync_decision_index,
        "decision_tracking": _run_sync_decision_tracking,
        "design_document_index": _run_sync_design_document_index,
        "design_tracking": _run_sync_design_tracking,
        "foundation_index": _run_sync_foundation_index,
        "github_tasks": _run_sync_github_tasks,
        "initiative_index": _run_sync_initiative_index,
        "initiative_tracking": _run_sync_initiative_tracking,
        "planning_catalog": _run_sync_planning_catalog,
        "prd_index": _run_sync_prd_index,
        "prd_tracking": _run_sync_prd_tracking,
        "reference_index": _run_sync_reference_index,
        "repository_paths": _run_sync_repository_paths,
        "route_index": _run_sync_route_index,
        "standard_index": _run_sync_standard_index,
        "task_index": _run_sync_task_index,
        "task_tracking": _run_sync_task_tracking,
        "traceability_index": _run_sync_traceability_index,
        "workflow_index": _run_sync_workflow_index,
    }
    sync_subparsers = build_sync_subparsers(subparsers, help_handler=_run_help)
    register_special_sync_commands(sync_subparsers, handlers)
    register_document_sync_commands(sync_subparsers, handlers)
    register_tracking_sync_commands(sync_subparsers, handlers)
