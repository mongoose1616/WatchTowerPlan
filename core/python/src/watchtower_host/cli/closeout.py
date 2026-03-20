"""Host-owned retained closeout command registration and handlers."""

from __future__ import annotations

import argparse
from textwrap import dedent

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

InitiativeCloseoutService = None


def _run_closeout_initiative(args: argparse.Namespace) -> int:
    service_type = InitiativeCloseoutService
    if service_type is None:
        from watchtower_plan.closeout import InitiativeCloseoutService as service_type

    service = service_type(ControlPlaneLoader())
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core closeout initiative",
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
        return 1

    payload = {
        "command": "watchtower-core closeout initiative",
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
        print(f"Closed initiative {result.trace_id} as {result.initiative_status}.")
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


def register_closeout_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the retained trace closeout command family."""

    closeout_parser = subparsers.add_parser(
        "closeout",
        help="Close retained traced initiatives after live work has already been promoted or purged.",
        description=dedent(
            """
            Apply terminal initiative state to retained traced initiatives
            after live `plan/**` work has already been promoted or purged.

            Live initiative-package closeout and trace purge now live under
            `watchtower-core plan closeout ...`.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status completed --closure-reason \"Closed the retained traced planning package\"",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status superseded --superseded-by-trace-id trace.replacement "
            "--closure-reason \"Replaced by the new initiative\" --format json",
        ),
        formatter_class=HelpFormatter,
    )
    closeout_subparsers = closeout_parser.add_subparsers(
        dest="closeout_command",
        title="closeout commands",
        metavar="<closeout_command>",
    )
    closeout_parser.set_defaults(handler=_run_help, help_parser=closeout_parser)

    initiative_parser = closeout_subparsers.add_parser(
        "initiative",
        help="Set terminal closeout state for one traced initiative.",
        description=dedent(
            """
            Set terminal closeout state for one traced initiative and, in write
            mode, persist it to the traceability index plus the derived
            initiative, coordination, decision, design, and implementation trackers.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status completed --closure-reason \"Delivered and validated\"",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status cancelled --closure-reason \"No longer in scope\" --write",
        ),
        formatter_class=HelpFormatter,
    )
    initiative_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.governed_acceptance_example.",
    )
    initiative_parser.add_argument(
        "--initiative-status",
        required=True,
        choices=("completed", "superseded", "cancelled", "abandoned"),
        help="Terminal initiative status to record on the trace.",
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
        "--allow-open-tasks",
        action="store_true",
        help="Allow terminal closeout even if linked tasks are still open.",
    )
    initiative_parser.add_argument(
        "--allow-acceptance-issues",
        action="store_true",
        help=(
            "Allow terminal closeout even when acceptance reconciliation reports issues. "
            "Use only when the validation exception is intentional and explicit."
        ),
    )
    initiative_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the updated closeout state and regenerated trackers to their canonical paths.",
    )
    add_human_json_format_argument(initiative_parser)
    initiative_parser.set_defaults(handler=_run_closeout_initiative)


__all__ = ["register_closeout_family", "_run_closeout_initiative"]
