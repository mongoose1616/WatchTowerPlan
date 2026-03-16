"""Closeout command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import HelpFormatter, examples


def register_closeout_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the closeout command family."""
    from watchtower_core.cli.closeout_handlers import (
        _run_closeout_initiative,
        _run_closeout_purge_trace,
    )
    from watchtower_core.cli.handler_common import _run_help

    closeout_parser = subparsers.add_parser(
        "closeout",
        help="Close traced initiatives or purge eligible closed trace packages.",
        description=dedent(
            """
            Apply terminal initiative state to traced planning surfaces or
            purge one eligible closed trace package after validating the
            repository's retention and reference-safety rules.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status completed --closure-reason \"Delivered and validated\"",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status superseded --superseded-by-trace-id trace.replacement "
            "--closure-reason \"Replaced by the new initiative\" --format json",
            "uv run watchtower-core closeout purge-trace --trace-id trace.example "
            "--retained-authority-path docs/standards/governance/example.md --write",
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
            mode, persist it to the traceability index plus the derived
            initiative, coordination, PRD, decision, and design trackers.
            """
        ).strip(),
        epilog=examples(
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
        "--allow-acceptance-issues",
        action="store_true",
        help=(
            "Allow terminal closeout even when acceptance reconciliation reports issues. "
            "Use only when the validation exception is intentional and explicit."
        ),
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

    closeout_purge_parser = closeout_subparsers.add_parser(
        "purge-trace",
        help="Purge one eligible closed trace package and write the purge ledger.",
        description=dedent(
            """
            Delete one closed trace-local planning package only after verifying
            terminal initiative state, no open tasks, clean acceptance
            reconciliation, and no surviving canonical references to the
            purgeable trace material.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core closeout purge-trace --trace-id trace.example "
            "--retained-authority-path docs/standards/governance/example.md",
            "uv run watchtower-core closeout purge-trace --trace-id trace.example "
            "--retained-authority-path core/python/src/watchtower_core/repo_ops/example.py "
            "--write --format json",
        ),
        formatter_class=HelpFormatter,
    )
    closeout_purge_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.core_python_foundation.",
    )
    closeout_purge_parser.add_argument(
        "--retained-authority-path",
        action="append",
        default=[],
        help=(
            "Repository-relative canonical path that remains authoritative after purge. "
            "Repeat to record more than one surviving path."
        ),
    )
    closeout_purge_parser.add_argument(
        "--purged-at",
        help="Explicit RFC 3339 UTC purge timestamp. Defaults to the current UTC time.",
    )
    closeout_purge_parser.add_argument(
        "--write",
        action="store_true",
        help="Delete the trace package, write the purge ledger, and refresh derived surfaces.",
    )
    closeout_purge_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    closeout_purge_parser.set_defaults(handler=_run_closeout_purge_trace)
