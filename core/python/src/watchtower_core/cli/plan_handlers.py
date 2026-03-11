"""Runtime handlers for planning scaffold commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_command_error, _print_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.planning_scaffolds import (
    PlanBootstrapParams,
    PlanBootstrapResult,
    PlanningScaffoldService,
    PlanScaffoldParams,
    ScaffoldDocumentResult,
)


def _run_plan_scaffold(args: argparse.Namespace) -> int:
    service = PlanningScaffoldService(ControlPlaneLoader())
    try:
        result = service.scaffold(
            PlanScaffoldParams(
                kind=args.kind,
                trace_id=args.trace_id,
                document_id=args.document_id,
                title=args.title,
                summary=args.summary,
                owner=args.owner,
                status=args.status,
                applies_to=tuple(args.applies_to),
                aliases=tuple(args.alias),
                file_stem=args.file_stem,
                linked_prd_ids=tuple(args.linked_prd),
                linked_decision_ids=tuple(args.linked_decision),
                linked_design_ids=tuple(args.linked_design),
                linked_plan_ids=tuple(args.linked_plan),
                linked_acceptance_ids=tuple(args.linked_acceptance),
                source_requests=tuple(args.source_request),
                references=tuple(args.reference),
                updated_at=args.updated_at,
            ),
            write=args.write,
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core plan scaffold",
            str(exc),
            prefix="Plan scaffold error",
        )
    return _emit_scaffold_result(
        args,
        command_name="watchtower-core plan scaffold",
        result=result,
        include_document=args.include_document,
    )


def _run_plan_bootstrap(args: argparse.Namespace) -> int:
    if args.decision_id is not None and not args.include_decision:
        return _emit_command_error(
            args,
            "watchtower-core plan bootstrap",
            "--decision-id requires --include-decision.",
            prefix="Plan bootstrap error",
        )

    service = PlanningScaffoldService(ControlPlaneLoader())
    try:
        result = service.bootstrap(
            PlanBootstrapParams(
                trace_id=args.trace_id,
                title=args.title,
                summary=args.summary,
                owner=args.owner,
                applies_to=tuple(args.applies_to),
                aliases=tuple(args.alias),
                file_stem=args.file_stem,
                include_decision=args.include_decision,
                decision_id=args.decision_id,
                source_requests=tuple(args.source_request),
                references=tuple(args.reference),
                task_id=args.task_id,
                task_owner=args.task_owner,
                task_kind=args.task_kind,
                task_priority=args.task_priority,
                updated_at=args.updated_at,
            ),
            write=args.write,
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core plan bootstrap",
            str(exc),
            prefix="Plan bootstrap error",
        )
    return _emit_bootstrap_result(
        args,
        command_name="watchtower-core plan bootstrap",
        result=result,
        include_documents=args.include_documents,
    )


def _emit_scaffold_result(
    args: argparse.Namespace,
    *,
    command_name: str,
    result: ScaffoldDocumentResult,
    include_document: bool,
) -> int:
    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "kind": result.kind,
        "document_id": result.document_id,
        "trace_id": result.trace_id,
        "title": result.title,
        "summary": result.summary,
        "document_status": result.status,
        "doc_path": result.doc_path,
        "wrote": result.wrote,
    }
    if include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    action = "Wrote" if result.wrote else "Prepared"
    print(f"{action} {result.kind} scaffold at {result.doc_path}.")
    print(f"Document ID: {result.document_id}")
    if include_document:
        print("")
        print(result.content.rstrip())
        return 0
    if result.wrote:
        print("Derived planning surfaces were refreshed.")
    else:
        print("Dry-run only. Use --write to persist or --include-document to inspect the scaffold.")
    return 0


def _emit_bootstrap_result(
    args: argparse.Namespace,
    *,
    command_name: str,
    result: PlanBootstrapResult,
    include_documents: bool,
) -> int:
    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "document_count": len(result.documents),
        "wrote": result.wrote,
        "sync_refreshed": result.sync_refreshed,
        "documents": [
            {
                "kind": document.kind,
                "document_id": document.document_id,
                "trace_id": document.trace_id,
                "title": document.title,
                "summary": document.summary,
                "document_status": document.status,
                "doc_path": document.doc_path,
                **({"document": document.content} if include_documents else {}),
            }
            for document in result.documents
        ],
        "acceptance_contract": {
            "contract_id": result.acceptance_contract.contract_id,
            "trace_id": result.acceptance_contract.trace_id,
            "source_prd_id": result.acceptance_contract.source_prd_id,
            "title": result.acceptance_contract.title,
            "doc_path": result.acceptance_contract.doc_path,
            "wrote": result.acceptance_contract.wrote,
            **(
                {"document": result.acceptance_contract.content}
                if include_documents
                else {}
            ),
        },
        "validation_evidence": {
            "evidence_id": result.validation_evidence.evidence_id,
            "trace_id": result.validation_evidence.trace_id,
            "title": result.validation_evidence.title,
            "overall_result": result.validation_evidence.overall_result,
            "doc_path": result.validation_evidence.doc_path,
            "wrote": result.validation_evidence.wrote,
            **(
                {"document": result.validation_evidence.content}
                if include_documents
                else {}
            ),
        },
        "task": {
            "task_id": result.task_result.task_id,
            "title": result.task_result.title,
            "summary": result.task_result.summary,
            "task_status": result.task_result.task_status,
            "task_kind": result.task_result.task_kind,
            "priority": result.task_result.priority,
            "owner": result.task_result.owner,
            "doc_path": result.task_result.doc_path,
            "wrote": result.task_result.wrote,
        },
    }
    if _print_payload(args, payload) == 0:
        return 0

    action = "Wrote" if result.wrote else "Prepared"
    print(
        f"{action} bootstrap chain with {len(result.documents)} planning documents and "
        f"task {result.task_result.task_id}."
    )
    for document in result.documents:
        print(f"- {document.kind}: {document.doc_path}")
        if include_documents:
            print("")
            print(document.content.rstrip())
            print("")
    print(f"- acceptance_contract: {result.acceptance_contract.doc_path}")
    if include_documents:
        print("")
        print(result.acceptance_contract.content.rstrip())
        print("")
    print(f"- validation_evidence: {result.validation_evidence.doc_path}")
    if include_documents:
        print("")
        print(result.validation_evidence.content.rstrip())
        print("")
    print(f"- task: {result.task_result.doc_path}")
    if result.wrote:
        print("Derived planning surfaces were refreshed.")
    else:
        print("Dry-run only. Use --write to persist or --include-documents to inspect content.")
    return 0
