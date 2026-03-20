"""Reusable sync command helpers shared by core and pack-owned CLI surfaces."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping
from importlib import import_module
from pathlib import Path
from typing import Any, Protocol, cast

from watchtower_core.cli.handler_common import (
    _emit_detail_result,
    _resolve_output_path,
    _task_filter_kwargs,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader


class DocumentSyncService(Protocol):
    """Protocol for document-oriented sync services."""

    def build_document(self) -> dict[str, Any]:
        """Build the artifact document."""

    def write_document(
        self,
        document: Mapping[str, Any],
        destination: Path | None = None,
    ) -> Path:
        """Write the artifact document."""


def load_sync_class(module_name: str, class_name: str) -> Any:
    """Load one named class from the requested module."""

    return getattr(import_module(module_name), class_name)


def load_document_sync_service(module_name: str, class_name: str) -> DocumentSyncService:
    """Load one document sync service rooted at the current repository."""

    service_class = load_sync_class(module_name, class_name)
    return cast(DocumentSyncService, service_class.from_repo_root())


def run_document_sync_command(
    args: argparse.Namespace,
    *,
    command_name: str,
    artifact_label: str,
    service: DocumentSyncService,
) -> int:
    """Run one document-oriented sync command."""

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


def load_tracking_sync_service(module_name: str, class_name: str) -> Any:
    """Load one tracker sync service rooted at the current repository."""

    return load_sync_class(module_name, class_name).from_repo_root()


def run_tracking_sync(
    args: argparse.Namespace,
    *,
    module_name: str,
    class_name: str,
    command_name: str,
    payload_counts_factory: Callable[[Any], dict[str, object]],
    wrote_message_factory: Callable[[Any, str], str],
    dry_run_message_factory: Callable[[Any], str],
) -> int:
    """Run one tracker-oriented sync command."""

    service = load_tracking_sync_service(module_name, class_name)
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        **payload_counts_factory(result),
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content

    def _render_human() -> None:
        if wrote and destination is not None:
            print(wrote_message_factory(result, destination))
            return
        print(dry_run_message_factory(result))
        print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def run_multi_target_sync(
    args: argparse.Namespace,
    *,
    module_name: str,
    class_name: str,
    command_name: str,
    human_label: str,
) -> int:
    """Run one multi-target sync orchestration."""

    service = load_sync_class(module_name, class_name).from_repo_root()
    result = service.run(write=args.write, output_dir=args.output_dir)
    payload = {
        "command": command_name,
        "status": "ok",
        "result_count": len(result.records),
        "wrote": result.wrote,
        "output_dir": result.output_dir,
        "results": [
            {
                "target": record.target,
                "artifact_kind": record.artifact_kind,
                "relative_output_path": record.relative_output_path,
                "output_path": record.output_path,
                "wrote": record.wrote,
                "record_count": record.record_count,
                "details": record.details,
            }
            for record in result.records
        ],
    }

    def _render_human() -> None:
        mode = (
            f"output-dir mode at {result.output_dir}"
            if result.output_dir is not None
            else ("write mode" if result.wrote else "dry-run mode")
        )
        print(f"Ran {human_label} across {len(result.records)} targets in {mode}.")
        for record in result.records:
            print(
                f"- {record.target} [{record.artifact_kind}] "
                f"record_count={record.record_count}"
            )
            if record.output_path is not None:
                print(f"  Wrote to {record.output_path}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def build_github_task_sync_params(args: argparse.Namespace, params_class: type[Any]) -> Any:
    """Build GitHub task sync params from one parsed CLI namespace."""

    return params_class(
        **_task_filter_kwargs(args),
        repository=args.repo,
        project_owner=args.project_owner,
        project_owner_type=args.project_owner_type,
        project_number=args.project_number,
        project_status_field_name=args.project_status_field,
        token_env=args.token_env,
        sync_labels=not args.no_label_sync,
    )


def build_loader() -> ControlPlaneLoader:
    """Return the default control-plane loader for pack-aware CLI commands."""

    return ControlPlaneLoader()
