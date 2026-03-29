"""Lookup-oriented parser registration for `watchtower-core plan query`."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    add_query_argument,
    examples,
)
from watchtower_plan.cli.query_common import (
    IMPLEMENTATION_PATH,
    add_output_arguments,
)
from watchtower_plan.cli.query_lookup_handlers import (
    _run_query_authority,
    _run_query_project_context,
    _run_query_projects,
    _run_query_trace,
)


def register_lookup_query_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register the lookup-oriented `plan query` leaf commands."""

    query_project_context_parser = query_subparsers.add_parser(
        "project-context",
        help="Load the machine-first context for one project container.",
        description=dedent(
            """
            Load one project-scoped runtime context on top of the always-loaded
            pack context.

            Use this when a command, workflow, or implementation step targets
            exactly one project and you need the validated project record,
            initiative root, and linked repository metadata without relying on
            rendered views.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query project-context --project-slug watchtower",
            (
                "uv run watchtower-core plan query project-context "
                "--project-slug watchtower --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    query_project_context_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_project_context_parser.add_argument(
        "--project-slug",
        required=True,
        help="Project slug such as watchtower.",
    )
    add_human_json_format_argument(query_project_context_parser)
    query_project_context_parser.set_defaults(handler=_run_query_project_context)

    query_projects_parser = query_subparsers.add_parser(
        "projects",
        help="Search the live plan project index.",
        description=dedent(
            """
            Search the pack-level project index for project containers and their
            linked repositories.

            Use this when you need project lookup without loading one full
            project context.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query projects --slug watchtower",
            (
                "uv run watchtower-core plan query projects "
                "--repository-role implementation --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_projects_parser,
        help_text=(
            "Free-text query over project fields such as project ID, slug, "
            "title, summary, and repository locators."
        ),
    )
    query_projects_parser.add_argument(
        "--project-id",
        help="Exact project identifier such as project.watchtower.",
    )
    query_projects_parser.add_argument(
        "--slug",
        help="Exact project slug such as watchtower.",
    )
    query_projects_parser.add_argument(
        "--status",
        help="Exact project status filter such as active or planned.",
    )
    query_projects_parser.add_argument(
        "--repository-role",
        help="Exact repository-role filter such as implementation or planning.",
    )
    add_output_arguments(query_projects_parser)
    query_projects_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_projects_parser.set_defaults(handler=_run_query_projects)

    query_authority_parser = query_subparsers.add_parser(
        "authority",
        help="Resolve the canonical machine surface for planning or governance questions.",
        description=dedent(
            """
            Search the authored authority map for canonical planning and
            governance surfaces, preferred commands, and documented fallback
            paths.

            Use this when you know the class of question you need to answer but
            are not sure which machine surface is canonical, or when you need a
            compact policy answer instead of scanning several indexes and docs.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query authority --domain planning",
            (
                "uv run watchtower-core plan query authority --question-id "
                "authority.planning.deep_trace_context --format json"
            ),
            "uv run watchtower-core plan query authority --artifact-kind route_index",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_authority_parser,
        help_text=(
            "Free-text query over authority-map fields such as the question, "
            "canonical path, preferred command, aliases, and fallback paths."
        ),
    )
    query_authority_parser.add_argument(
        "--question-id",
        help="Exact authority question filter such as authority.planning.current_state.",
    )
    query_authority_parser.add_argument(
        "--domain",
        choices=("planning", "governance"),
        help="Exact authority domain filter.",
    )
    query_authority_parser.add_argument(
        "--artifact-kind",
        help="Exact canonical artifact-kind filter such as coordination_index or route_index.",
    )
    add_output_arguments(query_authority_parser)
    query_authority_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_authority_parser.set_defaults(handler=_run_query_authority)

    query_trace_parser = query_subparsers.add_parser(
        "trace",
        help="Resolve one traceability record by trace ID.",
        description=dedent(
            """
            Resolve one traceability record by its stable trace identifier.

            Use this when you already know the trace you want and need the
            linked initiative, decision, design, implementation, task,
            validator, or evidence IDs.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query trace --trace-id "
            "trace.governed_acceptance_example",
            "uv run watchtower-core plan query trace --trace-id "
            "trace.governed_acceptance_example --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_trace_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.governed_acceptance_example.",
    )
    add_human_json_format_argument(query_trace_parser)
    query_trace_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_trace_parser.set_defaults(handler=_run_query_trace)
