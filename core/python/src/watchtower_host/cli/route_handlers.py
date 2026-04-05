"""Runtime handlers for route preview commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_detail_result
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query.routes import RoutePreviewService


def _run_route_preview(args: argparse.Namespace) -> int:
    service = RoutePreviewService(ControlPlaneLoader())
    result = service.preview(request_text=args.request, task_type=args.task_type)
    assisted_module_suggestions = tuple(
        getattr(result, "assisted_module_suggestions", ())
    )
    payload = {
        "command": "watchtower-core route preview",
        "status": "ok",
        "request": args.request,
        "task_type": args.task_type,
        "selected_route_count": len(result.selected_routes),
        "selected_routes": [
            {
                "route_id": match.route_id,
                "task_type": match.task_type,
                "score": match.score,
                "matched_keywords": list(match.matched_keywords),
                "required_workflow_ids": list(match.required_workflow_ids),
                "required_workflow_paths": list(match.required_workflow_paths),
            }
            for match in result.selected_routes
        ],
        "selected_workflows": [
            {
                "workflow_id": workflow.workflow_id,
                "workflow_kind": workflow.workflow_kind,
                "title": workflow.title,
                "doc_path": workflow.doc_path,
                "phase_type": workflow.phase_type,
                "task_family": workflow.task_family,
                "composes_module_paths": list(workflow.composes_module_paths),
            }
            for workflow in result.selected_workflows
        ],
        "assisted_module_suggestions": [
            {
                "workflow_id": suggestion.workflow_id,
                "workflow_kind": suggestion.workflow_kind,
                "title": suggestion.title,
                "doc_path": suggestion.doc_path,
                "phase_type": suggestion.phase_type,
                "task_family": suggestion.task_family,
                "score": suggestion.score,
                "matched_signals": list(suggestion.matched_signals),
                "suggested_load_paths": list(suggestion.suggested_load_paths),
            }
            for suggestion in assisted_module_suggestions
        ],
        "warnings": list(result.warnings),
    }

    def _render_human() -> None:
        if not result.selected_routes:
            print("No route matched the request text strongly enough.")
            print(
                "Use --task-type for an explicit route or refine the request "
                "using routing-table terms."
            )
            if assisted_module_suggestions:
                print("Advisory workflow suggestions:")
                for suggestion in assisted_module_suggestions:
                    matched = (
                        ", ".join(suggestion.matched_signals)
                        if suggestion.matched_signals
                        else "heuristic"
                    )
                    load_paths = ", ".join(suggestion.suggested_load_paths)
                    print(
                        f"- {suggestion.workflow_id} "
                        f"[{suggestion.workflow_kind}, {suggestion.phase_type}, "
                        f"{suggestion.task_family}] score={suggestion.score} "
                        f"matched={matched} load={load_paths}"
                    )
            for warning in result.warnings:
                print(f"Warning: {warning}")
            return

        print("Selected routes:")
        for match in result.selected_routes:
            matched = ", ".join(match.matched_keywords) if match.matched_keywords else "explicit"
            print(f"- {match.task_type} [{match.route_id}] score={match.score} matched={matched}")

        print("Active workflows:")
        for workflow in result.selected_workflows:
            print(
                f"- {workflow.workflow_id} "
                f"[{workflow.workflow_kind}, {workflow.phase_type}, {workflow.task_family}] "
                f"{workflow.doc_path}"
            )

        for warning in result.warnings:
            print(f"Warning: {warning}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )
