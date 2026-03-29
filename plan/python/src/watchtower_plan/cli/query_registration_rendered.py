"""Rendered-surface parser registration for `watchtower-core plan query`."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, add_query_argument, examples
from watchtower_plan.cli.query_common import IMPLEMENTATION_PATH, add_output_arguments
from watchtower_plan.cli.query_rendered_handlers import (
    _run_query_coordination,
    _run_query_initiatives,
)


def register_rendered_query_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register the rendered-surface `plan query` leaf commands."""

    query_coordination_parser = query_subparsers.add_parser(
        "coordination",
        help="Start with the current planning coordination view.",
        description=dedent(
            """
            Search the coordination index through the machine start-here
            path for live current planning state.

            By default this command returns active initiatives only. Use
            `initiatives` for broader family lookup or pass `--initiative-status`
            explicitly when you want a narrower historical state.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query coordination",
            "uv run watchtower-core plan query coordination --blocked-only --format json",
            "uv run watchtower-core plan query coordination --initiative-status completed "
            "--trace-id trace.governed_acceptance_example",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_coordination_parser,
        help_text=(
            "Free-text query over coordination fields such as trace ID, "
            "title, next action, and active task summaries."
        ),
    )
    query_coordination_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.governed_acceptance_example.",
    )
    query_coordination_parser.add_argument(
        "--initiative-status",
        help=(
            "Exact initiative-status filter such as active, completed, or "
            "superseded. Defaults to active when omitted."
        ),
    )
    query_coordination_parser.add_argument(
        "--current-phase",
        help=(
            "Exact current-phase filter such as capture, execution, closeout, "
            "or closed."
        ),
    )
    query_coordination_parser.add_argument(
        "--owner",
        help="Exact owner filter against the current active owners for the initiative.",
    )
    query_coordination_parser.add_argument(
        "--blocked-only",
        action="store_true",
        help="Return only initiatives with one or more currently blocked active tasks.",
    )
    add_output_arguments(query_coordination_parser)
    query_coordination_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_coordination_parser.set_defaults(handler=_run_query_coordination)

    query_initiatives_parser = query_subparsers.add_parser(
        "initiatives",
        help="Search the initiative index.",
        description=dedent(
            """
            Search the cross-family initiative index for the current phase,
            active ownership, blockers, and next step of a traced initiative.

            Use this when you need broader initiative-family lookup or
            historical closed-state inspection beyond the start-here
            `coordination` path. When invoked with no explicit filters, it
            defaults to active initiatives; use `--initiative-status` for
            explicit history browsing.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query initiatives --current-phase execution",
            "uv run watchtower-core plan query initiatives --blocked-only --format json",
            "uv run watchtower-core plan query initiatives --trace-id "
            "trace.governed_acceptance_example",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_initiatives_parser,
        help_text=(
            "Free-text query over initiative fields such as trace ID, title, "
            "summary, owner, next action, and linked artifact IDs."
        ),
    )
    query_initiatives_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.governed_acceptance_example.",
    )
    query_initiatives_parser.add_argument(
        "--initiative-status",
        help=(
            "Exact initiative-status filter such as active or completed. "
            "When omitted for filterless browse, the command defaults to active."
        ),
    )
    query_initiatives_parser.add_argument(
        "--current-phase",
        help=(
            "Exact current-phase filter such as capture, execution, closeout, "
            "or closed."
        ),
    )
    query_initiatives_parser.add_argument(
        "--owner",
        help="Exact owner filter against the current active owners for the initiative.",
    )
    query_initiatives_parser.add_argument(
        "--blocked-only",
        action="store_true",
        help="Return only initiatives with one or more currently blocked active tasks.",
    )
    add_output_arguments(query_initiatives_parser)
    query_initiatives_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_initiatives_parser.set_defaults(handler=_run_query_initiatives)
