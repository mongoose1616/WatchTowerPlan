"""Route command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples


def register_route_family(subparsers: argparse._SubParsersAction) -> None:
    """Register the route command family and its subcommands."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_core.cli.route_handlers import _run_route_preview

    route_parser = subparsers.add_parser(
        "route",
        help="Preview the workflow-module route for a request or explicit task type.",
        description=dedent(
            """
            Preview the workflow modules that the current routing surfaces would
            activate for a request.

            This command is deterministic and advisory. Workflow modules and the
            routing table remain the procedural authority.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core route preview --request "
            "\"review code and commit the change\"",
            "uv run watchtower-core route preview --task-type \"Repository Review\" --format json",
        ),
        formatter_class=HelpFormatter,
    )
    route_subparsers = route_parser.add_subparsers(
        dest="route_command",
        title="route commands",
        metavar="<route_command>",
    )
    route_parser.set_defaults(handler=_run_help, help_parser=route_parser)

    preview_parser = route_subparsers.add_parser(
        "preview",
        help="Preview the route for a request or explicit task type.",
        description=dedent(
            """
            Preview the workflow-module route selected by the current routing
            data.

            Provide either free-form request text or one exact task type.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core route preview --request "
            "\"implement the feature and validate it\"",
            "uv run watchtower-core route preview --task-type \"Task Lifecycle Management\" "
            "--format json",
        ),
        formatter_class=HelpFormatter,
    )
    selection_group = preview_parser.add_mutually_exclusive_group(required=True)
    selection_group.add_argument(
        "--request",
        help="Free-form request text to score against the governed route index.",
    )
    selection_group.add_argument(
        "--task-type",
        help="Exact task type from the governed route index.",
    )
    preview_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    preview_parser.set_defaults(handler=_run_route_preview)
