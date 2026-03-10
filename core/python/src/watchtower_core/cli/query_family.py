"""Query command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.handler_common import _run_help
from watchtower_core.cli.query_coordination_family import (
    register_query_coordination_commands,
)
from watchtower_core.cli.query_discovery_family import register_query_discovery_commands
from watchtower_core.cli.query_knowledge_family import register_query_knowledge_commands
from watchtower_core.cli.query_records_family import register_query_record_commands


def register_query_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the query command family and its subcommands."""
    query_parser = subparsers.add_parser(
        "query",
        help="Search governed indexes for paths, commands, planning docs, tasks, and traces.",
        description=dedent(
            """
            Search the governed lookup surfaces without opening the raw JSON
            artifacts directly.

            Use `paths` for repository navigation, `commands` for CLI discovery,
            `coordination` for the machine start-here planning view, `foundations`
            for the intent-layer foundation corpus, `workflows` for workflow-module
            lookup, `references` for the reference library, `standards` for governed
            repository standards, `prds`, `decisions`, `designs`, `acceptance`,
            `evidence`, and `tasks` for planning and execution lookup,
            `initiatives` for broader initiative-family lookup including history,
            and `trace` when you already know the trace identifier you want.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query paths --query control plane",
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core query coordination --format json",
            "uv run watchtower-core query foundations --query philosophy",
            "uv run watchtower-core query workflows --related-path "
            "docs/standards/documentation/workflow_md_standard.md",
            "uv run watchtower-core query references --query github",
            "uv run watchtower-core query standards --reference-path "
            "docs/references/github_collaboration_reference.md",
            "uv run watchtower-core query prds --trace-id trace.core_python_foundation",
            "uv run watchtower-core query initiatives --owner repository_maintainer",
            "uv run watchtower-core query decisions --decision-status accepted",
            "uv run watchtower-core query designs --family implementation_plan",
            "uv run watchtower-core query acceptance --trace-id trace.core_python_foundation",
            "uv run watchtower-core query evidence --trace-id trace.core_python_foundation",
            "uv run watchtower-core query tasks --task-status backlog",
            "uv run watchtower-core query tasks --blocked-only --include-dependency-details",
            "uv run watchtower-core query trace --trace-id trace.core_python_foundation",
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
    register_query_coordination_commands(query_subparsers)
