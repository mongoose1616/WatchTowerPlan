"""Registration helpers for coordination-oriented query subcommands."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.query_coordination_handlers import (
    _run_query_coordination,
    _run_query_initiatives,
    _run_query_tasks,
    _run_query_trace,
)


def register_query_coordination_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register coordination-oriented query commands."""
    query_tasks_parser = query_subparsers.add_parser(
        "tasks",
        help="Search the task index.",
        description=dedent(
            """
            Search the task index for local-first task records.

            Use this when you need to find work by task status, owner, trace,
            priority, task kind, or free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query tasks --task-status backlog",
            (
                "uv run watchtower-core query tasks "
                "--blocked-by task.local_task_tracking.github_sync.001"
            ),
            "uv run watchtower-core query tasks --trace-id trace.local_task_tracking --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_tasks_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed task fields such as IDs, title, "
            "summary, owner, related IDs, and applies-to paths."
        ),
    )
    query_tasks_parser.add_argument(
        "--task-id",
        action="append",
        default=[],
        help="Exact task identifier filter. Repeat for multiple task IDs.",
    )
    query_tasks_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.local_task_tracking.",
    )
    query_tasks_parser.add_argument(
        "--task-status",
        help="Exact task-status filter such as backlog, in_progress, or done.",
    )
    query_tasks_parser.add_argument(
        "--priority",
        help="Exact priority filter such as critical, high, medium, or low.",
    )
    query_tasks_parser.add_argument(
        "--owner",
        help="Exact owner filter such as repository_maintainer.",
    )
    query_tasks_parser.add_argument(
        "--task-kind",
        help="Exact task-kind filter such as feature, bug, or chore.",
    )
    query_tasks_parser.add_argument(
        "--blocked-only",
        action="store_true",
        help="Return only tasks that list one or more blocking task IDs.",
    )
    query_tasks_parser.add_argument(
        "--blocked-by",
        help="Return only tasks blocked by the given task ID.",
    )
    query_tasks_parser.add_argument(
        "--depends-on",
        help="Return only tasks that depend on the given task ID.",
    )
    query_tasks_parser.add_argument(
        "--include-dependency-details",
        action="store_true",
        help="Include forward and reverse dependency detail in the result payload or human output.",
    )
    query_tasks_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_tasks_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_tasks_parser.set_defaults(handler=_run_query_tasks)

    query_coordination_parser = query_subparsers.add_parser(
        "coordination",
        help="Start with the current planning coordination view.",
        description=dedent(
            """
            Search the coordination index through the machine start-here
            path for current planning state.

            By default this command returns active initiatives only. Use
            `initiatives` for broader family lookup or pass `--initiative-status`
            explicitly when you want a narrower historical state.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query coordination",
            "uv run watchtower-core query coordination --blocked-only --format json",
            "uv run watchtower-core query coordination --initiative-status completed "
            "--trace-id trace.core_python_foundation",
        ),
        formatter_class=HelpFormatter,
    )
    query_coordination_parser.add_argument(
        "--query",
        help=(
            "Free-text query over coordination fields such as trace ID, title, "
            "next action, and active task summaries."
        ),
    )
    query_coordination_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_coordination_parser.add_argument(
        "--initiative-status",
        help=(
            "Exact initiative-status filter such as active, completed, or superseded. "
            "Defaults to active when omitted."
        ),
    )
    query_coordination_parser.add_argument(
        "--current-phase",
        help="Exact current-phase filter such as prd, execution, or closeout.",
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
    query_coordination_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_coordination_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
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
            `coordination` path.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query initiatives --current-phase execution",
            "uv run watchtower-core query initiatives --blocked-only --format json",
            "uv run watchtower-core query initiatives --trace-id trace.core_python_foundation",
        ),
        formatter_class=HelpFormatter,
    )
    query_initiatives_parser.add_argument(
        "--query",
        help=(
            "Free-text query over initiative fields such as trace ID, title, "
            "summary, owner, next action, and linked artifact IDs."
        ),
    )
    query_initiatives_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_initiatives_parser.add_argument(
        "--initiative-status",
        help="Exact initiative-status filter such as active or completed.",
    )
    query_initiatives_parser.add_argument(
        "--current-phase",
        help="Exact current-phase filter such as prd, execution, or closeout.",
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
    query_initiatives_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_initiatives_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_initiatives_parser.set_defaults(handler=_run_query_initiatives)

    query_trace_parser = query_subparsers.add_parser(
        "trace",
        help="Resolve one traceability record by trace ID.",
        description=dedent(
            """
            Resolve one traceability record by its stable trace identifier.

            Use this when you already know the trace you want and need the
            linked PRD, decision, design, plan, task, validator, or evidence IDs.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query trace --trace-id trace.core_python_foundation",
            "uv run watchtower-core query trace --trace-id "
            "trace.core_python_foundation --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_trace_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.core_python_foundation.",
    )
    query_trace_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_trace_parser.set_defaults(handler=_run_query_trace)
