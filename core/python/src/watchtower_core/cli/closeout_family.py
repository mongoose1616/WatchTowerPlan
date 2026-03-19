"""Closeout command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_human_json_format_argument,
    examples,
)


def register_closeout_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the closeout command family."""
    from watchtower_core.cli.closeout_handlers import (
        _run_closeout_initiative,
        _run_closeout_plan_initiative,
        _run_closeout_purge_trace,
    )
    from watchtower_core.cli.handler_common import _run_help

    closeout_parser = subparsers.add_parser(
        "closeout",
        help="Close live or retained initiatives, or purge eligible closed trace packages.",
        description=dedent(
            """
            Apply terminal initiative state to live `plan/**` initiative
            packages, close retained traced initiatives when historical trace
            state must be finalized, or purge one eligible closed trace
            package after validating the repository's retention and
            reference-safety rules.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core closeout plan-initiative --initiative-slug plan_workspace_bootstrap "
            "--initiative-status completed --closure-reason \"Live plan slice delivered\" --write",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status completed --closure-reason \"Closed the retained traced planning package\"",
            "uv run watchtower-core closeout initiative --trace-id trace.example "
            "--initiative-status superseded --superseded-by-trace-id trace.replacement "
            "--closure-reason \"Replaced by the new initiative\" --format json",
            "uv run watchtower-core closeout purge-trace --trace-id trace.example "
            "--retained-authority-path plan/docs/standards/governance/example.md --write",
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
            initiative, coordination, decision, design, and implementation trackers.
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
        help="Stable trace identifier such as trace.governed_acceptance_example.",
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
    add_human_json_format_argument(closeout_initiative_parser)
    closeout_initiative_parser.set_defaults(handler=_run_closeout_initiative)

    closeout_plan_initiative_parser = closeout_subparsers.add_parser(
        "plan-initiative",
        help="Set terminal closeout state for one live plan initiative package.",
        description=dedent(
            """
            Set terminal closeout state for one pack-wide or project-scoped
            live initiative package under `plan/**` and refresh the derived
            plan indexes plus rendered views that surface active and recent
            closeouts.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core closeout plan-initiative --initiative-slug plan_workspace_bootstrap "
            "--initiative-status completed --closure-reason \"Delivered the live plan slice\"",
            "uv run watchtower-core closeout plan-initiative --project-slug watchtower "
            "--initiative-slug watchtower_work_item_notes --initiative-status completed "
            "--closure-reason \"Implemented and validated work-item notes\" --write",
        ),
        formatter_class=HelpFormatter,
    )
    closeout_plan_initiative_parser.add_argument(
        "--initiative-slug",
        required=True,
        help="Initiative slug such as plan_workspace_bootstrap or watchtower_work_item_notes.",
    )
    closeout_plan_initiative_parser.add_argument(
        "--project-slug",
        help="Project slug when the initiative is project-scoped, such as watchtower.",
    )
    closeout_plan_initiative_parser.add_argument(
        "--initiative-status",
        required=True,
        choices=("completed", "superseded", "cancelled"),
        help="Terminal initiative status to record on the live plan package.",
    )
    closeout_plan_initiative_parser.add_argument(
        "--closure-reason",
        required=True,
        help="Short human-readable reason for the closeout decision.",
    )
    closeout_plan_initiative_parser.add_argument(
        "--superseded-by-trace-id",
        help="Replacement trace identifier. Required when initiative-status is superseded.",
    )
    closeout_plan_initiative_parser.add_argument(
        "--closed-at",
        help="Explicit RFC 3339 UTC closeout timestamp. Defaults to the current UTC time.",
    )
    closeout_plan_initiative_parser.add_argument(
        "--write",
        action="store_true",
        help="Persist the updated closeout state and regenerated plan surfaces.",
    )
    add_human_json_format_argument(closeout_plan_initiative_parser)
    closeout_plan_initiative_parser.set_defaults(handler=_run_closeout_plan_initiative)

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
            "--retained-authority-path plan/docs/standards/governance/example.md",
            "uv run watchtower-core closeout purge-trace --trace-id trace.example "
            "--retained-authority-path core/python/src/watchtower_core/plan_runtime/example.py "
            "--write --format json",
        ),
        formatter_class=HelpFormatter,
    )
    closeout_purge_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.governed_acceptance_example.",
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
    add_human_json_format_argument(closeout_purge_parser)
    closeout_purge_parser.set_defaults(handler=_run_closeout_purge_trace)
