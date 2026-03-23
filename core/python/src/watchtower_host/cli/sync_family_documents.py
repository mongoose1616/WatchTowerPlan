"""Document-oriented sync parser registration helpers."""

from __future__ import annotations

import argparse

from watchtower_core.cli.sync_family_common import (
    HandlerMap,
    SyncCommandSpec,
    register_spec_sync_commands,
)

_DOCUMENT_COMMAND_SPECS: tuple[SyncCommandSpec, ...] = (
    {
        "name": "command-index",
        "handler": "command_index",
        "help": "Rebuild the command index from registry-backed CLI metadata.",
        "description": """
            Rebuild the command index from the registry-backed CLI parser
            metadata while keeping the human-readable companion pages under
            `core/docs/commands/` for shared commands and the owning pack docs
            root for pack-native commands.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync command-index --output "
            "/tmp/command_index.json --format json",
        ),
    },
    {
        "name": "route-index",
        "handler": "route_index",
        "help": "Rebuild the route index from the canonical routing table.",
        "description": """
            Rebuild the route index from `core/workflows/ROUTING_TABLE.md`
            plus any pack-owned routing tables.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync route-index",
            "uv run watchtower-core sync route-index --write",
            "uv run watchtower-core sync route-index --output /tmp/route_index.json --format json",
        ),
    },
    {
        "name": "repository-paths",
        "handler": "repository_paths",
        "help": "Rebuild the repository path index from README inventories.",
        "description": """
            Rebuild the repository path index from README inventory tables.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core sync repository-paths --write",
            "uv run watchtower-core sync repository-paths --output "
            "/tmp/repository_path_index.json --format json",
        ),
    },
)


def register_document_sync_commands(
    sync_subparsers: argparse._SubParsersAction,
    handlers: HandlerMap,
) -> None:
    """Register the document-oriented sync commands."""

    register_spec_sync_commands(
        sync_subparsers,
        handlers=handlers,
        specs=_DOCUMENT_COMMAND_SPECS,
    )
