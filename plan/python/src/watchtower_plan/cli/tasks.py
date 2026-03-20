"""Pack-owned `watchtower-core plan task` registration and handlers."""

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
from watchtower_plan.task_lifecycle import (
    TASK_KIND_CHOICES,
    TASK_PRIORITY_CHOICES,
    TASK_STATUS_CHOICES,
    TaskCreateParams,
    TaskLifecycleService,
    TaskMutationResult,
    TaskTransitionParams,
    TaskUpdateParams,
)

IMPLEMENTATION_PATH = "plan/python/src/watchtower_plan/cli/tasks.py"


def register_plan_task_commands(plan_subparsers: argparse._SubParsersAction) -> None:
    """Register the pack-owned `plan task` namespace."""

    task_parser = plan_subparsers.add_parser(
        "task",
        help="Create, update, and transition initiative-local live task records.",
        description=dedent(
            """
            Create, update, and transition initiative-local live task records
            under `plan/**/.wt/tasks/**` while refreshing the derived
            plan-workspace and coordination surfaces on write.

            These commands are dry-run by default. Add `--write` to persist the
            task change and rebuild the dependent live indexes, rendered views,
            and coordination surfaces.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan task create --task-id task.example.001 "
            "--title \"Draft the example\" --summary \"Creates the example task.\" "
            "--task-kind documentation --priority medium --owner repository_maintainer "
            "--scope \"Write the example\" --done-when \"The example exists\"",
            "uv run watchtower-core plan task update --task-id task.example.001 "
            "--task-status in_progress --owner implementation_engineer --format json",
            "uv run watchtower-core plan task transition --task-id task.example.001 "
            "--task-status completed --write",
        ),
        formatter_class=HelpFormatter,
    )
    task_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    task_subparsers = task_parser.add_subparsers(
        dest="task_command",
        title="task commands",
        metavar="<task_command>",
    )
    task_parser.set_defaults(handler=_run_help, help_parser=task_parser)

    create_parser = task_subparsers.add_parser(
        "create",
        help="Create one initiative-local live task record.",
        description=dedent(
            """
            Create one initiative-local live task record from compact
            structured inputs.

            The live task state stays authoritative. On write, the plan
            workspace and coordination surfaces are refreshed so task,
            readiness, initiative, and overview views stay aligned.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan task create --task-id task.example.001 "
            "--title \"Draft the example\" --summary \"Creates the example task.\" "
            "--task-kind documentation --priority medium --owner repository_maintainer "
            "--scope \"Write the example\" --done-when \"The example exists\"",
            "uv run watchtower-core plan task create --task-id task.traceable.example.001 "
            "--trace-id trace.example --title \"Implement the slice\" "
            "--summary \"Implements the bounded slice.\" --task-kind feature "
            "--priority high --owner implementation_engineer --applies-to core/python/src/ "
            "--related-id design.features.example --scope \"Ship the slice\" "
            "--done-when \"Tests pass\" --format json",
        ),
        formatter_class=HelpFormatter,
    )
    create_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    create_parser.add_argument("--task-id", required=True, help="Stable task identifier.")
    create_parser.add_argument("--trace-id", help="Optional trace identifier for linked work.")
    create_parser.add_argument("--title", required=True, help="Human-readable task title.")
    create_parser.add_argument(
        "--summary",
        required=True,
        help="One-line task summary used in trackers and indexes.",
    )
    create_parser.add_argument(
        "--task-kind",
        required=True,
        choices=TASK_KIND_CHOICES,
        help="Governed task kind.",
    )
    create_parser.add_argument(
        "--priority",
        required=True,
        choices=TASK_PRIORITY_CHOICES,
        help="Governed task priority.",
    )
    create_parser.add_argument("--owner", required=True, help="Current task owner.")
    create_parser.add_argument(
        "--task-status",
        choices=TASK_STATUS_CHOICES,
        default="planned",
        help="Initial task execution status.",
    )
    create_parser.add_argument(
        "--scope",
        action="append",
        required=True,
        help="Scope item. Repeat for multiple values.",
    )
    create_parser.add_argument(
        "--done-when",
        action="append",
        required=True,
        help="Completion condition. Repeat for multiple values.",
    )
    create_parser.add_argument(
        "--applies-to",
        action="append",
        default=[],
        help="Optional path or concept the task applies to. Repeat for multiple values.",
    )
    create_parser.add_argument(
        "--related-id",
        action="append",
        default=[],
        help="Optional related planning or governance ID. Repeat for multiple values.",
    )
    create_parser.add_argument(
        "--depends-on",
        action="append",
        default=[],
        help="Optional blocking dependency task ID. Repeat for multiple values.",
    )
    create_parser.add_argument(
        "--blocked-by",
        action="append",
        default=[],
        help="Optional explicit blocker task ID. Repeat for multiple values.",
    )
    create_parser.add_argument(
        "--file-stem",
        help="Optional output filename stem. Defaults to a slug derived from the title.",
    )
    create_parser.add_argument(
        "--updated-at",
        help="Optional explicit RFC 3339 UTC timestamp. Defaults to now.",
    )
    create_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the live task record and refresh the derived plan surfaces.",
    )
    add_human_json_format_argument(create_parser)
    create_parser.set_defaults(handler=_run_task_create)

    update_parser = task_subparsers.add_parser(
        "update",
        help="Apply structured field updates to one live task record.",
        description=dedent(
            """
            Update one initiative-local live task record without hand-editing
            the underlying task JSON.

            Replacement list flags overwrite the current values. Use the
            matching clear flag when you want to remove a list field.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan task update --task-id task.example.001 "
            "--task-status in_progress --owner implementation_engineer",
            "uv run watchtower-core plan task update --task-id task.example.001 "
            "--blocked-by task.other.001 --depends-on task.other.001 --write",
            "uv run watchtower-core plan task update --task-id task.example.001 "
            "--clear-blocked-by --clear-depends-on --format json",
        ),
        formatter_class=HelpFormatter,
    )
    update_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    update_parser.add_argument("--task-id", required=True, help="Stable task identifier.")
    update_parser.add_argument("--title", help="Replacement task title.")
    update_parser.add_argument("--summary", help="Replacement task summary.")
    update_parser.add_argument(
        "--task-kind",
        choices=TASK_KIND_CHOICES,
        help="Replacement governed task kind.",
    )
    update_parser.add_argument(
        "--priority",
        choices=TASK_PRIORITY_CHOICES,
        help="Replacement governed task priority.",
    )
    update_parser.add_argument("--owner", help="Replacement task owner.")
    update_parser.add_argument(
        "--task-status",
        choices=TASK_STATUS_CHOICES,
        help="Replacement task execution status.",
    )
    update_parser.add_argument(
        "--scope",
        action="append",
        default=None,
        help="Replacement scope item. Repeat for multiple values.",
    )
    update_parser.add_argument(
        "--done-when",
        action="append",
        default=None,
        help="Replacement completion condition. Repeat for multiple values.",
    )
    update_parser.add_argument(
        "--applies-to",
        action="append",
        default=None,
        help="Replacement applies-to value. Repeat for multiple values.",
    )
    update_parser.add_argument(
        "--clear-applies-to",
        action="store_true",
        help="Remove the current applies-to list.",
    )
    update_parser.add_argument(
        "--related-id",
        action="append",
        default=None,
        help="Replacement related ID. Repeat for multiple values.",
    )
    update_parser.add_argument(
        "--clear-related-ids",
        action="store_true",
        help="Remove the current related ID list.",
    )
    update_parser.add_argument(
        "--depends-on",
        action="append",
        default=None,
        help="Replacement dependency task ID. Repeat for multiple values.",
    )
    update_parser.add_argument(
        "--clear-depends-on",
        action="store_true",
        help="Remove the current dependency list.",
    )
    update_parser.add_argument(
        "--blocked-by",
        action="append",
        default=None,
        help="Replacement blocker task ID. Repeat for multiple values.",
    )
    update_parser.add_argument(
        "--clear-blocked-by",
        action="store_true",
        help="Remove the current blocker list.",
    )
    update_parser.add_argument(
        "--updated-at",
        help="Optional explicit RFC 3339 UTC timestamp. Defaults to now when changes occur.",
    )
    update_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the updated live task record and refresh the derived plan surfaces.",
    )
    add_human_json_format_argument(update_parser)
    update_parser.set_defaults(handler=_run_task_update)

    transition_parser = task_subparsers.add_parser(
        "transition",
        help="Apply a bounded handoff-style status or ownership change.",
        description=dedent(
            """
            Apply a narrower handoff-style transition over the same governed
            task lifecycle used by the broader update command.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan task transition --task-id task.example.001 "
            "--task-status in_review --next-owner validation_engineer",
            "uv run watchtower-core plan task transition --task-id task.example.001 "
            "--task-status completed --clear-blocked-by --clear-depends-on --write",
        ),
        formatter_class=HelpFormatter,
    )
    transition_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    transition_parser.add_argument("--task-id", required=True, help="Stable task identifier.")
    transition_parser.add_argument(
        "--task-status",
        required=True,
        choices=TASK_STATUS_CHOICES,
        help="Next task execution status.",
    )
    transition_parser.add_argument(
        "--next-owner",
        help="Optional next responsible owner.",
    )
    transition_parser.add_argument(
        "--depends-on",
        action="append",
        default=None,
        help="Replacement dependency task ID. Repeat for multiple values.",
    )
    transition_parser.add_argument(
        "--clear-depends-on",
        action="store_true",
        help="Remove the current dependency list.",
    )
    transition_parser.add_argument(
        "--blocked-by",
        action="append",
        default=None,
        help="Replacement blocker task ID. Repeat for multiple values.",
    )
    transition_parser.add_argument(
        "--clear-blocked-by",
        action="store_true",
        help="Remove the current blocker list.",
    )
    transition_parser.add_argument(
        "--updated-at",
        help="Optional explicit RFC 3339 UTC timestamp. Defaults to now when changes occur.",
    )
    transition_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the transitioned live task record and refresh the derived plan surfaces.",
    )
    add_human_json_format_argument(transition_parser)
    transition_parser.set_defaults(handler=_run_task_transition)


def _run_task_create(args: argparse.Namespace) -> int:
    service = TaskLifecycleService(ControlPlaneLoader())
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core plan task create",
        prefix="Task create error",
        operation=lambda: service.create(
            TaskCreateParams(
                task_id=args.task_id,
                trace_id=args.trace_id,
                title=args.title,
                summary=args.summary,
                task_kind=args.task_kind,
                priority=args.priority,
                owner=args.owner,
                task_status=args.task_status,
                scope_items=tuple(args.scope),
                done_when_items=tuple(args.done_when),
                applies_to=tuple(args.applies_to),
                related_ids=tuple(args.related_id),
                depends_on=tuple(args.depends_on),
                blocked_by=tuple(args.blocked_by),
                file_stem=args.file_stem,
                updated_at=args.updated_at,
            ),
            write=args.write,
        ),
    )
    if result is None:
        return 1
    return _emit_task_result(args, command_name="watchtower-core plan task create", result=result)


def _run_task_update(args: argparse.Namespace) -> int:
    service = TaskLifecycleService(ControlPlaneLoader())
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core plan task update",
        prefix="Task update error",
        operation=lambda: service.update(
            TaskUpdateParams(
                task_id=args.task_id,
                title=args.title,
                summary=args.summary,
                task_kind=args.task_kind,
                priority=args.priority,
                owner=args.owner,
                task_status=args.task_status,
                scope_items=None if args.scope is None else tuple(args.scope),
                done_when_items=None if args.done_when is None else tuple(args.done_when),
                applies_to=None if args.applies_to is None else tuple(args.applies_to),
                clear_applies_to=args.clear_applies_to,
                related_ids=None if args.related_id is None else tuple(args.related_id),
                clear_related_ids=args.clear_related_ids,
                depends_on=None if args.depends_on is None else tuple(args.depends_on),
                clear_depends_on=args.clear_depends_on,
                blocked_by=None if args.blocked_by is None else tuple(args.blocked_by),
                clear_blocked_by=args.clear_blocked_by,
                updated_at=args.updated_at,
            ),
            write=args.write,
        ),
    )
    if result is None:
        return 1
    return _emit_task_result(args, command_name="watchtower-core plan task update", result=result)


def _run_task_transition(args: argparse.Namespace) -> int:
    service = TaskLifecycleService(ControlPlaneLoader())
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core plan task transition",
        prefix="Task transition error",
        operation=lambda: service.transition(
            TaskTransitionParams(
                task_id=args.task_id,
                task_status=args.task_status,
                next_owner=args.next_owner,
                depends_on=None if args.depends_on is None else tuple(args.depends_on),
                clear_depends_on=args.clear_depends_on,
                blocked_by=None if args.blocked_by is None else tuple(args.blocked_by),
                clear_blocked_by=args.clear_blocked_by,
                updated_at=args.updated_at,
            ),
            write=args.write,
        ),
    )
    if result is None:
        return 1
    return _emit_task_result(
        args,
        command_name="watchtower-core plan task transition",
        result=result,
    )


def _emit_task_result(
    args: argparse.Namespace,
    *,
    command_name: str,
    result: TaskMutationResult,
) -> int:
    payload = {
        "command": command_name,
        "status": "ok",
        "task_id": result.task_id,
        "title": result.title,
        "summary": result.summary,
        "trace_id": result.trace_id,
        "task_status": result.task_status,
        "task_kind": result.task_kind,
        "priority": result.priority,
        "owner": result.owner,
        "updated_at": result.updated_at,
        "doc_path": result.doc_path,
        "previous_doc_path": result.previous_doc_path,
        "moved": result.moved,
        "changed": result.changed,
        "wrote": result.wrote,
        "coordination_refreshed": result.coordination_refreshed,
        "closeout_recommended": result.closeout_recommended,
    }

    def _render_human() -> None:
        if not result.changed:
            print(f"No task changes detected for {result.task_id}.")
            print("Use additional flags to change task metadata or body content.")
            return

        action = "Wrote" if result.wrote else "Prepared"
        print(f"{action} task {result.task_id} at {result.doc_path}.")
        print(f"Status: {result.task_status}")
        print(f"Owner: {result.owner}")
        if result.moved and result.previous_doc_path is not None:
            print(f"Moved From: {result.previous_doc_path}")
        if result.closeout_recommended and result.trace_id is not None:
            print(f"Closeout Recommended: {result.trace_id}")
        if result.wrote:
            print("Coordination surfaces were refreshed.")
        else:
            print(
                "Dry-run only. Use --write to persist the task change and refresh coordination."
            )

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


__all__ = ["register_plan_task_commands"]
