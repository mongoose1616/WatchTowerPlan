"""Runtime handlers for authority, task, and trace query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_command_error,
    _print_payload,
    _task_dependency_payload,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import AuthorityMapEntry
from watchtower_core.repo_ops.query import (
    AuthorityMapQueryService,
    AuthorityMapSearchParams,
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
