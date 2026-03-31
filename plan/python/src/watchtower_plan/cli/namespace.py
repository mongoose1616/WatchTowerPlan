"""Pack-owned registration for the `watchtower-core plan` namespace."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)

IMPLEMENTATION_PATH = "plan/python/src/watchtower_plan/cli/namespace.py"
SUBCOMMAND_IMPLEMENTATION_PATH = "plan/python/src/watchtower_plan/cli/handlers.py"
_PLAN_SUBCOMMANDS = frozenset(
    {
        "approve",
        "bootstrap",
        "closeout",
        "confirm-inputs",
        "query",
        "sync",
        "task",
    }
)


def _run_plan_bootstrap(args: argparse.Namespace) -> int:
    from watchtower_plan.cli.handlers import _run_plan_bootstrap as _delegate

    return _delegate(args)


def _run_plan_confirm_inputs(args: argparse.Namespace) -> int:
    from watchtower_plan.cli.handlers import _run_plan_confirm_inputs as _delegate

    return _delegate(args)


def _run_plan_approve(args: argparse.Namespace) -> int:
    from watchtower_plan.cli.handlers import _run_plan_approve as _delegate

    return _delegate(args)


def _selected_plan_subcommand(selected_subcommand: str | None) -> str | None:
    if selected_subcommand in _PLAN_SUBCOMMANDS:
        return selected_subcommand
    return None


def _should_register_plan_command(
    selected_subcommand: str | None,
    command_name: str,
) -> bool:
    return selected_subcommand is None or selected_subcommand == command_name


def register_plan_namespace(
    subparsers: argparse._SubParsersAction,
    *,
    selected_subcommand: str | None = None,
) -> None:
    """Register the pack-owned `plan` namespace."""

    from watchtower_core.cli.handler_common import _run_help
    from watchtower_plan.tasks import TASK_KIND_CHOICES, TASK_PRIORITY_CHOICES
    active_subcommand = _selected_plan_subcommand(selected_subcommand)

    plan_parser = subparsers.add_parser(
        "plan",
        help="Bootstrap live initiative packages and advance readiness gates.",
        description=dedent(
            """
            Bootstrap live initiative packages, inspect live plan state, and
            advance initiative readiness through the captured-input and approval
            gates.

            These commands are dry-run by default. Add `--write` to persist the
            initiative-state change and refresh the derived plan surfaces.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan bootstrap --trace-id trace.example "
            '--title "Example Initiative" '
            '--summary "Bootstraps the example initiative." --format json',
            "uv run watchtower-core plan query coordination --format json",
            "uv run watchtower-core plan sync coordination --format json",
            "uv run watchtower-core plan approve --initiative-slug example_initiative --write",
        ),
        formatter_class=HelpFormatter,
    )
    plan_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    plan_subparsers = plan_parser.add_subparsers(
        dest="plan_command",
        title="plan commands",
        metavar="<plan_command>",
    )
    plan_parser.set_defaults(handler=_run_help, help_parser=plan_parser)

    if _should_register_plan_command(active_subcommand, "query"):
        from watchtower_plan.cli.query import register_plan_query_commands

        register_plan_query_commands(plan_subparsers)
    if _should_register_plan_command(active_subcommand, "sync"):
        from watchtower_plan.cli.sync import register_plan_sync_commands

        register_plan_sync_commands(plan_subparsers)

    if _should_register_plan_command(active_subcommand, "bootstrap"):
        bootstrap_parser = plan_subparsers.add_parser(
            "bootstrap",
            help="Bootstrap one live initiative package and its initial bootstrap task.",
            description=dedent(
                """
                Bootstrap one live initiative package rooted under `plan/**`.

                The bootstrap flow seeds the initiative-authored inputs,
                initiative-local machine state, evidence and closeout shells, and
                one bootstrap task. Add `--include-decision` when you want
                `decision_notes.md` in the initial package.
                """
            ).strip(),
            epilog=examples(
                "uv run watchtower-core plan bootstrap --trace-id trace.example "
                '--title "Example Initiative" --summary "Bootstraps the example initiative."',
                "uv run watchtower-core plan bootstrap --trace-id trace.example "
                '--title "Example Initiative" --summary "Bootstraps the example initiative." '
                "--include-decision --task-priority high --write --format json",
                "uv run watchtower-core plan bootstrap --project-slug watchtower "
                '--trace-id trace.watchtower.example --title "WatchTower Initiative" '
                '--summary "Bootstraps a project-scoped initiative." --write',
            ),
            formatter_class=HelpFormatter,
        )
        bootstrap_parser.set_defaults(_implementation_path=SUBCOMMAND_IMPLEMENTATION_PATH)
        bootstrap_parser.add_argument(
            "--trace-id", required=True, help="Stable trace identifier."
        )
        bootstrap_parser.add_argument(
            "--initiative-slug",
            help="Optional initiative slug. Defaults to a slug derived from the trace ID.",
        )
        bootstrap_parser.add_argument(
            "--project-slug",
            help="Optional project slug for project-scoped initiative bootstrap.",
        )
        bootstrap_parser.add_argument(
            "--title", required=True, help="Initiative title root."
        )
        bootstrap_parser.add_argument(
            "--summary",
            required=True,
            help="One-line initiative summary applied to the live package.",
        )
        bootstrap_parser.add_argument(
            "--owner",
            default="repository_maintainer",
            help="Initiative owner recorded in authored inputs and task state.",
        )
        bootstrap_parser.add_argument(
            "--include-decision",
            action="store_true",
            help="Also create `decision_notes.md` in the initial package.",
        )
        bootstrap_parser.add_argument(
            "--governing-doc",
            action="append",
            default=[],
            help="Additional governing Markdown document path. Repeat for multiple values.",
        )
        bootstrap_parser.add_argument(
            "--task-id",
            help="Optional explicit bootstrap task ID. Defaults to task.<trace_suffix>.bootstrap.001.",
        )
        bootstrap_parser.add_argument(
            "--task-owner",
            help="Optional bootstrap task owner. Defaults to --owner.",
        )
        bootstrap_parser.add_argument(
            "--task-kind",
            choices=TASK_KIND_CHOICES,
            default="governance",
            help="Bootstrap task kind.",
        )
        bootstrap_parser.add_argument(
            "--task-priority",
            choices=TASK_PRIORITY_CHOICES,
            default="medium",
            help="Bootstrap task priority.",
        )
        bootstrap_parser.add_argument(
            "--updated-at",
            help="Optional explicit RFC 3339 UTC timestamp. Defaults to now.",
        )
        bootstrap_parser.add_argument(
            "--write",
            action="store_true",
            help="Write the initiative package and refresh derived plan surfaces.",
        )
        add_human_json_format_argument(bootstrap_parser)
        bootstrap_parser.set_defaults(handler=_run_plan_bootstrap)

    if _should_register_plan_command(active_subcommand, "confirm-inputs"):
        confirm_inputs_parser = plan_subparsers.add_parser(
            "confirm-inputs",
            help="Confirm authored initiative inputs into machine state.",
            description=dedent(
                """
                Confirm the current initiative-authored inputs into machine state
                after review so the readiness gate reflects the latest captured
                package before execution approval.
                """
            ).strip(),
            epilog=examples(
                "uv run watchtower-core plan confirm-inputs --initiative-slug example_initiative",
                "uv run watchtower-core plan confirm-inputs --project-slug watchtower "
                "--initiative-slug watchtower_work_item_notes --write --format json",
            ),
            formatter_class=HelpFormatter,
        )
        confirm_inputs_parser.set_defaults(
            _implementation_path=SUBCOMMAND_IMPLEMENTATION_PATH
        )
        confirm_inputs_parser.add_argument(
            "--initiative-slug",
            required=True,
            help="Initiative slug such as example_initiative or watchtower_work_item_notes.",
        )
        confirm_inputs_parser.add_argument(
            "--project-slug",
            help="Project slug when the initiative is project-scoped, such as watchtower.",
        )
        confirm_inputs_parser.add_argument(
            "--actor-id",
            default="actor.repository_maintainer",
            help="Approver actor identifier used for the confirmation event.",
        )
        confirm_inputs_parser.add_argument(
            "--write",
            action="store_true",
            help="Persist the confirmation state and refresh derived plan surfaces.",
        )
        add_human_json_format_argument(confirm_inputs_parser)
        confirm_inputs_parser.set_defaults(handler=_run_plan_confirm_inputs)

    if _should_register_plan_command(active_subcommand, "approve"):
        approve_parser = plan_subparsers.add_parser(
            "approve",
            help="Approve one live initiative package for execution.",
            description=dedent(
                """
                Approve one validated live initiative package into
                ready_for_execution so task transitions can begin real execution
                without violating the hard no-start gate.
                """
            ).strip(),
            epilog=examples(
                "uv run watchtower-core plan approve --initiative-slug example_initiative",
                "uv run watchtower-core plan approve --project-slug watchtower "
                "--initiative-slug watchtower_work_item_notes --write --format json",
            ),
            formatter_class=HelpFormatter,
        )
        approve_parser.set_defaults(_implementation_path=SUBCOMMAND_IMPLEMENTATION_PATH)
        approve_parser.add_argument(
            "--initiative-slug",
            required=True,
            help="Initiative slug such as example_initiative or watchtower_work_item_notes.",
        )
        approve_parser.add_argument(
            "--project-slug",
            help="Project slug when the initiative is project-scoped, such as watchtower.",
        )
        approve_parser.add_argument(
            "--actor-id",
            default="actor.repository_maintainer",
            help="Approver actor identifier used for the approval event.",
        )
        approve_parser.add_argument(
            "--write",
            action="store_true",
            help="Persist the approval state and refresh derived plan surfaces.",
        )
        add_human_json_format_argument(approve_parser)
        approve_parser.set_defaults(handler=_run_plan_approve)

    if _should_register_plan_command(active_subcommand, "closeout"):
        from watchtower_plan.cli.closeout import register_plan_closeout_commands

        register_plan_closeout_commands(plan_subparsers)
    if _should_register_plan_command(active_subcommand, "task"):
        from watchtower_plan.cli.tasks import register_plan_task_commands

        register_plan_task_commands(plan_subparsers)


__all__ = [
    "IMPLEMENTATION_PATH",
    "SUBCOMMAND_IMPLEMENTATION_PATH",
    "register_plan_namespace",
]
