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
            metadata while keeping the command pages under `docs/commands/`
            as the human-readable companion surface.

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
        "name": "foundation-index",
        "handler": "foundation_index",
        "help": "Rebuild the foundation index from governed foundation docs.",
        "description": """
            Rebuild the foundation index from the governed foundation documents
            under `core/docs/foundations/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync foundation-index",
            "uv run watchtower-core sync foundation-index --write",
            "uv run watchtower-core sync foundation-index --output "
            "/tmp/foundation_index.json --format json",
        ),
    },
    {
        "name": "reference-index",
        "handler": "reference_index",
        "help": "Rebuild the reference index from governed reference docs.",
        "description": """
            Rebuild the reference index from the governed reference documents
            under `docs/references/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync reference-index",
            "uv run watchtower-core sync reference-index --write",
            "uv run watchtower-core sync reference-index --output "
            "/tmp/reference_index.json --format json",
        ),
    },
    {
        "name": "route-index",
        "handler": "route_index",
        "help": "Rebuild the route index from the canonical routing table.",
        "description": """
            Rebuild the route index from `core/workflows/ROUTING_TABLE.md` and `plan/workflows/ROUTING_TABLE.md`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync route-index",
            "uv run watchtower-core sync route-index --write",
            "uv run watchtower-core sync route-index --output /tmp/route_index.json "
            "--format json",
        ),
    },
    {
        "name": "standard-index",
        "handler": "standard_index",
        "help": "Rebuild the standard index from governed standards.",
        "description": """
            Rebuild the standard index from the governed standards under
            `docs/standards/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync standard-index",
            "uv run watchtower-core sync standard-index --write",
            "uv run watchtower-core sync standard-index --output "
            "/tmp/standard_index.json --format json",
        ),
    },
    {
        "name": "workflow-index",
        "handler": "workflow_index",
        "help": "Rebuild the workflow index from governed workflow modules.",
        "description": """
            Rebuild the workflow index from the workflow modules under
            `core/workflows/modules/` and `plan/workflows/modules/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync workflow-index",
            "uv run watchtower-core sync workflow-index --write",
            "uv run watchtower-core sync workflow-index --output "
            "/tmp/workflow_index.json --format json",
        ),
    },
    {
        "name": "initiative-index",
        "handler": "initiative_index",
        "help": "Rebuild the initiative index from traceability, planning, and task indexes.",
        "description": """
            Rebuild the cross-family initiative index from traceability plus
            the current planning and task indexes.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync initiative-index",
            "uv run watchtower-core sync initiative-index --write",
            "uv run watchtower-core sync initiative-index --output "
            "/tmp/initiative_index.json --format json",
        ),
    },
    {
        "name": "task-index",
        "handler": "task_index",
        "help": "Rebuild the live plan task index from initiative-local task state.",
        "description": """
            Rebuild the live plan task index from initiative-local task state
            under `plan/**/.wt/tasks/**`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync task-index",
            "uv run watchtower-core sync task-index --write",
            "uv run watchtower-core sync task-index --output /tmp/task_index.json --format json",
        ),
    },
    {
        "name": "traceability-index",
        "handler": "traceability_index",
        "help": "Rebuild the traceability index from governed planning and evidence sources.",
        "description": """
            Rebuild the traceability index from the governed planning indexes,
            acceptance contracts, and validation evidence artifacts.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """,
        "examples": (
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync traceability-index --write",
            "uv run watchtower-core sync traceability-index --output "
            "/tmp/traceability_index.json --format json",
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
