"""Pack-owned `watchtower-core plan sync` registration and handlers."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)
from watchtower_core.cli.handler_common import _emit_detail_result, _run_help
from watchtower_core.cli.sync_family_common import (
    HandlerMap,
    SyncCommandSpec,
    register_spec_sync_commands,
)
from watchtower_core.cli.sync_runtime_helpers import (
    build_github_task_sync_params,
    build_loader,
    load_document_sync_service,
    load_sync_class,
    run_document_sync_command,
    run_multi_target_sync,
    run_tracking_sync,
)

IMPLEMENTATION_PATH = "plan/python/src/watchtower_plan/cli/sync.py"


_DOCUMENT_COMMAND_SPECS: tuple[SyncCommandSpec, ...] = (
    {
        "name": "reference-index",
        "handler": "reference_index",
        "help": "Rebuild the reference index from governed reference docs.",
        "description": """
            Rebuild the plan-owned reference index from the governed reference
            documents under `core/docs/references/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync reference-index",
            "uv run watchtower-core plan sync reference-index --write",
            "uv run watchtower-core plan sync reference-index --output "
            "/tmp/reference_index.json --format json",
        ),
    },
    {
        "name": "foundation-index",
        "handler": "foundation_index",
        "help": "Rebuild the foundation index from governed foundation docs.",
        "description": """
            Rebuild the plan-owned foundation index from the governed foundation
            documents under `core/docs/foundations/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync foundation-index",
            "uv run watchtower-core plan sync foundation-index --write",
            "uv run watchtower-core plan sync foundation-index --output "
            "/tmp/foundation_index.json --format json",
        ),
    },
    {
        "name": "standard-index",
        "handler": "standard_index",
        "help": "Rebuild the standard index from governed standards.",
        "description": """
            Rebuild the standard index from the governed standards under
            `core/docs/standards/` and `plan/docs/standards/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync standard-index",
            "uv run watchtower-core plan sync standard-index --write",
            "uv run watchtower-core plan sync standard-index --output "
            "/tmp/standard_index.json --format json",
        ),
    },
    {
        "name": "workflow-index",
        "handler": "workflow_index",
        "help": "Rebuild the workflow index from governed workflow modules.",
        "description": """
            Rebuild the workflow index from the workflow modules under
            `core/workflows/modules/` and `plan/workflows/modules/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync workflow-index",
            "uv run watchtower-core plan sync workflow-index --write",
            "uv run watchtower-core plan sync workflow-index --output "
            "/tmp/workflow_index.json --format json",
        ),
    },
    {
        "name": "initiative-index",
        "handler": "initiative_index",
        "help": "Rebuild the initiative index from traceability, planning, and task indexes.",
        "description": """
            Rebuild the cross-family initiative index from traceability plus
            the current planning and task indexes.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync initiative-index",
            "uv run watchtower-core plan sync initiative-index --write",
            "uv run watchtower-core plan sync initiative-index --output "
            "/tmp/initiative_index.json --format json",
        ),
    },
    {
        "name": "task-index",
        "handler": "task_index",
        "help": "Rebuild the live plan task index from initiative-local task state.",
        "description": """
            Rebuild the live plan task index from initiative-local task state
            under `plan/**/.wt/tasks/**`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync task-index",
            "uv run watchtower-core plan sync task-index --write",
            "uv run watchtower-core plan sync task-index --output "
            "/tmp/task_index.json --format json",
        ),
    },
    {
        "name": "review-index",
        "handler": "review_index",
        "help": "Rebuild the live plan review index from initiative-local review state.",
        "description": """
            Rebuild the live plan review index from initiative-local review,
            approval, and readiness state under `plan/**/.wt/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync review-index",
            "uv run watchtower-core plan sync review-index --write",
            "uv run watchtower-core plan sync review-index --output "
            "/tmp/review_index.json --format json",
        ),
    },
    {
        "name": "traceability-index",
        "handler": "traceability_index",
        "help": "Rebuild the traceability index from governed planning and evidence sources.",
        "description": """
            Rebuild the traceability index from the governed planning indexes,
            acceptance contracts, and validation evidence artifacts.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync traceability-index",
            "uv run watchtower-core plan sync traceability-index --write",
            "uv run watchtower-core plan sync traceability-index --output "
            "/tmp/traceability_index.json --format json",
        ),
    },
)

_TRACKING_COMMAND_SPECS: tuple[SyncCommandSpec, ...] = (
    {
        "name": "initiative-tracking",
        "handler": "initiative_tracking",
        "help": "Rebuild the human-readable initiative tracker from the initiative index.",
        "description": """
            Rebuild the human-readable initiative tracker from the governed
            initiative index.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync initiative-tracking",
            "uv run watchtower-core plan sync initiative-tracking --write",
            "uv run watchtower-core plan sync initiative-tracking --output "
            "/tmp/initiative_tracking.md --format json",
        ),
    },
    {
        "name": "task-tracking",
        "handler": "task_tracking",
        "help": "Rebuild the human-readable task tracker from live initiative-local task state.",
        "description": """
            Rebuild the human-readable task tracker from initiative-local live
            task state under `plan/**/.wt/tasks/**`.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """,
        "examples": (
            "uv run watchtower-core plan sync task-tracking",
            "uv run watchtower-core plan sync task-tracking --write",
            "uv run watchtower-core plan sync task-tracking --output "
            "/tmp/task_tracking.md --format json",
        ),
    },
)

_DOCUMENT_HANDLER_SPECS = (
    (
        "reference_index",
        "watchtower_core.sync.reference_index",
        "ReferenceIndexSyncService",
        "watchtower-core plan sync reference-index",
        "reference index",
    ),
    (
        "foundation_index",
        "watchtower_core.sync.foundation_index",
        "FoundationIndexSyncService",
        "watchtower-core plan sync foundation-index",
        "foundation index",
    ),
    (
        "standard_index",
        "watchtower_core.sync.standard_index",
        "StandardIndexSyncService",
        "watchtower-core plan sync standard-index",
        "standard index",
    ),
    (
        "workflow_index",
        "watchtower_core.sync.workflow_index",
        "WorkflowIndexSyncService",
        "watchtower-core plan sync workflow-index",
        "workflow index",
    ),
    (
        "initiative_index",
        "watchtower_plan.sync.initiative_index",
        "InitiativeIndexSyncService",
        "watchtower-core plan sync initiative-index",
        "initiative index",
    ),
    (
        "task_index",
        "watchtower_plan.sync.task_index",
        "TaskIndexSyncService",
        "watchtower-core plan sync task-index",
        "task index",
    ),
    (
        "review_index",
        "watchtower_plan.sync.review_index",
        "ReviewIndexSyncService",
        "watchtower-core plan sync review-index",
        "review index",
    ),
    (
        "traceability_index",
        "watchtower_plan.sync.traceability",
        "TraceabilityIndexSyncService",
        "watchtower-core plan sync traceability-index",
        "traceability index",
    ),
)


def _build_document_handler(
    handler_key: str,
    module_name: str,
    class_name: str,
    command_name: str,
    artifact_label: str,
) -> tuple[str, Callable[[argparse.Namespace], int]]:
    def _handler(args: argparse.Namespace) -> int:
        return run_document_sync_command(
            args,
            command_name=command_name,
            artifact_label=artifact_label,
            service=load_document_sync_service(module_name, class_name),
        )

    _handler.__name__ = f"_run_plan_sync_{handler_key}"
    return handler_key, _handler


def _run_plan_sync_all(args: argparse.Namespace) -> int:
    return run_multi_target_sync(
        args,
        module_name="watchtower_plan.sync.all",
        class_name="AllSyncService",
        command_name="watchtower-core plan sync all",
        human_label="plan sync all",
    )


def _run_plan_sync_coordination(args: argparse.Namespace) -> int:
    return run_multi_target_sync(
        args,
        module_name="watchtower_plan.sync.coordination",
        class_name="CoordinationSyncService",
        command_name="watchtower-core plan sync coordination",
        human_label="plan sync coordination",
    )


def _run_plan_sync_initiative_tracking(args: argparse.Namespace) -> int:
    return run_tracking_sync(
        args,
        module_name="watchtower_plan.sync.initiative_tracking",
        class_name="InitiativeTrackingSyncService",
        command_name="watchtower-core plan sync initiative-tracking",
        payload_counts_factory=lambda result: {
            "initiative_count": result.initiative_count,
            "active_count": result.active_count,
            "closed_count": result.closed_count,
        },
        wrote_message_factory=lambda result, destination: (
            "Rebuilt initiative tracking with "
            f"{result.initiative_count} initiatives and wrote it to {destination}."
        ),
        dry_run_message_factory=lambda result: (
            "Rebuilt initiative tracking with "
            f"{result.initiative_count} initiatives in dry-run mode."
        ),
    )


def _run_plan_sync_task_tracking(args: argparse.Namespace) -> int:
    return run_tracking_sync(
        args,
        module_name="watchtower_plan.sync.task_tracking",
        class_name="TaskTrackingSyncService",
        command_name="watchtower-core plan sync task-tracking",
        payload_counts_factory=lambda result: {
            "task_count": result.task_count,
            "open_count": result.open_count,
            "closed_count": result.closed_count,
        },
        wrote_message_factory=lambda result, destination: (
            f"Rebuilt task tracking with {result.task_count} tasks and wrote it to {destination}."
        ),
        dry_run_message_factory=lambda result: (
            f"Rebuilt task tracking with {result.task_count} tasks in dry-run mode."
        ),
    )


def _run_plan_sync_github_tasks(args: argparse.Namespace) -> int:
    params_class = load_sync_class(
        "watchtower_plan.sync.github_tasks", "GitHubTaskSyncParams"
    )
    service = load_sync_class(
        "watchtower_plan.sync.github_tasks", "GitHubTaskSyncService"
    )(build_loader())
    result = service.sync(
        build_github_task_sync_params(args, params_class),
        write=args.write,
    )
    payload = {
        "command": "watchtower-core plan sync github-tasks",
        "status": "ok" if all(record.success for record in result.records) else "error",
        "wrote": result.wrote,
        "result_count": len(result.records),
        "synced_task_count": result.synced_task_count,
        "local_change_count": result.local_change_count,
        "rebuilt_task_index": result.rebuilt_task_index,
        "rebuilt_task_tracking": result.rebuilt_task_tracking,
        "rebuilt_traceability_index": result.rebuilt_traceability_index,
        "results": [
            {
                "task_id": record.task_id,
                "doc_path": record.doc_path,
                "repository": record.repository,
                "task_status": record.task_status,
                "issue_action": record.issue_action,
                "project_action": record.project_action,
                "success": record.success,
                "message": record.message,
                "github_issue_number": record.github_issue_number,
                "github_issue_url": record.github_issue_url,
                "github_project_item_id": record.github_project_item_id,
                "labels": list(record.labels),
            }
            for record in result.records
        ],
    }
    exit_code = 0 if payload["status"] == "ok" else 1

    def _render_human() -> None:
        if not result.records:
            print("No task entries matched the requested sync filters.")
            return
        for record in result.records:
            state = "ok" if record.success else "error"
            print(f"- {record.task_id} [{state}]")
            print(f"  Issue action: {record.issue_action}")
            if record.project_action is not None:
                print(f"  Project action: {record.project_action}")
            if record.labels:
                print(f"  Labels: {', '.join(record.labels)}")
            if record.github_issue_url is not None:
                print(f"  GitHub Issue: {record.github_issue_url}")
            print(f"  {record.message}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
        exit_code=exit_code,
    )


PLAN_SYNC_HANDLERS: dict[str, Callable[[argparse.Namespace], int]] = {
    "all": _run_plan_sync_all,
    "coordination": _run_plan_sync_coordination,
    "initiative_tracking": _run_plan_sync_initiative_tracking,
    "task_tracking": _run_plan_sync_task_tracking,
    "github_tasks": _run_plan_sync_github_tasks,
    **dict(_build_document_handler(*spec) for spec in _DOCUMENT_HANDLER_SPECS),
}


def _register_materialized_sync_commands(
    sync_subparsers: argparse._SubParsersAction,
    handlers: HandlerMap,
) -> None:
    specs: tuple[SyncCommandSpec, ...] = (
        {
            "name": "all",
            "handler": "all",
            "help": "Rebuild all plan-owned local derived indexes and trackers in dependency order.",
            "description": """
                Rebuild all plan-owned local deterministic sync surfaces in one
                run.

                This includes plan indexes and trackers only. It does not call
                hosted integrations such as GitHub task sync.
                """,
            "examples": (
                "uv run watchtower-core plan sync all",
                "uv run watchtower-core plan sync all --write",
                "uv run watchtower-core plan sync all --output-dir /tmp/watchtower_plan_sync --format json",
            ),
        },
        {
            "name": "coordination",
            "handler": "coordination",
            "help": "Rebuild the deterministic plan coordination slice and compact human tracker.",
            "description": """
                Rebuild the deterministic coordination slice for task,
                traceability, initiative, coordination-index, and compact
                coordination-tracking surfaces in dependency order.

                This is the focused rebuild path for local execution
                coordination without refreshing unrelated reference, standards,
                or command docs.
                """,
            "examples": (
                "uv run watchtower-core plan sync coordination",
                "uv run watchtower-core plan sync coordination --write",
                "uv run watchtower-core plan sync coordination --output-dir "
                "/tmp/watchtower_plan_coordination --format json",
            ),
        },
    )
    for spec in specs:
        parser = sync_subparsers.add_parser(
            spec["name"],
            help=spec["help"],
            description=dedent(spec["description"]).strip(),
            epilog=examples(*spec["examples"]),
            formatter_class=HelpFormatter,
        )
        parser.add_argument(
            "--write",
            action="store_true",
            help="Write rebuilt artifacts and trackers to their canonical repository paths.",
        )
        parser.add_argument(
            "--output-dir",
            type=Path,
            help=(
                "Optional explicit directory for materializing rebuilt surfaces while "
                "preserving repo-relative paths."
            ),
        )
        add_human_json_format_argument(parser)
        parser.set_defaults(handler=handlers[spec["handler"]])


def _register_github_task_sync(sync_subparsers: argparse._SubParsersAction) -> None:
    parser = sync_subparsers.add_parser(
        "github-tasks",
        help="Push local task records to GitHub issues and optional project items.",
        description=dedent(
            """
            Push local-first task records to GitHub in a push-only, local-source
            model.

            Start with dry-run output first. Add `--write` to call the GitHub
            APIs, persist the returned foreign keys on the live task records,
            and rebuild the live task indexes plus companion human trackers.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan sync github-tasks --repo owner/repo",
            "uv run watchtower-core plan sync github-tasks --repo owner/repo "
            "--task-id task.local_task_tracking.github_sync.001 --write",
            "uv run watchtower-core plan sync github-tasks --repo owner/repo "
            "--project-owner owner --project-owner-type organization "
            "--project-number 7 --write --format json",
            "uv run watchtower-core plan sync github-tasks --repo owner/repo "
            "--no-label-sync --write",
        ),
        formatter_class=HelpFormatter,
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "Call the GitHub APIs, persist returned foreign keys locally, and "
            "rebuild derived task surfaces."
        ),
    )
    parser.add_argument(
        "--repo",
        help="GitHub repository in owner/name form. Falls back to task metadata or GITHUB_REPOSITORY.",
    )
    parser.add_argument(
        "--task-id",
        action="append",
        default=[],
        help="Exact live task identifier filter. Repeat for multiple task IDs.",
    )
    parser.add_argument("--trace-id", help="Exact trace filter.")
    parser.add_argument("--task-status", help="Exact task-status filter.")
    parser.add_argument("--priority", help="Exact priority filter.")
    parser.add_argument("--owner", help="Exact owner filter.")
    parser.add_argument("--task-kind", help="Exact task-kind filter.")
    parser.add_argument(
        "--blocked-only",
        action="store_true",
        help="Select only tasks that currently declare blocking task IDs.",
    )
    parser.add_argument(
        "--blocked-by", help="Select only tasks blocked by the given task ID."
    )
    parser.add_argument(
        "--depends-on", help="Select only tasks that depend on the given task ID."
    )
    parser.add_argument(
        "--project-owner",
        help="GitHub project owner login when also syncing to a project.",
    )
    parser.add_argument(
        "--project-owner-type",
        choices=("user", "organization"),
        help="GitHub project owner type when also syncing to a project.",
    )
    parser.add_argument(
        "--project-number",
        type=int,
        help="GitHub project number when also syncing to a project.",
    )
    parser.add_argument(
        "--project-status-field",
        default="Status",
        help="GitHub single-select status field name for project status updates.",
    )
    parser.add_argument(
        "--no-label-sync",
        action="store_true",
        help="Skip the managed GitHub label upsert and label mirroring step.",
    )
    parser.add_argument(
        "--token-env",
        default="GITHUB_TOKEN",
        help="Environment variable that holds the GitHub token used for write mode.",
    )
    add_human_json_format_argument(parser)
    parser.set_defaults(handler=_run_plan_sync_github_tasks)


def register_plan_sync_commands(plan_subparsers: argparse._SubParsersAction) -> None:
    """Register the pack-owned `plan sync` namespace."""

    sync_parser = plan_subparsers.add_parser(
        "sync",
        help="Rebuild plan-owned derived indexes, trackers, and orchestration slices.",
        description=dedent(
            """
            Rebuild plan-owned derived indexes, trackers, and orchestration
            slices from authored pack surfaces and live plan machine state.

            Start with dry-run output first. Use `--write` only when you intend
            to update canonical plan-owned artifacts.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan sync all",
            "uv run watchtower-core plan sync coordination --write",
            "uv run watchtower-core plan sync reference-index",
            "uv run watchtower-core plan sync initiative-index --write",
            "uv run watchtower-core plan sync task-tracking --format json",
            "uv run watchtower-core plan sync github-tasks --repo owner/repo",
        ),
        formatter_class=HelpFormatter,
    )
    sync_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    sync_subparsers = sync_parser.add_subparsers(
        dest="plan_sync_command",
        title="sync commands",
        metavar="<sync_command>",
    )
    sync_parser.set_defaults(handler=_run_help, help_parser=sync_parser)

    _register_materialized_sync_commands(sync_subparsers, PLAN_SYNC_HANDLERS)
    register_spec_sync_commands(
        sync_subparsers, handlers=PLAN_SYNC_HANDLERS, specs=_DOCUMENT_COMMAND_SPECS
    )
    register_spec_sync_commands(
        sync_subparsers, handlers=PLAN_SYNC_HANDLERS, specs=_TRACKING_COMMAND_SPECS
    )
    _register_github_task_sync(sync_subparsers)


__all__ = [
    "IMPLEMENTATION_PATH",
    "PLAN_SYNC_HANDLERS",
    "register_plan_sync_commands",
]
