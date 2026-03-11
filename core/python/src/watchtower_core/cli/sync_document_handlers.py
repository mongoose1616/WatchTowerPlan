"""Document-oriented sync command handlers."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from importlib import import_module
from pathlib import Path
from typing import Any, Protocol, cast

from watchtower_core.cli.handler_common import _print_payload, _resolve_output_path


class _DocumentSyncService(Protocol):
    def build_document(self) -> dict[str, Any]:
        """Build the artifact document."""

    def write_document(
        self,
        document: Mapping[str, Any],
        destination: Path | None = None,
    ) -> Path:
        """Write the artifact document."""


def _load_document_sync_service(module_name: str, class_name: str) -> _DocumentSyncService:
    service_class = getattr(import_module(module_name), class_name)
    return cast(_DocumentSyncService, service_class.from_repo_root())


def _run_sync_repository_paths(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync repository-paths",
        artifact_label="repository path index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.repository_paths",
            "RepositoryPathIndexSyncService",
        ),
    )


def _run_sync_command_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync command-index",
        artifact_label="command index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.command_index",
            "CommandIndexSyncService",
        ),
    )


def _run_sync_reference_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync reference-index",
        artifact_label="reference index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.reference_index",
            "ReferenceIndexSyncService",
        ),
    )


def _run_sync_route_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync route-index",
        artifact_label="route index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.route_index",
            "RouteIndexSyncService",
        ),
    )


def _run_sync_foundation_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync foundation-index",
        artifact_label="foundation index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.foundation_index",
            "FoundationIndexSyncService",
        ),
    )


def _run_sync_standard_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync standard-index",
        artifact_label="standard index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.standard_index",
            "StandardIndexSyncService",
        ),
    )


def _run_sync_prd_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync prd-index",
        artifact_label="PRD index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.prd_index",
            "PrdIndexSyncService",
        ),
    )


def _run_sync_decision_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync decision-index",
        artifact_label="decision index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.decision_index",
            "DecisionIndexSyncService",
        ),
    )


def _run_sync_design_document_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync design-document-index",
        artifact_label="design-document index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.design_document_index",
            "DesignDocumentIndexSyncService",
        ),
    )


def _run_sync_initiative_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync initiative-index",
        artifact_label="initiative index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.initiative_index",
            "InitiativeIndexSyncService",
        ),
    )


def _run_sync_planning_catalog(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync planning-catalog",
        artifact_label="planning catalog",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.planning_catalog",
            "PlanningCatalogSyncService",
        ),
    )


def _run_sync_task_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync task-index",
        artifact_label="task index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.task_index",
            "TaskIndexSyncService",
        ),
    )


def _run_sync_traceability_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync traceability-index",
        artifact_label="traceability index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.traceability",
            "TraceabilityIndexSyncService",
        ),
    )


def _run_sync_workflow_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync workflow-index",
        artifact_label="workflow index",
        service=_load_document_sync_service(
            "watchtower_core.repo_ops.sync.workflow_index",
            "WorkflowIndexSyncService",
        ),
    )


def _run_sync_document_command(
    args: argparse.Namespace,
    *,
    command_name: str,
    artifact_label: str,
    service: _DocumentSyncService,
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
