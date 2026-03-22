"""Pack-owned runtime handlers for the `watchtower-core plan` namespace."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_detail_result,
    _run_value_error_operation,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry import telemetry_operation
from watchtower_plan.initiatives import (
    InitiativeBootstrapParams,
    InitiativePackageResult,
    InitiativePackageService,
    InitiativeTaskSpec,
)


def _run_plan_bootstrap(args: argparse.Namespace) -> int:
    service = InitiativePackageService(ControlPlaneLoader())
    bootstrap_task_summary = f"Bootstrap {args.title} live initiative package."
    with telemetry_operation(
        "plan_command",
        "plan_bootstrap",
        attributes={
            "trace_id": args.trace_id,
            "project_slug": args.project_slug,
            "initiative_slug": args.initiative_slug,
            "write": args.write,
        },
    ) as operation:
        result = _run_value_error_operation(
            args,
            command_name="watchtower-core plan bootstrap",
            prefix="Plan bootstrap error",
            operation=lambda: (
                service.bootstrap_project_scoped(
                    args.project_slug,
                    InitiativeBootstrapParams(
                        trace_id=args.trace_id,
                        title=args.title,
                        summary=args.summary,
                        initiative_slug=args.initiative_slug,
                        owner=args.owner,
                        task_specs=(
                            InitiativeTaskSpec(
                                task_id=args.task_id,
                                owner=args.task_owner or args.owner,
                                title=f"Bootstrap {args.title}",
                                summary=bootstrap_task_summary,
                                task_kind=args.task_kind,
                                priority=args.task_priority,
                            ),
                        ),
                        include_decision_notes=args.include_decision,
                        updated_at=args.updated_at,
                    ),
                    write=args.write,
                )
                if args.project_slug
                else service.bootstrap_packwide(
                    InitiativeBootstrapParams(
                        trace_id=args.trace_id,
                        title=args.title,
                        summary=args.summary,
                        initiative_slug=args.initiative_slug,
                        owner=args.owner,
                        task_specs=(
                            InitiativeTaskSpec(
                                task_id=args.task_id,
                                owner=args.task_owner or args.owner,
                                title=f"Bootstrap {args.title}",
                                summary=bootstrap_task_summary,
                                task_kind=args.task_kind,
                                priority=args.task_priority,
                            ),
                        ),
                        include_decision_notes=args.include_decision,
                        updated_at=args.updated_at,
                    ),
                    write=args.write,
                )
            ),
        )
        if result is None:
            if operation is not None:
                operation.set_result(status="value_error")
            return 1
        if operation is not None:
            operation.set_result(
                status="ok",
                initiative_id=result.initiative_id,
                trace_id=result.trace_id,
                lifecycle_stage=result.lifecycle_stage,
                review_status=result.review_status,
                ready_for_execution=result.ready_for_execution,
                validation_passed=result.validation_passed,
                wrote=result.wrote,
            )
    if result is None:
        return 1
    return _emit_initiative_package_result(
        args,
        command_name="watchtower-core plan bootstrap",
        action_summary="Bootstrapped live initiative package",
        result=result,
    )


def _run_plan_confirm_inputs(args: argparse.Namespace) -> int:
    service = InitiativePackageService(ControlPlaneLoader())
    command_name = "watchtower-core plan confirm-inputs"
    with telemetry_operation(
        "plan_command",
        "plan_confirm_inputs",
        attributes={
            "project_slug": args.project_slug,
            "initiative_slug": args.initiative_slug,
            "actor_id": args.actor_id,
            "write": args.write,
        },
    ) as operation:
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
            if operation is not None:
                operation.set_result(status="value_error")
            return 1
        if operation is not None:
            operation.set_result(
                status="ok",
                initiative_id=result.initiative_id,
                trace_id=result.trace_id,
                lifecycle_stage=result.lifecycle_stage,
                review_status=result.review_status,
                ready_for_execution=result.ready_for_execution,
                validation_passed=result.validation_passed,
                wrote=result.wrote,
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
    with telemetry_operation(
        "plan_command",
        "plan_approve",
        attributes={
            "project_slug": args.project_slug,
            "initiative_slug": args.initiative_slug,
            "actor_id": args.actor_id,
            "write": args.write,
        },
    ) as operation:
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
            if operation is not None:
                operation.set_result(status="value_error")
            return 1
        if operation is not None:
            operation.set_result(
                status="ok",
                initiative_id=result.initiative_id,
                trace_id=result.trace_id,
                lifecycle_stage=result.lifecycle_stage,
                review_status=result.review_status,
                ready_for_execution=result.ready_for_execution,
                validation_passed=result.validation_passed,
                wrote=result.wrote,
            )
    if result is None:
        return 1
    return _emit_initiative_package_result(
        args,
        command_name=command_name,
        action_summary="Approved live initiative",
        result=result,
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


__all__ = [
    "_run_plan_approve",
    "_run_plan_bootstrap",
    "_run_plan_confirm_inputs",
]
