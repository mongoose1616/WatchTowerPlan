"""Thin CLI entrypoints for the WatchTower core workspace."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from textwrap import dedent

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.evidence import EvidenceWriteResult, ValidationEvidenceRecorder
from watchtower_core.query import (
    CommandQueryService,
    CommandSearchParams,
    RepositoryPathQueryService,
    RepositoryPathSearchParams,
    TraceabilityQueryService,
)
from watchtower_core.sync import (
    CommandIndexSyncService,
    DecisionIndexSyncService,
    DesignDocumentIndexSyncService,
    PrdIndexSyncService,
    RepositoryPathIndexSyncService,
    TraceabilityIndexSyncService,
)
from watchtower_core.validation import (
    ArtifactValidationService,
    FrontMatterValidationService,
    ValidationExecutionError,
    ValidationResult,
    ValidationSelectionError,
)


class HelpFormatter(
    argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter
):
    """Formatter that preserves examples and shows defaults."""


ValidationServiceFactory = Callable[
    [ControlPlaneLoader],
    FrontMatterValidationService | ArtifactValidationService,
]


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
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync repository-paths",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
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
        help=(
            "Free-text query over indexed command fields such as command name, "
            "summary, synopsis, or aliases."
        ),
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
            "uv run watchtower-core query trace --trace-id "
            "trace.core_python_foundation --format json",
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
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync decision-index",
            "uv run watchtower-core sync design-document-index",
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync traceability-index --write",
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

    sync_command_index_parser = sync_subparsers.add_parser(
        "command-index",
        help="Rebuild the command index from authored command docs.",
        description=dedent(
            """
            Rebuild the command index from the authored command pages under
            `docs/commands/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync command-index",
            "uv run watchtower-core sync command-index --write",
            "uv run watchtower-core sync command-index --output "
            "/tmp/command_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_command_index_parser)
    sync_command_index_parser.set_defaults(handler=_run_sync_command_index)

    sync_prd_index_parser = sync_subparsers.add_parser(
        "prd-index",
        help="Rebuild the PRD index from governed PRD documents.",
        description=dedent(
            """
            Rebuild the PRD index from the governed PRD documents under
            `docs/planning/prds/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync prd-index",
            "uv run watchtower-core sync prd-index --write",
            "uv run watchtower-core sync prd-index --output /tmp/prd_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_prd_index_parser)
    sync_prd_index_parser.set_defaults(handler=_run_sync_prd_index)

    sync_decision_index_parser = sync_subparsers.add_parser(
        "decision-index",
        help="Rebuild the decision index from governed decision records.",
        description=dedent(
            """
            Rebuild the decision index from the governed decision records under
            `docs/planning/decisions/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync decision-index",
            "uv run watchtower-core sync decision-index --write",
            "uv run watchtower-core sync decision-index --output "
            "/tmp/decision_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_decision_index_parser)
    sync_decision_index_parser.set_defaults(handler=_run_sync_decision_index)

    sync_design_document_index_parser = sync_subparsers.add_parser(
        "design-document-index",
        help="Rebuild the design-document index from governed design docs.",
        description=dedent(
            """
            Rebuild the design-document index from the governed design documents
            under `docs/planning/design/`.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync design-document-index",
            "uv run watchtower-core sync design-document-index --write",
            "uv run watchtower-core sync design-document-index --output "
            "/tmp/design_document_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_design_document_index_parser)
    sync_design_document_index_parser.set_defaults(handler=_run_sync_design_document_index)

    sync_traceability_index_parser = sync_subparsers.add_parser(
        "traceability-index",
        help="Rebuild the traceability index from governed planning and evidence sources.",
        description=dedent(
            """
            Rebuild the traceability index from the governed planning indexes,
            acceptance contracts, and validation evidence artifacts.

            By default this is a dry run. Add `--write` to update the canonical
            artifact or `--output` to materialize the rebuilt document elsewhere.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core sync traceability-index",
            "uv run watchtower-core sync traceability-index --write",
            "uv run watchtower-core sync traceability-index --output "
            "/tmp/traceability_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_traceability_index_parser)
    sync_traceability_index_parser.set_defaults(handler=_run_sync_traceability_index)

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
            "uv run watchtower-core sync repository-paths --output "
            "/tmp/repository_path_index.v1.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    _add_common_sync_arguments(sync_repository_paths_parser)
    sync_repository_paths_parser.set_defaults(handler=_run_sync_repository_paths)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Run governed validation commands.",
        description=dedent(
            """
            Run validation commands against governed repository artifacts and
            document surfaces.

            Use `front-matter` for governed Markdown metadata and `artifact`
            for schema-backed JSON contracts, indexes, ledgers, and similar
            machine-readable artifacts.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core validate front-matter --path "
            "docs/references/front_matter_reference.md",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/indexes/traceability/traceability_index.v1.json "
            "--format json",
            "uv run watchtower-core validate front-matter --path "
            "docs/standards/metadata/front_matter_standard.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    validate_subparsers = validate_parser.add_subparsers(
        dest="validate_command",
        title="validate commands",
        metavar="<validate_command>",
    )
    validate_parser.set_defaults(handler=_run_help, help_parser=validate_parser)

    validate_front_matter_parser = validate_subparsers.add_parser(
        "front-matter",
        help="Validate one Markdown document front-matter block.",
        description=dedent(
            """
            Validate one Markdown document front-matter block against the
            governed front-matter profiles published in the control plane.

            The command auto-selects the validator from the registry when the
            path is repository-local, or you can provide `--validator-id`
            explicitly.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core validate front-matter --path "
            "docs/references/front_matter_reference.md",
            "uv run watchtower-core validate front-matter --path "
            "docs/standards/metadata/front_matter_standard.md --format json",
            "uv run watchtower-core validate front-matter --path /tmp/example.md "
            "--validator-id validator.documentation.standard_front_matter",
            "uv run watchtower-core validate front-matter --path "
            "docs/standards/metadata/front_matter_standard.md --record-evidence "
            "--trace-id trace.core_python_foundation",
        ),
        formatter_class=HelpFormatter,
    )
    validate_front_matter_parser.add_argument(
        "--path",
        required=True,
        help="Repository-relative or absolute path to the Markdown document to validate.",
    )
    validate_front_matter_parser.add_argument(
        "--validator-id",
        help=(
            "Optional explicit validator identifier. Required for files outside "
            "the repository tree."
        ),
    )
    _add_common_validation_arguments(validate_front_matter_parser)
    validate_front_matter_parser.set_defaults(handler=_run_validate_front_matter)

    validate_artifact_parser = validate_subparsers.add_parser(
        "artifact",
        help="Validate one governed JSON artifact against registry-backed schema validators.",
        description=dedent(
            """
            Validate one governed JSON artifact against the active schema-backed
            validators published in the control plane.

            The command auto-selects the validator from the registry when the
            path is repository-local, or you can provide `--validator-id`
            explicitly for external or temporary files.
            """
        ).strip(),
        epilog=_examples(
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/indexes/traceability/traceability_index.v1.json "
            "--format json",
            "uv run watchtower-core validate artifact --path /tmp/example.json "
            "--validator-id validator.control_plane.acceptance_contract",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json "
            "--record-evidence --trace-id trace.core_python_foundation",
        ),
        formatter_class=HelpFormatter,
    )
    validate_artifact_parser.add_argument(
        "--path",
        required=True,
        help="Repository-relative or absolute path to the JSON artifact to validate.",
    )
    validate_artifact_parser.add_argument(
        "--validator-id",
        help=(
            "Optional explicit validator identifier. Required for files outside "
            "the repository tree."
        ),
    )
    _add_common_validation_arguments(validate_artifact_parser)
    validate_artifact_parser.set_defaults(handler=_run_validate_artifact)
    return parser


def _add_common_validation_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )
    parser.add_argument(
        "--record-evidence",
        action="store_true",
        help="Write a durable validation-evidence artifact and synchronized traceability update.",
    )
    parser.add_argument(
        "--trace-id",
        help="Required with --record-evidence. Shared trace identifier for the recorded evidence.",
    )
    parser.add_argument(
        "--evidence-id",
        help=(
            "Optional explicit evidence identifier. Otherwise the command "
            "derives one deterministically."
        ),
    )
    parser.add_argument(
        "--subject-id",
        action="append",
        default=[],
        help=(
            "Optional subject identifier to attach to the evidence check. "
            "Repeat for multiple values."
        ),
    )
    parser.add_argument(
        "--acceptance-id",
        action="append",
        default=[],
        help=(
            "Optional acceptance identifier to attach to the evidence check. "
            "Repeat for multiple values."
        ),
    )
    parser.add_argument(
        "--evidence-output",
        type=Path,
        help="Optional explicit output path for the evidence artifact.",
    )
    parser.add_argument(
        "--traceability-output",
        type=Path,
        help="Optional explicit output path for the updated traceability index.",
    )


def _add_common_sync_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the rebuilt artifact to the canonical control-plane path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional explicit output path for the rebuilt artifact.",
    )
    parser.add_argument(
        "--include-document",
        action="store_true",
        help="Include the generated document in json output for inspection or downstream tooling.",
    )
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Use json for scripts, workflows, or agent calls.",
    )


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


def _print_payload(args: argparse.Namespace, payload: Mapping[str, object]) -> int:
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
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync repository-paths",
        artifact_label="repository path index",
        service=RepositoryPathIndexSyncService.from_repo_root(),
    )


def _run_sync_command_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync command-index",
        artifact_label="command index",
        service=CommandIndexSyncService.from_repo_root(),
    )


def _run_sync_prd_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync prd-index",
        artifact_label="PRD index",
        service=PrdIndexSyncService.from_repo_root(),
    )


def _run_sync_decision_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync decision-index",
        artifact_label="decision index",
        service=DecisionIndexSyncService.from_repo_root(),
    )


def _run_sync_design_document_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync design-document-index",
        artifact_label="design-document index",
        service=DesignDocumentIndexSyncService.from_repo_root(),
    )


def _run_sync_traceability_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync traceability-index",
        artifact_label="traceability index",
        service=TraceabilityIndexSyncService.from_repo_root(),
    )


def _run_sync_document_command(
    args: argparse.Namespace,
    *,
    command_name: str,
    artifact_label: str,
    service: (
        CommandIndexSyncService
        | DecisionIndexSyncService
        | DesignDocumentIndexSyncService
        | PrdIndexSyncService
        | RepositoryPathIndexSyncService
        | TraceabilityIndexSyncService
    ),
) -> int:
    document = service.build_document()
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise RuntimeError(f"{artifact_label.capitalize()} document is missing its entries list.")
    entry_count = len(entries)
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(document, target))
        wrote = True

    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "entry_count": entry_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = document
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(f"Rebuilt {artifact_label} with {entry_count} entries and wrote it to {destination}.")
        return 0

    print(f"Rebuilt {artifact_label} with {entry_count} entries in dry-run mode.")
    print("Use --write to update the canonical artifact or --output <path> to write elsewhere.")
    return 0


def _run_validate_front_matter(args: argparse.Namespace) -> int:
    return _run_validation_command(
        args,
        command_name="watchtower-core validate front-matter",
        success_message="Front matter validated successfully.",
        service_factory=FrontMatterValidationService,
    )


def _run_validate_artifact(args: argparse.Namespace) -> int:
    return _run_validation_command(
        args,
        command_name="watchtower-core validate artifact",
        success_message="Artifact validated successfully.",
        service_factory=ArtifactValidationService,
    )


def _run_validation_command(
    args: argparse.Namespace,
    *,
    command_name: str,
    success_message: str,
    service_factory: ValidationServiceFactory,
) -> int:
    message = _validate_evidence_arguments(args)
    if message is not None:
        return _emit_command_error(args, command_name, message)

    loader = ControlPlaneLoader()
    service = service_factory(loader)
    try:
        result = service.validate(args.path, validator_id=args.validator_id)
    except (ValidationExecutionError, ValidationSelectionError) as exc:
        return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    evidence_write = None
    if args.record_evidence:
        recorder = ValidationEvidenceRecorder(loader)
        try:
            evidence_write = recorder.record(
                result,
                trace_id=args.trace_id,
                evidence_id=args.evidence_id,
                subject_ids=tuple(args.subject_id),
                acceptance_ids=tuple(args.acceptance_id),
                evidence_output=_resolve_output_path(args.evidence_output),
                traceability_output=_resolve_output_path(args.traceability_output),
            )
        except ValueError as exc:
            return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    result_payload = _build_validation_payload(
        command_name=command_name,
        result=result,
        evidence_write=evidence_write,
    )
    if _print_payload(args, result_payload) == 0:
        return 0 if result.passed else 1

    return _print_validation_summary(
        result,
        evidence_write=evidence_write,
        success_message=success_message,
    )


def _validate_evidence_arguments(args: argparse.Namespace) -> str | None:
    if not args.record_evidence and (
        args.trace_id
        or args.evidence_id
        or args.subject_id
        or args.acceptance_id
        or args.evidence_output is not None
        or args.traceability_output is not None
    ):
        return (
            "--trace-id, --evidence-id, --subject-id, --acceptance-id, "
            "--evidence-output, and --traceability-output require --record-evidence."
        )
    if args.record_evidence and not args.trace_id:
        return "--trace-id is required when --record-evidence is used."
    return None


def _emit_command_error(
    args: argparse.Namespace,
    command_name: str,
    message: str,
    *,
    prefix: str | None = None,
) -> int:
    payload = {
        "command": command_name,
        "status": "error",
        "message": message,
    }
    if _print_payload(args, payload) == 0:
        return 1
    if prefix is None:
        print(message)
    else:
        print(f"{prefix}: {message}")
    return 1


def _resolve_output_path(path: Path | None) -> Path | None:
    return path.resolve() if path is not None else None


def _build_validation_payload(
    *,
    command_name: str,
    result: ValidationResult,
    evidence_write: EvidenceWriteResult | None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "passed": result.passed,
        "validator_id": result.validator_id,
        "target_path": result.target_path,
        "engine": result.engine,
        "schema_ids": list(result.schema_ids),
        "issue_count": result.issue_count,
        "issues": [
            {
                "code": issue.code,
                "message": issue.message,
                "location": issue.location,
                "schema_id": issue.schema_id,
            }
            for issue in result.issues
        ],
    }
    if evidence_write is not None:
        payload["evidence"] = {
            "evidence_id": evidence_write.evidence_id,
            "evidence_relative_path": evidence_write.evidence_relative_path,
            "trace_id": evidence_write.trace_id,
            "recorded_at": evidence_write.recorded_at,
            "overall_result": evidence_write.overall_result,
            "evidence_output_path": evidence_write.evidence_output_path,
            "traceability_output_path": evidence_write.traceability_output_path,
        }
    return payload


def _print_validation_summary(
    result: ValidationResult,
    *,
    evidence_write: EvidenceWriteResult | None,
    success_message: str,
) -> int:
    verdict = "PASS" if result.passed else "FAIL"
    print(f"{verdict} {result.target_path}")
    print(f"Validator: {result.validator_id}")
    if result.schema_ids:
        print(f"Schemas: {', '.join(result.schema_ids)}")
    if evidence_write is not None:
        print(f"Evidence: {evidence_write.evidence_id}")
        print(f"Evidence Path: {evidence_write.evidence_output_path}")
        print(f"Traceability Path: {evidence_write.traceability_output_path}")
    if result.passed:
        print(success_message)
        return 0

    print(f"Issues: {result.issue_count}")
    for issue in result.issues:
        location = f" ({issue.location})" if issue.location else ""
        schema = f" [{issue.schema_id}]" if issue.schema_id else ""
        print(f"- {issue.code}{location}{schema}: {issue.message}")
    return 1


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
