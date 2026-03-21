"""Runtime handlers for hosted-pack inspection and validation commands."""

from __future__ import annotations

import argparse
import importlib
from typing import Any

from watchtower_core.cli.handler_common import (
    _emit_collection_query_results,
    _emit_command_error,
    _emit_detail_result,
    _run_value_error_operation,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import PackRegistryEntry
from watchtower_core.pack_integration.runtime import (
    load_pack_query_runtime,
    load_pack_sync_runtime,
)
from watchtower_core.pack_integration.scaffold import (
    PackScaffoldRequest,
    scaffold_hosted_pack,
)
from watchtower_core.validation.pack_contract import (
    PACK_CONTRACT_VALIDATOR_ID,
    PackContractValidationService,
)


def _run_pack_list(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    registry = loader.load_pack_registry()
    entries = tuple(registry.packs)

    return _emit_collection_query_results(
        args,
        command_name="watchtower-core pack list",
        entries=entries,
        noun="hosted pack",
        empty_message="No hosted packs are registered.",
        payload_results_factory=lambda: [
            {
                "pack_id": entry.pack_id,
                "pack_slug": entry.pack_slug,
                "command_namespace": entry.command_namespace,
                "pack_settings_path": entry.pack_settings_path,
                "pack_runtime_manifest_path": entry.pack_runtime_manifest_path,
                "python_distribution": entry.python_distribution,
                "python_package": entry.python_package,
                "default_repo_pack": entry.default_repo_pack,
                "notes": entry.notes,
            }
            for entry in entries
        ],
        render_entry=_render_pack_registry_entry,
    )


def _run_pack_describe(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    resolved = _run_value_error_operation(
        args,
        command_name="watchtower-core pack describe",
        prefix="Pack error",
        operation=lambda: _resolve_registry_entry(loader, args.pack),
    )
    if resolved is None:
        return 1
    entry = resolved
    manifest = loader.load_pack_runtime_manifest(pack_settings_path=entry.pack_settings_path)

    integration_importable = False
    integration_error: str | None = None
    descriptor = None
    query_runtime_commands: list[str] | None = None
    query_runtime_error: str | None = None
    sync_runtime_targets: list[str] | None = None
    sync_runtime_error: str | None = None
    try:
        module = importlib.import_module(manifest.integration_module)
        descriptor = getattr(module, "PACK_INTEGRATION", None)
        integration_importable = True
    except Exception as exc:  # pragma: no cover - fail-closed operator path
        integration_error = str(exc)

    if integration_importable:
        try:
            query_runtime_commands = list(
                load_pack_query_runtime(
                    loader,
                    pack_settings_path=entry.pack_settings_path,
                ).commands
            )
        except Exception as exc:  # pragma: no cover - fail-closed operator path
            query_runtime_error = str(exc)
        try:
            sync_runtime_targets = list(
                load_pack_sync_runtime(
                    loader,
                    pack_settings_path=entry.pack_settings_path,
                ).targets
            )
        except Exception as exc:  # pragma: no cover - fail-closed operator path
            sync_runtime_error = str(exc)

    payload = {
        "command": "watchtower-core pack describe",
        "status": "ok",
        "pack": {
            "pack_id": entry.pack_id,
            "pack_slug": entry.pack_slug,
            "command_namespace": entry.command_namespace,
            "pack_settings_path": entry.pack_settings_path,
            "pack_runtime_manifest_path": entry.pack_runtime_manifest_path,
            "python_distribution": entry.python_distribution,
            "python_package": entry.python_package,
            "default_repo_pack": entry.default_repo_pack,
            "notes": entry.notes,
        },
        "runtime_manifest": {
            "integration_module": manifest.integration_module,
            "declared_capabilities": list(manifest.declared_capabilities),
            "required_validation_suite_ids": list(manifest.required_validation_suite_ids),
            "owned_roots": {
                "workspace_root": manifest.owned_roots.workspace_root,
                "machine_root": manifest.owned_roots.machine_root,
                "docs_root": manifest.owned_roots.docs_root,
                "workflows_root": manifest.owned_roots.workflows_root,
                "tracking_root": manifest.owned_roots.tracking_root,
                "python_root": manifest.owned_roots.python_root,
                "initiatives_root": manifest.owned_roots.initiatives_root,
                "projects_root": manifest.owned_roots.projects_root,
                "domain_roots": dict(manifest.owned_roots.domain_roots),
            },
        },
        "integration": {
            "importable": integration_importable,
            "error": integration_error,
            "descriptor_type": type(descriptor).__name__ if descriptor is not None else None,
            "command_implementation_path": getattr(
                descriptor,
                "command_implementation_path",
                None,
            ),
            "command_subcommand_implementation_paths": list(
                getattr(descriptor, "command_subcommand_implementation_paths", ())
            ),
            "query_runtime_commands": query_runtime_commands,
            "query_runtime_error": query_runtime_error,
            "sync_runtime_targets": sync_runtime_targets,
            "sync_runtime_error": sync_runtime_error,
        },
    }

    def _render_human() -> None:
        print(f"Pack: {entry.pack_slug} ({entry.pack_id})")
        print(f"Namespace: {entry.command_namespace}")
        print(f"Distribution: {entry.python_distribution}")
        print(f"Python Package: {entry.python_package}")
        print(f"Pack Settings: {entry.pack_settings_path}")
        print(f"Runtime Manifest: {entry.pack_runtime_manifest_path}")
        if entry.notes:
            print(f"Notes: {entry.notes}")
        print(f"Integration Module: {manifest.integration_module}")
        print(
            "Capabilities: "
            + ", ".join(manifest.declared_capabilities)
        )
        print(
            "Owned Roots: "
            f"workspace={manifest.owned_roots.workspace_root}, "
            f"machine={manifest.owned_roots.machine_root}, "
            f"docs={manifest.owned_roots.docs_root}, "
            f"workflows={manifest.owned_roots.workflows_root}, "
            f"tracking={manifest.owned_roots.tracking_root}, "
            f"python={manifest.owned_roots.python_root}"
        )
        if manifest.owned_roots.domain_roots:
            print(
                "Domain Roots: "
                + ", ".join(
                    f"{name}={path}" for name, path in manifest.owned_roots.domain_roots
                )
            )
        print(
            "Integration Import: "
            + ("ok" if integration_importable else f"failed ({integration_error})")
        )
        if query_runtime_commands is not None:
            print("Query Commands: " + ", ".join(query_runtime_commands))
        elif query_runtime_error:
            print(f"Query Commands: invalid ({query_runtime_error})")
        if sync_runtime_targets is not None:
            print("Sync Targets: " + ", ".join(sync_runtime_targets))
        elif sync_runtime_error:
            print(f"Sync Targets: invalid ({sync_runtime_error})")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _run_pack_validate(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    resolved_pack_settings_path = _run_value_error_operation(
        args,
        command_name="watchtower-core pack validate",
        prefix="Pack error",
        operation=lambda: (
            args.pack_settings_path
            if args.pack_settings_path
            else _resolve_registry_entry(loader, args.pack).pack_settings_path
        ),
    )
    if resolved_pack_settings_path is None:
        return 1
    pack_settings_path = resolved_pack_settings_path
    result = PackContractValidationService(loader).validate(pack_settings_path)
    payload = {
        "command": "watchtower-core pack validate",
        "status": "ok",
        "pack": args.pack,
        "pack_settings_path": pack_settings_path,
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

    def _render_human() -> None:
        print(
            "PASS" if result.passed else "FAIL",
            pack_settings_path,
        )
        print(f"Validator: {PACK_CONTRACT_VALIDATOR_ID}")
        if result.passed:
            print("Hosted-pack contract validated successfully.")
            return
        print(f"Issues: {result.issue_count}")
        for issue in result.issues:
            location = f" ({issue.location})" if issue.location else ""
            schema = f" [{issue.schema_id}]" if issue.schema_id else ""
            print(f"- {issue.code}{location}{schema}: {issue.message}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
        exit_code=0 if result.passed else 1,
    )


def _run_pack_scaffold(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core pack scaffold",
        prefix="Pack scaffold error",
        operation=lambda: scaffold_hosted_pack(
            loader.repo_root,
            PackScaffoldRequest(
                pack_slug=args.pack_slug,
                pack_root=args.pack_root,
                command_namespace=args.command_namespace,
                python_distribution=args.python_distribution,
                python_package=args.python_package,
                domain_root_names=tuple(args.domain_root),
            ),
        ),
    )
    if result is None:
        return 1

    payload = {
        "command": "watchtower-core pack scaffold",
        "status": "ok",
        "pack_slug": result.pack_slug,
        "pack_root": result.pack_root,
        "command_namespace": result.command_namespace,
        "python_distribution": result.python_distribution,
        "python_package": result.python_package,
        "pack_settings_path": result.pack_settings_path,
        "pack_runtime_manifest_path": result.pack_runtime_manifest_path,
        "created_paths": list(result.created_paths),
        "pack_registry_entry": result.pack_registry_entry,
        "core_python_workspace_registration": {
            "dependency": result.core_python_dependency,
            "uv_source": dict(result.core_python_uv_source),
        },
        "next_steps": [
            (
                "Add the emitted pack_registry_entry to "
                "core/control_plane/registries/pack_registry.json."
            ),
            (
                "Add the emitted dependency and uv source to core/python/pyproject.toml, "
                "then run uv sync in core/python."
            ),
            (
                "Validate the hosted pack with "
                f"watchtower-core pack validate --pack-settings-path "
                f"{result.pack_settings_path} --format json."
            ),
        ],
    }

    def _render_human() -> None:
        print(f"Scaffolded pack: {result.pack_slug}")
        print(f"Pack Root: {result.pack_root}")
        print(f"Namespace: {result.command_namespace}")
        print(f"Python Distribution: {result.python_distribution}")
        print(f"Python Package: {result.python_package}")
        print("Created Paths:")
        for path in result.created_paths:
            print(f"- {path}")
        print("Pack Registry Entry:")
        print(json.dumps(result.pack_registry_entry, indent=2, sort_keys=True))
        print("Core Python Workspace Registration:")
        print(
            json.dumps(
                {
                    "dependency": result.core_python_dependency,
                    "uv_source": result.core_python_uv_source,
                },
                indent=2,
                sort_keys=True,
            )
        )
        print("Next Steps:")
        for step in payload["next_steps"]:
            print(f"- {step}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _resolve_registry_entry(
    loader: ControlPlaneLoader,
    pack_slug: str | None,
) -> PackRegistryEntry:
    registry = loader.load_pack_registry()
    if pack_slug is None:
        return registry.default_pack()
    try:
        return registry.get_by_pack_slug(pack_slug)
    except KeyError:
        available = ", ".join(entry.pack_slug for entry in registry.packs)
        raise ValueError(
            f"Unknown pack slug: {pack_slug}. Available packs: {available}"
        ) from None


def _render_pack_registry_entry(entry: PackRegistryEntry) -> None:
    default_suffix = " default=yes" if entry.default_repo_pack else ""
    print(
        f"- {entry.pack_slug} ({entry.pack_id}) "
        f"namespace={entry.command_namespace} "
        f"distribution={entry.python_distribution}{default_suffix}"
    )


__all__ = [
    "_run_pack_describe",
    "_run_pack_list",
    "_run_pack_validate",
]
