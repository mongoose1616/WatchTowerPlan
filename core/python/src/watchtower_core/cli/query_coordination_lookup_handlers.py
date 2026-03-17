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
from watchtower_core.repo_ops.project_context import load_project_context
from watchtower_core.repo_ops.query import (
    AuthorityMapQueryService,
    AuthorityMapSearchParams,
    DiscrepancyQueryService,
    DiscrepancySearchParams,
    ProjectQueryService,
    ProjectSearchParams,
    ReadinessQueryService,
    ReadinessSearchParams,
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
            _task_entry_payload(
                entry,
                service=service,
                reverse_dependencies=reverse_dependencies,
                include_dependency_details=args.include_dependency_details,
            )
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
        task_status = getattr(entry, "status", getattr(entry, "task_status", "unknown"))
        print(f"- {entry.task_id} [{task_status}, {entry.priority}]")
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


def _run_query_readiness(args: argparse.Namespace) -> int:
    service = ReadinessQueryService(ControlPlaneLoader())
    ready_for_execution = (
        None
        if args.ready_for_execution is None
        else args.ready_for_execution == "true"
    )
    entries = service.search(
        ReadinessSearchParams(
            query=args.query,
            initiative_id=args.initiative_id,
            project_id=args.project_id,
            trace_id=args.trace_id,
            lifecycle_stage=args.lifecycle_stage,
            review_status=args.review_status,
            ready_for_execution=ready_for_execution,
            blocked_only=args.blocked_only,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query readiness",
        "status": "ok",
        "result_count": len(entries),
        "results": [_readiness_entry_payload(entry) for entry in entries],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No readiness entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} readiness entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        readiness_state = "ready" if entry.ready_for_execution else "not_ready"
        print(
            f"- {entry.trace_id} [{entry.lifecycle_stage}, {entry.review_status}, {readiness_state}]"
        )
        print(f"  {entry.title}")
        if entry.project_id is not None:
            print(f"  Project: {entry.project_id}")
        print(
            "  Capture/Machine/Approval: "
            f"{'complete' if entry.capture_complete else 'incomplete'}, "
            f"{'valid' if entry.machine_valid else 'invalid'}, "
            f"{entry.approval_status}"
        )
        if entry.blocking_reasons:
            print(f"  Blocking reasons: {', '.join(entry.blocking_reasons)}")
        print(f"  Root: {entry.initiative_root}")
    return 0


def _run_query_discrepancies(args: argparse.Namespace) -> int:
    service = DiscrepancyQueryService(ControlPlaneLoader())
    entries = service.search(
        DiscrepancySearchParams(
            query=args.query,
            initiative_id=args.initiative_id,
            project_id=args.project_id,
            trace_id=args.trace_id,
            category=args.category,
            severity=args.severity,
            status=args.status,
            blocking_only=args.blocking_only,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query discrepancies",
        "status": "ok",
        "result_count": len(entries),
        "results": [_discrepancy_entry_payload(entry) for entry in entries],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No discrepancy entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} discrepancy entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(
            f"- {entry.discrepancy_id} "
            f"[{entry.severity}, {entry.gate_effect}, {entry.status}]"
        )
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(f"  Category: {entry.category}")
        if entry.source_paths:
            print(f"  Sources: {', '.join(entry.source_paths)}")
    return 0


def _run_query_projects(args: argparse.Namespace) -> int:
    service = ProjectQueryService(ControlPlaneLoader())
    entries = service.search(
        ProjectSearchParams(
            query=args.query,
            project_id=args.project_id,
            slug=args.slug,
            status=args.status,
            repository_role=args.repository_role,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query projects",
        "status": "ok",
        "result_count": len(entries),
        "results": [_project_entry_payload(entry) for entry in entries],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No project entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} project entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.project_id} [{entry.status}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Initiatives: "
            f"active={entry.active_initiative_count} blocked={entry.blocked_initiative_count}"
        )
        print(
            "  Repositories: "
            f"{entry.repository_count} via {', '.join(entry.linked_repository_roles)}"
        )
        print(f"  Root: {entry.project_root}")
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


def _run_query_project_context(args: argparse.Namespace) -> int:
    try:
        context = load_project_context(ControlPlaneLoader(), args.project_slug)
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core query project-context",
            str(exc),
        )

    payload = {
        "command": "watchtower-core query project-context",
        "status": "ok",
        "result": {
            "pack_context": {
                "pack_id": context.pack_context.pack_settings.pack_id,
                "pack_settings_path": context.pack_context.pack_settings_path,
            },
            "project_id": context.project_id,
            "slug": context.slug,
            "title": context.title,
            "summary": context.summary,
            "status": context.status,
            "project_root": context.project_root,
            "initiative_root": context.initiative_root,
            "repository_links": [
                {
                    "repository_id": link.repository_id,
                    "repository_role": link.repository_role,
                    "repository_locator": link.repository_locator,
                    "repository_kind": link.repository_kind,
                    "owner": link.owner,
                    "access": link.access,
                    "active": link.active,
                }
                for link in context.repository_links
            ],
        },
    }
    if _print_payload(args, payload) == 0:
        return 0

    print(f"{context.project_id}: {context.title} [{context.status}]")
    print(context.summary)
    print(
        "Pack Context: "
        f"{context.pack_context.pack_settings.pack_id} via "
        f"{context.pack_context.pack_settings_path}"
    )
    print(f"Project Root: {context.project_root}")
    print(f"Initiative Root: {context.initiative_root}")
    if context.repository_links:
        print("Repositories:")
        for link in context.repository_links:
            state = "active" if link.active else "inactive"
            print(
                "- "
                f"{link.repository_role}: {link.repository_locator} "
                f"[{link.repository_kind}, {state}]"
            )
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


def _task_entry_payload(
    entry: object,
    *,
    service: TaskQueryService,
    reverse_dependencies: dict[str, tuple[object, ...]],
    include_dependency_details: bool,
) -> dict[str, object]:
    status = getattr(entry, "status", getattr(entry, "task_status", None))
    payload: dict[str, object] = {
        "task_id": entry.task_id,
        "initiative_id": getattr(entry, "initiative_id", None),
        "project_id": getattr(entry, "project_id", None),
        "trace_id": entry.trace_id,
        "initiative_title": getattr(entry, "initiative_title", None),
        "title": entry.title,
        "summary": entry.summary,
        "status": status,
        "task_status": status,
        "task_kind": getattr(entry, "task_kind", None),
        "priority": entry.priority,
        "owner": entry.owner,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
        "blocked_by": list(getattr(entry, "blocked_by", ())),
        "depends_on": list(getattr(entry, "depends_on", ())),
        "related_ids": list(getattr(entry, "related_ids", ())),
    }
    if include_dependency_details:
        payload["blocked_by_details"] = [
            _task_dependency_payload(service.get(task_id))
            for task_id in getattr(entry, "blocked_by", ())
        ]
        payload["depends_on_details"] = [
            _task_dependency_payload(service.get(task_id))
            for task_id in getattr(entry, "depends_on", ())
        ]
        payload["reverse_dependency_details"] = [
            _task_dependency_payload(task)
            for task in reverse_dependencies.get(entry.task_id, ())
        ]
    return {key: value for key, value in payload.items() if value is not None}


def _readiness_entry_payload(entry: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "initiative_id": entry.initiative_id,
        "project_id": entry.project_id,
        "trace_id": entry.trace_id,
        "title": entry.title,
        "initiative_root": entry.initiative_root,
        "scope_type": entry.scope_type,
        "lifecycle_stage": entry.lifecycle_stage,
        "review_status": entry.review_status,
        "capture_complete": entry.capture_complete,
        "machine_valid": entry.machine_valid,
        "approval_status": entry.approval_status,
        "ready_for_execution": entry.ready_for_execution,
        "blocking_reasons": list(entry.blocking_reasons),
        "updated_at": entry.updated_at,
    }
    return {key: value for key, value in payload.items() if value is not None}


def _discrepancy_entry_payload(entry: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "discrepancy_id": entry.discrepancy_id,
        "initiative_id": entry.initiative_id,
        "project_id": entry.project_id,
        "trace_id": entry.trace_id,
        "title": entry.title,
        "category": entry.category,
        "severity": entry.severity,
        "gate_effect": entry.gate_effect,
        "status": entry.status,
        "summary": entry.summary,
        "source_paths": list(entry.source_paths),
        "updated_at": entry.updated_at,
    }
    return {key: value for key, value in payload.items() if value is not None}


def _project_entry_payload(entry: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "project_id": entry.project_id,
        "slug": entry.slug,
        "title": entry.title,
        "summary": entry.summary,
        "status": entry.status,
        "project_root": entry.project_root,
        "initiative_root": entry.initiative_root,
        "repository_count": entry.repository_count,
        "active_initiative_count": entry.active_initiative_count,
        "blocked_initiative_count": entry.blocked_initiative_count,
        "linked_repository_roles": list(entry.linked_repository_roles),
        "repository_locators": list(entry.repository_locators),
        "updated_at": entry.updated_at,
    }
    return {key: value for key, value in payload.items() if value is not None}
