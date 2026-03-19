"""Tracker-oriented sync command handlers."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from importlib import import_module
from typing import Any

from watchtower_core.cli.handler_common import (
    _emit_detail_result,
    _resolve_output_path,
)


def _load_tracking_sync_service(module_name: str, class_name: str) -> Any:
    service_class = getattr(import_module(module_name), class_name)
    return service_class.from_repo_root()


def _run_tracking_sync(
    args: argparse.Namespace,
    *,
    module_name: str,
    class_name: str,
    command_name: str,
    payload_counts_factory: Callable[[Any], dict[str, object]],
    wrote_message_factory: Callable[[Any, str], str],
    dry_run_message_factory: Callable[[Any], str],
) -> int:
    service = _load_tracking_sync_service(module_name, class_name)
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        **payload_counts_factory(result),
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    def _render_human() -> None:
        if wrote and destination is not None:
            print(wrote_message_factory(result, destination))
            return

        print(dry_run_message_factory(result))
        print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _run_sync_initiative_tracking(args: argparse.Namespace) -> int:
    return _run_tracking_sync(
        args,
        module_name="watchtower_core.plan_runtime.sync.initiative_tracking",
        class_name="InitiativeTrackingSyncService",
        command_name="watchtower-core sync initiative-tracking",
        payload_counts_factory=lambda result: {
            "initiative_count": result.initiative_count,
            "active_count": result.active_count,
            "closed_count": result.closed_count,
        },
        wrote_message_factory=lambda result, destination: (
            "Rebuilt initiative tracking with "
            f"{result.initiative_count} initiatives and wrote it to {destination}."
        ),
        dry_run_message_factory=lambda result: (
            "Rebuilt initiative tracking with "
            f"{result.initiative_count} initiatives in dry-run mode."
        ),
    )


def _run_sync_task_tracking(args: argparse.Namespace) -> int:
    return _run_tracking_sync(
        args,
        module_name="watchtower_core.plan_runtime.sync.task_tracking",
        class_name="TaskTrackingSyncService",
        command_name="watchtower-core sync task-tracking",
        payload_counts_factory=lambda result: {
            "task_count": result.task_count,
            "open_count": result.open_count,
            "closed_count": result.closed_count,
        },
        wrote_message_factory=lambda result, destination: (
            f"Rebuilt task tracking with {result.task_count} tasks and wrote it to {destination}."
        ),
        dry_run_message_factory=lambda result: (
            f"Rebuilt task tracking with {result.task_count} tasks in dry-run mode."
        ),
    )


TRACKING_SYNC_HANDLERS = {
    "initiative_tracking": _run_sync_initiative_tracking,
    "task_tracking": _run_sync_task_tracking,
}
