"""Runtime handlers for knowledge-oriented query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _print_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query import (
    FoundationQueryService,
    FoundationSearchParams,
    ReferenceQueryService,
    ReferenceSearchParams,
    StandardQueryService,
    StandardSearchParams,
    WorkflowQueryService,
    WorkflowSearchParams,
)


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
            repository_status=args.repository_status,
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
                "repository_status": entry.repository_status,
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
        print(f"- {entry.reference_id} [{entry.status}, {entry.repository_status}]")
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
            owner=args.owner,
            tag=args.tag,
            applies_to=args.applies_to,
            related_path=args.related_path,
            reference_path=args.reference_path,
            operationalization_mode=args.operationalization_mode,
            operationalization_path=args.operationalization_path,
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
                "owner": entry.owner,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "uses_internal_references": entry.uses_internal_references,
                "uses_external_references": entry.uses_external_references,
                "applies_to": list(entry.applies_to),
                "related_paths": list(entry.related_paths),
                "reference_doc_paths": list(entry.reference_doc_paths),
                "internal_reference_paths": list(entry.internal_reference_paths),
                "applied_reference_paths": list(entry.applied_reference_paths),
                "external_reference_urls": list(entry.external_reference_urls),
                "applied_external_reference_urls": list(
                    entry.applied_external_reference_urls
                ),
                "operationalization_modes": list(entry.operationalization_modes),
                "operationalization_paths": list(entry.operationalization_paths),
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
        print(f"- {entry.standard_id} [{entry.category}, owner={entry.owner}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        print(
            "  Operationalization: "
            + ", ".join(entry.operationalization_modes)
            + f" across {len(entry.operationalization_paths)} surface(s)"
        )
    return 0
