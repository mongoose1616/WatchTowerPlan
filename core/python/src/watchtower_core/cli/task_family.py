"""Task command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples


def register_task_family(subparsers: argparse._SubParsersAction) -> None:
    """Register the task command family and its subcommands."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_core.cli.task_handlers import (
        _run_task_create,
        _run_task_transition,
        _run_task_update,
    )
    from watchtower_core.repo_ops.task_lifecycle import (
        TASK_KIND_CHOICES,
        TASK_PRIORITY_CHOICES,
        TASK_STATUS_CHOICES,
    )

    task_parser = subparsers.add_parser(
        "task",
        help="Create, update, and transition governed local task records.",
        description=dedent(
            """
            Create, update, and transition governed local task records while
            keeping task documents authoritative and refreshing the derived
            coordination slice on write.

            These commands are dry-run by default. Add `--write` to persist the
            task change and rebuild the dependent task, traceability,
            initiative, and coordination surfaces.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core task create --task-id task.example.001 "
            "--title \"Draft the example\" --summary \"Creates the example task.\" "
            "--task-kind documentation --priority medium --owner repository_maintainer "
            "--scope \"Write the example\" --done-when \"The example exists\"",
            "uv run watchtower-core task update --task-id task.example.001 "
            "--task-status in_progress --owner implementation_engineer --format json",
            "uv run watchtower-core task transition --task-id task.example.001 "
            "--task-status done --write",
        ),
        formatter_class=HelpFormatter,
    )
    task_subparsers = task_parser.add_subparsers(
        dest="task_command",
        title="task commands",
        metavar="<task_command>",
    )
    task_parser.set_defaults(handler=_run_help, help_parser=task_parser)

    create_parser = task_subparsers.add_parser(
        "create",
        help="Create one governed local task document.",
        description=dedent(
            """
            Create one governed local task document from compact structured
            inputs.

            The task document stays authoritative. On write, the coordination
            slice is refreshed so task, traceability, initiative, and
            coordination views stay aligned.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core task create --task-id task.example.001 "
            "--title \"Draft the example\" --summary \"Creates the example task.\" "
            "--task-kind documentation --priority medium --owner repository_maintainer "
            "--scope \"Write the example\" --done-when \"The example exists\"",
            "uv run watchtower-core task create --task-id task.traceable.example.001 "
            "--trace-id trace.example --title \"Implement the slice\" "
            "--summary \"Implements the bounded slice.\" --task-kind feature "
            "--priority high --owner implementation_engineer --applies-to core/python/src/ "
            "--related-id design.features.example --scope \"Ship the slice\" "
            "--done-when \"Tests pass\" --format json",
        ),
        formatter_class=HelpFormatter,
    )
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
        default="backlog",
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
        help="Write the task document and refresh the coordination slice.",
    )
    create_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    create_parser.set_defaults(handler=_run_task_create)

    update_parser = task_subparsers.add_parser(
        "update",
        help="Apply structured field updates to one governed task document.",
        description=dedent(
            """
            Update one governed task document without hand-editing front matter.

            Replacement list flags overwrite the current values. Use the
            matching clear flag when you want to remove a list field or
            `trace_id`.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core task update --task-id task.example.001 "
            "--task-status in_progress --owner implementation_engineer",
            "uv run watchtower-core task update --task-id task.example.001 "
            "--blocked-by task.other.001 --depends-on task.other.001 --write",
            "uv run watchtower-core task update --task-id task.example.001 "
            "--clear-blocked-by --clear-depends-on --format json",
        ),
        formatter_class=HelpFormatter,
    )
    update_parser.add_argument("--task-id", required=True, help="Stable task identifier.")
    update_parser.add_argument("--trace-id", help="Replacement trace identifier.")
    update_parser.add_argument(
        "--clear-trace-id",
        action="store_true",
        help="Remove the current trace identifier.",
    )
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
        "--file-stem",
        help="Optional replacement filename stem. The task ID stays authoritative.",
    )
    update_parser.add_argument(
        "--updated-at",
        help="Optional explicit RFC 3339 UTC timestamp. Defaults to now when changes occur.",
    )
    update_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the updated task document and refresh the coordination slice.",
    )
    update_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    update_parser.set_defaults(handler=_run_task_update)

    transition_parser = task_subparsers.add_parser(
        "transition",
        help="Apply a handoff-style task status or ownership transition.",
        description=dedent(
            """
            Apply a bounded handoff-style transition to one task by updating the
            task status, owner, or blocker state while preserving task-document
            authority.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core task transition --task-id task.example.001 "
            "--task-status in_review --next-owner validation_engineer",
            "uv run watchtower-core task transition --task-id task.example.001 "
            "--task-status done --clear-blocked-by --clear-depends-on --write",
        ),
        formatter_class=HelpFormatter,
    )
    transition_parser.add_argument("--task-id", required=True, help="Stable task identifier.")
    transition_parser.add_argument(
        "--task-status",
        required=True,
        choices=TASK_STATUS_CHOICES,
        help="Next task execution status.",
    )
    transition_parser.add_argument("--next-owner", help="Optional next responsible owner.")
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
        "--file-stem",
        help="Optional replacement filename stem when the transition also moves the file.",
    )
    transition_parser.add_argument(
        "--updated-at",
        help="Optional explicit RFC 3339 UTC timestamp. Defaults to now when changes occur.",
    )
    transition_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the transitioned task document and refresh the coordination slice.",
    )
    transition_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    transition_parser.set_defaults(handler=_run_task_transition)
