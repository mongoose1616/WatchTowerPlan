"""Runtime handlers for discovery-oriented query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_collection_query_results
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import CommandIndexEntry, RepositoryPathEntry
from watchtower_core.query import (
    CommandQueryService,
    CommandSearchParams,
    RepositoryPathQueryService,
    RepositoryPathSearchParams,
)


def _run_query_paths(args: argparse.Namespace) -> int:
    service = RepositoryPathQueryService(ControlPlaneLoader())
    entries = service.search(
        RepositoryPathSearchParams(
            query=args.query,
            surface_kind=args.surface_kind,
            maturity=args.maturity,
            priority=args.priority,
            audience_hint=args.audience_hint,
            tag=args.tag,
            parent_path=args.parent_path,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query paths",
        entries=entries,
        noun="repository path",
        empty_message="No repository path entries matched the requested filters.",
        payload_results_factory=lambda: [_path_entry_payload(entry) for entry in entries],
        render_entry=_print_path_entry,
    )


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
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query commands",
        entries=entries,
        noun="command",
        empty_message="No command entries matched the requested filters.",
        payload_results_factory=lambda: [_command_entry_payload(entry) for entry in entries],
        render_entry=_print_command_entry,
    )


def _path_entry_payload(entry: RepositoryPathEntry) -> dict[str, object]:
    return {
        "path": entry.path,
        "kind": entry.kind,
        "surface_kind": entry.surface_kind,
        "summary": entry.summary,
        "parent_path": entry.parent_path,
        "maturity": entry.maturity,
        "priority": entry.priority,
        "audience_hint": entry.audience_hint,
        "aliases": list(entry.aliases),
        "tags": list(entry.tags),
        "related_paths": list(entry.related_paths),
    }


def _print_path_entry(entry: RepositoryPathEntry) -> None:
    print(
        f"- {entry.path} "
        f"[{entry.surface_kind}, {entry.maturity}, {entry.priority}, {entry.audience_hint}]"
    )
    print(f"  {entry.summary}")


def _command_entry_payload(entry: CommandIndexEntry) -> dict[str, object]:
    return {
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


def _print_command_entry(entry: CommandIndexEntry) -> None:
    print(f"- {entry.command} [{entry.kind}]")
    print(f"  {entry.summary}")
