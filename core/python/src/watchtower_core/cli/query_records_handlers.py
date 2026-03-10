"""Runtime handlers for planning-record query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _print_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query import (
    AcceptanceContractQueryService,
    AcceptanceContractSearchParams,
    DecisionQueryService,
    DecisionSearchParams,
    DesignDocumentQueryService,
    DesignDocumentSearchParams,
    PrdQueryService,
    PrdSearchParams,
    ValidationEvidenceQueryService,
    ValidationEvidenceSearchParams,
)


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
