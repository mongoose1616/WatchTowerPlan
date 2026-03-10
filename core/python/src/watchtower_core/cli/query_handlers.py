"""Runtime handlers for query command families."""

from __future__ import annotations

import argparse
import json

from watchtower_core.cli.handler_common import _print_payload, _task_dependency_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import InitiativeIndexEntry
from watchtower_core.repo_ops.query import (
    AcceptanceContractQueryService,
    AcceptanceContractSearchParams,
    CommandQueryService,
    CommandSearchParams,
    CoordinationQueryService,
    CoordinationSearchParams,
    DecisionQueryService,
    DecisionSearchParams,
    DesignDocumentQueryService,
    DesignDocumentSearchParams,
    FoundationQueryService,
    FoundationSearchParams,
    InitiativeQueryService,
    InitiativeSearchParams,
    PrdQueryService,
    PrdSearchParams,
    ReferenceQueryService,
    ReferenceSearchParams,
    RepositoryPathQueryService,
    RepositoryPathSearchParams,
    StandardQueryService,
    StandardSearchParams,
    TaskQueryService,
    TaskSearchParams,
    TraceabilityQueryService,
    ValidationEvidenceQueryService,
    ValidationEvidenceSearchParams,
    WorkflowQueryService,
    WorkflowSearchParams,
)


def _run_query_paths(args: argparse.Namespace) -> int:
    service = RepositoryPathQueryService(ControlPlaneLoader())
    entries = service.search(
        RepositoryPathSearchParams(
            query=args.query,
            surface_kind=args.surface_kind,
            maturity=args.maturity,
            priority=args.priority,
            audience_hint=args.audience_hint,
            tag=args.tag,
            parent_path=args.parent_path,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query paths",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "path": entry.path,
                "kind": entry.kind,
                "surface_kind": entry.surface_kind,
                "summary": entry.summary,
                "parent_path": entry.parent_path,
                "maturity": entry.maturity,
                "priority": entry.priority,
                "audience_hint": entry.audience_hint,
                "aliases": list(entry.aliases),
                "tags": list(entry.tags),
                "related_paths": list(entry.related_paths),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No repository path entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} repository path entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(
            f"- {entry.path} "
            f"[{entry.surface_kind}, {entry.maturity}, {entry.priority}, {entry.audience_hint}]"
        )
        print(f"  {entry.summary}")
    return 0


def _run_query_commands(args: argparse.Namespace) -> int:
    service = CommandQueryService(ControlPlaneLoader())
    entries = service.search(
        CommandSearchParams(
            query=args.query,
            kind=args.kind,
            tag=args.tag,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query commands",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "command_id": entry.command_id,
                "command": entry.command,
                "kind": entry.kind,
                "summary": entry.summary,
                "doc_path": entry.doc_path,
                "synopsis": entry.synopsis,
                "implementation_path": entry.implementation_path,
                "parent_command_id": entry.parent_command_id,
                "output_formats": list(entry.output_formats),
                "default_output_format": entry.default_output_format,
                "aliases": list(entry.aliases),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No command entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} command entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.command} [{entry.kind}]")
        print(f"  {entry.summary}")
    return 0


def _run_query_foundations(args: argparse.Namespace) -> int:
    service = FoundationQueryService(ControlPlaneLoader())
    entries = service.search(
        FoundationSearchParams(
            query=args.query,
            foundation_id=args.foundation_id,
            audience=args.audience,
            authority=args.authority,
            tag=args.tag,
            related_path=args.related_path,
            reference_path=args.reference_path,
            cited_by_path=args.cited_by_path,
            applied_by_path=args.applied_by_path,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query foundations",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "foundation_id": entry.foundation_id,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "audience": entry.audience,
                "authority": entry.authority,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "uses_internal_references": entry.uses_internal_references,
                "uses_external_references": entry.uses_external_references,
                "related_paths": list(entry.related_paths),
                "reference_doc_paths": list(entry.reference_doc_paths),
                "internal_reference_paths": list(entry.internal_reference_paths),
                "external_reference_urls": list(entry.external_reference_urls),
                "cited_by_paths": list(entry.cited_by_paths),
                "applied_by_paths": list(entry.applied_by_paths),
                "aliases": list(entry.aliases),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No foundation entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} foundation entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.foundation_id} [{entry.authority}, {entry.audience}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Usage: "
            f"cited_by={len(entry.cited_by_paths)}, applied_by={len(entry.applied_by_paths)}"
        )
    return 0


def _run_query_workflows(args: argparse.Namespace) -> int:
    service = WorkflowQueryService(ControlPlaneLoader())
    entries = service.search(
        WorkflowSearchParams(
            query=args.query,
            workflow_id=args.workflow_id,
            phase_type=args.phase_type,
            task_family=args.task_family,
            trigger_tag=args.trigger_tag,
            related_path=args.related_path,
            reference_path=args.reference_path,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query workflows",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "workflow_id": entry.workflow_id,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "doc_path": entry.doc_path,
                "phase_type": entry.phase_type,
                "task_family": entry.task_family,
                "uses_internal_references": entry.uses_internal_references,
                "uses_external_references": entry.uses_external_references,
                "primary_risks": list(entry.primary_risks),
                "trigger_tags": list(entry.trigger_tags),
                "companion_workflow_ids": list(entry.companion_workflow_ids),
                "related_paths": list(entry.related_paths),
                "reference_doc_paths": list(entry.reference_doc_paths),
                "internal_reference_paths": list(entry.internal_reference_paths),
                "external_reference_urls": list(entry.external_reference_urls),
                "aliases": list(entry.aliases),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No workflow entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} workflow entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.workflow_id} [{entry.status}, {entry.phase_type}, {entry.task_family}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Reference use: "
            f"internal={'yes' if entry.uses_internal_references else 'no'}, "
            f"external={'yes' if entry.uses_external_references else 'no'}"
        )
    return 0


def _run_query_references(args: argparse.Namespace) -> int:
    service = ReferenceQueryService(ControlPlaneLoader())
    entries = service.search(
        ReferenceSearchParams(
            query=args.query,
            reference_id=args.reference_id,
            tag=args.tag,
            related_path=args.related_path,
            upstream_url=args.upstream_url,
            cited_by_path=args.cited_by_path,
            applied_by_path=args.applied_by_path,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query references",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "reference_id": entry.reference_id,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "uses_internal_references": entry.uses_internal_references,
                "uses_external_references": entry.uses_external_references,
                "canonical_upstream_urls": list(entry.canonical_upstream_urls),
                "cited_by_paths": list(entry.cited_by_paths),
                "applied_by_paths": list(entry.applied_by_paths),
                "related_paths": list(entry.related_paths),
                "aliases": list(entry.aliases),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No reference entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} reference entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.reference_id} [{entry.status}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Reference use: "
            f"internal={'yes' if entry.uses_internal_references else 'no'}, "
            f"external={'yes' if entry.uses_external_references else 'no'}"
        )
        if entry.applied_by_paths:
            print(f"  Applied by {len(entry.applied_by_paths)} doc(s).")
        elif entry.cited_by_paths:
            print(f"  Cited by {len(entry.cited_by_paths)} doc(s).")
    return 0


def _run_query_standards(args: argparse.Namespace) -> int:
    service = StandardQueryService(ControlPlaneLoader())
    entries = service.search(
        StandardSearchParams(
            query=args.query,
            standard_id=args.standard_id,
            category=args.category,
            tag=args.tag,
            related_path=args.related_path,
            reference_path=args.reference_path,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query standards",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "standard_id": entry.standard_id,
                "category": entry.category,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "uses_internal_references": entry.uses_internal_references,
                "uses_external_references": entry.uses_external_references,
                "related_paths": list(entry.related_paths),
                "reference_doc_paths": list(entry.reference_doc_paths),
                "internal_reference_paths": list(entry.internal_reference_paths),
                "applied_reference_paths": list(entry.applied_reference_paths),
                "external_reference_urls": list(entry.external_reference_urls),
                "applied_external_reference_urls": list(
                    entry.applied_external_reference_urls
                ),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No standard entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} standard entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.standard_id} [{entry.category}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Reference use: "
            f"internal={'yes' if entry.uses_internal_references else 'no'}, "
            f"external={'yes' if entry.uses_external_references else 'no'}"
        )
    return 0


def _run_query_prds(args: argparse.Namespace) -> int:
    service = PrdQueryService(ControlPlaneLoader())
    entries = service.search(
        PrdSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            tag=args.tag,
            requirement_id=args.requirement_id,
            acceptance_id=args.acceptance_id,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query prds",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "trace_id": entry.trace_id,
                "prd_id": entry.prd_id,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "uses_internal_references": entry.uses_internal_references,
                "uses_external_references": entry.uses_external_references,
                "requirement_ids": list(entry.requirement_ids),
                "acceptance_ids": list(entry.acceptance_ids),
                "linked_decision_ids": list(entry.linked_decision_ids),
                "linked_design_ids": list(entry.linked_design_ids),
                "linked_plan_ids": list(entry.linked_plan_ids),
                "related_paths": list(entry.related_paths),
                "internal_reference_paths": list(entry.internal_reference_paths),
                "external_reference_urls": list(entry.external_reference_urls),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No PRD entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} PRD entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.prd_id} [{entry.status}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Reference use: "
            f"internal={'yes' if entry.uses_internal_references else 'no'}, "
            f"external={'yes' if entry.uses_external_references else 'no'}"
        )
    return 0


def _run_query_decisions(args: argparse.Namespace) -> int:
    service = DecisionQueryService(ControlPlaneLoader())
    entries = service.search(
        DecisionSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            decision_status=args.decision_status,
            tag=args.tag,
            linked_prd_id=args.linked_prd_id,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query decisions",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "trace_id": entry.trace_id,
                "decision_id": entry.decision_id,
                "title": entry.title,
                "summary": entry.summary,
                "record_status": entry.record_status,
                "decision_status": entry.decision_status,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "uses_internal_references": entry.uses_internal_references,
                "uses_external_references": entry.uses_external_references,
                "linked_prd_ids": list(entry.linked_prd_ids),
                "linked_design_ids": list(entry.linked_design_ids),
                "linked_plan_ids": list(entry.linked_plan_ids),
                "related_paths": list(entry.related_paths),
                "internal_reference_paths": list(entry.internal_reference_paths),
                "external_reference_urls": list(entry.external_reference_urls),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No decision entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} decision entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.decision_id} [{entry.decision_status}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Reference use: "
            f"internal={'yes' if entry.uses_internal_references else 'no'}, "
            f"external={'yes' if entry.uses_external_references else 'no'}"
        )
    return 0


def _run_query_designs(args: argparse.Namespace) -> int:
    service = DesignDocumentQueryService(ControlPlaneLoader())
    entries = service.search(
        DesignDocumentSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            family=args.family,
            tag=args.tag,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query designs",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "document_id": entry.document_id,
                "trace_id": entry.trace_id,
                "family": entry.family,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "uses_internal_references": entry.uses_internal_references,
                "uses_external_references": entry.uses_external_references,
                "source_paths": list(entry.source_paths),
                "related_paths": list(entry.related_paths),
                "internal_reference_paths": list(entry.internal_reference_paths),
                "external_reference_urls": list(entry.external_reference_urls),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No design-document entries matched the requested filters.")
        return 0

    print(
        f"Found {len(entries)} design-document entr"
        f"{'y' if len(entries) == 1 else 'ies'}:"
    )
    for entry in entries:
        print(f"- {entry.document_id} [{entry.family}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Reference use: "
            f"internal={'yes' if entry.uses_internal_references else 'no'}, "
            f"external={'yes' if entry.uses_external_references else 'no'}"
        )
    return 0


def _run_query_acceptance(args: argparse.Namespace) -> int:
    service = AcceptanceContractQueryService(ControlPlaneLoader())
    entries = service.search(
        AcceptanceContractSearchParams(
            trace_id=args.trace_id,
            source_prd_id=args.source_prd_id,
            acceptance_id=args.acceptance_id,
        )
    )
    payload = {
        "command": "watchtower-core query acceptance",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "contract_id": entry.contract_id,
                "title": entry.title,
                "status": entry.status,
                "trace_id": entry.trace_id,
                "source_prd_id": entry.source_prd_id,
                "doc_path": entry.doc_path,
                "acceptance_ids": [item.acceptance_id for item in entry.entries],
                "required_validator_ids": sorted(
                    {
                        validator_id
                        for item in entry.entries
                        for validator_id in item.required_validator_ids
                    }
                ),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No acceptance contracts matched the requested filters.")
        return 0

    print(
        f"Found {len(entries)} acceptance contract entr"
        f"{'y' if len(entries) == 1 else 'ies'}:"
    )
    for entry in entries:
        print(f"- {entry.contract_id} [{entry.status}]")
        print(f"  Trace: {entry.trace_id}")
        print(f"  Source PRD: {entry.source_prd_id}")
        print(f"  Acceptance IDs: {', '.join(item.acceptance_id for item in entry.entries)}")
    return 0


def _run_query_evidence(args: argparse.Namespace) -> int:
    service = ValidationEvidenceQueryService(ControlPlaneLoader())
    entries = service.search(
        ValidationEvidenceSearchParams(
            trace_id=args.trace_id,
            overall_result=args.result,
            acceptance_id=args.acceptance_id,
            validator_id=args.validator_id,
        )
    )
    payload = {
        "command": "watchtower-core query evidence",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "evidence_id": entry.evidence_id,
                "title": entry.title,
                "status": entry.status,
                "trace_id": entry.trace_id,
                "overall_result": entry.overall_result,
                "recorded_at": entry.recorded_at,
                "doc_path": entry.doc_path,
                "source_prd_ids": list(entry.source_prd_ids),
                "source_acceptance_contract_ids": list(entry.source_acceptance_contract_ids),
                "check_count": len(entry.checks),
                "acceptance_ids": sorted(
                    {
                        acceptance_id
                        for check in entry.checks
                        for acceptance_id in check.acceptance_ids
                    }
                ),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No validation-evidence artifacts matched the requested filters.")
        return 0

    print(
        f"Found {len(entries)} validation-evidence artifact entr"
        f"{'y' if len(entries) == 1 else 'ies'}:"
    )
    for entry in entries:
        print(f"- {entry.evidence_id} [{entry.overall_result}]")
        print(f"  Trace: {entry.trace_id}")
        print(f"  Recorded At: {entry.recorded_at}")
        print(f"  Checks: {len(entry.checks)}")
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
                print(
                    f"- {entry.trace_id} [{entry.initiative_status}] "
                    f"{entry.closed_at}"
                )
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
        if args.format == "json":
            print(
                json.dumps(
                    {
                        "command": "watchtower-core query trace",
                        "status": "error",
                        "message": f"Unknown trace ID: {args.trace_id}",
                    },
                    sort_keys=True,
                )
            )
            return 1
        print(f"Unknown trace ID: {args.trace_id}")
        return 1

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
