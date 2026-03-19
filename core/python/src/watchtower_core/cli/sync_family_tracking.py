"""Tracker-oriented sync parser registration helpers."""

from __future__ import annotations

import argparse

from watchtower_core.cli.sync_family_common import (
    HandlerMap,
    SyncCommandSpec,
    register_spec_sync_commands,
)

_TRACKING_COMMAND_SPECS: tuple[SyncCommandSpec, ...] = (
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
        "help": "Rebuild the human-readable task tracker from live initiative-local task state.",
        "description": """
            Rebuild the human-readable task tracker from initiative-local live
            task state under `plan/**/.wt/tasks/**`.

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

    register_spec_sync_commands(
        sync_subparsers,
        handlers=handlers,
        specs=_TRACKING_COMMAND_SPECS,
    )
