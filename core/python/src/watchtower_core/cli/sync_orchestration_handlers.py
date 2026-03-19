"""Aggregate and integration-oriented sync command handlers."""

from __future__ import annotations

import argparse
from importlib import import_module
from typing import Any

from watchtower_core.cli.handler_common import _emit_detail_result, _task_filter_kwargs
from watchtower_core.control_plane.loader import ControlPlaneLoader


def _load_sync_class(module_name: str, class_name: str) -> Any:
    return getattr(import_module(module_name), class_name)


def _run_multi_target_sync(
    args: argparse.Namespace,
    *,
    module_name: str,
    class_name: str,
    command_name: str,
    human_label: str,
) -> int:
    service = _load_sync_class(module_name, class_name).from_repo_root()
    result = service.run(write=args.write, output_dir=args.output_dir)
    payload = {
        "command": command_name,
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
    def _render_human() -> None:
        mode = (
            f"output-dir mode at {result.output_dir}"
            if result.output_dir is not None
            else ("write mode" if result.wrote else "dry-run mode")
        )
        print(f"Ran {human_label} across {len(result.records)} targets in {mode}.")
        for record in result.records:
            print(
                f"- {record.target} [{record.artifact_kind}] "
                f"record_count={record.record_count}"
            )
            if record.output_path is not None:
                print(f"  Wrote to {record.output_path}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _run_sync_all(args: argparse.Namespace) -> int:
    return _run_multi_target_sync(
        args,
        module_name="watchtower_core.plan_runtime.sync.all",
        class_name="AllSyncService",
        command_name="watchtower-core sync all",
        human_label="sync all",
    )


def _run_sync_coordination(args: argparse.Namespace) -> int:
    return _run_multi_target_sync(
        args,
        module_name="watchtower_core.plan_runtime.sync.coordination",
        class_name="CoordinationSyncService",
        command_name="watchtower-core sync coordination",
        human_label="sync coordination",
    )


def _run_sync_github_tasks(args: argparse.Namespace) -> int:
    params_class = _load_sync_class(
        "watchtower_core.plan_runtime.sync.github_tasks",
        "GitHubTaskSyncParams",
    )
    service = _load_sync_class(
        "watchtower_core.plan_runtime.sync.github_tasks",
        "GitHubTaskSyncService",
    )(ControlPlaneLoader())
    result = service.sync(
        params_class(
            **_task_filter_kwargs(args),
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
    def _render_human() -> None:
        if not result.records:
            print("No task entries matched the requested sync filters.")
            return
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

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
        exit_code=exit_code,
    )


ORCHESTRATION_SYNC_HANDLERS = {
    "all": _run_sync_all,
    "coordination": _run_sync_coordination,
    "github_tasks": _run_sync_github_tasks,
}
