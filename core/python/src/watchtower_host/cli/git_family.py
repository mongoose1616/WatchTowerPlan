"""Git command-family registration."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, add_human_json_format_argument, examples


def register_git_family(subparsers: argparse._SubParsersAction) -> None:
    """Register the local git hygiene command family."""

    from watchtower_core.cli.handler_common import _run_help
    from watchtower_host.cli.git_handlers import _run_git_hygiene

    git_parser = subparsers.add_parser(
        "git",
        help="Inspect and apply local branch and worktree hygiene decisions.",
        description=dedent(
            """
            Inspect local branch and worktree hygiene using the repository's
            current git-workflow policy.

            This command family evaluates which branches or worktrees look old,
            which ones still appear active, and which conservative cleanup
            actions are safe to apply automatically.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core git hygiene --format json",
            "uv run watchtower-core git hygiene --base-ref main --apply --format json",
        ),
        formatter_class=HelpFormatter,
    )
    git_subparsers = git_parser.add_subparsers(
        dest="git_command",
        title="git commands",
        metavar="<git_command>",
    )
    git_parser.set_defaults(handler=_run_help, help_parser=git_parser)

    hygiene_parser = git_subparsers.add_parser(
        "hygiene",
        help="Evaluate local branches and worktrees for merge, review, or cleanup.",
        description=dedent(
            """
            Evaluate local branches and worktrees against the repository's
            origin-aware branch and cleanup policy.

            The command is read-only by default. Pass `--apply` to perform only
            the conservative cleanup actions that the evaluator marks safe,
            currently merged-or-empty branch deletion and clean temporary
            worktree removal.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core git hygiene --format json",
            "uv run watchtower-core git hygiene --repo-root /path/to/repo --format json",
            "uv run watchtower-core git hygiene --base-ref origin/main --apply --format json",
        ),
        formatter_class=HelpFormatter,
    )
    hygiene_parser.add_argument(
        "--repo-root",
        type=Path,
        help=(
            "Optional repository path inside the git worktree to inspect. Defaults to the "
            "current working directory."
        ),
    )
    hygiene_parser.add_argument(
        "--base-ref",
        default="main",
        help="Base ref used to evaluate merge state and unique branch commits. Defaults to main.",
    )
    hygiene_parser.add_argument(
        "--inactive-days",
        type=int,
        default=14,
        help="Inactivity threshold used as one old-state signal. Defaults to 14 days.",
    )
    hygiene_parser.add_argument(
        "--override-path",
        type=Path,
        help=(
            "Optional JSON file carrying local-only defer, handoff, or supersession overrides. "
            "Defaults to the shared git common-dir watchtower override path."
        ),
    )
    hygiene_parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Apply only conservative cleanup actions that the evaluation marks safe. "
            "Ambiguous cases remain review-only."
        ),
    )
    add_human_json_format_argument(hygiene_parser)
    hygiene_parser.set_defaults(handler=_run_git_hygiene)
