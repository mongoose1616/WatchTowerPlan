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
from watchtower_core.sync.cache import (
    finalize_document_sync_cache,
    prepare_document_sync_cache,
    validate_prepared_document_sync_cache,
)
from watchtower_core.telemetry import telemetry_operation


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
    loader = getattr(service, "_loader", None)
    with telemetry_operation(
        "sync_command",
        command_name,
        attributes={
            "artifact_label": artifact_label,
            "write": args.write,
            "output": str(args.output) if args.output is not None else None,
        },
    ) as operation:
        prepared_cache = None
        if isinstance(loader, ControlPlaneLoader):
            try:
                relative_output_path = _service_relative_output_path(service)
            except RuntimeError:
                relative_output_path = None
            if relative_output_path is not None:
                prepared_cache = prepare_document_sync_cache(
                    loader,
                    service,
                    relative_output_path=relative_output_path,
                )
                prepared_cache = validate_prepared_document_sync_cache(loader, prepared_cache)
        document = (
            prepared_cache.document if prepared_cache is not None else None
        ) or service.build_document()
        if isinstance(loader, ControlPlaneLoader):
            loader.schema_store.validate_instance(document)
        entries = document.get("entries")
        if not isinstance(entries, list):
            raise RuntimeError(
                f"{artifact_label.capitalize()} document is missing its entries list."
            )
        entry_count = len(entries)
        destination: str | None = None
        wrote = False

        if args.write or args.output is not None:
            target = _resolve_output_path(args.output)
            destination = str(service.write_document(document, target))
            wrote = True
        if prepared_cache is not None:
            finalize_document_sync_cache(prepared_cache, document=document)
        if operation is not None:
            operation.set_result(
                status="ok",
                entry_count=entry_count,
                wrote=wrote,
                artifact_path=destination,
                cache_status=(
                    prepared_cache.cache_status if prepared_cache is not None else "disabled"
                ),
                cache_input_count=(
                    prepared_cache.input_file_count if prepared_cache is not None else 0
                ),
            )

    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "entry_count": entry_count,
        "wrote": wrote,
        "artifact_path": destination,
        "cache_status": prepared_cache.cache_status if prepared_cache is not None else "disabled",
        "cache_input_count": (prepared_cache.input_file_count if prepared_cache is not None else 0),
    }
    if args.include_document:
        payload["document"] = document

    def _render_human() -> None:
        if prepared_cache is not None and prepared_cache.cache_status == "hit":
            if wrote:
                print(
                    "Reused cached "
                    f"{artifact_label} with {entry_count} entries and wrote it to "
                    f"{destination}."
                )
                return
            print(f"Reused cached {artifact_label} with {entry_count} entries in dry-run mode.")
            print(
                "Use --write to refresh the canonical artifact or --output <path> to write "
                "elsewhere."
            )
            return
        if wrote:
            print(
                "Rebuilt "
                f"{artifact_label} with {entry_count} entries and wrote it to "
                f"{destination}."
            )
            return
        print(f"Rebuilt {artifact_label} with {entry_count} entries in dry-run mode.")
        print("Use --write to update the canonical artifact or --output <path> to write elsewhere.")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _service_relative_output_path(service: DocumentSyncService) -> str:
    for attr in ("OUTPUT_PATH", "_output_path"):
        value = getattr(service, attr, None)
        if isinstance(value, str) and value:
            return value
    raise RuntimeError("Document sync service does not declare a canonical output path.")


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
    with telemetry_operation(
        "sync_command",
        command_name,
        attributes={
            "module_name": module_name,
            "class_name": class_name,
            "write": args.write,
            "output": str(args.output) if args.output is not None else None,
        },
    ) as operation:
        service = load_tracking_sync_service(module_name, class_name)
        result = service.build_document()
        destination: str | None = None
        wrote = False

        if args.write or args.output is not None:
            target = _resolve_output_path(args.output)
            destination = str(service.write_document(result, target))
            wrote = True
        if operation is not None:
            counts = payload_counts_factory(result)
            operation.set_result(
                status="ok",
                wrote=wrote,
                artifact_path=destination,
                result_counts=counts,
            )

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
    with telemetry_operation(
        "sync_command",
        command_name,
        attributes={
            "module_name": module_name,
            "class_name": class_name,
            "write": args.write,
            "output_dir": str(args.output_dir) if args.output_dir is not None else None,
        },
    ) as operation:
        service = load_sync_class(module_name, class_name).from_repo_root()
        result = service.run(write=args.write, output_dir=args.output_dir)
        if operation is not None:
            operation.set_result(
                status="ok",
                result_count=len(result.records),
                wrote=result.wrote,
                output_dir=result.output_dir,
            )
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
                "drift_detected": getattr(record, "drift_detected", False),
                "drift_reason": getattr(record, "drift_reason", None),
                "cache_status": getattr(record, "cache_status", None),
                "cache_input_count": getattr(record, "cache_input_count", 0),
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
            drift_label = (
                f" drift={record.drift_reason}"
                if getattr(record, "drift_detected", False)
                and getattr(record, "drift_reason", None) is not None
                else ""
            )
            print(
                f"- {record.target} [{record.artifact_kind}] "
                f"record_count={record.record_count}{drift_label}"
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
