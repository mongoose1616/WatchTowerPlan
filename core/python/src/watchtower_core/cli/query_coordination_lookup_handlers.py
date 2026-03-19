"""Runtime handlers for authority, task, and trace query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_collection_query_results,
    _emit_command_error,
    _emit_detail_result,
    _parse_optional_bool_arg,
    _run_value_error_operation,
    _task_dependency_payload,
    _task_filter_kwargs,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ArtifactIndexEntry, AuthorityMapEntry
from watchtower_core.repo_ops.project_context import load_project_context
from watchtower_core.repo_ops.query import (
    ArtifactQueryService,
    ArtifactSearchParams,
    AuthorityMapQueryService,
    AuthorityMapSearchParams,
    DiscrepancyQueryService,
    DiscrepancySearchParams,
    PlanCloseoutQueryService,
    PlanCloseoutSearchParams,
    PlanEvidenceQueryService,
    PlanEvidenceSearchParams,
    PlanReviewQueryService,
    PlanReviewSearchParams,
    ProjectQueryService,
    ProjectSearchParams,
    ReadinessQueryService,
    ReadinessSearchParams,
    TaskQueryService,
    TaskSearchParams,
    TraceabilityQueryService,
)


def _without_none_values(payload: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in payload.items() if value is not None}


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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query authority",
        entries=entries,
        noun="authority",
        empty_message="No authority-map entries matched the requested filters.",
        payload_results_factory=lambda: [_authority_entry_payload(entry) for entry in entries],
        render_entry=_print_authority_entry,
    )


def _run_query_artifacts(args: argparse.Namespace) -> int:
    service = ArtifactQueryService(ControlPlaneLoader())
    entries = service.search(
        ArtifactSearchParams(
            query=args.query,
            artifact_id=args.artifact_id,
            artifact_family=args.artifact_family,
            context_id=args.context_id,
            source_context=args.source_context,
            source_channel=args.source_channel,
            status=args.status,
            authoritative=_parse_optional_bool_arg(args.authoritative),
            derived=_parse_optional_bool_arg(args.derived),
            hidden=_parse_optional_bool_arg(args.hidden),
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query artifacts",
        entries=entries,
        noun="artifact",
        empty_message="No artifact entries matched the requested filters.",
        payload_results_factory=lambda: [_artifact_entry_payload(entry) for entry in entries],
        render_entry=_print_artifact_entry,
    )


def _run_query_tasks(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    service = TaskQueryService(loader)
    entries = service.search(
        TaskSearchParams(
            query=args.query,
            **_task_filter_kwargs(args),
            limit=args.limit,
        )
    )
    reverse_dependencies = (
        service.reverse_dependencies_for(tuple(entry.task_id for entry in entries))
        if args.include_dependency_details
        else {}
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query tasks",
        entries=entries,
        noun="task",
        empty_message="No task entries matched the requested filters.",
        payload_results_factory=lambda: [
            _task_entry_payload(
                entry,
                service=service,
                reverse_dependencies=reverse_dependencies,
                include_dependency_details=args.include_dependency_details,
            )
            for entry in entries
        ],
        render_entry=lambda entry: _print_task_entry(
            entry,
            include_dependency_details=args.include_dependency_details,
            reverse_dependencies=reverse_dependencies,
        ),
    )


def _run_query_readiness(args: argparse.Namespace) -> int:
    service = ReadinessQueryService(ControlPlaneLoader())
    ready_for_execution = _parse_optional_bool_arg(args.ready_for_execution)
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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query readiness",
        entries=entries,
        noun="readiness",
        empty_message="No readiness entries matched the requested filters.",
        payload_results_factory=lambda: [_readiness_entry_payload(entry) for entry in entries],
        render_entry=_print_readiness_entry,
    )


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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query discrepancies",
        entries=entries,
        noun="discrepancy",
        empty_message="No discrepancy entries matched the requested filters.",
        payload_results_factory=lambda: [_discrepancy_entry_payload(entry) for entry in entries],
        render_entry=_print_discrepancy_entry,
    )


def _run_query_plan_evidence(args: argparse.Namespace) -> int:
    service = PlanEvidenceQueryService(ControlPlaneLoader())
    entries = service.search(
        PlanEvidenceSearchParams(
            query=args.query,
            initiative_id=args.initiative_id,
            project_id=args.project_id,
            trace_id=args.trace_id,
            status=args.status,
            owner=args.owner,
            target_phase=args.target_phase,
            validation_type=args.validation_type,
            acceptance_label=args.acceptance_label,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query plan-evidence",
        entries=entries,
        noun="plan evidence",
        empty_message="No plan evidence entries matched the requested filters.",
        payload_results_factory=lambda: [_plan_evidence_entry_payload(entry) for entry in entries],
        render_entry=_print_plan_evidence_entry,
    )


def _run_query_closeouts(args: argparse.Namespace) -> int:
    service = PlanCloseoutQueryService(ControlPlaneLoader())
    promotion_review_required = _parse_optional_bool_arg(args.promotion_review_required)
    entries = service.search(
        PlanCloseoutSearchParams(
            query=args.query,
            initiative_id=args.initiative_id,
            project_id=args.project_id,
            trace_id=args.trace_id,
            status=args.status,
            terminal_state=args.terminal_state,
            promotion_review_required=promotion_review_required,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query closeouts",
        entries=entries,
        noun="closeout",
        empty_message="No closeout entries matched the requested filters.",
        payload_results_factory=lambda: [_closeout_entry_payload(entry) for entry in entries],
        render_entry=_print_closeout_entry,
    )


def _run_query_reviews(args: argparse.Namespace) -> int:
    service = PlanReviewQueryService(ControlPlaneLoader())
    ready_for_execution = _parse_optional_bool_arg(args.ready_for_execution)
    entries = service.search(
        PlanReviewSearchParams(
            query=args.query,
            subject_kind=args.subject_kind,
            initiative_id=args.initiative_id,
            project_id=args.project_id,
            trace_id=args.trace_id,
            review_state=args.review_state,
            ready_for_execution=ready_for_execution,
            review_ref=args.review_ref,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query reviews",
        entries=entries,
        noun="review",
        empty_message="No review entries matched the requested filters.",
        payload_results_factory=lambda: [_review_entry_payload(entry) for entry in entries],
        render_entry=_print_review_entry,
    )


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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query projects",
        entries=entries,
        noun="project",
        empty_message="No project entries matched the requested filters.",
        payload_results_factory=lambda: [_project_entry_payload(entry) for entry in entries],
        render_entry=_print_project_entry,
    )


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
    def _render_human() -> None:
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

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _run_query_project_context(args: argparse.Namespace) -> int:
    context = _run_value_error_operation(
        args,
        command_name="watchtower-core query project-context",
        operation=lambda: load_project_context(ControlPlaneLoader(), args.project_slug),
    )
    if context is None:
        return 1

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
    def _render_human() -> None:
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

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


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


def _print_authority_entry(entry: AuthorityMapEntry) -> None:
    print(f"- {entry.question_id} [{entry.domain} -> {entry.artifact_kind}]")
    print(f"  {entry.question}")
    print(f"  Canonical: {entry.canonical_path}")
    print(f"  Command: {entry.preferred_command}")
    if entry.preferred_human_path is not None:
        print(f"  Human: {entry.preferred_human_path}")
    if entry.status_fields:
        print(f"  Status fields: {', '.join(entry.status_fields)}")


def _print_artifact_entry(entry: ArtifactIndexEntry) -> None:
    print(f"- {entry.artifact_id} [{entry.artifact_family}, {entry.status}]")
    if entry.title is not None:
        print(f"  {entry.title}")
    if entry.summary is not None:
        print(f"  {entry.summary}")
    print(f"  Path: {entry.path}")
    if entry.context_ids:
        print(f"  Context IDs: {', '.join(entry.context_ids)}")
    if entry.source_context is not None or entry.source_channel is not None:
        print(f"  Source: {entry.source_context or '-'} / {entry.source_channel or '-'}")
    print(
        "  Authority: "
        f"authoritative={entry.authoritative} derived={entry.derived} hidden={entry.hidden}"
    )


def _task_entry_payload(
    entry: object,
    *,
    service: TaskQueryService,
    reverse_dependencies: dict[str, tuple[object, ...]],
    include_dependency_details: bool,
) -> dict[str, object]:
    artifact_status = getattr(entry, "status", None)
    task_status = getattr(entry, "task_status", artifact_status)
    payload: dict[str, object] = {
        "task_id": entry.task_id,
        "initiative_id": getattr(entry, "initiative_id", None),
        "project_id": getattr(entry, "project_id", None),
        "trace_id": entry.trace_id,
        "initiative_title": getattr(entry, "initiative_title", None),
        "title": entry.title,
        "summary": entry.summary,
        "status": artifact_status,
        "task_status": task_status,
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
    return _without_none_values(payload)


def _print_task_entry(
    entry: object,
    *,
    include_dependency_details: bool,
    reverse_dependencies: dict[str, tuple[object, ...]],
) -> None:
    task_status = getattr(entry, "task_status", getattr(entry, "status", "unknown"))
    print(f"- {entry.task_id} [{task_status}, {entry.priority}]")
    print(f"  {entry.title}")
    print(f"  {entry.summary}")
    if include_dependency_details:
        if entry.blocked_by:
            print(f"  Blocked by: {', '.join(entry.blocked_by)}")
        if entry.depends_on:
            print(f"  Depends on: {', '.join(entry.depends_on)}")
        reverse_links = reverse_dependencies.get(entry.task_id, ())
        if reverse_links:
            print("  Reverse dependencies: " + ", ".join(task.task_id for task in reverse_links))


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
    return _without_none_values(payload)


def _print_readiness_entry(entry: object) -> None:
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
    return _without_none_values(payload)


def _print_discrepancy_entry(entry: object) -> None:
    print(f"- {entry.discrepancy_id} [{entry.severity}, {entry.gate_effect}, {entry.status}]")
    print(f"  {entry.title}")
    print(f"  {entry.summary}")
    print(f"  Category: {entry.category}")
    if entry.source_paths:
        print(f"  Sources: {', '.join(entry.source_paths)}")


def _plan_evidence_entry_payload(entry: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "evidence_id": entry.evidence_id,
        "initiative_id": entry.initiative_id,
        "project_id": entry.project_id,
        "trace_id": entry.trace_id,
        "initiative_title": entry.initiative_title,
        "title": entry.title,
        "status": entry.status,
        "initiative_root": entry.initiative_root,
        "entry_count": entry.entry_count,
        "acceptance_labels": list(entry.acceptance_labels),
        "validation_types": list(entry.validation_types),
        "owners": list(entry.owners),
        "target_phases": list(entry.target_phases),
        "expected_output_paths": list(entry.expected_output_paths),
        "updated_at": entry.updated_at,
    }
    return _without_none_values(payload)


def _print_plan_evidence_entry(entry: object) -> None:
    print(f"- {entry.evidence_id} [{entry.status}, {entry.entry_count} checks]")
    print(f"  {entry.initiative_title}")
    print(f"  Validation types: {', '.join(entry.validation_types)}")
    print(f"  Owners: {', '.join(entry.owners)}")
    print(f"  Target phases: {', '.join(entry.target_phases)}")


def _closeout_entry_payload(entry: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "closeout_id": entry.closeout_id,
        "initiative_id": entry.initiative_id,
        "project_id": entry.project_id,
        "trace_id": entry.trace_id,
        "initiative_title": entry.initiative_title,
        "title": entry.title,
        "status": entry.status,
        "initiative_root": entry.initiative_root,
        "expected_outcome": entry.expected_outcome,
        "acceptance_ids": list(entry.acceptance_ids),
        "evidence_ids": list(entry.evidence_ids),
        "follow_up_handling": entry.follow_up_handling,
        "promotion_review_required": entry.promotion_review_required,
        "terminal_state_options": list(entry.terminal_state_options),
        "terminal_state": entry.terminal_state,
        "updated_at": entry.updated_at,
    }
    return _without_none_values(payload)


def _print_closeout_entry(entry: object) -> None:
    terminal_state = entry.terminal_state or "-"
    print(f"- {entry.closeout_id} [{entry.status}, terminal={terminal_state}]")
    print(f"  {entry.initiative_title}")
    print(f"  Expected outcome: {entry.expected_outcome}")
    print(
        "  Promotion review: "
        f"{'required' if entry.promotion_review_required else 'not required'}"
    )


def _review_entry_payload(entry: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "review_subject_id": entry.review_subject_id,
        "subject_kind": entry.subject_kind,
        "initiative_id": entry.initiative_id,
        "project_id": entry.project_id,
        "trace_id": entry.trace_id,
        "initiative_title": entry.initiative_title,
        "title": entry.title,
        "review_state": entry.review_state,
        "review_refs": list(entry.review_refs),
        "evidence_refs": list(entry.evidence_refs),
        "updated_at": entry.updated_at,
        "lifecycle_stage": entry.lifecycle_stage,
        "ready_for_execution": entry.ready_for_execution,
    }
    return _without_none_values(payload)


def _print_review_entry(entry: object) -> None:
    readiness = (
        "-"
        if entry.ready_for_execution is None
        else ("ready" if entry.ready_for_execution else "not_ready")
    )
    print(
        f"- {entry.review_subject_id} "
        f"[{entry.subject_kind}, {entry.review_state}, readiness={readiness}]"
    )
    print(f"  {entry.title}")
    if entry.review_refs:
        print(f"  Review refs: {', '.join(entry.review_refs)}")


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
    return _without_none_values(payload)


def _print_project_entry(entry: object) -> None:
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


def _artifact_entry_payload(entry: ArtifactIndexEntry) -> dict[str, object]:
    payload: dict[str, object] = {
        "artifact_id": entry.artifact_id,
        "artifact_family": entry.artifact_family,
        "path": entry.path,
        "pack": entry.pack,
        "status": entry.status,
        "authoritative": entry.authoritative,
        "hidden": entry.hidden,
        "derived": entry.derived,
        "created_at": entry.created_at,
        "updated_at": entry.updated_at,
        "context_ids": list(entry.context_ids),
        "related_artifact_ids": list(entry.related_artifact_ids),
    }
    if entry.subdomain is not None:
        payload["subdomain"] = entry.subdomain
    if entry.title is not None:
        payload["title"] = entry.title
    if entry.summary is not None:
        payload["summary"] = entry.summary
    if entry.parent_artifact_id is not None:
        payload["parent_artifact_id"] = entry.parent_artifact_id
    if entry.route_id is not None:
        payload["route_id"] = entry.route_id
    if entry.rendered_view_path is not None:
        payload["rendered_view_path"] = entry.rendered_view_path
    if entry.workflow_surface is not None:
        payload["workflow_surface"] = entry.workflow_surface
    if entry.review_status is not None:
        payload["review_status"] = entry.review_status
    if entry.source_context is not None:
        payload["source_context"] = entry.source_context
    if entry.source_channel is not None:
        payload["source_channel"] = entry.source_channel
    if entry.source_summary is not None:
        payload["source_summary"] = entry.source_summary
    if entry.source_url is not None:
        payload["source_url"] = entry.source_url
    if entry.source_ref is not None:
        payload["source_ref"] = entry.source_ref
    if entry.source_type is not None:
        payload["source_type"] = entry.source_type
    return payload
