"""Runtime handlers for planning scaffold commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_command_error,
    _emit_detail_result,
    _run_value_error_operation,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.initiative_packages import (
    InitiativePackageResult,
    InitiativePackageService,
)
from watchtower_core.repo_ops.planning_scaffolds import (
    PlanBootstrapParams,
    PlanBootstrapResult,
    PlanningScaffoldService,
    PlanScaffoldParams,
    ScaffoldDocumentResult,
)


def _run_plan_scaffold(args: argparse.Namespace) -> int:
    service = PlanningScaffoldService(ControlPlaneLoader())
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core plan scaffold",
        prefix="Plan scaffold error",
        operation=lambda: service.scaffold(
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
        ),
    )
    if result is None:
        return 1
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
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core plan bootstrap",
        prefix="Plan bootstrap error",
        operation=lambda: service.bootstrap(
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
        ),
    )
    if result is None:
        return 1
    return _emit_bootstrap_result(
        args,
        command_name="watchtower-core plan bootstrap",
        result=result,
        include_documents=args.include_documents,
    )


def _run_plan_confirm_inputs(args: argparse.Namespace) -> int:
    service = InitiativePackageService(ControlPlaneLoader())
    command_name = "watchtower-core plan confirm-inputs"
    result = _run_value_error_operation(
        args,
        command_name=command_name,
        prefix="Plan confirm-inputs error",
        operation=lambda: (
            service.confirm_project_scoped_inputs(
                args.project_slug,
                args.initiative_slug,
                args.actor_id,
                write=args.write,
            )
            if args.project_slug
            else service.confirm_authored_inputs(
                args.initiative_slug,
                args.actor_id,
                write=args.write,
            )
        ),
    )
    if result is None:
        return 1
    return _emit_initiative_package_result(
        args,
        command_name=command_name,
        action_summary="Confirmed authored inputs",
        result=result,
    )


def _run_plan_approve(args: argparse.Namespace) -> int:
    service = InitiativePackageService(ControlPlaneLoader())
    command_name = "watchtower-core plan approve"
    result = _run_value_error_operation(
        args,
        command_name=command_name,
        prefix="Plan approve error",
        operation=lambda: (
            service.approve_project_scoped(
                args.project_slug,
                args.initiative_slug,
                args.actor_id,
                write=args.write,
            )
            if args.project_slug
            else service.approve_packwide(
                args.initiative_slug,
                args.actor_id,
                write=args.write,
            )
        ),
    )
    if result is None:
        return 1
    return _emit_initiative_package_result(
        args,
        command_name=command_name,
        action_summary="Approved live initiative",
        result=result,
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

    def _render_human() -> None:
        action = "Wrote" if result.wrote else "Prepared"
        print(f"{action} {result.kind} scaffold at {result.doc_path}.")
        print(f"Document ID: {result.document_id}")
        if include_document:
            print("")
            print(result.content.rstrip())
            return
        if result.wrote:
            print("Derived planning surfaces were refreshed.")
        else:
            print(
                "Dry-run only. Use --write to persist or "
                "--include-document to inspect the scaffold."
            )

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


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

    def _render_human() -> None:
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
            print(
                "Dry-run only. Use --write to persist or --include-documents to inspect content."
            )

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _emit_initiative_package_result(
    args: argparse.Namespace,
    *,
    command_name: str,
    action_summary: str,
    result: InitiativePackageResult,
) -> int:
    payload = {
        "command": command_name,
        "status": "ok",
        "initiative_id": result.initiative_id,
        "trace_id": result.trace_id,
        "initiative_root": result.initiative_root,
        "lifecycle_stage": result.lifecycle_stage,
        "review_status": result.review_status,
        "ready_for_execution": result.ready_for_execution,
        "validation_passed": result.validation_passed,
        "wrote": result.wrote,
    }

    def _render_human() -> None:
        print(f"{action_summary} {result.trace_id}.")
        print(f"Initiative Root: {result.initiative_root}")
        print(f"Lifecycle Stage: {result.lifecycle_stage}")
        print(f"Review Status: {result.review_status}")
        print(f"Ready For Execution: {result.ready_for_execution}")
        if result.wrote:
            print("Initiative state and derived plan surfaces were updated.")
        else:
            print("Dry-run only. Use --write to persist the updated initiative state.")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )
