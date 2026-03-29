"""Pack-owned registration for the `watchtower-core plan query` namespace."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_plan.cli.query_common import IMPLEMENTATION_PATH
from watchtower_plan.cli.query_registration_indexes import (
    register_index_query_commands,
)
from watchtower_plan.cli.query_registration_lookup import (
    register_lookup_query_commands,
)
from watchtower_plan.cli.query_registration_rendered import (
    register_rendered_query_commands,
)


def register_plan_query_commands(
    plan_subparsers: argparse._SubParsersAction,
) -> None:
    """Register the pack-owned `plan query` command group."""

    from watchtower_core.cli.handler_common import _run_help

    query_parser = plan_subparsers.add_parser(
        "query",
        help="Search live plan state, plan-owned indexes, and retained planning records.",
        description=dedent(
            """
            Search the plan-owned machine lookup surfaces without opening the raw
            JSON artifacts directly.

            Use `coordination` for the machine start-here planning view,
            `initiatives` for broader initiative-family lookup including
            history, `tasks` for initiative-local task execution state,
            `artifacts` for the cross-family plan artifact catalog,
            `readiness` for execution-gate state, `discrepancies` for blocking
            drift or mismatch records, `projects` for pack-level project
            lookup, `project-context` for one fully loaded project container,
            `authority` for canonical planning and governance surface lookup,
            `plan-evidence` for initiative-local evidence bundles, `reviews`
            for initiative or promotion review state, `closeouts` for closeout
            recap state, and `trace` for one retained traceability record.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query coordination --format json",
            "uv run watchtower-core plan query initiatives --current-phase execution",
            "uv run watchtower-core plan query tasks --task-status planned --format json",
            "uv run watchtower-core plan query readiness --ready-for-execution true --format json",
            "uv run watchtower-core plan query authority --domain planning --format json",
            "uv run watchtower-core plan query trace --trace-id "
            "trace.governed_acceptance_example --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_subparsers = query_parser.add_subparsers(
        dest="plan_query_command",
        title="plan query commands",
        metavar="<plan_query_command>",
    )
    query_parser.set_defaults(handler=_run_help, help_parser=query_parser)

    register_lookup_query_commands(query_subparsers)
    register_index_query_commands(query_subparsers)
    register_rendered_query_commands(query_subparsers)
