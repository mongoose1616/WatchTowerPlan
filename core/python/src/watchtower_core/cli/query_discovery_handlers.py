"""Runtime handlers for discovery-oriented query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _print_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query import (
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
    payload = {
        "command": "watchtower-core query paths",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
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
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No repository path entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} repository path entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(
            f"- {entry.path} "
            f"[{entry.surface_kind}, {entry.maturity}, {entry.priority}, {entry.audience_hint}]"
        )
        print(f"  {entry.summary}")
    return 0


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
    payload = {
        "command": "watchtower-core query commands",
        "status": "ok",
        "result_count": len(entries),
        "results": [
            {
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
            for entry in entries
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    if not entries:
        print("No command entries matched the requested filters.")
        return 0

    print(f"Found {len(entries)} command entr{'y' if len(entries) == 1 else 'ies'}:")
    for entry in entries:
        print(f"- {entry.command} [{entry.kind}]")
        print(f"  {entry.summary}")
    return 0
