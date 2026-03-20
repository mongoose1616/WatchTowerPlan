"""Pack-owned registration for the `watchtower-core plan query` namespace."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    add_limit_argument,
    add_query_argument,
    add_tri_state_bool_argument,
    examples,
)
from watchtower_plan.cli.query_lookup_handlers import (
    _run_query_artifacts,
    _run_query_authority,
    _run_query_closeouts,
    _run_query_discrepancies,
    _run_query_plan_evidence,
    _run_query_project_context,
    _run_query_projects,
    _run_query_readiness,
    _run_query_reviews,
    _run_query_tasks,
    _run_query_trace,
)
from watchtower_plan.cli.query_rendered_handlers import (
    _run_query_coordination,
    _run_query_initiatives,
)

IMPLEMENTATION_PATH = "plan/python/src/watchtower_plan/cli/query.py"


def _add_live_scope_arguments(
    parser: argparse.ArgumentParser,
    *,
    initiative_help: str,
    trace_help: str,
    project_help: str = "Exact project identifier such as project.watchtower.",
) -> None:
    parser.add_argument("--initiative-id", help=initiative_help)
    parser.add_argument("--project-id", help=project_help)
    parser.add_argument("--trace-id", help=trace_help)


def _add_output_arguments(
    parser: argparse.ArgumentParser,
    *,
    limit_default: int = 10,
) -> None:
    add_limit_argument(parser, default=limit_default)
    add_human_json_format_argument(parser)


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
            "uv run watchtower-core plan query project-context --project-slug watchtower --format json",
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
            "uv run watchtower-core plan query tasks --task-status planned",
            (
                "uv run watchtower-core plan query tasks "
                "--blocked-by task.plan_live_query_authority_cutover."
                "reroot_public_planning_queries_onto_live_plan_indexes"
            ),
            (
                "uv run watchtower-core plan query tasks "
                "--trace-id trace.plan_live_query_authority_cutover --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_tasks_parser,
        help_text=(
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
    _add_output_arguments(query_tasks_parser)
    query_tasks_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_tasks_parser.set_defaults(handler=_run_query_tasks)

    query_artifacts_parser = query_subparsers.add_parser(
        "artifacts",
        help="Search the live plan artifact index.",
        description=dedent(
            """
            Search the cross-family plan artifact index for live machine
            artifacts and aggregate indexes.

            Use this when you need one query surface across initiative-local
            machine artifacts, project machine artifacts, and pack-level live
            indexes without crawling the workspace manually.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query artifacts --artifact-family initiative_state",
            (
                "uv run watchtower-core plan query artifacts "
                "--context-id trace.plan_artifact_index_runtime_foundation --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_artifacts_parser,
        help_text=(
            "Free-text query over artifact fields such as IDs, family, path, title, "
            "summary, and context IDs."
        ),
    )
    query_artifacts_parser.add_argument(
        "--artifact-id",
        help="Exact artifact identifier such as initiative.plan_artifact_index_runtime_foundation.",
    )
    query_artifacts_parser.add_argument(
        "--artifact-family",
        help="Exact artifact-family filter such as initiative_state, task_state, or artifact_index.",
    )
    query_artifacts_parser.add_argument(
        "--context-id",
        help="Exact context identifier filter such as trace.plan_artifact_index_runtime_foundation or project.watchtower.",
    )
    query_artifacts_parser.add_argument(
        "--source-context",
        help="Exact source-context filter such as initiative.plan_artifact_index_runtime_foundation or pack.plan.",
    )
    query_artifacts_parser.add_argument(
        "--source-channel",
        help="Exact source-channel filter such as initiative_package, project_container, event_stream, or aggregate_index.",
    )
    query_artifacts_parser.add_argument(
        "--status",
        help="Exact artifact status filter such as ready_for_execution, planned, active, or completed.",
    )
    add_tri_state_bool_argument(
        query_artifacts_parser,
        "--authoritative",
        help_text="Filter by whether the artifact is authoritative.",
    )
    add_tri_state_bool_argument(
        query_artifacts_parser,
        "--derived",
        help_text="Filter by whether the artifact is derived.",
    )
    add_tri_state_bool_argument(
        query_artifacts_parser,
        "--hidden",
        help_text="Filter by whether the artifact lives on a hidden machine surface.",
    )
    _add_output_arguments(query_artifacts_parser)
    query_artifacts_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_artifacts_parser.set_defaults(handler=_run_query_artifacts)

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
            "uv run watchtower-core plan query readiness --ready-for-execution true",
            (
                "uv run watchtower-core plan query readiness "
                "--trace-id trace.plan_live_query_authority_cutover --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_readiness_parser,
        help_text=(
            "Free-text query over readiness entry fields such as trace ID, title, "
            "and blocking reasons."
        ),
    )
    _add_live_scope_arguments(
        query_readiness_parser,
        initiative_help=(
            "Exact initiative identifier such as initiative.plan_live_query_authority_cutover."
        ),
        trace_help="Exact trace filter such as trace.plan_live_query_authority_cutover.",
    )
    query_readiness_parser.add_argument(
        "--lifecycle-stage",
        help="Exact lifecycle-stage filter such as ready_for_execution, in_progress, or completed.",
    )
    query_readiness_parser.add_argument(
        "--review-status",
        help="Exact review-status filter such as approved or pending.",
    )
    add_tri_state_bool_argument(
        query_readiness_parser,
        "--ready-for-execution",
        help_text=(
            "Filter by whether the initiative is currently marked ready_for_execution."
        ),
    )
    query_readiness_parser.add_argument(
        "--blocked-only",
        action="store_true",
        help="Return only entries with one or more blocking reasons.",
    )
    _add_output_arguments(query_readiness_parser)
    query_readiness_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
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
            "uv run watchtower-core plan query discrepancies --blocking-only",
            (
                "uv run watchtower-core plan query discrepancies "
                "--trace-id trace.plan_core_documentation_template_authority_foundation "
                "--format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_discrepancies_parser,
        help_text=(
            "Free-text query over discrepancy fields such as IDs, title, summary, "
            "category, and source paths."
        ),
    )
    _add_live_scope_arguments(
        query_discrepancies_parser,
        initiative_help=(
            "Exact initiative identifier such as initiative.plan_live_query_authority_cutover."
        ),
        trace_help=(
            "Exact trace filter such as trace.plan_core_documentation_template_authority_foundation."
        ),
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
    _add_output_arguments(query_discrepancies_parser)
    query_discrepancies_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_discrepancies_parser.set_defaults(handler=_run_query_discrepancies)

    query_plan_evidence_parser = query_subparsers.add_parser(
        "plan-evidence",
        help="Search the live plan evidence index.",
        description=dedent(
            """
            Search the live evidence index for initiative-local validation
            bundles captured under the plan workspace.

            Use this when you need the current planned or completed validation
            contract for one initiative without opening the local evidence
            bundle directly.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query plan-evidence --status planned",
            (
                "uv run watchtower-core plan query plan-evidence "
                "--trace-id trace.plan_live_evidence_closeout_review_indexes_foundation "
                "--format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_plan_evidence_parser,
        help_text=(
            "Free-text query over evidence fields such as IDs, title, acceptance "
            "labels, owners, and output paths."
        ),
    )
    _add_live_scope_arguments(
        query_plan_evidence_parser,
        initiative_help=(
            "Exact initiative identifier such as "
            "initiative.plan_live_evidence_closeout_review_indexes_foundation."
        ),
        trace_help=(
            "Exact trace filter such as "
            "trace.plan_live_evidence_closeout_review_indexes_foundation."
        ),
    )
    query_plan_evidence_parser.add_argument(
        "--status",
        help="Exact evidence status such as planned, active, or completed.",
    )
    query_plan_evidence_parser.add_argument(
        "--owner",
        help="Exact owner filter such as repository_maintainer.",
    )
    query_plan_evidence_parser.add_argument(
        "--target-phase",
        help="Exact target-phase filter such as readiness, execution, or closeout.",
    )
    query_plan_evidence_parser.add_argument(
        "--validation-type",
        help="Exact validation-type filter such as unit_tests or integration_tests.",
    )
    query_plan_evidence_parser.add_argument(
        "--acceptance-label",
        help="Exact acceptance-label filter as captured in the validation bundle.",
    )
    _add_output_arguments(query_plan_evidence_parser)
    query_plan_evidence_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_plan_evidence_parser.set_defaults(handler=_run_query_plan_evidence)

    query_closeouts_parser = query_subparsers.add_parser(
        "closeouts",
        help="Search the live plan closeout index.",
        description=dedent(
            """
            Search the live closeout index for initiative-local closeout
            contracts and terminal recap state.

            Use this when you need the expected outcome, evidence references,
            promotion-review expectation, or terminal-state summary without
            opening one initiative root directly.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query closeouts --status planned",
            (
                "uv run watchtower-core plan query closeouts "
                "--promotion-review-required true --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_closeouts_parser,
        help_text=(
            "Free-text query over closeout fields such as IDs, title, expected "
            "outcome, and follow-up handling."
        ),
    )
    _add_live_scope_arguments(
        query_closeouts_parser,
        initiative_help=(
            "Exact initiative identifier such as "
            "initiative.plan_live_evidence_closeout_review_indexes_foundation."
        ),
        trace_help=(
            "Exact trace filter such as "
            "trace.plan_live_evidence_closeout_review_indexes_foundation."
        ),
    )
    query_closeouts_parser.add_argument(
        "--status",
        help="Exact closeout status such as planned, active, or completed.",
    )
    query_closeouts_parser.add_argument(
        "--terminal-state",
        help="Exact terminal-state filter such as completed, superseded, or cancelled.",
    )
    add_tri_state_bool_argument(
        query_closeouts_parser,
        "--promotion-review-required",
        help_text="Filter by whether the closeout recap requires promotion review.",
    )
    _add_output_arguments(query_closeouts_parser)
    query_closeouts_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_closeouts_parser.set_defaults(handler=_run_query_closeouts)

    query_reviews_parser = query_subparsers.add_parser(
        "reviews",
        help="Search the live plan review index.",
        description=dedent(
            """
            Search the live review index for initiative review state and
            promotion approval state.

            Use this when you need one machine-readable review surface without
            stitching together readiness and promotion records manually.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core plan query reviews --review-state pending",
            (
                "uv run watchtower-core plan query reviews "
                "--subject-kind promotion --format json"
            ),
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_reviews_parser,
        help_text=(
            "Free-text query over review fields such as IDs, trace, title, review "
            "refs, and evidence refs."
        ),
    )
    query_reviews_parser.add_argument(
        "--subject-kind",
        help="Exact subject-kind filter such as initiative or promotion.",
    )
    _add_live_scope_arguments(
        query_reviews_parser,
        initiative_help=(
            "Exact initiative identifier such as "
            "initiative.plan_live_evidence_closeout_review_indexes_foundation."
        ),
        trace_help=(
            "Exact trace filter such as "
            "trace.plan_live_evidence_closeout_review_indexes_foundation."
        ),
    )
    query_reviews_parser.add_argument(
        "--review-state",
        help="Exact review-state filter such as pending or approved.",
    )
    add_tri_state_bool_argument(
        query_reviews_parser,
        "--ready-for-execution",
        help_text=(
            "Filter initiative review entries by whether the subject is ready for execution."
        ),
    )
    query_reviews_parser.add_argument(
        "--review-ref",
        help="Exact review-ref filter such as repository_maintainer_review or actor.repository_maintainer.",
    )
    _add_output_arguments(query_reviews_parser)
    query_reviews_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_reviews_parser.set_defaults(handler=_run_query_reviews)

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
            "uv run watchtower-core plan query projects --repository-role implementation --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_query_argument(
        query_projects_parser,
        help_text=(
            "Free-text query over project fields such as project ID, slug, title, "
            "summary, and repository locators."
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
    _add_output_arguments(query_projects_parser)
    query_projects_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
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
            "Free-text query over coordination fields such as trace ID, title, "
            "next action, and active task summaries."
        ),
    )
    query_coordination_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.governed_acceptance_example.",
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
            "Exact current-phase filter such as capture, "
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
    _add_output_arguments(query_coordination_parser)
    query_coordination_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
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
            "uv run watchtower-core plan query authority --domain planning",
            "uv run watchtower-core plan query authority --question-id "
            "authority.planning.deep_trace_context --format json",
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
    _add_output_arguments(query_authority_parser)
    query_authority_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_authority_parser.set_defaults(handler=_run_query_authority)

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
            "Exact current-phase filter such as capture, "
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
    _add_output_arguments(query_initiatives_parser)
    query_initiatives_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_initiatives_parser.set_defaults(handler=_run_query_initiatives)

    query_trace_parser = query_subparsers.add_parser(
        "trace",
        help="Resolve one traceability record by trace ID.",
        description=dedent(
            """
            Resolve one traceability record by its stable trace identifier.

            Use this when you already know the trace you want and need the
            linked initiative, decision, design, implementation, task, validator, or evidence IDs.
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
