"""Runtime handlers for closeout command families."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_detail_result,
    _run_value_error_operation,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.closeout import InitiativeCloseoutService


def _run_closeout_initiative(args: argparse.Namespace) -> int:
    service = InitiativeCloseoutService(ControlPlaneLoader())
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
