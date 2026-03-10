"""Sync command-family registration."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, add_common_sync_arguments, examples


def register_sync_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the sync command family and its subcommands."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_core.cli.sync_handlers import (
        _run_sync_all,
        _run_sync_command_index,
        _run_sync_coordination,
        _run_sync_decision_index,
        _run_sync_decision_tracking,
        _run_sync_design_document_index,
        _run_sync_design_tracking,
        _run_sync_foundation_index,
        _run_sync_github_tasks,
        _run_sync_initiative_index,
        _run_sync_initiative_tracking,
        _run_sync_prd_index,
        _run_sync_prd_tracking,
        _run_sync_reference_index,
        _run_sync_repository_paths,
        _run_sync_standard_index,
        _run_sync_task_index,
        _run_sync_task_tracking,
        _run_sync_traceability_index,
        _run_sync_workflow_index,
    )

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
        epilog=examples(
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync all",
            "uv run watchtower-core sync all --write",
            "uv run watchtower-core sync coordination",
            "uv run watchtower-core sync coordination --write",
            "uv run watchtower-core sync reference-index",
            "uv run watchtower-core sync reference-index --write",
            "uv run watchtower-core sync standard-index",
            "uv run watchtower-core sync standard-index --write",
            "uv run watchtower-core sync workflow-index",
            "uv run watchtower-core sync workflow-index --write",
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync prd-tracking",
            "uv run watchtower-core sync decision-index",
            "uv run watchtower-core sync decision-tracking",
            "uv run watchtower-core sync design-document-index",
            "uv run watchtower-core sync design-tracking",
            "uv run watchtower-core sync initiative-index",
            "uv run watchtower-core sync initiative-tracking",
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
        help="Rebuild the command index from registry-backed CLI metadata.",
        description=dedent(
            """
            Rebuild the command index from the registry-backed CLI parser
            metadata while keeping the command pages under `docs/commands/`
            as the human-readable companion surface.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync command-index --output "
            "/tmp/command_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_command_index_parser)
    sync_command_index_parser.set_defaults(handler=_run_sync_command_index)

    sync_foundation_index_parser = sync_subparsers.add_parser(
        "foundation-index",
        help="Rebuild the foundation index from governed foundation docs.",
        description=dedent(
            """
            Rebuild the foundation index from the governed foundation documents
            under `docs/foundations/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync foundation-index",
            "uv run watchtower-core sync foundation-index --write",
            "uv run watchtower-core sync foundation-index --output "
            "/tmp/foundation_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_foundation_index_parser)
    sync_foundation_index_parser.set_defaults(handler=_run_sync_foundation_index)

    sync_all_parser = sync_subparsers.add_parser(
        "all",
        help="Rebuild all local derived indexes and trackers in dependency order.",
        description=dedent(
            """
            Rebuild all local deterministic sync surfaces in one run.

            This includes local index and tracker surfaces only. It does not call
            hosted integrations such as GitHub task sync.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync all",
            "uv run watchtower-core sync all --write",
            "uv run watchtower-core sync all --output-dir /tmp/watchtower_sync --format json",
        ),
        formatter_class=HelpFormatter,
    )
    sync_all_parser.add_argument(
        "--write",
        action="store_true",
        help="Write rebuilt artifacts and trackers to their canonical repository paths.",
    )
    sync_all_parser.add_argument(
        "--output-dir",
        type=Path,
        help=(
            "Optional explicit directory for materializing all rebuilt surfaces while "
            "preserving their repo-relative paths."
        ),
    )
    sync_all_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    sync_all_parser.set_defaults(handler=_run_sync_all)

    sync_coordination_parser = sync_subparsers.add_parser(
        "coordination",
        help="Rebuild the deterministic coordination slice and compact human tracker.",
        description=dedent(
            """
            Rebuild the deterministic coordination slice for task, traceability,
            initiative, coordination-index, and compact coordination-tracking
            surfaces in dependency order.

            This is the focused rebuild path for local execution coordination
            without refreshing unrelated reference, standards, or command docs.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync coordination",
            "uv run watchtower-core sync coordination --write",
            "uv run watchtower-core sync coordination --output-dir "
            "/tmp/watchtower_coordination --format json",
        ),
        formatter_class=HelpFormatter,
    )
    sync_coordination_parser.add_argument(
        "--write",
        action="store_true",
        help="Write rebuilt coordination surfaces to their canonical repository paths.",
    )
    sync_coordination_parser.add_argument(
        "--output-dir",
        type=Path,
        help=(
            "Optional explicit directory for materializing the coordination slice while "
            "preserving repo-relative paths."
        ),
    )
    sync_coordination_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    sync_coordination_parser.set_defaults(handler=_run_sync_coordination)

    sync_reference_index_parser = sync_subparsers.add_parser(
        "reference-index",
        help="Rebuild the reference index from governed reference docs.",
        description=dedent(
            """
            Rebuild the reference index from the governed reference documents
            under `docs/references/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync reference-index",
            "uv run watchtower-core sync reference-index --write",
            "uv run watchtower-core sync reference-index --output "
            "/tmp/reference_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_reference_index_parser)
    sync_reference_index_parser.set_defaults(handler=_run_sync_reference_index)

    sync_standard_index_parser = sync_subparsers.add_parser(
        "standard-index",
        help="Rebuild the standard index from governed standards.",
        description=dedent(
            """
            Rebuild the standard index from the governed standards under
            `docs/standards/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync standard-index",
            "uv run watchtower-core sync standard-index --write",
            "uv run watchtower-core sync standard-index --output "
            "/tmp/standard_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_standard_index_parser)
    sync_standard_index_parser.set_defaults(handler=_run_sync_standard_index)

    sync_workflow_index_parser = sync_subparsers.add_parser(
        "workflow-index",
        help="Rebuild the workflow index from governed workflow modules.",
        description=dedent(
            """
            Rebuild the workflow index from the workflow modules under
            `workflows/modules/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync workflow-index",
            "uv run watchtower-core sync workflow-index --write",
            "uv run watchtower-core sync workflow-index --output "
            "/tmp/workflow_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_workflow_index_parser)
    sync_workflow_index_parser.set_defaults(handler=_run_sync_workflow_index)

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
        epilog=examples(
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync prd-index --write",
            "uv run watchtower-core sync prd-index --output /tmp/prd_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_prd_index_parser)
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
        epilog=examples(
            "uv run watchtower-core sync prd-tracking",
            "uv run watchtower-core sync prd-tracking --write",
            "uv run watchtower-core sync prd-tracking --output /tmp/prd_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_prd_tracking_parser)
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
        epilog=examples(
            "uv run watchtower-core sync decision-index",
            "uv run watchtower-core sync decision-index --write",
            "uv run watchtower-core sync decision-index --output "
            "/tmp/decision_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_decision_index_parser)
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
        epilog=examples(
            "uv run watchtower-core sync decision-tracking",
            "uv run watchtower-core sync decision-tracking --write",
            "uv run watchtower-core sync decision-tracking --output "
            "/tmp/decision_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_decision_tracking_parser)
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
        epilog=examples(
            "uv run watchtower-core sync design-document-index",
            "uv run watchtower-core sync design-document-index --write",
            "uv run watchtower-core sync design-document-index --output "
            "/tmp/design_document_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_design_document_index_parser)
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
        epilog=examples(
            "uv run watchtower-core sync design-tracking",
            "uv run watchtower-core sync design-tracking --write",
            "uv run watchtower-core sync design-tracking --output "
            "/tmp/design_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_design_tracking_parser)
    sync_design_tracking_parser.set_defaults(handler=_run_sync_design_tracking)

    sync_initiative_index_parser = sync_subparsers.add_parser(
        "initiative-index",
        help="Rebuild the initiative index from traceability, planning, and task indexes.",
        description=dedent(
            """
            Rebuild the cross-family initiative index from traceability plus
            the current planning and task indexes.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync initiative-index",
            "uv run watchtower-core sync initiative-index --write",
            "uv run watchtower-core sync initiative-index --output "
            "/tmp/initiative_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_initiative_index_parser)
    sync_initiative_index_parser.set_defaults(handler=_run_sync_initiative_index)

    sync_initiative_tracking_parser = sync_subparsers.add_parser(
        "initiative-tracking",
        help="Rebuild the human-readable initiative tracker from the initiative index.",
        description=dedent(
            """
            Rebuild the human-readable initiative tracker from the governed
            initiative index.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core sync initiative-tracking",
            "uv run watchtower-core sync initiative-tracking --write",
            "uv run watchtower-core sync initiative-tracking --output "
            "/tmp/initiative_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_initiative_tracking_parser)
    sync_initiative_tracking_parser.set_defaults(handler=_run_sync_initiative_tracking)

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
        epilog=examples(
            "uv run watchtower-core sync task-index",
            "uv run watchtower-core sync task-index --write",
            "uv run watchtower-core sync task-index --output /tmp/task_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_task_index_parser)
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
        epilog=examples(
            "uv run watchtower-core sync task-tracking",
            "uv run watchtower-core sync task-tracking --write",
            "uv run watchtower-core sync task-tracking --output "
            "/tmp/task_tracking.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_task_tracking_parser)
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
        epilog=examples(
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
        epilog=examples(
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync traceability-index --write",
            "uv run watchtower-core sync traceability-index --output "
            "/tmp/traceability_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_traceability_index_parser)
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
        epilog=examples(
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core sync repository-paths --write",
            "uv run watchtower-core sync repository-paths --output "
            "/tmp/repository_path_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    add_common_sync_arguments(sync_repository_paths_parser)
    sync_repository_paths_parser.set_defaults(handler=_run_sync_repository_paths)
