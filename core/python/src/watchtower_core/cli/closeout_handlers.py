"""Runtime handlers for closeout command families."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_command_error, _print_payload
from watchtower_core.closeout import InitiativeCloseoutService
from watchtower_core.control_plane.loader import ControlPlaneLoader


def _run_closeout_initiative(args: argparse.Namespace) -> int:
    service = InitiativeCloseoutService(ControlPlaneLoader())
    try:
        result = service.close(
            trace_id=args.trace_id,
            initiative_status=args.initiative_status,
            closure_reason=args.closure_reason,
            superseded_by_trace_id=args.superseded_by_trace_id,
            closed_at=args.closed_at,
            write=args.write,
            allow_open_tasks=args.allow_open_tasks,
            allow_acceptance_issues=args.allow_acceptance_issues,
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core closeout initiative",
            str(exc),
            prefix="Closeout error",
        )

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
        "planning_catalog_output_path": result.planning_catalog_output_path,
        "coordination_index_output_path": result.coordination_index_output_path,
        "initiative_tracking_output_path": result.initiative_tracking_output_path,
        "coordination_tracking_output_path": result.coordination_tracking_output_path,
        "prd_tracking_output_path": result.prd_tracking_output_path,
        "decision_tracking_output_path": result.decision_tracking_output_path,
        "design_tracking_output_path": result.design_tracking_output_path,
    }
    if _print_payload(args, payload) == 0:
        return 0

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
            "Canonical traceability, initiative, planning catalog, coordination, "
            "and planning trackers were updated."
        )
    else:
        print("Dry-run only. Use --write to persist the closeout state.")
    return 0
