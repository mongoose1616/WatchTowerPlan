"""Shared runtime helpers for CLI handler modules."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping, Sequence
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


def _emit_detail_result(
    args: argparse.Namespace,
    *,
    payload_factory: Callable[[], Mapping[str, object]],
    render_human: Callable[[], int | None],
    exit_code: int = 0,
) -> int:
    """Emit one standard detail payload or fall back to the human renderer."""

    if _print_payload_factory(args, payload_factory) == 0:
        return exit_code
    human_result = render_human()
    return exit_code if human_result is None else human_result


def _emit_collection_query_results[EntryT](
    args: argparse.Namespace,
    *,
    command_name: str,
    entries: Sequence[EntryT],
    noun: str,
    empty_message: str,
    payload_results_factory: Callable[[], Sequence[object]],
    render_entry: Callable[[EntryT], None],
    extra_payload: Mapping[str, object] | None = None,
) -> int:
    """Emit one standard collection-query payload or human summary."""

    if _print_payload_factory(
        args,
        lambda: _collection_query_payload(
            command_name=command_name,
            entries=entries,
            payload_results_factory=payload_results_factory,
            extra_payload=extra_payload,
        ),
    ) == 0:
        return 0

    if not entries:
        print(empty_message)
        return 0

    print(f"Found {len(entries)} {noun} entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        render_entry(entry)
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


def _run_value_error_operation[ResultT](
    args: argparse.Namespace,
    *,
    command_name: str,
    operation: Callable[[], ResultT],
    prefix: str | None = None,
) -> ResultT | None:
    """Run one operation and convert ValueError into a standard CLI error."""

    try:
        return operation()
    except ValueError as exc:
        _emit_command_error(args, command_name, str(exc), prefix=prefix)
        return None


def _print_reference_usage_summary(
    *,
    header: str,
    title: str,
    summary: str,
    uses_internal_references: bool,
    uses_external_references: bool,
) -> None:
    """Print one shared heading, summary, and reference-usage block."""

    print(header)
    print(f"  {title}")
    print(f"  {summary}")
    print(
        "  Reference use: "
        f"internal={'yes' if uses_internal_references else 'no'}, "
        f"external={'yes' if uses_external_references else 'no'}"
    )


def _parse_optional_bool_arg(value: str | None) -> bool | None:
    """Parse one CLI true/false option into a tri-state boolean."""

    if value is None:
        return None
    return value == "true"


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


def _task_filter_kwargs(args: argparse.Namespace) -> dict[str, object]:
    """Build the shared task-filter keyword arguments used across CLI commands."""

    return {
        "task_ids": tuple(args.task_id),
        "trace_id": args.trace_id,
        "task_status": args.task_status,
        "priority": args.priority,
        "owner": args.owner,
        "task_kind": args.task_kind,
        "blocked_only": args.blocked_only,
        "blocked_by_task_id": args.blocked_by,
        "depends_on_task_id": args.depends_on,
    }


def _resolve_output_path(path: Path | None) -> Path | None:
    return path.resolve() if path is not None else None


def _collection_query_payload(
    *,
    command_name: str,
    entries: Sequence[object],
    payload_results_factory: Callable[[], Sequence[object]],
    extra_payload: Mapping[str, object] | None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "result_count": len(entries),
        "results": list(payload_results_factory()),
    }
    if extra_payload is not None:
        payload.update(extra_payload)
    return payload
