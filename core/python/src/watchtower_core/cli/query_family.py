"""Query command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples


def register_query_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the query command family and its subcommands."""
    from watchtower_core.cli.handlers import (
        _run_help,
        _run_query_acceptance,
        _run_query_commands,
        _run_query_decisions,
        _run_query_designs,
        _run_query_evidence,
        _run_query_foundations,
        _run_query_initiatives,
        _run_query_paths,
        _run_query_prds,
        _run_query_references,
        _run_query_standards,
        _run_query_tasks,
        _run_query_trace,
        _run_query_workflows,
    )

    query_parser = subparsers.add_parser(
        "query",
        help="Search governed indexes for paths, commands, planning docs, tasks, and traces.",
        description=dedent(
            """
            Search the governed lookup surfaces without opening the raw JSON
            artifacts directly.

            Use `paths` for repository navigation, `commands` for CLI discovery,
            `foundations` for the intent-layer foundation corpus, `workflows`
            for workflow-module lookup, `references` for the reference library,
            `standards` for governed repository standards, `prds`,
            `decisions`, `designs`, `acceptance`, `evidence`, and `tasks`
            for planning and execution lookup, and
            `initiatives` for the cross-family phase and ownership view, and
            `trace` when you already know the trace identifier you want.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query paths --query control plane",
            "uv run watchtower-core query commands --query doctor --format json",
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

    query_foundations_parser = query_subparsers.add_parser(
        "foundations",
        help="Search the foundation index.",
        description=dedent(
            """
            Search the governed foundation index for repository intent-layer
            documents such as design philosophy, product shape, and technology
            direction.

            Use this when you need to confirm which foundation doc governs an
            area or where a foundation doc is currently cited or applied.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query foundations --query philosophy",
            "uv run watchtower-core query foundations --audience maintainers",
            "uv run watchtower-core query foundations --applied-by-path "
            "docs/standards/engineering/engineering_best_practices_standard.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_foundations_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed foundation fields such as ID, title, "
            "summary, aliases, and related paths."
        ),
    )
    query_foundations_parser.add_argument(
        "--foundation-id",
        help="Exact foundation identifier such as foundation.engineering_design_principles.",
    )
    query_foundations_parser.add_argument(
        "--audience",
        help="Exact audience filter such as shared, maintainers, or contributors.",
    )
    query_foundations_parser.add_argument(
        "--authority",
        help="Exact authority filter such as authoritative or supporting.",
    )
    query_foundations_parser.add_argument("--tag", help="Exact tag filter.")
    query_foundations_parser.add_argument(
        "--related-path",
        help="Exact repository-path filter such as core/python/ or workflows/modules/.",
    )
    query_foundations_parser.add_argument(
        "--reference-path",
        help="Exact governed reference-doc filter such as docs/references/uv_reference.md.",
    )
    query_foundations_parser.add_argument(
        "--cited-by-path",
        help="Exact doc-path filter for documents that cite the foundation doc.",
    )
    query_foundations_parser.add_argument(
        "--applied-by-path",
        help=(
            "Exact doc-path filter for documents that apply the foundation doc "
            "in an applied-reference section."
        ),
    )
    query_foundations_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_foundations_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_foundations_parser.set_defaults(handler=_run_query_foundations)

    query_workflows_parser = query_subparsers.add_parser(
        "workflows",
        help="Search the workflow index.",
        description=dedent(
            """
            Search the governed workflow index for workflow modules and the
            standards, references, or canonical files that govern them.

            Use this when you know the behavior or governing surface you need,
            but not yet the exact workflow module name.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query workflows --query validation",
            "uv run watchtower-core query workflows --reference-path "
            "docs/references/github_collaboration_reference.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_workflows_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed workflow fields such as workflow ID, "
            "title, summary, related paths, and references."
        ),
    )
    query_workflows_parser.add_argument(
        "--workflow-id",
        help="Exact workflow identifier such as workflow.code_validation.",
    )
    query_workflows_parser.add_argument(
        "--related-path",
        help=(
            "Exact repository-path filter such as "
            "docs/standards/documentation/workflow_md_standard.md."
        ),
    )
    query_workflows_parser.add_argument(
        "--reference-path",
        help=(
            "Exact governed reference-doc filter such as "
            "docs/references/github_collaboration_reference.md."
        ),
    )
    query_workflows_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_workflows_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_workflows_parser.set_defaults(handler=_run_query_workflows)

    query_references_parser = query_subparsers.add_parser(
        "references",
        help="Search the reference index.",
        description=dedent(
            """
            Search the governed reference index for curated internal reference
            documents and their upstream authority links.

            Use this when you know the topic you want, but not yet the exact
            reference document path.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query references --query uv",
            "uv run watchtower-core query references --related-path core/python/ --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_references_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed reference fields such as reference ID, "
            "title, summary, upstream URLs, related paths, aliases, and tags."
        ),
    )
    query_references_parser.add_argument(
        "--reference-id",
        help="Exact reference identifier such as ref.uv.",
    )
    query_references_parser.add_argument("--tag", help="Exact tag filter.")
    query_references_parser.add_argument(
        "--related-path",
        help="Exact repository-path filter such as core/python/ or docs/standards/engineering/.",
    )
    query_references_parser.add_argument(
        "--upstream-url",
        help="Exact canonical-upstream URL filter.",
    )
    query_references_parser.add_argument(
        "--cited-by-path",
        help="Exact doc-path filter for documents that cite the reference.",
    )
    query_references_parser.add_argument(
        "--applied-by-path",
        help=(
            "Exact doc-path filter for documents that apply the reference in an "
            "applied-reference section."
        ),
    )
    query_references_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_references_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_references_parser.set_defaults(handler=_run_query_references)

    query_standards_parser = query_subparsers.add_parser(
        "standards",
        help="Search the standard index.",
        description=dedent(
            """
            Search the governed standard index for repository standards and
            best-practice docs.

            Use this when you need to find standards by category, local
            reference doc, related path, or free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query standards --category governance",
            "uv run watchtower-core query standards --reference-path "
            "docs/references/github_collaboration_reference.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_standards_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed standard fields such as ID, title, "
            "summary, category, references, and related paths."
        ),
    )
    query_standards_parser.add_argument(
        "--standard-id",
        help="Exact standard identifier such as std.engineering.best_practices.",
    )
    query_standards_parser.add_argument(
        "--category",
        help="Exact top-level standards category such as governance or engineering.",
    )
    query_standards_parser.add_argument("--tag", help="Exact tag filter.")
    query_standards_parser.add_argument(
        "--related-path",
        help="Exact repository-path filter such as .github/ or core/python/.",
    )
    query_standards_parser.add_argument(
        "--reference-path",
        help=(
            "Exact governed reference-doc filter such as "
            "docs/references/github_collaboration_reference.md."
        ),
    )
    query_standards_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_standards_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_standards_parser.set_defaults(handler=_run_query_standards)

    query_prds_parser = query_subparsers.add_parser(
        "prds",
        help="Search the PRD index.",
        description=dedent(
            """
            Search the PRD index for governed product requirements documents.

            Use this when you need to find a PRD by trace, requirement ID,
            acceptance ID, or free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query prds --trace-id trace.core_python_foundation",
            "uv run watchtower-core query prds --requirement-id req.core_python_foundation.003 "
            "--format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_prds_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed PRD fields such as IDs, title, "
            "summary, tags, and linked surfaces."
        ),
    )
    query_prds_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_prds_parser.add_argument(
        "--tag",
        help="Exact tag filter.",
    )
    query_prds_parser.add_argument(
        "--requirement-id",
        help="Exact requirement-ID filter such as req.core_python_foundation.003.",
    )
    query_prds_parser.add_argument(
        "--acceptance-id",
        help="Exact acceptance-ID filter such as ac.core_python_foundation.002.",
    )
    query_prds_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_prds_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_prds_parser.set_defaults(handler=_run_query_prds)

    query_decisions_parser = query_subparsers.add_parser(
        "decisions",
        help="Search the decision index.",
        description=dedent(
            """
            Search the decision index for governed durable decision records.

            Use this when you need to find a decision by trace, decision status,
            linked PRD, or free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query decisions --decision-status accepted",
            "uv run watchtower-core query decisions --linked-prd-id prd.core_python_foundation "
            "--format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_decisions_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed decision fields such as IDs, title, "
            "summary, tags, and linked surfaces."
        ),
    )
    query_decisions_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_decisions_parser.add_argument(
        "--decision-status",
        help="Exact decision-status filter such as accepted or proposed.",
    )
    query_decisions_parser.add_argument(
        "--tag",
        help="Exact tag filter.",
    )
    query_decisions_parser.add_argument(
        "--linked-prd-id",
        help="Exact linked PRD filter such as prd.core_python_foundation.",
    )
    query_decisions_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_decisions_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_decisions_parser.set_defaults(handler=_run_query_decisions)

    query_designs_parser = query_subparsers.add_parser(
        "designs",
        help="Search the design-document index.",
        description=dedent(
            """
            Search the design-document index for governed feature designs and
            implementation plans.

            Use this when you need to find designs by trace, family, tag, or
            free-text summary content.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query designs --family feature_design",
            "uv run watchtower-core query designs --trace-id trace.core_python_foundation "
            "--format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_designs_parser.add_argument(
        "--query",
        help=(
            "Free-text query over indexed design fields such as IDs, title, "
            "summary, tags, and linked paths."
        ),
    )
    query_designs_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_designs_parser.add_argument(
        "--family",
        help="Exact design-family filter such as feature_design or implementation_plan.",
    )
    query_designs_parser.add_argument(
        "--tag",
        help="Exact tag filter.",
    )
    query_designs_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_designs_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_designs_parser.set_defaults(handler=_run_query_designs)

    query_acceptance_parser = query_subparsers.add_parser(
        "acceptance",
        help="Search governed acceptance contracts.",
        description=dedent(
            """
            Search governed acceptance contracts by trace, source PRD, or
            acceptance ID.

            Use this when you need the machine-readable acceptance boundary for
            a traced initiative without opening the raw contract JSON by hand.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query acceptance --trace-id trace.core_python_foundation",
            "uv run watchtower-core query acceptance --acceptance-id "
            "ac.core_python_foundation.002 --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_acceptance_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_acceptance_parser.add_argument(
        "--source-prd-id",
        help="Exact source PRD filter such as prd.core_python_foundation.",
    )
    query_acceptance_parser.add_argument(
        "--acceptance-id",
        help="Exact acceptance-ID filter such as ac.core_python_foundation.002.",
    )
    query_acceptance_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_acceptance_parser.set_defaults(handler=_run_query_acceptance)

    query_evidence_parser = query_subparsers.add_parser(
        "evidence",
        help="Search governed validation evidence.",
        description=dedent(
            """
            Search governed validation-evidence artifacts by trace, overall
            result, acceptance ID, or validator ID.

            Use this when you need to inspect durable validation proof without
            opening the raw ledger JSON directly.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core query evidence --trace-id trace.core_python_foundation",
            "uv run watchtower-core query evidence --acceptance-id "
            "ac.core_python_foundation.003 --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_evidence_parser.add_argument(
        "--trace-id",
        help="Exact trace filter such as trace.core_python_foundation.",
    )
    query_evidence_parser.add_argument(
        "--result",
        help="Exact overall-result filter such as passed or failed.",
    )
    query_evidence_parser.add_argument(
        "--acceptance-id",
        help="Exact acceptance-ID filter such as ac.core_python_foundation.003.",
    )
    query_evidence_parser.add_argument(
        "--validator-id",
        help="Exact validator-ID filter such as validator.control_plane.traceability_index.",
    )
    query_evidence_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_evidence_parser.set_defaults(handler=_run_query_evidence)

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

    query_initiatives_parser = query_subparsers.add_parser(
        "initiatives",
        help="Search the initiative index.",
        description=dedent(
            """
            Search the cross-family initiative index for the current phase,
            active ownership, blockers, and next step of a traced initiative.

            Use this when the main question is where an initiative is in the
            PRD -> design -> implementation -> validation -> closeout flow.
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
