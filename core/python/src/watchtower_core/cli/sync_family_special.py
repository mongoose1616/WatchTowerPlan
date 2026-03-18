"""Root and special-case sync parser registration helpers."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path
from textwrap import dedent
from typing import TypedDict, cast

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)
from watchtower_core.cli.sync_family_common import HandlerMap


class _MaterializedSyncCommandSpec(TypedDict):
    name: str
    handler: str
    help: str
    description: str
    examples: tuple[str, ...]
    write_help: str
    output_dir_help: str


_MATERIALIZED_SYNC_COMMAND_SPECS: tuple[_MaterializedSyncCommandSpec, ...] = (
    {
        "name": "all",
        "handler": "all",
        "help": "Rebuild all local derived indexes and trackers in dependency order.",
        "description": """
            Rebuild all local deterministic sync surfaces in one run.

            This includes local index and tracker surfaces only. It does not call
            hosted integrations such as GitHub task sync.
            """,
        "examples": (
            "uv run watchtower-core sync all",
            "uv run watchtower-core sync all --write",
            "uv run watchtower-core sync all --output-dir /tmp/watchtower_sync --format json",
        ),
        "write_help": "Write rebuilt artifacts and trackers to their canonical repository paths.",
        "output_dir_help": (
            "Optional explicit directory for materializing all rebuilt surfaces while "
            "preserving their repo-relative paths."
        ),
    },
    {
        "name": "coordination",
        "handler": "coordination",
        "help": "Rebuild the deterministic coordination slice and compact human tracker.",
        "description": """
            Rebuild the deterministic coordination slice for task, traceability,
            initiative, coordination-index, and compact coordination-tracking
            surfaces in dependency order.

            This is the focused rebuild path for local execution coordination
            without refreshing unrelated reference, standards, or command docs.
            """,
        "examples": (
            "uv run watchtower-core sync coordination",
            "uv run watchtower-core sync coordination --write",
            "uv run watchtower-core sync coordination --output-dir "
            "/tmp/watchtower_coordination --format json",
        ),
        "write_help": "Write rebuilt coordination surfaces to their canonical repository paths.",
        "output_dir_help": (
            "Optional explicit directory for materializing the coordination slice while "
            "preserving repo-relative paths."
        ),
    },
)


def build_sync_subparsers(
    subparsers: argparse._SubParsersAction,
    *,
    help_handler: Callable[..., int],
) -> argparse._SubParsersAction:
    """Create the root sync parser and return its subparser collection."""

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
            "uv run watchtower-core sync route-index",
            "uv run watchtower-core sync route-index --write",
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
            "uv run watchtower-core sync planning-catalog",
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
    sync_parser.set_defaults(handler=help_handler, help_parser=sync_parser)
    return cast(argparse._SubParsersAction, sync_subparsers)


def register_special_sync_commands(
    sync_subparsers: argparse._SubParsersAction,
    handlers: HandlerMap,
) -> None:
    """Register orchestration and integration sync commands."""

    for spec in _MATERIALIZED_SYNC_COMMAND_SPECS:
        parser = sync_subparsers.add_parser(
            spec["name"],
            help=spec["help"],
            description=dedent(spec["description"]).strip(),
            epilog=examples(*spec["examples"]),
            formatter_class=HelpFormatter,
        )
        parser.add_argument(
            "--write",
            action="store_true",
            help=spec["write_help"],
        )
        parser.add_argument(
            "--output-dir",
            type=Path,
            help=spec["output_dir_help"],
        )
        add_human_json_format_argument(parser)
        parser.set_defaults(handler=handlers[spec["handler"]])

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

            The dry-run command output is the authoritative preview for this
            command's task-selection filters.
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
        help="Exact docs-backed task identifier filter. Repeat for multiple task IDs.",
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
    add_human_json_format_argument(sync_github_tasks_parser)
    sync_github_tasks_parser.set_defaults(handler=handlers["github_tasks"])
