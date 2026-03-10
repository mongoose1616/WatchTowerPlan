"""Registration helpers for discovery-oriented query subcommands."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.query_discovery_handlers import (
    _run_query_commands,
    _run_query_paths,
)


def register_query_discovery_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register discovery-oriented query commands."""
    query_paths_parser = query_subparsers.add_parser(
        "paths",
        help="Search the repository path index.",
        description=dedent(
            """
            Search the repository path index by free text or exact filters.

            Omit `--query` to browse by surface kind, tag, or parent path.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query paths --query command",
            "uv run watchtower-core query paths --maturity authoritative --priority high",
            "uv run watchtower-core query paths --surface-kind command_doc --limit 5 --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_paths_parser.add_argument(
        "--query",
        help="Free-text query over indexed path fields such as path, summary, aliases, and tags.",
    )
    query_paths_parser.add_argument(
        "--surface-kind",
        help="Exact surface-kind filter such as command_doc, standard_doc, or control_plane_index.",
    )
    query_paths_parser.add_argument(
        "--maturity",
        help="Exact retrieval-maturity filter such as authoritative, supporting, or scaffold.",
    )
    query_paths_parser.add_argument(
        "--priority",
        help="Exact retrieval-priority filter such as high, medium, or low.",
    )
    query_paths_parser.add_argument(
        "--audience-hint",
        help="Exact audience-hint filter such as shared, automation, or maintainer.",
    )
    query_paths_parser.add_argument("--tag", help="Exact tag filter.")
    query_paths_parser.add_argument(
        "--parent-path",
        help="Exact parent-path filter such as docs/commands/core_python/.",
    )
    query_paths_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_paths_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_paths_parser.set_defaults(handler=_run_query_paths)

    query_commands_parser = query_subparsers.add_parser(
        "commands",
        help="Search the command index.",
        description=dedent(
            """
            Search the command index for documented repository commands and
            subcommands.

            Use this when you know what task you want to perform but do not yet
            know the exact command name.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query commands --query doctor",
            "uv run watchtower-core query commands --tag query --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_commands_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed command fields such as command name, "
            "summary, synopsis, or aliases."
        ),
    )
    query_commands_parser.add_argument(
        "--kind",
        help="Exact command-kind filter such as root_command or subcommand.",
    )
    query_commands_parser.add_argument("--tag", help="Exact tag filter.")
    query_commands_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_commands_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_commands_parser.set_defaults(handler=_run_query_commands)
