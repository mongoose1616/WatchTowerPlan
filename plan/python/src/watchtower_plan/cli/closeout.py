"""Pack-owned `watchtower-core plan closeout` registration and handlers."""

from __future__ import annotations

import argparse
from textwrap import dedent
from typing import Any

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)
from watchtower_core.cli.handler_common import (
    _emit_detail_result,
    _run_help,
    _run_value_error_operation,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry import telemetry_operation

IMPLEMENTATION_PATH = "plan/python/src/watchtower_plan/cli/closeout.py"
InitiativePackageService: type[Any] | None = None
InitiativeCloseoutService: type[Any] | None = None


def _initiative_package_service_type() -> type[Any]:
    global InitiativePackageService
    if InitiativePackageService is None:
        from watchtower_plan import InitiativePackageService as initiative_package_service

        InitiativePackageService = initiative_package_service
    return InitiativePackageService


def _initiative_closeout_service_type() -> type[Any]:
    global InitiativeCloseoutService
    if InitiativeCloseoutService is None:
        from watchtower_plan.closeout import (
            InitiativeCloseoutService as initiative_closeout_service,
        )

        InitiativeCloseoutService = initiative_closeout_service
    return InitiativeCloseoutService


def register_plan_closeout_commands(
    plan_subparsers: argparse._SubParsersAction,
) -> None:
    """Register the pack-owned `plan closeout` namespace."""

    closeout_parser = plan_subparsers.add_parser(
        "closeout",
        help="Close live initiatives or retained trace records.",
        description=dedent(
            """
            Apply terminal closeout state to live plan initiative packages,
            or close one retained trace record after live work is already
            promoted or otherwise retired from the active workspace.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan closeout initiative --initiative-slug "
            "plan_workspace_bootstrap --initiative-status completed "
            '--closure-reason "Live plan slice delivered" --write',
            "uv run watchtower-core plan closeout retained-initiative --trace-id "
            "trace.example --initiative-status completed --closure-reason "
            '"Closed the retained trace record" --write',
        ),
        formatter_class=HelpFormatter,
    )
    closeout_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    closeout_subparsers = closeout_parser.add_subparsers(
        dest="plan_closeout_command",
        title="closeout commands",
        metavar="<closeout_command>",
    )
    closeout_parser.set_defaults(handler=_run_help, help_parser=closeout_parser)

    initiative_parser = closeout_subparsers.add_parser(
        "initiative",
        help="Set terminal closeout state for one live plan initiative package.",
        description=dedent(
            """
            Set terminal closeout state for one pack-wide or project-scoped
            live initiative package under `plan/**` and refresh the derived
            plan indexes plus rendered views that surface active and recent
            closeouts.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan closeout initiative --initiative-slug "
            "plan_workspace_bootstrap --initiative-status completed "
            '--closure-reason "Delivered the live plan slice"',
            "uv run watchtower-core plan closeout initiative --project-slug watchtower "
            "--initiative-slug watchtower_work_item_notes --initiative-status completed "
            '--closure-reason "Implemented and validated work-item notes" --write',
        ),
        formatter_class=HelpFormatter,
    )
    initiative_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    initiative_parser.add_argument(
        "--initiative-slug",
        required=True,
        help="Initiative slug such as plan_workspace_bootstrap or watchtower_work_item_notes.",
    )
    initiative_parser.add_argument(
        "--project-slug",
        help="Project slug when the initiative is project-scoped, such as watchtower.",
    )
    initiative_parser.add_argument(
        "--initiative-status",
        required=True,
        choices=("completed", "superseded", "cancelled"),
        help="Terminal initiative status to record on the live plan package.",
    )
    initiative_parser.add_argument(
        "--closure-reason",
        required=True,
        help="Short human-readable reason for the closeout decision.",
    )
    initiative_parser.add_argument(
        "--superseded-by-trace-id",
        help="Replacement trace identifier. Required when initiative-status is superseded.",
    )
    initiative_parser.add_argument(
        "--closed-at",
        help="Explicit RFC 3339 UTC closeout timestamp. Defaults to the current UTC time.",
    )
    initiative_parser.add_argument(
        "--write",
        action="store_true",
        help="Persist the updated closeout state and regenerated plan surfaces.",
    )
    add_human_json_format_argument(initiative_parser)
    initiative_parser.set_defaults(handler=_run_closeout_plan_initiative)

    retained_initiative_parser = closeout_subparsers.add_parser(
        "retained-initiative",
        help="Set terminal closeout state for one retained trace record.",
        description=dedent(
            """
            Set terminal closeout state for one retained trace record and, in
            write mode, persist it to the traceability index plus the derived
            initiative and coordination surfaces that still mirror retained
            trace state.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan closeout retained-initiative --trace-id "
            "trace.example --initiative-status completed --closure-reason "
            '"Delivered and validated"',
            "uv run watchtower-core plan closeout retained-initiative --trace-id "
            "trace.example --initiative-status superseded --superseded-by-trace-id "
            'trace.replacement --closure-reason "Replaced by the new initiative" '
            "--format json",
        ),
        formatter_class=HelpFormatter,
    )
    retained_initiative_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    retained_initiative_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.governed_acceptance_example.",
    )
    retained_initiative_parser.add_argument(
        "--initiative-status",
        required=True,
        choices=("completed", "superseded", "cancelled", "abandoned"),
        help="Terminal initiative status to record on the retained trace record.",
    )
    retained_initiative_parser.add_argument(
        "--closure-reason",
        required=True,
        help="Short human-readable reason for the closeout decision.",
    )
    retained_initiative_parser.add_argument(
        "--superseded-by-trace-id",
        help="Replacement trace identifier. Required when initiative-status is superseded.",
    )
    retained_initiative_parser.add_argument(
        "--closed-at",
        help="Explicit RFC 3339 UTC closeout timestamp. Defaults to the current UTC time.",
    )
    retained_initiative_parser.add_argument(
        "--allow-open-tasks",
        action="store_true",
        help="Allow terminal closeout even if linked tasks are still open.",
    )
    retained_initiative_parser.add_argument(
        "--allow-acceptance-issues",
        action="store_true",
        help=(
            "Allow terminal closeout even when acceptance reconciliation reports issues. "
            "Use only when the validation exception is intentional and explicit."
        ),
    )
    retained_initiative_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the updated closeout state and regenerated trackers to their canonical paths.",
    )
    add_human_json_format_argument(retained_initiative_parser)
    retained_initiative_parser.set_defaults(handler=_run_closeout_retained_initiative)


def _run_closeout_plan_initiative(args: argparse.Namespace) -> int:
    service = _initiative_package_service_type()(ControlPlaneLoader())
    with telemetry_operation(
        "plan_closeout",
        "plan_closeout_initiative",
        attributes={
            "project_slug": args.project_slug,
            "initiative_slug": args.initiative_slug,
            "initiative_status": args.initiative_status,
            "write": args.write,
        },
    ) as operation:
        result = _run_value_error_operation(
            args,
            command_name="watchtower-core plan closeout initiative",
            prefix="Closeout error",
            operation=lambda: (
                service.close_project_scoped(
                    args.project_slug,
                    args.initiative_slug,
                    initiative_status=args.initiative_status,
                    closure_reason=args.closure_reason,
                    closed_at=args.closed_at,
                    superseded_by_trace_id=args.superseded_by_trace_id,
                    write=args.write,
                )
                if args.project_slug
                else service.close_packwide(
                    args.initiative_slug,
                    initiative_status=args.initiative_status,
                    closure_reason=args.closure_reason,
                    closed_at=args.closed_at,
                    superseded_by_trace_id=args.superseded_by_trace_id,
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
                initiative_status=result.initiative_status,
                scope_type=result.scope_type,
                wrote=result.wrote,
            )
    if result is None:
        return 1

    payload = {
        "command": "watchtower-core plan closeout initiative",
        "status": "ok",
        "initiative_id": result.initiative_id,
        "trace_id": result.trace_id,
        "initiative_root": result.initiative_root,
        "scope_type": result.scope_type,
        "initiative_status": result.initiative_status,
        "closed_at": result.closed_at,
        "closure_reason": result.closure_reason,
        "superseded_by_trace_id": result.superseded_by_trace_id,
        "wrote": result.wrote,
    }

    def _render_human() -> None:
        print(
            f"Closed live plan initiative {result.trace_id} as {result.initiative_status}."
        )
        print(f"Initiative Root: {result.initiative_root}")
        print(f"Closed At: {result.closed_at}")
        print(f"Reason: {result.closure_reason}")
        if result.superseded_by_trace_id is not None:
            print(f"Superseded By: {result.superseded_by_trace_id}")
        if result.wrote:
            print(
                "Initiative state, local artifacts, and derived plan surfaces were updated."
            )
        else:
            print("Dry-run only. Use --write to persist the terminal closeout state.")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _run_closeout_retained_initiative(args: argparse.Namespace) -> int:
    service = _initiative_closeout_service_type()(ControlPlaneLoader())
    with telemetry_operation(
        "plan_closeout",
        "plan_closeout_retained_initiative",
        attributes={
            "trace_id": args.trace_id,
            "initiative_status": args.initiative_status,
            "write": args.write,
            "allow_open_tasks": args.allow_open_tasks,
            "allow_acceptance_issues": args.allow_acceptance_issues,
        },
    ) as operation:
        result = _run_value_error_operation(
            args,
            command_name="watchtower-core plan closeout retained-initiative",
            prefix="Closeout error",
            operation=lambda: service.close(
                trace_id=args.trace_id,
                initiative_status=args.initiative_status,
                closure_reason=args.closure_reason,
                superseded_by_trace_id=args.superseded_by_trace_id,
                closed_at=args.closed_at,
                write=args.write,
                allow_open_tasks=args.allow_open_tasks,
                allow_acceptance_issues=args.allow_acceptance_issues,
            ),
        )
        if result is None:
            if operation is not None:
                operation.set_result(status="value_error")
            return 1
        if operation is not None:
            operation.set_result(
                status="ok",
                trace_id=result.trace_id,
                initiative_status=result.initiative_status,
                wrote=result.wrote,
                acceptance_issue_count=result.acceptance_issue_count,
                open_task_count=len(result.open_task_ids),
            )
    if result is None:
        return 1

    payload = {
        "command": "watchtower-core plan closeout retained-initiative",
        "status": "ok",
        "trace_id": result.trace_id,
        "initiative_status": result.initiative_status,
        "closed_at": result.closed_at,
        "closure_reason": result.closure_reason,
        "superseded_by_trace_id": result.superseded_by_trace_id,
        "open_task_ids": list(result.open_task_ids),
        "acceptance_issue_count": result.acceptance_issue_count,
        "acceptance_issues_allowed": result.acceptance_issues_allowed,
        "wrote": result.wrote,
        "traceability_output_path": result.traceability_output_path,
        "initiative_index_output_path": result.initiative_index_output_path,
        "coordination_index_output_path": result.coordination_index_output_path,
        "initiative_tracking_output_path": result.initiative_tracking_output_path,
        "coordination_tracking_output_path": result.coordination_tracking_output_path,
    }

    def _render_human() -> None:
        print(f"Closed retained trace {result.trace_id} as {result.initiative_status}.")
        print(f"Closed At: {result.closed_at}")
        print(f"Reason: {result.closure_reason}")
        if result.superseded_by_trace_id is not None:
            print(f"Superseded By: {result.superseded_by_trace_id}")
        if result.open_task_ids:
            print(f"Open Tasks Left In Place: {', '.join(result.open_task_ids)}")
        if result.acceptance_issues_allowed:
            print(f"Acceptance Issues Left In Place: {result.acceptance_issue_count}")
        if result.wrote:
            print(
                "Canonical traceability, initiative, coordination, and live trackers "
                "were updated."
            )
        else:
            print("Dry-run only. Use --write to persist the closeout state.")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


__all__ = ["register_plan_closeout_commands"]
