"""Tracker-oriented sync command handlers."""

from __future__ import annotations

import argparse
from importlib import import_module
from typing import Any

from watchtower_core.cli.handler_common import _print_payload, _resolve_output_path


def _load_tracking_sync_service(module_name: str, class_name: str) -> Any:
    service_class = getattr(import_module(module_name), class_name)
    return service_class.from_repo_root()


def _run_sync_prd_tracking(args: argparse.Namespace) -> int:
    service = _load_tracking_sync_service(
        "watchtower_core.repo_ops.sync.prd_tracking",
        "PrdTrackingSyncService",
    )
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync prd-tracking",
        "status": "ok",
        "prd_count": result.prd_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            f"Rebuilt PRD tracking with {result.prd_count} entries and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt PRD tracking with {result.prd_count} entries in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_decision_tracking(args: argparse.Namespace) -> int:
    service = _load_tracking_sync_service(
        "watchtower_core.repo_ops.sync.decision_tracking",
        "DecisionTrackingSyncService",
    )
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync decision-tracking",
        "status": "ok",
        "decision_count": result.decision_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            "Rebuilt decision tracking with "
            f"{result.decision_count} entries and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt decision tracking with {result.decision_count} entries in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_design_tracking(args: argparse.Namespace) -> int:
    service = _load_tracking_sync_service(
        "watchtower_core.repo_ops.sync.design_tracking",
        "DesignTrackingSyncService",
    )
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync design-tracking",
        "status": "ok",
        "feature_design_count": result.feature_design_count,
        "implementation_plan_count": result.implementation_plan_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    total = result.feature_design_count + result.implementation_plan_count
    if wrote:
        print(f"Rebuilt design tracking with {total} documents and wrote it to {destination}.")
        return 0

    print(f"Rebuilt design tracking with {total} documents in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_initiative_tracking(args: argparse.Namespace) -> int:
    service = _load_tracking_sync_service(
        "watchtower_core.repo_ops.sync.initiative_tracking",
        "InitiativeTrackingSyncService",
    )
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync initiative-tracking",
        "status": "ok",
        "initiative_count": result.initiative_count,
        "active_count": result.active_count,
        "closed_count": result.closed_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            "Rebuilt initiative tracking with "
            f"{result.initiative_count} initiatives and wrote it to {destination}."
        )
        return 0

    print(
        "Rebuilt initiative tracking with "
        f"{result.initiative_count} initiatives in dry-run mode."
    )
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_task_tracking(args: argparse.Namespace) -> int:
    service = _load_tracking_sync_service(
        "watchtower_core.repo_ops.sync.task_tracking",
        "TaskTrackingSyncService",
    )
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync task-tracking",
        "status": "ok",
        "task_count": result.task_count,
        "open_count": result.open_count,
        "closed_count": result.closed_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            f"Rebuilt task tracking with {result.task_count} tasks and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt task tracking with {result.task_count} tasks in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0
