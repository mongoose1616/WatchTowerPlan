"""Runtime handlers for planning-record query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_collection_query_results,
    _print_reference_usage_summary,
)
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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query prds",
        entries=entries,
        noun="PRD",
        empty_message="No PRD entries matched the requested filters.",
        payload_results_factory=lambda: [_prd_entry_payload(entry) for entry in entries],
        render_entry=_print_prd_entry,
    )


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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query decisions",
        entries=entries,
        noun="decision",
        empty_message="No decision entries matched the requested filters.",
        payload_results_factory=lambda: [_decision_entry_payload(entry) for entry in entries],
        render_entry=_print_decision_entry,
    )


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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query designs",
        entries=entries,
        noun="design-document",
        empty_message="No design-document entries matched the requested filters.",
        payload_results_factory=lambda: [_design_entry_payload(entry) for entry in entries],
        render_entry=_print_design_entry,
    )


def _run_query_acceptance(args: argparse.Namespace) -> int:
    service = AcceptanceContractQueryService(ControlPlaneLoader())
    entries = service.search(
        AcceptanceContractSearchParams(
            trace_id=args.trace_id,
            source_prd_id=args.source_prd_id,
            acceptance_id=args.acceptance_id,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query acceptance",
        entries=entries,
        noun="acceptance contract",
        empty_message="No acceptance contracts matched the requested filters.",
        payload_results_factory=lambda: [
            _acceptance_contract_entry_payload(entry) for entry in entries
        ],
        render_entry=_print_acceptance_contract_entry,
    )


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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query evidence",
        entries=entries,
        noun="validation-evidence artifact",
        empty_message="No validation-evidence artifacts matched the requested filters.",
        payload_results_factory=lambda: [_evidence_entry_payload(entry) for entry in entries],
        render_entry=_print_evidence_entry,
    )


def _prd_entry_payload(entry: object) -> dict[str, object]:
    return {
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


def _print_prd_entry(entry: object) -> None:
    _print_reference_usage_summary(
        header=f"- {entry.prd_id} [{entry.status}]",
        title=entry.title,
        summary=entry.summary,
        uses_internal_references=entry.uses_internal_references,
        uses_external_references=entry.uses_external_references,
    )


def _decision_entry_payload(entry: object) -> dict[str, object]:
    return {
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


def _print_decision_entry(entry: object) -> None:
    _print_reference_usage_summary(
        header=f"- {entry.decision_id} [{entry.decision_status}]",
        title=entry.title,
        summary=entry.summary,
        uses_internal_references=entry.uses_internal_references,
        uses_external_references=entry.uses_external_references,
    )


def _design_entry_payload(entry: object) -> dict[str, object]:
    return {
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


def _print_design_entry(entry: object) -> None:
    _print_reference_usage_summary(
        header=f"- {entry.document_id} [{entry.family}]",
        title=entry.title,
        summary=entry.summary,
        uses_internal_references=entry.uses_internal_references,
        uses_external_references=entry.uses_external_references,
    )


def _acceptance_contract_entry_payload(entry: object) -> dict[str, object]:
    return {
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


def _print_acceptance_contract_entry(entry: object) -> None:
    print(f"- {entry.contract_id} [{entry.status}]")
    print(f"  Trace: {entry.trace_id}")
    print(f"  Source PRD: {entry.source_prd_id}")
    print(f"  Acceptance IDs: {', '.join(item.acceptance_id for item in entry.entries)}")


def _evidence_entry_payload(entry: object) -> dict[str, object]:
    return {
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


def _print_evidence_entry(entry: object) -> None:
    print(f"- {entry.evidence_id} [{entry.overall_result}]")
    print(f"  Trace: {entry.trace_id}")
    print(f"  Recorded At: {entry.recorded_at}")
    print(f"  Checks: {len(entry.checks)}")
