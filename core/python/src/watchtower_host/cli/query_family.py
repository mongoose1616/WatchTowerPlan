"""Query command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.handler_common import _run_help
from watchtower_host.cli.query_discovery_family import register_query_discovery_commands
from watchtower_host.cli.query_knowledge_family import register_query_knowledge_commands
from watchtower_host.cli.query_records_family import register_query_record_commands


def register_query_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the query command family and its subcommands."""
    query_parser = subparsers.add_parser(
        "query",
        help="Search shared governed lookup surfaces for commands, docs, and durable records.",
        description=dedent(
            """
            Search the governed lookup surfaces without opening the raw JSON
            artifacts directly.

            Use `paths` for repository navigation, `commands` for CLI discovery,
            `foundations` for the intent-layer foundation corpus, `workflows`
            for workflow-module lookup, `references` for the reference library,
            `standards` for governed repository standards, `acceptance` for
            governed acceptance contracts, and `evidence` for durable validation
            proof.

            Live plan-workspace queries now live under
            `watchtower-core plan query ...`.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query paths --query control plane",
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core query foundations --query philosophy",
            "uv run watchtower-core query workflows --related-path "
            "core/docs/standards/documentation/workflow_md_standard.md",
            "uv run watchtower-core query references --query github",
            "uv run watchtower-core query standards --reference-path "
            "core/docs/references/github_collaboration_reference.md",
            "uv run watchtower-core query acceptance --trace-id trace.governed_acceptance_example",
            "uv run watchtower-core query evidence --trace-id trace.governed_acceptance_example",
            "uv run watchtower-core plan query coordination --format json",
            "uv run watchtower-core plan query tasks --task-status planned --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_subparsers = query_parser.add_subparsers(
        dest="query_command",
        title="query commands",
        metavar="<query_command>",
    )
    query_parser.set_defaults(handler=_run_help, help_parser=query_parser)

    register_query_discovery_commands(query_subparsers)
    register_query_knowledge_commands(query_subparsers)
    register_query_record_commands(query_subparsers)
