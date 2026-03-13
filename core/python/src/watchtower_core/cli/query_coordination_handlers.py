"""Runtime handlers for coordination-oriented query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_command_error,
    _print_payload,
    _print_payload_factory,
    _task_dependency_payload,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    AuthorityMapEntry,
    InitiativeIndexEntry,
    PlanningCatalogEntry,
)
from watchtower_core.repo_ops.planning_projection_serialization import (
    serialize_initiative_entry,
    serialize_planning_catalog_entry,
)
from watchtower_core.repo_ops.query import (
    AuthorityMapQueryService,
    AuthorityMapSearchParams,
    CoordinationQueryResult,
    CoordinationQueryService,
    CoordinationSearchParams,
    InitiativeQueryService,
    InitiativeSearchParams,
    PlanningCatalogQueryService,
    PlanningCatalogSearchParams,
    TaskQueryService,
    TaskSearchParams,
    TraceabilityQueryService,
)


def _run_query_authority(args: argparse.Namespace) -> int:
    service = AuthorityMapQueryService(ControlPlaneLoader())
    entries = service.search(
        AuthorityMapSearchParams(
            query=args.query,
            question_id=args.question_id,
            domain=args.domain,
            artifact_kind=args.artifact_kind,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query authority",
        "status": "ok",
        "result_count": len(entries),
        "results": [_authority_entry_payload(entry) for entry in entries],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No authority-map entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} authority entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.question_id} [{entry.domain} -> {entry.artifact_kind}]")
        print(f"  {entry.question}")
        print(f"  Canonical: {entry.canonical_path}")
        print(f"  Command: {entry.preferred_command}")
        if entry.preferred_human_path is not None:
            print(f"  Human: {entry.preferred_human_path}")
        if entry.status_fields:
            print(f"  Status fields: {', '.join(entry.status_fields)}")
    return 0


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
    reverse_dependencies = (
        service.reverse_dependencies_for(tuple(entry.task_id for entry in entries))
        if args.include_dependency_details
        else {}
    )
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
                            for task in reverse_dependencies.get(entry.task_id, ())
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
            reverse_links = reverse_dependencies.get(entry.task_id, ())
            if reverse_links:
                print(
                    "  Reverse dependencies: "
                    + ", ".join(task.task_id for task in reverse_links)
                )
    return 0


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


def _authority_entry_payload(entry: AuthorityMapEntry) -> dict[str, object]:
    return {
        "question_id": entry.question_id,
        "domain": entry.domain,
        "question": entry.question,
        "status": entry.status,
        "artifact_kind": entry.artifact_kind,
        "canonical_path": entry.canonical_path,
        "preferred_command": entry.preferred_command,
        "preferred_human_path": entry.preferred_human_path,
        "status_fields": list(entry.status_fields),
        "fallback_paths": list(entry.fallback_paths),
        "aliases": list(entry.aliases),
        "notes": entry.notes,
    }


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
