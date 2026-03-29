"""Index-backed parser registration for `watchtower-core plan query`."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_query_argument,
    add_tri_state_bool_argument,
    examples,
)
from watchtower_plan.cli.query_common import (
    IMPLEMENTATION_PATH,
    add_live_scope_arguments,
    add_output_arguments,
)
from watchtower_plan.cli.query_lookup_handlers import (
    _run_query_artifacts,
    _run_query_closeouts,
    _run_query_discrepancies,
    _run_query_plan_evidence,
    _run_query_readiness,
    _run_query_reviews,
    _run_query_tasks,
)


def register_index_query_commands(
    query_subparsers: argparse._SubParsersAction,
) -> None:
    """Register the index-backed `plan query` leaf commands."""

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
        help=(
            "Include forward and reverse dependency detail in the result "
            "payload or human output."
        ),
    )
    add_output_arguments(query_tasks_parser)
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
            "Free-text query over artifact fields such as IDs, family, path, "
            "title, summary, and context IDs."
        ),
    )
    query_artifacts_parser.add_argument(
        "--artifact-id",
        help="Exact artifact identifier such as initiative.plan_artifact_index_runtime_foundation.",
    )
    query_artifacts_parser.add_argument(
        "--artifact-family",
        help=(
            "Exact artifact-family filter such as initiative_state, "
            "task_state, or artifact_index."
        ),
    )
    query_artifacts_parser.add_argument(
        "--context-id",
        help=(
            "Exact context identifier filter such as "
            "trace.plan_artifact_index_runtime_foundation or project.watchtower."
        ),
    )
    query_artifacts_parser.add_argument(
        "--source-context",
        help=(
            "Exact source-context filter such as "
            "initiative.plan_artifact_index_runtime_foundation or pack.plan."
        ),
    )
    query_artifacts_parser.add_argument(
        "--source-channel",
        help=(
            "Exact source-channel filter such as initiative_package, "
            "project_container, event_stream, or aggregate_index."
        ),
    )
    query_artifacts_parser.add_argument(
        "--status",
        help=(
            "Exact artifact status filter such as ready_for_execution, "
            "planned, active, or completed."
        ),
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
    add_output_arguments(query_artifacts_parser)
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
            "Free-text query over readiness entry fields such as trace ID, "
            "title, and blocking reasons."
        ),
    )
    add_live_scope_arguments(
        query_readiness_parser,
        initiative_help=(
            "Exact initiative identifier such as "
            "initiative.plan_live_query_authority_cutover."
        ),
        trace_help="Exact trace filter such as trace.plan_live_query_authority_cutover.",
    )
    query_readiness_parser.add_argument(
        "--lifecycle-stage",
        help=(
            "Exact lifecycle-stage filter such as ready_for_execution, "
            "in_progress, or completed."
        ),
    )
    query_readiness_parser.add_argument(
        "--review-status",
        help="Exact review-status filter such as approved or pending.",
    )
    add_tri_state_bool_argument(
        query_readiness_parser,
        "--ready-for-execution",
        help_text=(
            "Filter by whether the initiative is currently marked "
            "ready_for_execution."
        ),
    )
    query_readiness_parser.add_argument(
        "--blocked-only",
        action="store_true",
        help="Return only entries with one or more blocking reasons.",
    )
    add_output_arguments(query_readiness_parser)
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
            "Free-text query over discrepancy fields such as IDs, title, "
            "summary, category, and source paths."
        ),
    )
    add_live_scope_arguments(
        query_discrepancies_parser,
        initiative_help=(
            "Exact initiative identifier such as "
            "initiative.plan_live_query_authority_cutover."
        ),
        trace_help=(
            "Exact trace filter such as "
            "trace.plan_core_documentation_template_authority_foundation."
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
    add_output_arguments(query_discrepancies_parser)
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
            "Free-text query over evidence fields such as IDs, title, "
            "acceptance labels, owners, and output paths."
        ),
    )
    add_live_scope_arguments(
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
    add_output_arguments(query_plan_evidence_parser)
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
            "Free-text query over closeout fields such as IDs, title, "
            "expected outcome, and follow-up handling."
        ),
    )
    add_live_scope_arguments(
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
    add_output_arguments(query_closeouts_parser)
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
            "Free-text query over review fields such as IDs, trace, title, "
            "review refs, and evidence refs."
        ),
    )
    query_reviews_parser.add_argument(
        "--subject-kind",
        help="Exact subject-kind filter such as initiative or promotion.",
    )
    add_live_scope_arguments(
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
            "Filter initiative review entries by whether the subject is "
            "ready for execution."
        ),
    )
    query_reviews_parser.add_argument(
        "--review-ref",
        help=(
            "Exact review-ref filter such as repository_maintainer_review or "
            "actor.repository_maintainer."
        ),
    )
    add_output_arguments(query_reviews_parser)
    query_reviews_parser.set_defaults(_implementation_path=IMPLEMENTATION_PATH)
    query_reviews_parser.set_defaults(handler=_run_query_reviews)
