"""Thin CLI entrypoints for the WatchTower core workspace."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query import (
    CommandQueryService,
    CommandSearchParams,
    RepositoryPathQueryService,
    RepositoryPathSearchParams,
    TraceabilityQueryService,
)
from watchtower_core.sync import RepositoryPathIndexSyncService


class HelpFormatter(
    argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter
):
    """Formatter that preserves examples and shows defaults."""


def _examples(*lines: str) -> str:
    """Render a short examples block for argparse epilog text."""
    return "Examples:\n" + "\n".join(f"  {line}" for line in lines)


def build_parser() -> argparse.ArgumentParser:
    """Build the root CLI parser."""
    parser = argparse.ArgumentParser(
        prog="watchtower-core",
        description=dedent(
            """
            WatchTower core helper and harness workspace.

            Run this command from `core/python/` with `uv run` to inspect governed
            control-plane data, run lightweight workspace checks, and rebuild
            derived indexes.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core doctor",
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core sync repository-paths",
        ),
        formatter_class=HelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="<command>")

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Run a quick workspace smoke check.",
        description=dedent(
            """
            Run a small, low-risk check that confirms the core Python CLI is
            installed and reachable.

            Start here if you are new to the workspace or want the simplest
            successful `watchtower-core` invocation.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core doctor",
            "uv run watchtower-core doctor --format json",
        ),
        formatter_class=HelpFormatter,
    )
    doctor_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    doctor_parser.set_defaults(handler=_run_doctor)

    query_parser = subparsers.add_parser(
        "query",
        help="Search governed indexes for paths, commands, and traces.",
        description=dedent(
            """
            Search the governed lookup surfaces without opening the raw JSON
            artifacts directly.

            Use `paths` for repository navigation, `commands` for CLI discovery,
            and `trace` when you already know the trace identifier you want.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core query paths --query control plane",
            "uv run watchtower-core query commands --query doctor --format json",
            "uv run watchtower-core query trace --trace-id trace.core_python_foundation",
        ),
        formatter_class=HelpFormatter,
    )
    query_subparsers = query_parser.add_subparsers(
        dest="query_command",
        title="query commands",
        metavar="<query_command>",
    )
    query_parser.set_defaults(handler=_run_help, help_parser=query_parser)

    query_paths_parser = query_subparsers.add_parser(
        "paths",
        help="Search the repository path index.",
        description=dedent(
            """
            Search the repository path index by free text or exact filters.

            Omit `--query` to browse by surface kind, tag, or parent path.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core query paths --query command",
            "uv run watchtower-core query paths --surface-kind command_doc --limit 5 --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_paths_parser.add_argument(
        "--query",
        help="Free-text query over indexed path fields such as path, summary, aliases, and tags.",
    )
    query_paths_parser.add_argument(
        "--surface-kind",
        help="Exact surface-kind filter such as command_doc, standard_doc, or control_plane_index.",
    )
    query_paths_parser.add_argument("--tag", help="Exact tag filter.")
    query_paths_parser.add_argument(
        "--parent-path",
        help="Exact parent-path filter such as docs/commands/core_python/.",
    )
    query_paths_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_paths_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_paths_parser.set_defaults(handler=_run_query_paths)

    query_commands_parser = query_subparsers.add_parser(
        "commands",
        help="Search the command index.",
        description=dedent(
            """
            Search the command index for documented repository commands and
            subcommands.

            Use this when you know what task you want to perform but do not yet
            know the exact command name.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core query commands --query doctor",
            "uv run watchtower-core query commands --tag query --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_commands_parser.add_argument(
        "--query",
        help="Free-text query over indexed command fields such as command name, summary, synopsis, or aliases.",
    )
    query_commands_parser.add_argument(
        "--kind",
        help="Exact command-kind filter such as root_command or subcommand.",
    )
    query_commands_parser.add_argument("--tag", help="Exact tag filter.")
    query_commands_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return.",
    )
    query_commands_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_commands_parser.set_defaults(handler=_run_query_commands)

    query_trace_parser = query_subparsers.add_parser(
        "trace",
        help="Resolve one traceability record by trace ID.",
        description=dedent(
            """
            Resolve one traceability record by its stable trace identifier.

            Use this when you already know the trace you want and need the
            linked PRD, decision, design, plan, validator, or evidence IDs.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core query trace --trace-id trace.core_python_foundation",
            "uv run watchtower-core query trace --trace-id trace.core_python_foundation --format json",
        ),
        formatter_class=HelpFormatter,
    )
    query_trace_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.core_python_foundation.",
    )
    query_trace_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    query_trace_parser.set_defaults(handler=_run_query_trace)

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
        epilog=_examples(
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
    sync_parser.set_defaults(handler=_run_help, help_parser=sync_parser)

    sync_repository_paths_parser = sync_subparsers.add_parser(
        "repository-paths",
        help="Rebuild the repository path index from README inventories.",
        description=dedent(
            """
            Rebuild the repository path index from README inventory tables.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core sync repository-paths --write",
            "uv run watchtower-core sync repository-paths --output /tmp/repository_path_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    sync_repository_paths_parser.add_argument(
        "--write",
        action="store_true",
        help="Write the rebuilt artifact to the canonical control-plane path.",
    )
    sync_repository_paths_parser.add_argument(
        "--output",
        type=Path,
        help="Optional explicit output path for the rebuilt artifact.",
    )
    sync_repository_paths_parser.add_argument(
        "--include-document",
        action="store_true",
        help="Include the generated document in json output for inspection or downstream tooling.",
    )
    sync_repository_paths_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    sync_repository_paths_parser.set_defaults(handler=_run_sync_repository_paths)
    return parser


def _run_help(args: argparse.Namespace) -> int:
    help_parser = getattr(args, "help_parser", None)
    if help_parser is None:
        return 1
    help_parser.print_help()
    return 0


def _run_doctor(args: argparse.Namespace) -> int:
    payload = {
        "command": "watchtower-core doctor",
        "workspace": "core_python",
        "status": "ok",
        "message": "watchtower_core workspace scaffold is available.",
    }
    if args.format == "json":
        print(json.dumps(payload, sort_keys=True))
        return 0

    print(payload["message"])
    return 0


def _print_payload(args: argparse.Namespace, payload: dict[str, object]) -> int:
    if args.format == "json":
        print(json.dumps(payload, sort_keys=True))
        return 0
    return -1


def _run_query_paths(args: argparse.Namespace) -> int:
    service = RepositoryPathQueryService(ControlPlaneLoader())
    entries = service.search(
        RepositoryPathSearchParams(
            query=args.query,
            surface_kind=args.surface_kind,
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
        print(f"- {entry.path} [{entry.surface_kind}]")
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


def _run_query_trace(args: argparse.Namespace) -> int:
    service = TraceabilityQueryService(ControlPlaneLoader())
    try:
        entry = service.get(args.trace_id)
    except KeyError:
        if args.format == "json":
            print(
                json.dumps(
                    {
                        "command": "watchtower-core query trace",
                        "status": "error",
                        "message": f"Unknown trace ID: {args.trace_id}",
                    },
                    sort_keys=True,
                )
            )
            return 1
        print(f"Unknown trace ID: {args.trace_id}")
        return 1

    payload = {
        "command": "watchtower-core query trace",
        "status": "ok",
        "result": {
            "trace_id": entry.trace_id,
            "title": entry.title,
            "summary": entry.summary,
            "status": entry.status,
            "updated_at": entry.updated_at,
            "prd_ids": list(entry.prd_ids),
            "decision_ids": list(entry.decision_ids),
            "design_ids": list(entry.design_ids),
            "plan_ids": list(entry.plan_ids),
            "requirement_ids": list(entry.requirement_ids),
            "acceptance_ids": list(entry.acceptance_ids),
            "acceptance_contract_ids": list(entry.acceptance_contract_ids),
            "validator_ids": list(entry.validator_ids),
            "evidence_ids": list(entry.evidence_ids),
            "related_paths": list(entry.related_paths),
            "tags": list(entry.tags),
            "notes": entry.notes,
        },
    }
    if _print_payload(args, payload) == 0:
        return 0

    print(f"{entry.trace_id}: {entry.title}")
    print(entry.summary)
    if entry.prd_ids:
        print(f"PRDs: {', '.join(entry.prd_ids)}")
    if entry.decision_ids:
        print(f"Decisions: {', '.join(entry.decision_ids)}")
    if entry.design_ids:
        print(f"Designs: {', '.join(entry.design_ids)}")
    if entry.plan_ids:
        print(f"Plans: {', '.join(entry.plan_ids)}")
    if entry.acceptance_contract_ids:
        print(f"Acceptance Contracts: {', '.join(entry.acceptance_contract_ids)}")
    if entry.evidence_ids:
        print(f"Evidence: {', '.join(entry.evidence_ids)}")
    return 0


def _run_sync_repository_paths(args: argparse.Namespace) -> int:
    service = RepositoryPathIndexSyncService.from_repo_root()
    document = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = args.output.resolve() if args.output is not None else None
        destination = str(service.write_document(document, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync repository-paths",
        "status": "ok",
        "entry_count": len(document["entries"]),
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = document
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            f"Rebuilt repository path index with {len(document['entries'])} entries and wrote "
            f"it to {destination}."
        )
        return 0

    print(
        f"Rebuilt repository path index with {len(document['entries'])} entries in dry-run mode."
    )
    print("Use --write to update the canonical artifact or --output <path> to write elsewhere.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
