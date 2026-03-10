"""Runtime handlers for task lifecycle commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_command_error, _print_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.task_lifecycle import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskMutationResult,
    TaskTransitionParams,
    TaskUpdateParams,
)


def _run_task_create(args: argparse.Namespace) -> int:
    service = TaskLifecycleService(ControlPlaneLoader())
    try:
        result = service.create(
            TaskCreateParams(
                task_id=args.task_id,
                trace_id=args.trace_id,
                title=args.title,
                summary=args.summary,
                task_kind=args.task_kind,
                priority=args.priority,
                owner=args.owner,
                task_status=args.task_status,
                scope_items=tuple(args.scope),
                done_when_items=tuple(args.done_when),
                applies_to=tuple(args.applies_to),
                related_ids=tuple(args.related_id),
                depends_on=tuple(args.depends_on),
                blocked_by=tuple(args.blocked_by),
                file_stem=args.file_stem,
                updated_at=args.updated_at,
            ),
            write=args.write,
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core task create",
            str(exc),
            prefix="Task create error",
        )
    return _emit_task_result(args, command_name="watchtower-core task create", result=result)


def _run_task_update(args: argparse.Namespace) -> int:
    service = TaskLifecycleService(ControlPlaneLoader())
    try:
        result = service.update(
            TaskUpdateParams(
                task_id=args.task_id,
                trace_id=args.trace_id,
                clear_trace_id=args.clear_trace_id,
                title=args.title,
                summary=args.summary,
                task_kind=args.task_kind,
                priority=args.priority,
                owner=args.owner,
                task_status=args.task_status,
                scope_items=None if args.scope is None else tuple(args.scope),
                done_when_items=None if args.done_when is None else tuple(args.done_when),
                applies_to=None if args.applies_to is None else tuple(args.applies_to),
                clear_applies_to=args.clear_applies_to,
                related_ids=None if args.related_id is None else tuple(args.related_id),
                clear_related_ids=args.clear_related_ids,
                depends_on=None if args.depends_on is None else tuple(args.depends_on),
                clear_depends_on=args.clear_depends_on,
                blocked_by=None if args.blocked_by is None else tuple(args.blocked_by),
                clear_blocked_by=args.clear_blocked_by,
                file_stem=args.file_stem,
                updated_at=args.updated_at,
            ),
            write=args.write,
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core task update",
            str(exc),
            prefix="Task update error",
        )
    return _emit_task_result(args, command_name="watchtower-core task update", result=result)


def _run_task_transition(args: argparse.Namespace) -> int:
    service = TaskLifecycleService(ControlPlaneLoader())
    try:
        result = service.transition(
            TaskTransitionParams(
                task_id=args.task_id,
                task_status=args.task_status,
                next_owner=args.next_owner,
                depends_on=None if args.depends_on is None else tuple(args.depends_on),
                clear_depends_on=args.clear_depends_on,
                blocked_by=None if args.blocked_by is None else tuple(args.blocked_by),
                clear_blocked_by=args.clear_blocked_by,
                file_stem=args.file_stem,
                updated_at=args.updated_at,
            ),
            write=args.write,
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core task transition",
            str(exc),
            prefix="Task transition error",
        )
    return _emit_task_result(args, command_name="watchtower-core task transition", result=result)


def _emit_task_result(
    args: argparse.Namespace,
    *,
    command_name: str,
    result: TaskMutationResult,
) -> int:
    payload = {
        "command": command_name,
        "status": "ok",
        "task_id": result.task_id,
        "title": result.title,
        "summary": result.summary,
        "trace_id": result.trace_id,
        "task_status": result.task_status,
        "task_kind": result.task_kind,
        "priority": result.priority,
        "owner": result.owner,
        "updated_at": result.updated_at,
        "doc_path": result.doc_path,
        "previous_doc_path": result.previous_doc_path,
        "moved": result.moved,
        "changed": result.changed,
        "wrote": result.wrote,
        "coordination_refreshed": result.coordination_refreshed,
        "closeout_recommended": result.closeout_recommended,
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not result.changed:
        print(f"No task changes detected for {result.task_id}.")
        print("Use additional flags to change task metadata or body content.")
        return 0

    action = "Wrote" if result.wrote else "Prepared"
    print(f"{action} task {result.task_id} at {result.doc_path}.")
    print(f"Status: {result.task_status}")
    print(f"Owner: {result.owner}")
    if result.moved and result.previous_doc_path is not None:
        print(f"Moved From: {result.previous_doc_path}")
    if result.closeout_recommended and result.trace_id is not None:
        print(f"Closeout Recommended: {result.trace_id}")
    if result.wrote:
        print("Coordination surfaces were refreshed.")
    else:
        print("Dry-run only. Use --write to persist the task change and refresh coordination.")
    return 0
