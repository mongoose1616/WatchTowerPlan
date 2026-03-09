"""Thin CLI entrypoints for the WatchTower core workspace."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from textwrap import dedent

from watchtower_core.closeout import InitiativeCloseoutService
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import TaskIndexEntry
from watchtower_core.evidence import EvidenceWriteResult, ValidationEvidenceRecorder
from watchtower_core.query import (
    AcceptanceContractQueryService,
    AcceptanceContractSearchParams,
    CommandQueryService,
    CommandSearchParams,
    DecisionQueryService,
    DecisionSearchParams,
    DesignDocumentQueryService,
    DesignDocumentSearchParams,
    PrdQueryService,
    PrdSearchParams,
    RepositoryPathQueryService,
    RepositoryPathSearchParams,
    TaskQueryService,
    TaskSearchParams,
    TraceabilityQueryService,
    ValidationEvidenceQueryService,
    ValidationEvidenceSearchParams,
)
from watchtower_core.sync import (
    CommandIndexSyncService,
    DecisionIndexSyncService,
    DecisionTrackingSyncService,
    DesignDocumentIndexSyncService,
    DesignTrackingSyncService,
    GitHubTaskSyncParams,
    GitHubTaskSyncService,
    PrdIndexSyncService,
    PrdTrackingSyncService,
    RepositoryPathIndexSyncService,
    TaskIndexSyncService,
    TaskTrackingSyncService,
    TraceabilityIndexSyncService,
)
from watchtower_core.validation import (
    AcceptanceReconciliationService,
    ArtifactValidationService,
    FrontMatterValidationService,
    ValidationExecutionError,
    ValidationResult,
    ValidationSelectionError,
)


class HelpFormatter(
    argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter
):
    """Formatter that preserves examples and shows defaults."""


ValidationServiceFactory = Callable[
    [ControlPlaneLoader],
    FrontMatterValidationService | ArtifactValidationService,
]


def _examples(*lines: str) -> str:
    """Render a short examples block for argparse epilog text."""
    return "Examples:\n" + "\n".join(f"  {line}" for line in lines)


def build_parser() -> argparse.ArgumentParser:
    """Build the root CLI parser."""
    parser = argparse.ArgumentParser(
        prog="watchtower-core",
        description=dedent(
            """
            WatchTower core helper and harness workspace.

            Run this command from `core/python/` with `uv run` to inspect governed
            control-plane data, run lightweight workspace checks, and rebuild
            derived indexes.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core doctor",
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core query prds --trace-id trace.core_python_foundation",
            "uv run watchtower-core query acceptance --trace-id trace.core_python_foundation",
            "uv run watchtower-core query tasks --task-status backlog",
            "uv run watchtower-core query tasks --blocked-only --include-dependency-details",
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync task-index",
            "uv run watchtower-core sync task-tracking",
            "uv run watchtower-core sync github-tasks --repo owner/repo",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status completed --closure-reason \"Delivered and validated\"",
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
        ),
        formatter_class=HelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="<command>")

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Run a quick workspace smoke check.",
        description=dedent(
            """
            Run a small, low-risk check that confirms the core Python CLI is
            installed and reachable.

            Start here if you are new to the workspace or want the simplest
            successful `watchtower-core` invocation.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core doctor",
            "uv run watchtower-core doctor --format json",
        ),
        formatter_class=HelpFormatter,
    )
    doctor_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    doctor_parser.set_defaults(handler=_run_doctor)

    query_parser = subparsers.add_parser(
        "query",
        help="Search governed indexes for paths, commands, planning docs, tasks, and traces.",
        description=dedent(
            """
            Search the governed lookup surfaces without opening the raw JSON
            artifacts directly.

            Use `paths` for repository navigation, `commands` for CLI discovery,
            `prds`, `decisions`, `designs`, `acceptance`, `evidence`, and
            `tasks` for planning and execution lookup, and `trace` when you
            already know the trace identifier you want.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core query paths --query control plane",
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core query prds --trace-id trace.core_python_foundation",
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
        epilog=_examples(
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
        epilog=_examples(
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
        epilog=_examples(
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
        epilog=_examples(
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
        epilog=_examples(
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
        epilog=_examples(
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
        epilog=_examples(
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
        epilog=_examples(
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
        epilog=_examples(
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

    sync_parser = subparsers.add_parser(
        "sync",
        help="Rebuild or materialize derived governed artifacts.",
        description=dedent(
            """
            Rebuild derived governed artifacts from authored repository sources.

            Start with dry-run output first. Use `--write` only when you intend
            to update a canonical control-plane artifact.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync prd-tracking",
            "uv run watchtower-core sync decision-index",
            "uv run watchtower-core sync decision-tracking",
            "uv run watchtower-core sync design-document-index",
            "uv run watchtower-core sync design-tracking",
            "uv run watchtower-core sync task-index",
            "uv run watchtower-core sync task-tracking",
            "uv run watchtower-core sync github-tasks --repo owner/repo --task-id "
            "task.local_task_tracking.github_sync.001",
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync traceability-index --write",
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core sync repository-paths --write",
        ),
        formatter_class=HelpFormatter,
    )
    sync_subparsers = sync_parser.add_subparsers(
        dest="sync_command",
        title="sync commands",
        metavar="<sync_command>",
    )
    sync_parser.set_defaults(handler=_run_help, help_parser=sync_parser)

    sync_command_index_parser = sync_subparsers.add_parser(
        "command-index",
        help="Rebuild the command index from authored command docs.",
        description=dedent(
            """
            Rebuild the command index from the authored command pages under
            `docs/commands/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync command-index --output "
            "/tmp/command_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_command_index_parser)
    sync_command_index_parser.set_defaults(handler=_run_sync_command_index)

    sync_prd_index_parser = sync_subparsers.add_parser(
        "prd-index",
        help="Rebuild the PRD index from governed PRD documents.",
        description=dedent(
            """
            Rebuild the PRD index from the governed PRD documents under
            `docs/planning/prds/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync prd-index --write",
            "uv run watchtower-core sync prd-index --output /tmp/prd_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_prd_index_parser)
    sync_prd_index_parser.set_defaults(handler=_run_sync_prd_index)

    sync_prd_tracking_parser = sync_subparsers.add_parser(
        "prd-tracking",
        help="Rebuild the human-readable PRD tracker from the PRD index.",
        description=dedent(
            """
            Rebuild the human-readable PRD tracker from the governed PRD index
            and the initiative-closeout state stored in traceability.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync prd-tracking",
            "uv run watchtower-core sync prd-tracking --write",
            "uv run watchtower-core sync prd-tracking --output /tmp/prd_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_prd_tracking_parser)
    sync_prd_tracking_parser.set_defaults(handler=_run_sync_prd_tracking)

    sync_decision_index_parser = sync_subparsers.add_parser(
        "decision-index",
        help="Rebuild the decision index from governed decision records.",
        description=dedent(
            """
            Rebuild the decision index from the governed decision records under
            `docs/planning/decisions/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync decision-index",
            "uv run watchtower-core sync decision-index --write",
            "uv run watchtower-core sync decision-index --output "
            "/tmp/decision_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_decision_index_parser)
    sync_decision_index_parser.set_defaults(handler=_run_sync_decision_index)

    sync_decision_tracking_parser = sync_subparsers.add_parser(
        "decision-tracking",
        help="Rebuild the human-readable decision tracker from the decision index.",
        description=dedent(
            """
            Rebuild the human-readable decision tracker from the governed
            decision index and the initiative-closeout state stored in
            traceability.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync decision-tracking",
            "uv run watchtower-core sync decision-tracking --write",
            "uv run watchtower-core sync decision-tracking --output "
            "/tmp/decision_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_decision_tracking_parser)
    sync_decision_tracking_parser.set_defaults(handler=_run_sync_decision_tracking)

    sync_design_document_index_parser = sync_subparsers.add_parser(
        "design-document-index",
        help="Rebuild the design-document index from governed design docs.",
        description=dedent(
            """
            Rebuild the design-document index from the governed design documents
            under `docs/planning/design/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync design-document-index",
            "uv run watchtower-core sync design-document-index --write",
            "uv run watchtower-core sync design-document-index --output "
            "/tmp/design_document_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_design_document_index_parser)
    sync_design_document_index_parser.set_defaults(handler=_run_sync_design_document_index)

    sync_design_tracking_parser = sync_subparsers.add_parser(
        "design-tracking",
        help="Rebuild the human-readable design tracker from the design index.",
        description=dedent(
            """
            Rebuild the human-readable design tracker from the governed design
            index and the initiative-closeout state stored in traceability.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync design-tracking",
            "uv run watchtower-core sync design-tracking --write",
            "uv run watchtower-core sync design-tracking --output "
            "/tmp/design_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_design_tracking_parser)
    sync_design_tracking_parser.set_defaults(handler=_run_sync_design_tracking)

    sync_task_index_parser = sync_subparsers.add_parser(
        "task-index",
        help="Rebuild the task index from governed task records.",
        description=dedent(
            """
            Rebuild the task index from the governed task documents under
            `docs/planning/tasks/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync task-index",
            "uv run watchtower-core sync task-index --write",
            "uv run watchtower-core sync task-index --output /tmp/task_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_task_index_parser)
    sync_task_index_parser.set_defaults(handler=_run_sync_task_index)

    sync_task_tracking_parser = sync_subparsers.add_parser(
        "task-tracking",
        help="Rebuild the human-readable task tracker from governed task records.",
        description=dedent(
            """
            Rebuild the human-readable task tracker from the governed task
            documents under `docs/planning/tasks/`.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync task-tracking",
            "uv run watchtower-core sync task-tracking --write",
            "uv run watchtower-core sync task-tracking --output "
            "/tmp/task_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_task_tracking_parser)
    sync_task_tracking_parser.set_defaults(handler=_run_sync_task_tracking)

    sync_github_tasks_parser = sync_subparsers.add_parser(
        "github-tasks",
        help="Push local task records to GitHub issues and optional project items.",
        description=dedent(
            """
            Push local-first task records to GitHub in a push-only, local-source
            model.

            Start with dry-run output first. Add `--write` to call the GitHub
            APIs, persist the returned foreign keys on the task documents, and
            rebuild the local task index, task tracker, and traceability index.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync github-tasks --repo owner/repo",
            "uv run watchtower-core sync github-tasks --repo owner/repo "
            "--task-id task.local_task_tracking.github_sync.001 --write",
            "uv run watchtower-core sync github-tasks --repo owner/repo "
            "--project-owner owner --project-owner-type organization "
            "--project-number 7 --write --format json",
            "uv run watchtower-core sync github-tasks --repo owner/repo "
            "--no-label-sync --write",
        ),
        formatter_class=HelpFormatter,
    )
    sync_github_tasks_parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "Call the GitHub APIs, persist returned foreign keys locally, and "
            "rebuild derived task surfaces."
        ),
    )
    sync_github_tasks_parser.add_argument(
        "--repo",
        help=(
            "GitHub repository in owner/name form. Falls back to task metadata "
            "or GITHUB_REPOSITORY."
        ),
    )
    sync_github_tasks_parser.add_argument(
        "--task-id",
        action="append",
        default=[],
        help="Exact task identifier filter. Repeat for multiple task IDs.",
    )
    sync_github_tasks_parser.add_argument("--trace-id", help="Exact trace filter.")
    sync_github_tasks_parser.add_argument("--task-status", help="Exact task-status filter.")
    sync_github_tasks_parser.add_argument("--priority", help="Exact priority filter.")
    sync_github_tasks_parser.add_argument("--owner", help="Exact owner filter.")
    sync_github_tasks_parser.add_argument("--task-kind", help="Exact task-kind filter.")
    sync_github_tasks_parser.add_argument(
        "--blocked-only",
        action="store_true",
        help="Select only tasks that currently declare blocking task IDs.",
    )
    sync_github_tasks_parser.add_argument(
        "--blocked-by",
        help="Select only tasks blocked by the given task ID.",
    )
    sync_github_tasks_parser.add_argument(
        "--depends-on",
        help="Select only tasks that depend on the given task ID.",
    )
    sync_github_tasks_parser.add_argument(
        "--project-owner",
        help="GitHub project owner login when also syncing to a project.",
    )
    sync_github_tasks_parser.add_argument(
        "--project-owner-type",
        choices=("user", "organization"),
        help="GitHub project owner type when also syncing to a project.",
    )
    sync_github_tasks_parser.add_argument(
        "--project-number",
        type=int,
        help="GitHub project number when also syncing to a project.",
    )
    sync_github_tasks_parser.add_argument(
        "--project-status-field",
        default="Status",
        help="GitHub single-select status field name for project status updates.",
    )
    sync_github_tasks_parser.add_argument(
        "--no-label-sync",
        action="store_true",
        help="Skip the managed GitHub label upsert and label mirroring step.",
    )
    sync_github_tasks_parser.add_argument(
        "--token-env",
        default="GITHUB_TOKEN",
        help="Environment variable that holds the GitHub token used for write mode.",
    )
    sync_github_tasks_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    sync_github_tasks_parser.set_defaults(handler=_run_sync_github_tasks)

    sync_traceability_index_parser = sync_subparsers.add_parser(
        "traceability-index",
        help="Rebuild the traceability index from governed planning and evidence sources.",
        description=dedent(
            """
            Rebuild the traceability index from the governed planning indexes,
            acceptance contracts, and validation evidence artifacts.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync traceability-index --write",
            "uv run watchtower-core sync traceability-index --output "
            "/tmp/traceability_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_traceability_index_parser)
    sync_traceability_index_parser.set_defaults(handler=_run_sync_traceability_index)

    sync_repository_paths_parser = sync_subparsers.add_parser(
        "repository-paths",
        help="Rebuild the repository path index from README inventories.",
        description=dedent(
            """
            Rebuild the repository path index from README inventory tables.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core sync repository-paths --write",
            "uv run watchtower-core sync repository-paths --output "
            "/tmp/repository_path_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_repository_paths_parser)
    sync_repository_paths_parser.set_defaults(handler=_run_sync_repository_paths)

    closeout_parser = subparsers.add_parser(
        "closeout",
        help="Apply terminal closeout state to traced initiatives.",
        description=dedent(
            """
            Apply initiative-level closeout state to the governed traceability
            index and refresh the human-readable planning trackers that mirror
            that state.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status completed --closure-reason \"Delivered and validated\"",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status superseded --superseded-by-trace-id trace.replacement "
            "--closure-reason \"Replaced by the new initiative\" --format json",
        ),
        formatter_class=HelpFormatter,
    )
    closeout_subparsers = closeout_parser.add_subparsers(
        dest="closeout_command",
        title="closeout commands",
        metavar="<closeout_command>",
    )
    closeout_parser.set_defaults(handler=_run_help, help_parser=closeout_parser)

    closeout_initiative_parser = closeout_subparsers.add_parser(
        "initiative",
        help="Set terminal closeout state for one traced initiative.",
        description=dedent(
            """
            Set terminal closeout state for one traced initiative and, in write
            mode, persist it to the traceability index plus the derived PRD,
            decision, and design trackers.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status completed --closure-reason \"Delivered and validated\"",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status cancelled --closure-reason \"No longer in scope\" --write",
        ),
        formatter_class=HelpFormatter,
    )
    closeout_initiative_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.core_python_foundation.",
    )
    closeout_initiative_parser.add_argument(
        "--initiative-status",
        required=True,
        choices=("completed", "superseded", "cancelled", "abandoned"),
        help="Terminal initiative status to record on the trace.",
    )
    closeout_initiative_parser.add_argument(
        "--closure-reason",
        required=True,
        help="Short human-readable reason for the closeout decision.",
    )
    closeout_initiative_parser.add_argument(
        "--superseded-by-trace-id",
        help="Replacement trace identifier. Required when initiative-status is superseded.",
    )
    closeout_initiative_parser.add_argument(
        "--closed-at",
        help="Explicit RFC 3339 UTC closeout timestamp. Defaults to the current UTC time.",
    )
    closeout_initiative_parser.add_argument(
        "--allow-open-tasks",
        action="store_true",
        help="Allow terminal closeout even if linked tasks are still open.",
    )
    closeout_initiative_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the updated closeout state and regenerated trackers to their canonical paths.",
    )
    closeout_initiative_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    closeout_initiative_parser.set_defaults(handler=_run_closeout_initiative)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Run governed validation commands.",
        description=dedent(
            """
            Run validation commands against governed repository artifacts and
            document surfaces.

            Use `front-matter` for governed Markdown metadata, `artifact` for
            schema-backed JSON contracts, indexes, ledgers, and similar
            machine-readable artifacts, and `acceptance` for semantic
            reconciliation across PRDs, acceptance contracts, validation
            evidence, and traceability.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core validate front-matter --path "
            "docs/references/front_matter_reference.md",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/indexes/traceability/traceability_index.v1.json "
            "--format json",
            "uv run watchtower-core validate acceptance --trace-id "
            "trace.core_python_foundation --format json",
            "uv run watchtower-core validate front-matter --path "
            "docs/standards/metadata/front_matter_standard.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    validate_subparsers = validate_parser.add_subparsers(
        dest="validate_command",
        title="validate commands",
        metavar="<validate_command>",
    )
    validate_parser.set_defaults(handler=_run_help, help_parser=validate_parser)

    validate_front_matter_parser = validate_subparsers.add_parser(
        "front-matter",
        help="Validate one Markdown document front-matter block.",
        description=dedent(
            """
            Validate one Markdown document front-matter block against the
            governed front-matter profiles published in the control plane.

            The command auto-selects the validator from the registry when the
            path is repository-local, or you can provide `--validator-id`
            explicitly.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core validate front-matter --path "
            "docs/references/front_matter_reference.md",
            "uv run watchtower-core validate front-matter --path "
            "docs/standards/metadata/front_matter_standard.md --format json",
            "uv run watchtower-core validate front-matter --path /tmp/example.md "
            "--validator-id validator.documentation.standard_front_matter",
            "uv run watchtower-core validate front-matter --path "
            "docs/standards/metadata/front_matter_standard.md --record-evidence "
            "--trace-id trace.core_python_foundation",
        ),
        formatter_class=HelpFormatter,
    )
    validate_front_matter_parser.add_argument(
        "--path",
        required=True,
        help="Repository-relative or absolute path to the Markdown document to validate.",
    )
    validate_front_matter_parser.add_argument(
        "--validator-id",
        help=(
            "Optional explicit validator identifier. Required for files outside "
            "the repository tree."
        ),
    )
    _add_common_validation_arguments(validate_front_matter_parser)
    validate_front_matter_parser.set_defaults(handler=_run_validate_front_matter)

    validate_artifact_parser = validate_subparsers.add_parser(
        "artifact",
        help="Validate one governed JSON artifact against registry-backed schema validators.",
        description=dedent(
            """
            Validate one governed JSON artifact against the active schema-backed
            validators published in the control plane.

            The command auto-selects the validator from the registry when the
            path is repository-local, or you can provide `--validator-id`
            explicitly for external or temporary files.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/indexes/traceability/traceability_index.v1.json "
            "--format json",
            "uv run watchtower-core validate artifact --path /tmp/example.json "
            "--validator-id validator.control_plane.acceptance_contract",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json "
            "--record-evidence --trace-id trace.core_python_foundation",
        ),
        formatter_class=HelpFormatter,
    )
    validate_artifact_parser.add_argument(
        "--path",
        required=True,
        help="Repository-relative or absolute path to the JSON artifact to validate.",
    )
    validate_artifact_parser.add_argument(
        "--validator-id",
        help=(
            "Optional explicit validator identifier. Required for files outside "
            "the repository tree."
        ),
    )
    _add_common_validation_arguments(validate_artifact_parser)
    validate_artifact_parser.set_defaults(handler=_run_validate_artifact)

    validate_acceptance_parser = validate_subparsers.add_parser(
        "acceptance",
        help="Validate one trace across PRD acceptance, contracts, evidence, and traceability.",
        description=dedent(
            """
            Validate one traced initiative across PRD acceptance IDs,
            acceptance contracts, validation evidence, validator references,
            and the traceability index.

            Use this when you need semantic acceptance reconciliation rather
            than only schema validation.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core validate acceptance --trace-id "
            "trace.core_python_foundation",
            "uv run watchtower-core validate acceptance --trace-id "
            "trace.core_python_foundation --format json",
        ),
        formatter_class=HelpFormatter,
    )
    validate_acceptance_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.core_python_foundation.",
    )
    validate_acceptance_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    validate_acceptance_parser.set_defaults(handler=_run_validate_acceptance)
    return parser


def _add_common_validation_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    parser.add_argument(
        "--record-evidence",
        action="store_true",
        help="Write a durable validation-evidence artifact and synchronized traceability update.",
    )
    parser.add_argument(
        "--trace-id",
        help="Required with --record-evidence. Shared trace identifier for the recorded evidence.",
    )
    parser.add_argument(
        "--evidence-id",
        help=(
            "Optional explicit evidence identifier. Otherwise the command "
            "derives one deterministically."
        ),
    )
    parser.add_argument(
        "--subject-id",
        action="append",
        default=[],
        help=(
            "Optional subject identifier to attach to the evidence check. "
            "Repeat for multiple values."
        ),
    )
    parser.add_argument(
        "--acceptance-id",
        action="append",
        default=[],
        help=(
            "Optional acceptance identifier to attach to the evidence check. "
            "Repeat for multiple values."
        ),
    )
    parser.add_argument(
        "--evidence-output",
        type=Path,
        help="Optional explicit output path for the evidence artifact.",
    )
    parser.add_argument(
        "--traceability-output",
        type=Path,
        help="Optional explicit output path for the updated traceability index.",
    )


def _add_common_sync_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the rebuilt artifact to the canonical control-plane path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional explicit output path for the rebuilt artifact.",
    )
    parser.add_argument(
        "--include-document",
        action="store_true",
        help="Include the generated document in json output for inspection or downstream tooling.",
    )
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )


def _run_help(args: argparse.Namespace) -> int:
    help_parser = getattr(args, "help_parser", None)
    if help_parser is None:
        return 1
    help_parser.print_help()
    return 0


def _run_doctor(args: argparse.Namespace) -> int:
    payload = {
        "command": "watchtower-core doctor",
        "workspace": "core_python",
        "status": "ok",
        "message": "watchtower_core workspace scaffold is available.",
    }
    if args.format == "json":
        print(json.dumps(payload, sort_keys=True))
        return 0

    print(payload["message"])
    return 0


def _print_payload(args: argparse.Namespace, payload: Mapping[str, object]) -> int:
    if args.format == "json":
        print(json.dumps(payload, sort_keys=True))
        return 0
    return -1


def _run_query_paths(args: argparse.Namespace) -> int:
    service = RepositoryPathQueryService(ControlPlaneLoader())
    entries = service.search(
        RepositoryPathSearchParams(
            query=args.query,
            surface_kind=args.surface_kind,
            tag=args.tag,
            parent_path=args.parent_path,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query paths",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "path": entry.path,
                "kind": entry.kind,
                "surface_kind": entry.surface_kind,
                "summary": entry.summary,
                "parent_path": entry.parent_path,
                "aliases": list(entry.aliases),
                "tags": list(entry.tags),
                "related_paths": list(entry.related_paths),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No repository path entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} repository path entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.path} [{entry.surface_kind}]")
        print(f"  {entry.summary}")
    return 0


def _run_query_commands(args: argparse.Namespace) -> int:
    service = CommandQueryService(ControlPlaneLoader())
    entries = service.search(
        CommandSearchParams(
            query=args.query,
            kind=args.kind,
            tag=args.tag,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query commands",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "command_id": entry.command_id,
                "command": entry.command,
                "kind": entry.kind,
                "summary": entry.summary,
                "doc_path": entry.doc_path,
                "synopsis": entry.synopsis,
                "implementation_path": entry.implementation_path,
                "parent_command_id": entry.parent_command_id,
                "output_formats": list(entry.output_formats),
                "default_output_format": entry.default_output_format,
                "aliases": list(entry.aliases),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No command entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} command entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.command} [{entry.kind}]")
        print(f"  {entry.summary}")
    return 0


def _run_query_prds(args: argparse.Namespace) -> int:
    service = PrdQueryService(ControlPlaneLoader())
    entries = service.search(
        PrdSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            tag=args.tag,
            requirement_id=args.requirement_id,
            acceptance_id=args.acceptance_id,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query prds",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "trace_id": entry.trace_id,
                "prd_id": entry.prd_id,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "requirement_ids": list(entry.requirement_ids),
                "acceptance_ids": list(entry.acceptance_ids),
                "linked_decision_ids": list(entry.linked_decision_ids),
                "linked_design_ids": list(entry.linked_design_ids),
                "linked_plan_ids": list(entry.linked_plan_ids),
                "related_paths": list(entry.related_paths),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No PRD entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} PRD entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.prd_id} [{entry.status}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
    return 0


def _run_query_decisions(args: argparse.Namespace) -> int:
    service = DecisionQueryService(ControlPlaneLoader())
    entries = service.search(
        DecisionSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            decision_status=args.decision_status,
            tag=args.tag,
            linked_prd_id=args.linked_prd_id,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query decisions",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "trace_id": entry.trace_id,
                "decision_id": entry.decision_id,
                "title": entry.title,
                "summary": entry.summary,
                "record_status": entry.record_status,
                "decision_status": entry.decision_status,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "linked_prd_ids": list(entry.linked_prd_ids),
                "linked_design_ids": list(entry.linked_design_ids),
                "linked_plan_ids": list(entry.linked_plan_ids),
                "related_paths": list(entry.related_paths),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No decision entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} decision entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.decision_id} [{entry.decision_status}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
    return 0


def _run_query_designs(args: argparse.Namespace) -> int:
    service = DesignDocumentQueryService(ControlPlaneLoader())
    entries = service.search(
        DesignDocumentSearchParams(
            query=args.query,
            trace_id=args.trace_id,
            family=args.family,
            tag=args.tag,
            limit=args.limit,
        )
    )
    payload = {
        "command": "watchtower-core query designs",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "document_id": entry.document_id,
                "trace_id": entry.trace_id,
                "family": entry.family,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "source_paths": list(entry.source_paths),
                "related_paths": list(entry.related_paths),
                "tags": list(entry.tags),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No design-document entries matched the requested filters.")
        return 0

    print(
        f"Found {len(entries)} design-document entr"
        f"{'y' if len(entries) == 1 else 'ies'}:"
    )
    for entry in entries:
        print(f"- {entry.document_id} [{entry.family}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
    return 0


def _run_query_acceptance(args: argparse.Namespace) -> int:
    service = AcceptanceContractQueryService(ControlPlaneLoader())
    entries = service.search(
        AcceptanceContractSearchParams(
            trace_id=args.trace_id,
            source_prd_id=args.source_prd_id,
            acceptance_id=args.acceptance_id,
        )
    )
    payload = {
        "command": "watchtower-core query acceptance",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "contract_id": entry.contract_id,
                "title": entry.title,
                "status": entry.status,
                "trace_id": entry.trace_id,
                "source_prd_id": entry.source_prd_id,
                "doc_path": entry.doc_path,
                "acceptance_ids": [item.acceptance_id for item in entry.entries],
                "required_validator_ids": sorted(
                    {
                        validator_id
                        for item in entry.entries
                        for validator_id in item.required_validator_ids
                    }
                ),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No acceptance contracts matched the requested filters.")
        return 0

    print(
        f"Found {len(entries)} acceptance contract entr"
        f"{'y' if len(entries) == 1 else 'ies'}:"
    )
    for entry in entries:
        print(f"- {entry.contract_id} [{entry.status}]")
        print(f"  Trace: {entry.trace_id}")
        print(f"  Source PRD: {entry.source_prd_id}")
        print(f"  Acceptance IDs: {', '.join(item.acceptance_id for item in entry.entries)}")
    return 0


def _run_query_evidence(args: argparse.Namespace) -> int:
    service = ValidationEvidenceQueryService(ControlPlaneLoader())
    entries = service.search(
        ValidationEvidenceSearchParams(
            trace_id=args.trace_id,
            overall_result=args.result,
            acceptance_id=args.acceptance_id,
            validator_id=args.validator_id,
        )
    )
    payload = {
        "command": "watchtower-core query evidence",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "evidence_id": entry.evidence_id,
                "title": entry.title,
                "status": entry.status,
                "trace_id": entry.trace_id,
                "overall_result": entry.overall_result,
                "recorded_at": entry.recorded_at,
                "doc_path": entry.doc_path,
                "source_prd_ids": list(entry.source_prd_ids),
                "source_acceptance_contract_ids": list(entry.source_acceptance_contract_ids),
                "check_count": len(entry.checks),
                "acceptance_ids": sorted(
                    {
                        acceptance_id
                        for check in entry.checks
                        for acceptance_id in check.acceptance_ids
                    }
                ),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No validation-evidence artifacts matched the requested filters.")
        return 0

    print(
        f"Found {len(entries)} validation-evidence artifact entr"
        f"{'y' if len(entries) == 1 else 'ies'}:"
    )
    for entry in entries:
        print(f"- {entry.evidence_id} [{entry.overall_result}]")
        print(f"  Trace: {entry.trace_id}")
        print(f"  Recorded At: {entry.recorded_at}")
        print(f"  Checks: {len(entry.checks)}")
    return 0


def _run_query_tasks(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    service = TaskQueryService(loader)
    entries = service.search(
        TaskSearchParams(
            query=args.query,
            task_ids=tuple(args.task_id),
            trace_id=args.trace_id,
            task_status=args.task_status,
            priority=args.priority,
            owner=args.owner,
            task_kind=args.task_kind,
            blocked_only=args.blocked_only,
            blocked_by_task_id=args.blocked_by,
            depends_on_task_id=args.depends_on,
            limit=args.limit,
        )
    )
    reverse_dependencies = {
        entry.task_id: service.reverse_dependencies(entry.task_id)
        for entry in entries
    }
    payload = {
        "command": "watchtower-core query tasks",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
                "task_id": entry.task_id,
                "trace_id": entry.trace_id,
                "title": entry.title,
                "summary": entry.summary,
                "status": entry.status,
                "task_status": entry.task_status,
                "task_kind": entry.task_kind,
                "priority": entry.priority,
                "owner": entry.owner,
                "doc_path": entry.doc_path,
                "updated_at": entry.updated_at,
                "blocked_by": list(entry.blocked_by),
                "depends_on": list(entry.depends_on),
                "related_ids": list(entry.related_ids),
                "applies_to": list(entry.applies_to),
                "github_repository": entry.github_repository,
                "github_issue_number": entry.github_issue_number,
                "github_issue_node_id": entry.github_issue_node_id,
                "github_project_owner": entry.github_project_owner,
                "github_project_owner_type": entry.github_project_owner_type,
                "github_project_number": entry.github_project_number,
                "github_project_item_id": entry.github_project_item_id,
                "github_synced_at": entry.github_synced_at,
                "tags": list(entry.tags),
                **(
                    {
                        "blocked_by_details": [
                            _task_dependency_payload(service.get(task_id))
                            for task_id in entry.blocked_by
                        ],
                        "depends_on_details": [
                            _task_dependency_payload(service.get(task_id))
                            for task_id in entry.depends_on
                        ],
                        "reverse_dependency_details": [
                            _task_dependency_payload(task)
                            for task in reverse_dependencies[entry.task_id]
                        ],
                    }
                    if args.include_dependency_details
                    else {}
                ),
            }
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No task entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} task entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.task_id} [{entry.task_status}, {entry.priority}]")
        print(f"  {entry.title}")
        print(f"  {entry.summary}")
        if args.include_dependency_details:
            if entry.blocked_by:
                print(f"  Blocked by: {', '.join(entry.blocked_by)}")
            if entry.depends_on:
                print(f"  Depends on: {', '.join(entry.depends_on)}")
            reverse_links = reverse_dependencies[entry.task_id]
            if reverse_links:
                print(
                    "  Reverse dependencies: "
                    + ", ".join(task.task_id for task in reverse_links)
                )
    return 0


def _run_query_trace(args: argparse.Namespace) -> int:
    service = TraceabilityQueryService(ControlPlaneLoader())
    try:
        entry = service.get(args.trace_id)
    except KeyError:
        if args.format == "json":
            print(
                json.dumps(
                    {
                        "command": "watchtower-core query trace",
                        "status": "error",
                        "message": f"Unknown trace ID: {args.trace_id}",
                    },
                    sort_keys=True,
                )
            )
            return 1
        print(f"Unknown trace ID: {args.trace_id}")
        return 1

    payload = {
        "command": "watchtower-core query trace",
        "status": "ok",
        "result": {
            "trace_id": entry.trace_id,
            "title": entry.title,
            "summary": entry.summary,
            "status": entry.status,
            "initiative_status": entry.initiative_status,
            "updated_at": entry.updated_at,
            "closed_at": entry.closed_at,
            "closure_reason": entry.closure_reason,
            "superseded_by_trace_id": entry.superseded_by_trace_id,
            "prd_ids": list(entry.prd_ids),
            "decision_ids": list(entry.decision_ids),
            "design_ids": list(entry.design_ids),
            "plan_ids": list(entry.plan_ids),
            "task_ids": list(entry.task_ids),
            "requirement_ids": list(entry.requirement_ids),
            "acceptance_ids": list(entry.acceptance_ids),
            "acceptance_contract_ids": list(entry.acceptance_contract_ids),
            "validator_ids": list(entry.validator_ids),
            "evidence_ids": list(entry.evidence_ids),
            "related_paths": list(entry.related_paths),
            "tags": list(entry.tags),
            "notes": entry.notes,
        },
    }
    if _print_payload(args, payload) == 0:
        return 0

    print(f"{entry.trace_id}: {entry.title}")
    print(entry.summary)
    print(f"Initiative Status: {entry.initiative_status}")
    if entry.closed_at is not None:
        print(f"Closed At: {entry.closed_at}")
    if entry.closure_reason is not None:
        print(f"Closure Reason: {entry.closure_reason}")
    if entry.superseded_by_trace_id is not None:
        print(f"Superseded By: {entry.superseded_by_trace_id}")
    if entry.prd_ids:
        print(f"PRDs: {', '.join(entry.prd_ids)}")
    if entry.decision_ids:
        print(f"Decisions: {', '.join(entry.decision_ids)}")
    if entry.design_ids:
        print(f"Designs: {', '.join(entry.design_ids)}")
    if entry.plan_ids:
        print(f"Plans: {', '.join(entry.plan_ids)}")
    if entry.task_ids:
        print(f"Tasks: {', '.join(entry.task_ids)}")
    if entry.acceptance_contract_ids:
        print(f"Acceptance Contracts: {', '.join(entry.acceptance_contract_ids)}")
    if entry.evidence_ids:
        print(f"Evidence: {', '.join(entry.evidence_ids)}")
    return 0


def _run_sync_repository_paths(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync repository-paths",
        artifact_label="repository path index",
        service=RepositoryPathIndexSyncService.from_repo_root(),
    )


def _run_sync_command_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync command-index",
        artifact_label="command index",
        service=CommandIndexSyncService.from_repo_root(),
    )


def _run_sync_prd_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync prd-index",
        artifact_label="PRD index",
        service=PrdIndexSyncService.from_repo_root(),
    )


def _run_sync_prd_tracking(args: argparse.Namespace) -> int:
    service = PrdTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync prd-tracking",
        "status": "ok",
        "prd_count": result.prd_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            f"Rebuilt PRD tracking with {result.prd_count} entries and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt PRD tracking with {result.prd_count} entries in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_decision_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync decision-index",
        artifact_label="decision index",
        service=DecisionIndexSyncService.from_repo_root(),
    )


def _run_sync_decision_tracking(args: argparse.Namespace) -> int:
    service = DecisionTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync decision-tracking",
        "status": "ok",
        "decision_count": result.decision_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            "Rebuilt decision tracking with "
            f"{result.decision_count} entries and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt decision tracking with {result.decision_count} entries in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_design_document_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync design-document-index",
        artifact_label="design-document index",
        service=DesignDocumentIndexSyncService.from_repo_root(),
    )


def _run_sync_design_tracking(args: argparse.Namespace) -> int:
    service = DesignTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync design-tracking",
        "status": "ok",
        "feature_design_count": result.feature_design_count,
        "implementation_plan_count": result.implementation_plan_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    total = result.feature_design_count + result.implementation_plan_count
    if wrote:
        print(f"Rebuilt design tracking with {total} documents and wrote it to {destination}.")
        return 0

    print(f"Rebuilt design tracking with {total} documents in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_task_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync task-index",
        artifact_label="task index",
        service=TaskIndexSyncService.from_repo_root(),
    )


def _run_sync_task_tracking(args: argparse.Namespace) -> int:
    service = TaskTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync task-tracking",
        "status": "ok",
        "task_count": result.task_count,
        "open_count": result.open_count,
        "closed_count": result.closed_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            f"Rebuilt task tracking with {result.task_count} tasks and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt task tracking with {result.task_count} tasks in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_github_tasks(args: argparse.Namespace) -> int:
    service = GitHubTaskSyncService(ControlPlaneLoader())
    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=tuple(args.task_id),
            trace_id=args.trace_id,
            task_status=args.task_status,
            priority=args.priority,
            owner=args.owner,
            task_kind=args.task_kind,
            blocked_only=args.blocked_only,
            blocked_by_task_id=args.blocked_by,
            depends_on_task_id=args.depends_on,
            repository=args.repo,
            project_owner=args.project_owner,
            project_owner_type=args.project_owner_type,
            project_number=args.project_number,
            project_status_field_name=args.project_status_field,
            token_env=args.token_env,
            sync_labels=not args.no_label_sync,
        ),
        write=args.write,
    )
    payload = {
        "command": "watchtower-core sync github-tasks",
        "status": "ok" if all(record.success for record in result.records) else "error",
        "wrote": result.wrote,
        "result_count": len(result.records),
        "synced_task_count": result.synced_task_count,
        "local_change_count": result.local_change_count,
        "rebuilt_task_index": result.rebuilt_task_index,
        "rebuilt_task_tracking": result.rebuilt_task_tracking,
        "rebuilt_traceability_index": result.rebuilt_traceability_index,
        "results": [
            {
                "task_id": record.task_id,
                "doc_path": record.doc_path,
                "repository": record.repository,
                "task_status": record.task_status,
                "issue_action": record.issue_action,
                "project_action": record.project_action,
                "success": record.success,
                "message": record.message,
                "github_issue_number": record.github_issue_number,
                "github_issue_url": record.github_issue_url,
                "github_project_item_id": record.github_project_item_id,
                "labels": list(record.labels),
            }
            for record in result.records
        ],
    }
    exit_code = 0 if payload["status"] == "ok" else 1
    if _print_payload(args, payload) == 0:
        return exit_code

    if not result.records:
        print("No task entries matched the requested sync filters.")
        return 0
    for record in result.records:
        state = "ok" if record.success else "error"
        print(f"- {record.task_id} [{state}]")
        print(f"  Issue action: {record.issue_action}")
        if record.project_action is not None:
            print(f"  Project action: {record.project_action}")
        if record.labels:
            print(f"  Labels: {', '.join(record.labels)}")
        if record.github_issue_url is not None:
            print(f"  GitHub Issue: {record.github_issue_url}")
        print(f"  {record.message}")
    return exit_code


def _run_sync_traceability_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync traceability-index",
        artifact_label="traceability index",
        service=TraceabilityIndexSyncService.from_repo_root(),
    )


def _run_sync_document_command(
    args: argparse.Namespace,
    *,
    command_name: str,
    artifact_label: str,
    service: (
        CommandIndexSyncService
        | DecisionIndexSyncService
        | DesignDocumentIndexSyncService
        | PrdIndexSyncService
        | RepositoryPathIndexSyncService
        | TaskIndexSyncService
        | TraceabilityIndexSyncService
    ),
) -> int:
    document = service.build_document()
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise RuntimeError(f"{artifact_label.capitalize()} document is missing its entries list.")
    entry_count = len(entries)
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(document, target))
        wrote = True

    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "entry_count": entry_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = document
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(f"Rebuilt {artifact_label} with {entry_count} entries and wrote it to {destination}.")
        return 0

    print(f"Rebuilt {artifact_label} with {entry_count} entries in dry-run mode.")
    print("Use --write to update the canonical artifact or --output <path> to write elsewhere.")
    return 0


def _run_closeout_initiative(args: argparse.Namespace) -> int:
    service = InitiativeCloseoutService(ControlPlaneLoader())
    try:
        result = service.close(
            trace_id=args.trace_id,
            initiative_status=args.initiative_status,
            closure_reason=args.closure_reason,
            superseded_by_trace_id=args.superseded_by_trace_id,
            closed_at=args.closed_at,
            write=args.write,
            allow_open_tasks=args.allow_open_tasks,
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core closeout initiative",
            str(exc),
            prefix="Closeout error",
        )

    payload = {
        "command": "watchtower-core closeout initiative",
        "status": "ok",
        "trace_id": result.trace_id,
        "initiative_status": result.initiative_status,
        "closed_at": result.closed_at,
        "closure_reason": result.closure_reason,
        "superseded_by_trace_id": result.superseded_by_trace_id,
        "open_task_ids": list(result.open_task_ids),
        "wrote": result.wrote,
        "traceability_output_path": result.traceability_output_path,
        "prd_tracking_output_path": result.prd_tracking_output_path,
        "decision_tracking_output_path": result.decision_tracking_output_path,
        "design_tracking_output_path": result.design_tracking_output_path,
    }
    if _print_payload(args, payload) == 0:
        return 0

    print(f"Closed initiative {result.trace_id} as {result.initiative_status}.")
    print(f"Closed At: {result.closed_at}")
    print(f"Reason: {result.closure_reason}")
    if result.superseded_by_trace_id is not None:
        print(f"Superseded By: {result.superseded_by_trace_id}")
    if result.open_task_ids:
        print(f"Open Tasks Left In Place: {', '.join(result.open_task_ids)}")
    if result.wrote:
        print("Canonical traceability and planning trackers were updated.")
    else:
        print("Dry-run only. Use --write to persist the closeout state.")
    return 0


def _run_validate_front_matter(args: argparse.Namespace) -> int:
    return _run_validation_command(
        args,
        command_name="watchtower-core validate front-matter",
        success_message="Front matter validated successfully.",
        service_factory=FrontMatterValidationService,
    )


def _run_validate_artifact(args: argparse.Namespace) -> int:
    return _run_validation_command(
        args,
        command_name="watchtower-core validate artifact",
        success_message="Artifact validated successfully.",
        service_factory=ArtifactValidationService,
    )


def _run_validate_acceptance(args: argparse.Namespace) -> int:
    result = AcceptanceReconciliationService(ControlPlaneLoader()).validate(args.trace_id)
    payload = _build_validation_payload(
        command_name="watchtower-core validate acceptance",
        result=result,
        evidence_write=None,
    )
    exit_code = 0 if result.passed else 1
    if _print_payload(args, payload) == 0:
        return exit_code

    return _print_validation_summary(
        result,
        evidence_write=None,
        success_message="Acceptance reconciliation passed.",
    )


def _run_validation_command(
    args: argparse.Namespace,
    *,
    command_name: str,
    success_message: str,
    service_factory: ValidationServiceFactory,
) -> int:
    message = _validate_evidence_arguments(args)
    if message is not None:
        return _emit_command_error(args, command_name, message)

    loader = ControlPlaneLoader()
    service = service_factory(loader)
    try:
        result = service.validate(args.path, validator_id=args.validator_id)
    except (ValidationExecutionError, ValidationSelectionError) as exc:
        return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    evidence_write = None
    if args.record_evidence:
        recorder = ValidationEvidenceRecorder(loader)
        try:
            evidence_write = recorder.record(
                result,
                trace_id=args.trace_id,
                evidence_id=args.evidence_id,
                subject_ids=tuple(args.subject_id),
                acceptance_ids=tuple(args.acceptance_id),
                evidence_output=_resolve_output_path(args.evidence_output),
                traceability_output=_resolve_output_path(args.traceability_output),
            )
        except ValueError as exc:
            return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    result_payload = _build_validation_payload(
        command_name=command_name,
        result=result,
        evidence_write=evidence_write,
    )
    if _print_payload(args, result_payload) == 0:
        return 0 if result.passed else 1

    return _print_validation_summary(
        result,
        evidence_write=evidence_write,
        success_message=success_message,
    )


def _validate_evidence_arguments(args: argparse.Namespace) -> str | None:
    if not args.record_evidence and (
        args.trace_id
        or args.evidence_id
        or args.subject_id
        or args.acceptance_id
        or args.evidence_output is not None
        or args.traceability_output is not None
    ):
        return (
            "--trace-id, --evidence-id, --subject-id, --acceptance-id, "
            "--evidence-output, and --traceability-output require --record-evidence."
        )
    if args.record_evidence and not args.trace_id:
        return "--trace-id is required when --record-evidence is used."
    return None


def _emit_command_error(
    args: argparse.Namespace,
    command_name: str,
    message: str,
    *,
    prefix: str | None = None,
) -> int:
    payload = {
        "command": command_name,
        "status": "error",
        "message": message,
    }
    if _print_payload(args, payload) == 0:
        return 1
    if prefix is None:
        print(message)
    else:
        print(f"{prefix}: {message}")
    return 1


def _task_dependency_payload(task: TaskIndexEntry) -> dict[str, object]:
    return {
        "task_id": task.task_id,
        "title": task.title,
        "task_status": task.task_status,
        "priority": task.priority,
        "owner": task.owner,
        "doc_path": task.doc_path,
    }


def _resolve_output_path(path: Path | None) -> Path | None:
    return path.resolve() if path is not None else None


def _build_validation_payload(
    *,
    command_name: str,
    result: ValidationResult,
    evidence_write: EvidenceWriteResult | None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "passed": result.passed,
        "validator_id": result.validator_id,
        "target_path": result.target_path,
        "engine": result.engine,
        "schema_ids": list(result.schema_ids),
        "issue_count": result.issue_count,
        "issues": [
            {
                "code": issue.code,
                "message": issue.message,
                "location": issue.location,
                "schema_id": issue.schema_id,
            }
            for issue in result.issues
        ],
    }
    if evidence_write is not None:
        payload["evidence"] = {
            "evidence_id": evidence_write.evidence_id,
            "evidence_relative_path": evidence_write.evidence_relative_path,
            "trace_id": evidence_write.trace_id,
            "recorded_at": evidence_write.recorded_at,
            "overall_result": evidence_write.overall_result,
            "evidence_output_path": evidence_write.evidence_output_path,
            "traceability_output_path": evidence_write.traceability_output_path,
        }
    return payload


def _print_validation_summary(
    result: ValidationResult,
    *,
    evidence_write: EvidenceWriteResult | None,
    success_message: str,
) -> int:
    verdict = "PASS" if result.passed else "FAIL"
    print(f"{verdict} {result.target_path}")
    print(f"Validator: {result.validator_id}")
    if result.schema_ids:
        print(f"Schemas: {', '.join(result.schema_ids)}")
    if evidence_write is not None:
        print(f"Evidence: {evidence_write.evidence_id}")
        print(f"Evidence Path: {evidence_write.evidence_output_path}")
        print(f"Traceability Path: {evidence_write.traceability_output_path}")
    if result.passed:
        print(success_message)
        return 0

    print(f"Issues: {result.issue_count}")
    for issue in result.issues:
        location = f" ({issue.location})" if issue.location else ""
        schema = f" [{issue.schema_id}]" if issue.schema_id else ""
        print(f"- {issue.code}{location}{schema}: {issue.message}")
    return 1


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
