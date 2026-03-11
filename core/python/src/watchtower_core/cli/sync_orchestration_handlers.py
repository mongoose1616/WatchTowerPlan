"""Aggregate and integration-oriented sync command handlers."""

from __future__ import annotations

import argparse
from importlib import import_module
from typing import Any

from watchtower_core.cli.handler_common import _print_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader


def _load_sync_class(module_name: str, class_name: str) -> Any:
    return getattr(import_module(module_name), class_name)


def _run_sync_all(args: argparse.Namespace) -> int:
    service = _load_sync_class(
        "watchtower_core.repo_ops.sync.all",
        "AllSyncService",
    ).from_repo_root()
    result = service.run(write=args.write, output_dir=args.output_dir)
    payload = {
        "command": "watchtower-core sync all",
        "status": "ok",
        "result_count": len(result.records),
        "wrote": result.wrote,
        "output_dir": result.output_dir,
        "results": [
            {
                "target": record.target,
                "artifact_kind": record.artifact_kind,
                "relative_output_path": record.relative_output_path,
                "output_path": record.output_path,
                "wrote": record.wrote,
                "record_count": record.record_count,
                "details": record.details,
            }
            for record in result.records
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    mode = (
        f"output-dir mode at {result.output_dir}"
        if result.output_dir is not None
        else ("write mode" if result.wrote else "dry-run mode")
    )
    print(f"Ran sync all across {len(result.records)} targets in {mode}.")
    for record in result.records:
        print(
            f"- {record.target} [{record.artifact_kind}] "
            f"record_count={record.record_count}"
        )
        if record.output_path is not None:
            print(f"  Wrote to {record.output_path}")
    return 0


def _run_sync_coordination(args: argparse.Namespace) -> int:
    service = _load_sync_class(
        "watchtower_core.repo_ops.sync.coordination",
        "CoordinationSyncService",
    ).from_repo_root()
    result = service.run(write=args.write, output_dir=args.output_dir)
    payload = {
        "command": "watchtower-core sync coordination",
        "status": "ok",
        "result_count": len(result.records),
        "wrote": result.wrote,
        "output_dir": result.output_dir,
        "results": [
            {
                "target": record.target,
                "artifact_kind": record.artifact_kind,
                "relative_output_path": record.relative_output_path,
                "output_path": record.output_path,
                "wrote": record.wrote,
                "record_count": record.record_count,
                "details": record.details,
            }
            for record in result.records
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    mode = (
        f"output-dir mode at {result.output_dir}"
        if result.output_dir is not None
        else ("write mode" if result.wrote else "dry-run mode")
    )
    print(f"Ran sync coordination across {len(result.records)} targets in {mode}.")
    for record in result.records:
        print(
            f"- {record.target} [{record.artifact_kind}] "
            f"record_count={record.record_count}"
        )
        if record.output_path is not None:
            print(f"  Wrote to {record.output_path}")
    return 0


def _run_sync_github_tasks(args: argparse.Namespace) -> int:
    params_class = _load_sync_class(
        "watchtower_core.repo_ops.sync.github_tasks",
        "GitHubTaskSyncParams",
    )
    service = _load_sync_class(
        "watchtower_core.repo_ops.sync.github_tasks",
        "GitHubTaskSyncService",
    )(ControlPlaneLoader())
    result = service.sync(
        params_class(
            task_ids=tuple(args.task_id),
            trace_id=args.trace_id,
            task_status=args.task_status,
            priority=args.priority,
            owner=args.owner,
            task_kind=args.task_kind,
            blocked_only=args.blocked_only,
            blocked_by_task_id=args.blocked_by,
            depends_on_task_id=args.depends_on,
            repository=args.repo,
            project_owner=args.project_owner,
            project_owner_type=args.project_owner_type,
            project_number=args.project_number,
            project_status_field_name=args.project_status_field,
            token_env=args.token_env,
            sync_labels=not args.no_label_sync,
        ),
        write=args.write,
    )
    payload = {
        "command": "watchtower-core sync github-tasks",
        "status": "ok" if all(record.success for record in result.records) else "error",
        "wrote": result.wrote,
        "result_count": len(result.records),
        "synced_task_count": result.synced_task_count,
        "local_change_count": result.local_change_count,
        "rebuilt_task_index": result.rebuilt_task_index,
        "rebuilt_task_tracking": result.rebuilt_task_tracking,
        "rebuilt_traceability_index": result.rebuilt_traceability_index,
        "results": [
            {
                "task_id": record.task_id,
                "doc_path": record.doc_path,
                "repository": record.repository,
                "task_status": record.task_status,
                "issue_action": record.issue_action,
                "project_action": record.project_action,
                "success": record.success,
                "message": record.message,
                "github_issue_number": record.github_issue_number,
                "github_issue_url": record.github_issue_url,
                "github_project_item_id": record.github_project_item_id,
                "labels": list(record.labels),
            }
            for record in result.records
        ],
    }
    exit_code = 0 if payload["status"] == "ok" else 1
    if _print_payload(args, payload) == 0:
        return exit_code

    if not result.records:
        print("No task entries matched the requested sync filters.")
        return 0
    for record in result.records:
        state = "ok" if record.success else "error"
        print(f"- {record.task_id} [{state}]")
        print(f"  Issue action: {record.issue_action}")
        if record.project_action is not None:
            print(f"  Project action: {record.project_action}")
        if record.labels:
            print(f"  Labels: {', '.join(record.labels)}")
        if record.github_issue_url is not None:
            print(f"  GitHub Issue: {record.github_issue_url}")
        print(f"  {record.message}")
    return exit_code
