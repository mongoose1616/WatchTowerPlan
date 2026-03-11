"""Tracker-oriented sync parser registration helpers."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping
from textwrap import dedent
from typing import TypedDict

from watchtower_core.cli.common import HelpFormatter, add_common_sync_arguments, examples

HandlerMap = Mapping[str, Callable[..., int]]


class _TrackingCommandSpec(TypedDict):
    name: str
    handler: str
    help: str
    description: str
    examples: tuple[str, ...]


_TRACKING_COMMAND_SPECS: tuple[_TrackingCommandSpec, ...] = (
    {
        "name": "prd-tracking",
        "handler": "prd_tracking",
        "help": "Rebuild the human-readable PRD tracker from the PRD index.",
        "description": """
            Rebuild the human-readable PRD tracker from the governed PRD index
            and the initiative-closeout state stored in traceability.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync prd-tracking",
            "uv run watchtower-core sync prd-tracking --write",
            "uv run watchtower-core sync prd-tracking --output /tmp/prd_tracking.md --format json",
        ),
    },
    {
        "name": "decision-tracking",
        "handler": "decision_tracking",
        "help": "Rebuild the human-readable decision tracker from the decision index.",
        "description": """
            Rebuild the human-readable decision tracker from the governed
            decision index and the initiative-closeout state stored in
            traceability.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync decision-tracking",
            "uv run watchtower-core sync decision-tracking --write",
            "uv run watchtower-core sync decision-tracking --output "
            "/tmp/decision_tracking.md --format json",
        ),
    },
    {
        "name": "design-tracking",
        "handler": "design_tracking",
        "help": "Rebuild the human-readable design tracker from the design index.",
        "description": """
            Rebuild the human-readable design tracker from the governed design
            index and the initiative-closeout state stored in traceability.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync design-tracking",
            "uv run watchtower-core sync design-tracking --write",
            "uv run watchtower-core sync design-tracking --output "
            "/tmp/design_tracking.md --format json",
        ),
    },
    {
        "name": "initiative-tracking",
        "handler": "initiative_tracking",
        "help": "Rebuild the human-readable initiative tracker from the initiative index.",
        "description": """
            Rebuild the human-readable initiative tracker from the governed
            initiative index.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync initiative-tracking",
            "uv run watchtower-core sync initiative-tracking --write",
            "uv run watchtower-core sync initiative-tracking --output "
            "/tmp/initiative_tracking.md --format json",
        ),
    },
    {
        "name": "task-tracking",
        "handler": "task_tracking",
        "help": "Rebuild the human-readable task tracker from governed task records.",
        "description": """
            Rebuild the human-readable task tracker from the governed task
            documents under `docs/planning/tasks/`.

            By default this is a dry run. Add `--write` to update the canonical
            tracker or `--output` to materialize it elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync task-tracking",
            "uv run watchtower-core sync task-tracking --write",
            "uv run watchtower-core sync task-tracking --output "
            "/tmp/task_tracking.md --format json",
        ),
    },
)


def register_tracking_sync_commands(
    sync_subparsers: argparse._SubParsersAction,
    handlers: HandlerMap,
) -> None:
    """Register the tracker-oriented sync commands."""

    for spec in _TRACKING_COMMAND_SPECS:
        parser = sync_subparsers.add_parser(
            spec["name"],
            help=spec["help"],
            description=dedent(spec["description"]).strip(),
            epilog=examples(*spec["examples"]),
            formatter_class=HelpFormatter,
        )
        add_common_sync_arguments(parser)
        parser.set_defaults(handler=handlers[spec["handler"]])
