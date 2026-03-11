"""Runtime handlers for route preview commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _print_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query.routes import RoutePreviewService


def _run_route_preview(args: argparse.Namespace) -> int:
    service = RoutePreviewService(ControlPlaneLoader())
    result = service.preview(request_text=args.request, task_type=args.task_type)
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
                "title": workflow.title,
                "doc_path": workflow.doc_path,
                "phase_type": workflow.phase_type,
                "task_family": workflow.task_family,
            }
            for workflow in result.selected_workflows
        ],
        "warnings": list(result.warnings),
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not result.selected_routes:
        print("No route matched the request text strongly enough.")
        print(
            "Use --task-type for an explicit route or refine the request "
            "using routing-table terms."
        )
        return 0

    print("Selected routes:")
    for match in result.selected_routes:
        matched = ", ".join(match.matched_keywords) if match.matched_keywords else "explicit"
        print(f"- {match.task_type} [{match.route_id}] score={match.score} matched={matched}")

    print("Active workflow modules:")
    for workflow in result.selected_workflows:
        print(
            f"- {workflow.workflow_id} [{workflow.phase_type}, {workflow.task_family}] "
            f"{workflow.doc_path}"
        )

    for warning in result.warnings:
        print(f"Warning: {warning}")
    return 0
