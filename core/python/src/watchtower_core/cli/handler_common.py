"""Shared runtime helpers for CLI handler modules."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any


def _run_help(args: argparse.Namespace) -> int:
    help_parser = getattr(args, "help_parser", None)
    if help_parser is None:
        return 1
    help_parser.print_help()
    return 0


def _print_payload(args: argparse.Namespace, payload: Mapping[str, object]) -> int:
    if args.format == "json":
        print(json.dumps(payload, sort_keys=True))
        return 0
    return -1


def _print_payload_factory(
    args: argparse.Namespace,
    payload_factory: Callable[[], Mapping[str, object]],
) -> int:
    """Print one lazily constructed JSON payload when the caller requested JSON."""

    if args.format != "json":
        return -1
    print(json.dumps(payload_factory(), sort_keys=True))
    return 0


def _emit_command_error(
    args: argparse.Namespace,
    command_name: str,
    message: str,
    *,
    prefix: str | None = None,
) -> int:
    payload = {
        "command": command_name,
        "status": "error",
        "message": message,
    }
    if _print_payload(args, payload) == 0:
        return 1
    if prefix is None:
        print(message)
    else:
        print(f"{prefix}: {message}")
    return 1


def _task_dependency_payload(task: Any) -> dict[str, object]:
    task_status = getattr(task, "task_status", getattr(task, "status", None))
    return {
        "task_id": task.task_id,
        "title": task.title,
        "task_status": task_status,
        "priority": task.priority,
        "owner": task.owner,
        "doc_path": task.doc_path,
    }


def _resolve_output_path(path: Path | None) -> Path | None:
    return path.resolve() if path is not None else None
