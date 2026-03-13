"""Runtime handlers for coordination, initiative, and planning query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _print_payload_factory
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import InitiativeIndexEntry, PlanningCatalogEntry
from watchtower_core.repo_ops.planning_projection_serialization import (
    serialize_initiative_entry,
    serialize_planning_catalog_entry,
)
from watchtower_core.repo_ops.query import (
    CoordinationQueryResult,
    CoordinationQueryService,
    CoordinationSearchParams,
    InitiativeQueryService,
    InitiativeSearchParams,
    PlanningCatalogQueryService,
    PlanningCatalogSearchParams,
)


def _run_query_initiatives(args: argparse.Namespace) -> int:
    default_initiative_status = (
        "active" if _should_default_active_browse(args, include_blocked_only=True) else None
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
        command_name="watchtower-core query initiatives",
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
    if _print_payload_factory(
        args,
        lambda: _coordination_payload(
            result=result,
            initiative_status=initiative_status,
            include_default_status=(args.initiative_status is None),
        ),
    ) == 0:
        return 0

    print(f"Coordination mode: {result.index.coordination_mode}")
    print(result.index.summary)
    print(f"Next: {result.index.recommended_next_action}")
    print(f"Open first: {result.index.recommended_surface_path}")

    if not result.entries:
        if result.index.recent_closed_initiatives:
            print("Recent closeouts:")
            for entry in result.index.recent_closed_initiatives[:3]:
                print(f"- {entry.trace_id} [{entry.initiative_status}] {entry.closed_at}")
                print(f"  {entry.title}")
        return 0

    print(
        f"Found {len(result.entries)} "
        f"initiative entr{'y' if len(result.entries) == 1 else 'ies'}:"
    )
    for entry in result.entries:
        owner_text = entry.primary_owner or (
            ", ".join(entry.active_owners) if entry.active_owners else "unassigned"
        )
        print(f"- {entry.trace_id} [{entry.current_phase}, {entry.initiative_status}]")
        print(f"  {entry.title}")
        print(f"  Owners: {owner_text}")
        print(
            f"  Open tasks: {entry.open_task_count} "
            f"(blocked={entry.blocked_task_count})"
        )
        if entry.active_task_summaries:
            for task in entry.active_task_summaries:
                state = "actionable" if task.is_actionable else "blocked"
                print(
                    f"  Task: {task.task_id} "
                    f"[{task.task_status}, {task.priority}, {state}]"
                )
                print(f"    {task.title}")
        print(f"  Next: {entry.next_action}")
        print(f"  Open first: {entry.next_surface_path}")
    return 0


def _run_query_planning(args: argparse.Namespace) -> int:
    default_initiative_status = (
        "active" if _should_default_active_browse(args, include_blocked_only=False) else None
    )
    initiative_status = args.initiative_status or default_initiative_status
    service = PlanningCatalogQueryService(ControlPlaneLoader())
    entries = service.search(
        PlanningCatalogSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            initiative_status=initiative_status,
            current_phase=args.current_phase,
            owner=args.owner,
            limit=args.limit,
        )
    )
    if _print_payload_factory(
        args,
        lambda: _planning_query_payload(
            entries=entries,
            default_initiative_status=default_initiative_status,
        ),
    ) == 0:
        return 0

    if not entries:
        print(
            _history_browse_empty_message(
                "planning-catalog entries",
                default_initiative_status=default_initiative_status,
                include_trace_hint=True,
            )
        )
        return 0

    print(f"Found {len(entries)} planning entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        owner_text = entry.primary_owner or (
            ", ".join(entry.active_owners) if entry.active_owners else "unassigned"
        )
        print(
            f"- {entry.trace_id} "
            f"[{entry.current_phase}, {entry.initiative_status}, {entry.artifact_status}]"
        )
        print(f"  {entry.title}")
        print(f"  Owners: {owner_text}")
        print(f"  Next: {entry.coordination.next_action}")
        print(
            "  Sections: "
            f"prds={len(entry.prds)} decisions={len(entry.decisions)} "
            f"designs={len(entry.design_documents)} tasks={len(entry.tasks)} "
            f"contracts={len(entry.acceptance_contracts)} "
            f"evidence={len(entry.validation_evidence)}"
        )
    return 0


def _initiative_entry_payload(entry: InitiativeIndexEntry) -> dict[str, object]:
    return serialize_initiative_entry(entry, compact=False)


def _planning_entry_payload(entry: PlanningCatalogEntry) -> dict[str, object]:
    return serialize_planning_catalog_entry(entry, compact=False)


def _planning_query_payload(
    *,
    entries: tuple[PlanningCatalogEntry, ...],
    default_initiative_status: str | None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "command": "watchtower-core query planning",
        "status": "ok",
        "result_count": len(entries),
        "results": [_planning_entry_payload(entry) for entry in entries],
    }
    if default_initiative_status is not None:
        payload["default_initiative_status"] = default_initiative_status
    return payload


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
    history_hint = " Pass --initiative-status completed|cancelled|superseded for history browsing."
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
    if _print_payload_factory(
        args,
        lambda: _initiative_query_payload(
            command_name=command_name,
            entries=entries,
            default_initiative_status=default_initiative_status,
        ),
    ) == 0:
        return 0

    if not entries:
        print(empty_message)
        return 0

    print(f"Found {len(entries)} initiative entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        owner_text = entry.primary_owner or (
            ", ".join(entry.active_owners) if entry.active_owners else "unassigned"
        )
        print(f"- {entry.trace_id} [{entry.current_phase}, {entry.initiative_status}]")
        print(f"  {entry.title}")
        print(f"  Owners: {owner_text}")
        print(
            f"  Open tasks: {entry.open_task_count} "
            f"(blocked={entry.blocked_task_count})"
        )
        if show_task_summaries and entry.active_task_summaries:
            for task in entry.active_task_summaries:
                state = "actionable" if task.is_actionable else "blocked"
                print(
                    f"  Task: {task.task_id} "
                    f"[{task.task_status}, {task.priority}, {state}]"
                )
                print(f"    {task.title}")
        print(f"  Next: {entry.next_action}")
        print(f"  Open first: {entry.next_surface_path}")
    return 0


def _initiative_query_payload(
    *,
    command_name: str,
    entries: tuple[InitiativeIndexEntry, ...],
    default_initiative_status: str | None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "result_count": len(entries),
        "results": [_initiative_entry_payload(entry) for entry in entries],
    }
    if default_initiative_status is not None:
        payload["default_initiative_status"] = default_initiative_status
    return payload


def _coordination_payload(
    *,
    result: CoordinationQueryResult,
    initiative_status: str,
    include_default_status: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "command": "watchtower-core query coordination",
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
