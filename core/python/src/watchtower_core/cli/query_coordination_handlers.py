"""Runtime handlers for coordination-oriented query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_command_error,
    _print_payload,
    _task_dependency_payload,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import InitiativeIndexEntry
from watchtower_core.repo_ops.query import (
    CoordinationQueryService,
    CoordinationSearchParams,
    InitiativeQueryService,
    InitiativeSearchParams,
    TaskQueryService,
    TaskSearchParams,
    TraceabilityQueryService,
)


def _run_query_tasks(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    service = TaskQueryService(loader)
    entries = service.search(
        TaskSearchParams(
            query=args.query,
            task_ids=tuple(args.task_id),
            trace_id=args.trace_id,
            task_status=args.task_status,
            priority=args.priority,
            owner=args.owner,
            task_kind=args.task_kind,
            blocked_only=args.blocked_only,
            blocked_by_task_id=args.blocked_by,
            depends_on_task_id=args.depends_on,
            limit=args.limit,
        )
    )
    reverse_dependencies = {
        entry.task_id: service.reverse_dependencies(entry.task_id)
        for entry in entries
    }
    payload = {
        "command": "watchtower-core query tasks",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "task_id": entry.task_id,
                "trace_id": entry.trace_id,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "task_status": entry.task_status,
                "task_kind": entry.task_kind,
                "priority": entry.priority,
                "owner": entry.owner,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "blocked_by": list(entry.blocked_by),
                "depends_on": list(entry.depends_on),
                "related_ids": list(entry.related_ids),
                "applies_to": list(entry.applies_to),
                "github_repository": entry.github_repository,
                "github_issue_number": entry.github_issue_number,
                "github_issue_node_id": entry.github_issue_node_id,
                "github_project_owner": entry.github_project_owner,
                "github_project_owner_type": entry.github_project_owner_type,
                "github_project_number": entry.github_project_number,
                "github_project_item_id": entry.github_project_item_id,
                "github_synced_at": entry.github_synced_at,
                "tags": list(entry.tags),
                **(
                    {
                        "blocked_by_details": [
                            _task_dependency_payload(service.get(task_id))
                            for task_id in entry.blocked_by
                        ],
                        "depends_on_details": [
                            _task_dependency_payload(service.get(task_id))
                            for task_id in entry.depends_on
                        ],
                        "reverse_dependency_details": [
                            _task_dependency_payload(task)
                            for task in reverse_dependencies[entry.task_id]
                        ],
                    }
                    if args.include_dependency_details
                    else {}
                ),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No task entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} task entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.task_id} [{entry.task_status}, {entry.priority}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        if args.include_dependency_details:
            if entry.blocked_by:
                print(f"  Blocked by: {', '.join(entry.blocked_by)}")
            if entry.depends_on:
                print(f"  Depends on: {', '.join(entry.depends_on)}")
            reverse_links = reverse_dependencies[entry.task_id]
            if reverse_links:
                print(
                    "  Reverse dependencies: "
                    + ", ".join(task.task_id for task in reverse_links)
                )
    return 0


def _run_query_initiatives(args: argparse.Namespace) -> int:
    service = InitiativeQueryService(ControlPlaneLoader())
    entries = service.search(
        InitiativeSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            initiative_status=args.initiative_status,
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
        empty_message="No initiative entries matched the requested filters.",
        show_task_summaries=False,
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
    payload = {
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
    if args.initiative_status is None:
        payload["default_initiative_status"] = initiative_status
    if _print_payload(args, payload) == 0:
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


def _initiative_entry_payload(entry: InitiativeIndexEntry) -> dict[str, object]:
    return {
        "trace_id": entry.trace_id,
        "title": entry.title,
        "summary": entry.summary,
        "status": entry.status,
        "initiative_status": entry.initiative_status,
        "current_phase": entry.current_phase,
        "updated_at": entry.updated_at,
        "open_task_count": entry.open_task_count,
        "blocked_task_count": entry.blocked_task_count,
        "key_surface_path": entry.key_surface_path,
        "next_action": entry.next_action,
        "next_surface_path": entry.next_surface_path,
        "primary_owner": entry.primary_owner,
        "active_owners": list(entry.active_owners),
        "active_task_ids": list(entry.active_task_ids),
        "active_task_summaries": [
            {
                "task_id": task.task_id,
                "title": task.title,
                "task_status": task.task_status,
                "priority": task.priority,
                "owner": task.owner,
                "doc_path": task.doc_path,
                "is_actionable": task.is_actionable,
                "blocked_by": list(task.blocked_by),
                "depends_on": list(task.depends_on),
            }
            for task in entry.active_task_summaries
        ],
        "blocked_by_task_ids": list(entry.blocked_by_task_ids),
        "prd_ids": list(entry.prd_ids),
        "decision_ids": list(entry.decision_ids),
        "design_ids": list(entry.design_ids),
        "plan_ids": list(entry.plan_ids),
        "task_ids": list(entry.task_ids),
        "acceptance_ids": list(entry.acceptance_ids),
        "acceptance_contract_ids": list(entry.acceptance_contract_ids),
        "evidence_ids": list(entry.evidence_ids),
        "closed_at": entry.closed_at,
        "closure_reason": entry.closure_reason,
        "superseded_by_trace_id": entry.superseded_by_trace_id,
        "related_paths": list(entry.related_paths),
        "tags": list(entry.tags),
        "notes": entry.notes,
    }


def _emit_initiative_query_results(
    args: argparse.Namespace,
    *,
    command_name: str,
    entries: tuple[InitiativeIndexEntry, ...],
    empty_message: str,
    show_task_summaries: bool,
    default_initiative_status: str | None = None,
) -> int:
    payload = {
        "command": command_name,
        "status": "ok",
        "result_count": len(entries),
        "results": [_initiative_entry_payload(entry) for entry in entries],
    }
    if default_initiative_status is not None:
        payload["default_initiative_status"] = default_initiative_status
    if _print_payload(args, payload) == 0:
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


def _run_query_trace(args: argparse.Namespace) -> int:
    service = TraceabilityQueryService(ControlPlaneLoader())
    try:
        entry = service.get(args.trace_id)
    except KeyError:
        return _emit_command_error(
            args,
            "watchtower-core query trace",
            f"Unknown trace ID: {args.trace_id}",
        )

    payload = {
        "command": "watchtower-core query trace",
        "status": "ok",
        "result": {
            "trace_id": entry.trace_id,
            "title": entry.title,
            "summary": entry.summary,
            "status": entry.status,
            "initiative_status": entry.initiative_status,
            "updated_at": entry.updated_at,
            "closed_at": entry.closed_at,
            "closure_reason": entry.closure_reason,
            "superseded_by_trace_id": entry.superseded_by_trace_id,
            "prd_ids": list(entry.prd_ids),
            "decision_ids": list(entry.decision_ids),
            "design_ids": list(entry.design_ids),
            "plan_ids": list(entry.plan_ids),
            "task_ids": list(entry.task_ids),
            "requirement_ids": list(entry.requirement_ids),
            "acceptance_ids": list(entry.acceptance_ids),
            "acceptance_contract_ids": list(entry.acceptance_contract_ids),
            "validator_ids": list(entry.validator_ids),
            "evidence_ids": list(entry.evidence_ids),
            "related_paths": list(entry.related_paths),
            "tags": list(entry.tags),
            "notes": entry.notes,
        },
    }
    if _print_payload(args, payload) == 0:
        return 0

    print(f"{entry.trace_id}: {entry.title}")
    print(entry.summary)
    print(f"Initiative Status: {entry.initiative_status}")
    if entry.closed_at is not None:
        print(f"Closed At: {entry.closed_at}")
    if entry.closure_reason is not None:
        print(f"Closure Reason: {entry.closure_reason}")
    if entry.superseded_by_trace_id is not None:
        print(f"Superseded By: {entry.superseded_by_trace_id}")
    if entry.prd_ids:
        print(f"PRDs: {', '.join(entry.prd_ids)}")
    if entry.decision_ids:
        print(f"Decisions: {', '.join(entry.decision_ids)}")
    if entry.design_ids:
        print(f"Designs: {', '.join(entry.design_ids)}")
    if entry.plan_ids:
        print(f"Plans: {', '.join(entry.plan_ids)}")
    if entry.task_ids:
        print(f"Tasks: {', '.join(entry.task_ids)}")
    if entry.acceptance_contract_ids:
        print(f"Acceptance Contracts: {', '.join(entry.acceptance_contract_ids)}")
    if entry.evidence_ids:
        print(f"Evidence: {', '.join(entry.evidence_ids)}")
    return 0
