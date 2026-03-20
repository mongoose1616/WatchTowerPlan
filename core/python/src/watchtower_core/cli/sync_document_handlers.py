"""Document-oriented sync command handlers."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping
from importlib import import_module
from pathlib import Path
from typing import Any, Protocol, TypedDict, cast

from watchtower_core.cli.handler_common import _emit_detail_result, _resolve_output_path


class _DocumentSyncService(Protocol):
    def build_document(self) -> dict[str, Any]:
        """Build the artifact document."""

    def write_document(
        self,
        document: Mapping[str, Any],
        destination: Path | None = None,
    ) -> Path:
        """Write the artifact document."""


class _DocumentHandlerSpec(TypedDict):
    handler_key: str
    export_name: str
    module_name: str
    class_name: str
    command_name: str
    artifact_label: str


_DOCUMENT_SYNC_HANDLER_SPECS: tuple[_DocumentHandlerSpec, ...] = (
    {
        "handler_key": "repository_paths",
        "export_name": "_run_sync_repository_paths",
        "module_name": "watchtower_plan.sync.repository_paths",
        "class_name": "RepositoryPathIndexSyncService",
        "command_name": "watchtower-core sync repository-paths",
        "artifact_label": "repository path index",
    },
    {
        "handler_key": "command_index",
        "export_name": "_run_sync_command_index",
        "module_name": "watchtower_plan.sync.command_index",
        "class_name": "CommandIndexSyncService",
        "command_name": "watchtower-core sync command-index",
        "artifact_label": "command index",
    },
    {
        "handler_key": "reference_index",
        "export_name": "_run_sync_reference_index",
        "module_name": "watchtower_plan.sync.reference_index",
        "class_name": "ReferenceIndexSyncService",
        "command_name": "watchtower-core sync reference-index",
        "artifact_label": "reference index",
    },
    {
        "handler_key": "route_index",
        "export_name": "_run_sync_route_index",
        "module_name": "watchtower_plan.sync.route_index",
        "class_name": "RouteIndexSyncService",
        "command_name": "watchtower-core sync route-index",
        "artifact_label": "route index",
    },
    {
        "handler_key": "foundation_index",
        "export_name": "_run_sync_foundation_index",
        "module_name": "watchtower_plan.sync.foundation_index",
        "class_name": "FoundationIndexSyncService",
        "command_name": "watchtower-core sync foundation-index",
        "artifact_label": "foundation index",
    },
    {
        "handler_key": "standard_index",
        "export_name": "_run_sync_standard_index",
        "module_name": "watchtower_plan.sync.standard_index",
        "class_name": "StandardIndexSyncService",
        "command_name": "watchtower-core sync standard-index",
        "artifact_label": "standard index",
    },
    {
        "handler_key": "initiative_index",
        "export_name": "_run_sync_initiative_index",
        "module_name": "watchtower_plan.sync.initiative_index",
        "class_name": "InitiativeIndexSyncService",
        "command_name": "watchtower-core sync initiative-index",
        "artifact_label": "initiative index",
    },
    {
        "handler_key": "task_index",
        "export_name": "_run_sync_task_index",
        "module_name": "watchtower_plan.sync.task_index",
        "class_name": "TaskIndexSyncService",
        "command_name": "watchtower-core sync task-index",
        "artifact_label": "task index",
    },
    {
        "handler_key": "traceability_index",
        "export_name": "_run_sync_traceability_index",
        "module_name": "watchtower_plan.sync.traceability",
        "class_name": "TraceabilityIndexSyncService",
        "command_name": "watchtower-core sync traceability-index",
        "artifact_label": "traceability index",
    },
    {
        "handler_key": "workflow_index",
        "export_name": "_run_sync_workflow_index",
        "module_name": "watchtower_plan.sync.workflow_index",
        "class_name": "WorkflowIndexSyncService",
        "command_name": "watchtower-core sync workflow-index",
        "artifact_label": "workflow index",
    },
)


def _load_document_sync_service(module_name: str, class_name: str) -> _DocumentSyncService:
    service_class = getattr(import_module(module_name), class_name)
    return cast(_DocumentSyncService, service_class.from_repo_root())


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
    def _render_human() -> None:
        if wrote:
            print(f"Rebuilt {artifact_label} with {entry_count} entries and wrote it to {destination}.")
            return

        print(f"Rebuilt {artifact_label} with {entry_count} entries in dry-run mode.")
        print("Use --write to update the canonical artifact or --output <path> to write elsewhere.")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _build_document_sync_handler(
    spec: _DocumentHandlerSpec,
) -> Callable[[argparse.Namespace], int]:
    def _handler(args: argparse.Namespace) -> int:
        return _run_sync_document_command(
            args,
            command_name=spec["command_name"],
            artifact_label=spec["artifact_label"],
            service=_load_document_sync_service(spec["module_name"], spec["class_name"]),
        )

    _handler.__name__ = spec["export_name"]
    return _handler


DOCUMENT_SYNC_HANDLERS: dict[str, Callable[[argparse.Namespace], int]] = {
    spec["handler_key"]: _build_document_sync_handler(spec)
    for spec in _DOCUMENT_SYNC_HANDLER_SPECS
}

globals().update(
    {
        spec["export_name"]: DOCUMENT_SYNC_HANDLERS[spec["handler_key"]]
        for spec in _DOCUMENT_SYNC_HANDLER_SPECS
    }
)

__all__ = [
    "DOCUMENT_SYNC_HANDLERS",
    "_run_sync_document_command",
    *[spec["export_name"] for spec in _DOCUMENT_SYNC_HANDLER_SPECS],
]
