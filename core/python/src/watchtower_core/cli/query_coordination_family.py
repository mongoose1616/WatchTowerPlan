"""Registration helpers for coordination-oriented query subcommands."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples
from watchtower_core.cli.query_coordination_lookup_handlers import (
    _run_query_authority,
    _run_query_discrepancies,
    _run_query_project_context,
    _run_query_projects,
    _run_query_readiness,
    _run_query_tasks,
    _run_query_trace,
)
from watchtower_core.cli.query_coordination_rendered_handlers import (
    _run_query_coordination,
    _run_query_initiatives,
    _run_query_planning,
)


def register_query_coordination_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register coordination-oriented query commands."""
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
            "uv run watchtower-core query project-context --project-slug watchtower",
            "uv run watchtower-core query project-context --project-slug watchtower --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_project_context_parser.add_argument(
        "--project-slug",
        required=True,
        help="Project slug such as watchtower.",
    )
    query_project_context_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_project_context_parser.set_defaults(handler=_run_query_project_context)

    query_tasks_parser = query_subparsers.add_parser(
        "tasks",
        help="Search the live plan task index.",
        description=dedent(
            """
            Search the live plan task index for initiative-local task records.

            Use this when you need to find work by task status, owner, trace,
            priority, task kind, or free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query tasks --task-status planned",
            (
                "uv run watchtower-core query tasks "
                "--blocked-by task.plan_live_query_authority_cutover."
                "reroot_public_planning_queries_onto_live_plan_indexes"
            ),
            (
                "uv run watchtower-core query tasks "
                "--trace-id trace.plan_live_query_authority_cutover --format json"
            ),
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
        help="Exact trace filter such as trace.plan_live_query_authority_cutover.",
    )
    query_tasks_parser.add_argument(
        "--task-status",
        help=(
            "Exact task-status filter such as planned, ready, in_progress, "
            "blocked, completed, or cancelled."
        ),
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

    query_readiness_parser = query_subparsers.add_parser(
        "readiness",
        help="Search the live plan readiness index.",
        description=dedent(
            """
            Search the readiness-gate index for initiative execution readiness.

            Use this when you need to inspect capture completeness, approval
            state, lifecycle stage, or blocking gate reasons before execution
            starts or resumes.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query readiness --ready-for-execution true",
            (
                "uv run watchtower-core query readiness "
                "--trace-id trace.plan_live_query_authority_cutover --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    query_readiness_parser.add_argument(
        "--query",
        help="Free-text query over readiness entry fields such as trace ID, title, and blocking reasons.",
    )
    query_readiness_parser.add_argument(
        "--initiative-id",
        help="Exact initiative identifier such as initiative.plan_live_query_authority_cutover.",
    )
    query_readiness_parser.add_argument(
        "--project-id",
        help="Exact project identifier such as project.watchtower.",
    )
    query_readiness_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.plan_live_query_authority_cutover.",
    )
    query_readiness_parser.add_argument(
        "--lifecycle-stage",
        help="Exact lifecycle-stage filter such as ready_for_execution, in_progress, or completed.",
    )
    query_readiness_parser.add_argument(
        "--review-status",
        help="Exact review-status filter such as approved or pending.",
    )
    query_readiness_parser.add_argument(
        "--ready-for-execution",
        choices=("true", "false"),
        help="Filter by whether the initiative is currently marked ready_for_execution.",
    )
    query_readiness_parser.add_argument(
        "--blocked-only",
        action="store_true",
        help="Return only entries with one or more blocking reasons.",
    )
    query_readiness_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_readiness_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_readiness_parser.set_defaults(handler=_run_query_readiness)

    query_discrepancies_parser = query_subparsers.add_parser(
        "discrepancies",
        help="Search the live plan discrepancy index.",
        description=dedent(
            """
            Search the discrepancy index for drift, validation, and readiness
            mismatches captured in the live plan workspace.

            Use this when you need blocking discrepancy state without opening
            one initiative package directly.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query discrepancies --blocking-only",
            (
                "uv run watchtower-core query discrepancies "
                "--trace-id trace.plan_core_documentation_template_authority_foundation "
                "--format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    query_discrepancies_parser.add_argument(
        "--query",
        help="Free-text query over discrepancy fields such as IDs, title, summary, category, and source paths.",
    )
    query_discrepancies_parser.add_argument(
        "--initiative-id",
        help="Exact initiative identifier such as initiative.plan_live_query_authority_cutover.",
    )
    query_discrepancies_parser.add_argument(
        "--project-id",
        help="Exact project identifier such as project.watchtower.",
    )
    query_discrepancies_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.plan_core_documentation_template_authority_foundation.",
    )
    query_discrepancies_parser.add_argument(
        "--category",
        help="Exact discrepancy category such as stale_aggregate_index or scope_mismatch.",
    )
    query_discrepancies_parser.add_argument(
        "--severity",
        help="Exact severity filter such as low, high, or critical.",
    )
    query_discrepancies_parser.add_argument(
        "--status",
        help="Exact discrepancy status such as open or resolved.",
    )
    query_discrepancies_parser.add_argument(
        "--blocking-only",
        action="store_true",
        help="Return only discrepancies whose gate effect is blocking readiness or execution.",
    )
    query_discrepancies_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_discrepancies_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_discrepancies_parser.set_defaults(handler=_run_query_discrepancies)

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
            "uv run watchtower-core query projects --slug watchtower",
            "uv run watchtower-core query projects --repository-role implementation --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_projects_parser.add_argument(
        "--query",
        help="Free-text query over project fields such as project ID, slug, title, summary, and repository locators.",
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
    query_projects_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_projects_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_projects_parser.set_defaults(handler=_run_query_projects)

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
        help=(
            "Exact current-phase filter such as implementation_planning, "
            "execution, closeout, or closed."
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
            "uv run watchtower-core query authority --domain planning",
            "uv run watchtower-core query authority --question-id "
            "authority.planning.deep_trace_context --format json",
            "uv run watchtower-core query authority --artifact-kind route_index",
        ),
        formatter_class=HelpFormatter,
    )
    query_authority_parser.add_argument(
        "--query",
        help=(
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
        help="Exact canonical artifact-kind filter such as planning_catalog or route_index.",
    )
    query_authority_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_authority_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_authority_parser.set_defaults(handler=_run_query_authority)

    query_planning_parser = query_subparsers.add_parser(
        "planning",
        help="Search the canonical planning catalog.",
        description=dedent(
            """
            Search the canonical planning catalog for deep trace-linked planning
            context with explicit status semantics.

            Use this after `coordination` identifies the active trace you want,
            or when you need one machine-readable record that joins PRDs,
            decisions, design docs, tasks, acceptance contracts, validation
            evidence, and per-trace coordination state. When invoked as a
            filterless browse command, it defaults to active initiatives only;
            use `--initiative-status` or a known `--trace-id` for explicit
            history lookup.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query planning --trace-id trace.core_python_foundation",
            "uv run watchtower-core query planning --initiative-status active --format json",
            "uv run watchtower-core query planning --current-phase execution "
            "--owner repository_maintainer",
        ),
        formatter_class=HelpFormatter,
    )
    query_planning_parser.add_argument(
        "--query",
        help=(
            "Free-text query over planning-catalog fields such as trace ID, titles, "
            "status fields, linked IDs, next action, and related paths."
        ),
    )
    query_planning_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_planning_parser.add_argument(
        "--initiative-status",
        help=(
            "Exact initiative-status filter such as active, completed, or superseded. "
            "When omitted for filterless browse, the command defaults to active."
        ),
    )
    query_planning_parser.add_argument(
        "--current-phase",
        help="Exact current-phase filter such as execution or closed.",
    )
    query_planning_parser.add_argument(
        "--owner",
        help="Exact owner filter against the current active owners for the trace.",
    )
    query_planning_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_planning_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_planning_parser.set_defaults(handler=_run_query_planning)

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
        help=(
            "Exact initiative-status filter such as active or completed. "
            "When omitted for filterless browse, the command defaults to active."
        ),
    )
    query_initiatives_parser.add_argument(
        "--current-phase",
        help=(
            "Exact current-phase filter such as implementation_planning, "
            "execution, closeout, or closed."
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
