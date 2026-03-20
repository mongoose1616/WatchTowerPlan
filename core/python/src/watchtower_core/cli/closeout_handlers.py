"""Runtime handlers for closeout command families."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_detail_result,
    _run_value_error_operation,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan import InitiativePackageService
from watchtower_plan.closeout import InitiativeCloseoutService, TracePurgeService


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


def _run_closeout_purge_trace(args: argparse.Namespace) -> int:
    service = TracePurgeService(ControlPlaneLoader())
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core closeout purge-trace",
        prefix="Purge error",
        operation=lambda: service.purge(
            trace_id=args.trace_id,
            retained_authority_paths=tuple(args.retained_authority_path or ()),
            purged_at=args.purged_at,
            write=args.write,
        ),
    )
    if result is None:
        return 1

    payload = {
        "command": "watchtower-core closeout purge-trace",
        "status": "ok",
        "trace_id": result.trace_id,
        "title": result.title,
        "initiative_status": result.initiative_status,
        "closed_at": result.closed_at,
        "closure_reason": result.closure_reason,
        "purged_at": result.purged_at,
        "removed_paths": list(result.removed_paths),
        "retained_authority_paths": list(result.retained_authority_paths),
        "purge_ledger_relative_path": result.purge_ledger_relative_path,
        "purge_ledger_output_path": result.purge_ledger_output_path,
        "refreshed_targets": list(result.refreshed_targets),
        "wrote": result.wrote,
    }

    def _render_human() -> None:
        print(f"Prepared purge for {result.trace_id}.")
        print(f"Purged At: {result.purged_at}")
        print(f"Removed Paths: {len(result.removed_paths)}")
        print(f"Purge Ledger: {result.purge_ledger_relative_path}")
        print("Retained Authority Paths: " + ", ".join(result.retained_authority_paths))
        if result.wrote:
            print("Trace package was deleted and derived surfaces were refreshed.")
        else:
            print(
                "Dry-run only. Use --write to delete the trace package and write the purge ledger."
            )

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _run_closeout_plan_initiative(args: argparse.Namespace) -> int:
    service = InitiativePackageService(ControlPlaneLoader())
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core closeout plan-initiative",
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
        return 1

    payload = {
        "command": "watchtower-core closeout plan-initiative",
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
        print(f"Closed live plan initiative {result.trace_id} as {result.initiative_status}.")
        print(f"Initiative Root: {result.initiative_root}")
        print(f"Closed At: {result.closed_at}")
        print(f"Reason: {result.closure_reason}")
        if result.superseded_by_trace_id is not None:
            print(f"Superseded By: {result.superseded_by_trace_id}")
        if result.wrote:
            print("Initiative state, local artifacts, and derived plan surfaces were updated.")
        else:
            print("Dry-run only. Use --write to persist the terminal closeout state.")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )
