"""Runtime handlers for coordination and initiative query commands."""

from __future__ import annotations

import argparse
from typing import cast

from watchtower_core.cli.handler_common import (
    _emit_collection_query_results,
    _print_payload_factory,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import InitiativeIndexEntry
from watchtower_plan.rendering import serialize_initiative_entry
from watchtower_plan.query import (
    CoordinationQueryResult,
    CoordinationQueryService,
    CoordinationSearchParams,
    InitiativeQueryService,
    InitiativeSearchParams,
)


def _run_query_initiatives(args: argparse.Namespace) -> int:
    default_initiative_status = (
        "active"
        if _should_default_active_browse(args, include_blocked_only=True)
        else None
    )
    initiative_status = args.initiative_status or default_initiative_status
    service = InitiativeQueryService(ControlPlaneLoader())
    entries = service.search(
        InitiativeSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            initiative_status=initiative_status,
            current_phase=args.current_phase,
            owner=args.owner,
            blocked_only=args.blocked_only,
            limit=args.limit,
        )
    )
    return _emit_initiative_query_results(
        args,
        command_name="watchtower-core plan query initiatives",
        entries=entries,
        empty_message=_history_browse_empty_message(
            "initiative entries",
            default_initiative_status=default_initiative_status,
        ),
        show_task_summaries=False,
        default_initiative_status=default_initiative_status,
    )


def _run_query_coordination(args: argparse.Namespace) -> int:
    service = CoordinationQueryService(ControlPlaneLoader())
    initiative_status = args.initiative_status or "active"
    result = service.search(
        CoordinationSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            initiative_status=initiative_status,
            current_phase=args.current_phase,
            owner=args.owner,
            blocked_only=args.blocked_only,
            limit=args.limit,
        )
    )
    if (
        _print_payload_factory(
            args,
            lambda: _coordination_payload(
                result=result,
                initiative_status=initiative_status,
                include_default_status=(args.initiative_status is None),
            ),
        )
        == 0
    ):
        return 0

    print(f"Coordination mode: {result.index.coordination_mode}")
    print(result.index.summary)
    print(f"Next: {result.index.recommended_next_action}")
    print(f"Open first: {result.index.recommended_surface_path}")

    if not result.entries:
        if result.index.recent_closed_initiatives:
            print("Recent closeouts:")
            for entry in result.index.recent_closed_initiatives[:3]:
                print(
                    f"- {entry.trace_id} [{entry.initiative_status}] {entry.closed_at}"
                )
                print(f"  {entry.title}")
        return 0

    print(
        f"Found {len(result.entries)} "
        f"initiative entr{'y' if len(result.entries) == 1 else 'ies'}:"
    )
    for entry in result.entries:
        _print_initiative_entry_summary(entry, show_task_summaries=True)
    return 0


def _initiative_entry_payload(entry: InitiativeIndexEntry) -> dict[str, object]:
    return cast(dict[str, object], serialize_initiative_entry(entry, compact=False))


def _should_default_active_browse(
    args: argparse.Namespace,
    *,
    include_blocked_only: bool,
) -> bool:
    if args.initiative_status is not None:
        return False
    if args.query is not None:
        return False
    if args.trace_id is not None:
        return False
    if args.current_phase is not None:
        return False
    if args.owner is not None:
        return False
    if include_blocked_only and getattr(args, "blocked_only", False):
        return False
    return True


def _history_browse_empty_message(
    noun: str,
    *,
    default_initiative_status: str | None,
    include_trace_hint: bool = False,
) -> str:
    if default_initiative_status is None:
        return f"No {noun} matched the requested filters."
    history_hint = (
        " Pass --initiative-status completed|cancelled|superseded for history browsing."
    )
    if include_trace_hint:
        history_hint = (
            " Pass --initiative-status completed|cancelled|superseded for history "
            "browsing or --trace-id <trace_id> for one known closed trace."
        )
    return (
        f"No {default_initiative_status} {noun} matched the requested filters."
        f"{history_hint}"
    )


def _emit_initiative_query_results(
    args: argparse.Namespace,
    *,
    command_name: str,
    entries: tuple[InitiativeIndexEntry, ...],
    empty_message: str,
    show_task_summaries: bool,
    default_initiative_status: str | None = None,
) -> int:
    return _emit_collection_query_results(
        args,
        command_name=command_name,
        entries=entries,
        noun="initiative",
        empty_message=empty_message,
        payload_results_factory=lambda: [
            _initiative_entry_payload(entry) for entry in entries
        ],
        render_entry=lambda entry: _print_initiative_entry_summary(
            entry,
            show_task_summaries=show_task_summaries,
        ),
        extra_payload=(
            {"default_initiative_status": default_initiative_status}
            if default_initiative_status is not None
            else None
        ),
    )


def _coordination_payload(
    *,
    result: CoordinationQueryResult,
    initiative_status: str,
    include_default_status: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "command": "watchtower-core plan query coordination",
        "status": "ok",
        "coordination_mode": result.index.coordination_mode,
        "summary": result.index.summary,
        "recommended_next_action": result.index.recommended_next_action,
        "recommended_surface_path": result.index.recommended_surface_path,
        "active_initiative_count": result.index.active_initiative_count,
        "blocked_task_count": result.index.blocked_task_count,
        "actionable_task_count": result.index.actionable_task_count,
        "recent_closed_initiatives": [
            {
                "trace_id": entry.trace_id,
                "title": entry.title,
                "initiative_status": entry.initiative_status,
                "closed_at": entry.closed_at,
                "key_surface_path": entry.key_surface_path,
                "closure_reason": entry.closure_reason,
            }
            for entry in result.index.recent_closed_initiatives
        ],
        "actionable_tasks": [
            {
                "trace_id": entry.trace_id,
                "initiative_title": entry.initiative_title,
                "task_id": entry.task_id,
                "title": entry.title,
                "task_status": entry.task_status,
                "priority": entry.priority,
                "owner": entry.owner,
                "doc_path": entry.doc_path,
                "is_actionable": entry.is_actionable,
                "blocked_by": list(entry.blocked_by),
                "depends_on": list(entry.depends_on),
            }
            for entry in result.index.actionable_tasks
        ],
        "result_count": len(result.entries),
        "results": [_initiative_entry_payload(entry) for entry in result.entries],
    }
    if include_default_status:
        payload["default_initiative_status"] = initiative_status
    return payload


def _print_initiative_entry_summary(
    entry: InitiativeIndexEntry,
    *,
    show_task_summaries: bool,
) -> None:
    print(f"- {entry.trace_id} [{entry.current_phase}, {entry.initiative_status}]")
    print(f"  {entry.title}")
    print(f"  Owners: {_owner_text(entry.primary_owner, entry.active_owners)}")
    print(f"  Open tasks: {entry.open_task_count} (blocked={entry.blocked_task_count})")
    if show_task_summaries and entry.active_task_summaries:
        for task in entry.active_task_summaries:
            state = "actionable" if task.is_actionable else "blocked"
            print(
                f"  Task: {task.task_id} [{task.task_status}, {task.priority}, {state}]"
            )
            print(f"    {task.title}")
    print(f"  Next: {entry.next_action}")
    print(f"  Open first: {entry.next_surface_path}")


def _owner_text(primary_owner: str | None, active_owners: tuple[str, ...]) -> str:
    if primary_owner:
        return primary_owner
    if active_owners:
        return ", ".join(active_owners)
    return "unassigned"
