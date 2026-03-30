"""Runtime handlers for hosted-pack inspection and validation commands."""

from __future__ import annotations

import argparse
import json

from watchtower_core.cli.handler_common import (
    _emit_collection_query_results,
    _emit_detail_result,
    _run_value_error_operation,
)
from watchtower_core.control_plane.errors import ControlPlaneError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import PackRegistryEntry, PackRuntimeManifest
from watchtower_core.pack_integration.bootstrap import (
    PackBootstrapRequest,
    bootstrap_hosted_pack,
)
from watchtower_core.pack_integration.export import (
    PACK_BUNDLE_EXPORT_SCOPE,
    EngineeringCoreApplyRequest,
    EngineeringCoreExtractRequest,
    PackExportRequest,
    apply_engineering_core_extract,
    export_hosted_repository,
    extract_engineering_core,
)
from watchtower_core.pack_integration.importing import import_pack_integration_module
from watchtower_core.pack_integration.runtime import (
    load_pack_query_runtime,
    load_pack_sync_runtime,
)
from watchtower_core.pack_integration.runtime_registry import (
    effective_pack_registry_entries,
    resolve_runtime_pack_registry_entry,
)
from watchtower_core.pack_integration.scaffold import (
    PackScaffoldRequest,
    scaffold_hosted_pack,
)
from watchtower_core.utils.exception_formatting import format_exception_detail
from watchtower_core.validation.pack_contract import (
    PACK_CONTRACT_VALIDATOR_ID,
    PackContractValidationService,
)


def _run_pack_list(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    entries = effective_pack_registry_entries(loader)

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
        operation=lambda: _resolve_describe_context(loader, args.pack),
    )
    if resolved is None:
        return 1
    entry, manifest = resolved

    integration_importable = False
    integration_error: str | None = None
    descriptor = None
    query_runtime_commands: list[str] | None = None
    query_runtime_error: str | None = None
    sync_runtime_targets: list[str] | None = None
    sync_runtime_error: str | None = None
    try:
        module, _ = import_pack_integration_module(
            repo_root=loader.repo_root,
            integration_module=manifest.integration_module,
            python_package=manifest.python_package,
            python_root=manifest.owned_roots.python_root,
        )
        descriptor = getattr(module, "PACK_INTEGRATION", None)
        integration_importable = True
    except Exception as exc:  # pragma: no cover - fail-closed operator path
        integration_error = format_exception_detail(exc)

    if integration_importable:
        try:
            query_runtime_commands = list(
                load_pack_query_runtime(
                    loader,
                    pack_settings_path=entry.pack_settings_path,
                ).commands
            )
        except Exception as exc:  # pragma: no cover - fail-closed operator path
            query_runtime_error = format_exception_detail(exc)
        try:
            sync_runtime_targets = list(
                load_pack_sync_runtime(
                    loader,
                    pack_settings_path=entry.pack_settings_path,
                ).targets
            )
        except Exception as exc:  # pragma: no cover - fail-closed operator path
            sync_runtime_error = format_exception_detail(exc)

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
        print("Capabilities: " + ", ".join(manifest.declared_capabilities))
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
                + ", ".join(f"{name}={path}" for name, path in manifest.owned_roots.domain_roots)
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


def _run_pack_bootstrap(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    sync_extras = tuple(dict.fromkeys(args.sync_extra or ()))
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core pack bootstrap",
        prefix="Pack bootstrap error",
        operation=lambda: bootstrap_hosted_pack(
            loader.repo_root,
            PackBootstrapRequest(
                pack_settings_path=args.pack_settings_path,
                write=bool(args.write),
                sync_workspace=not bool(args.no_sync_workspace),
                sync_extras=sync_extras,
                replace_hosted_packs=bool(args.replace_hosted_packs),
            ),
        ),
    )
    if result is None:
        return 1

    next_steps: list[str] = (
        [
            (
                "Run "
                + _workspace_sync_command(sync_extras)
                + " in core/python before using the hosted pack from a clean shell "
                "or environment."
            ),
        ]
        if result.workspace_sync_required
        else []
    )
    command_namespace = result.pack_registry_entry.get("command_namespace")
    pack_sync_command = (
        f"watchtower-core {command_namespace} sync all --write --format json"
        if isinstance(command_namespace, str)
        and command_namespace
        and "all" in result.pack_sync_targets
        else None
    )
    if result.pack_sync_required and pack_sync_command is not None:
        next_steps.append(
            f"Run {pack_sync_command} after the shared workspace sync completes."
        )
    if result.workspace_sync_required:
        next_steps.append(
            "Run watchtower-core pack validate --pack-settings-path "
            f"{result.pack_settings_path} --format json after the workspace sync "
            "completes."
        )
    payload = {
        "command": "watchtower-core pack bootstrap",
        "status": "ok",
        "pack_slug": result.pack_slug,
        "pack_settings_path": result.pack_settings_path,
        "pack_runtime_manifest_path": result.pack_runtime_manifest_path,
        "replace_hosted_packs": result.replace_hosted_packs,
        "scrubbed_pack_slugs": list(result.scrubbed_pack_slugs),
        "pack_registry_entry": result.pack_registry_entry,
        "core_python_workspace_registration": {
            "dependency": result.core_python_workspace_registration.dependency,
            "uv_source": {
                "path": result.core_python_workspace_registration.uv_source_path,
                "editable": result.core_python_workspace_registration.editable,
            },
        },
        "pack_registry_changed": result.pack_registry_changed,
        "core_python_pyproject_changed": result.core_python_pyproject_changed,
        "workspace_sync_ran": result.workspace_sync_ran,
        "workspace_sync_required": result.workspace_sync_required,
        "workspace_sync_extras": list(result.workspace_sync_extras),
        "pack_sync_targets": list(result.pack_sync_targets),
        "pack_sync_ran": result.pack_sync_ran,
        "pack_sync_required": result.pack_sync_required,
        "validation_passed": result.validation_passed,
        "changed_paths": list(result.changed_paths),
        "wrote": result.wrote,
        "next_steps": next_steps,
    }

    def _render_human() -> None:
        print(f"Bootstrapped pack: {result.pack_slug}")
        print(f"Pack Settings: {result.pack_settings_path}")
        print(f"Runtime Manifest: {result.pack_runtime_manifest_path}")
        print("Replace Hosted Packs: " + ("yes" if result.replace_hosted_packs else "no"))
        if result.scrubbed_pack_slugs:
            print("Scrubbed Packs: " + ", ".join(result.scrubbed_pack_slugs))
        print("Shared Registry Entry:")
        print(json.dumps(result.pack_registry_entry, indent=2, sort_keys=True))
        print("Core Python Workspace Registration:")
        print(
            json.dumps(
                payload["core_python_workspace_registration"],
                indent=2,
                sort_keys=True,
            )
        )
        print(f"Wrote Changes: {'yes' if result.wrote else 'no'}")
        print("Registry Changed: " + ("yes" if result.pack_registry_changed else "no"))
        print(
            "Core Python Pyproject Changed: "
            + ("yes" if result.core_python_pyproject_changed else "no")
        )
        print("Workspace Sync: " + ("ran" if result.workspace_sync_ran else "skipped"))
        if result.workspace_sync_extras:
            print("Workspace Sync Extras: " + ", ".join(result.workspace_sync_extras))
        if result.pack_sync_targets:
            print("Pack Sync Targets: " + ", ".join(result.pack_sync_targets))
        if result.pack_sync_ran:
            print("Pack Sync: ran pack-local sync all.")
        elif result.pack_sync_required:
            print("Pack Sync: deferred until the shared workspace is synced.")
        if result.validation_passed is not None:
            print("Validation: " + ("passed" if result.validation_passed else "failed"))
        elif result.workspace_sync_required:
            print("Validation: deferred until the shared workspace is synced.")
        if result.changed_paths:
            print("Changed Paths:")
            for path in result.changed_paths:
                print(f"- {path}")
        if next_steps:
            print("Next Steps:")
            for step in next_steps:
                print(f"- {step}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _run_pack_extract_core(args: argparse.Namespace) -> int:
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core pack extract-core",
        prefix="Pack extract error",
        operation=lambda: extract_engineering_core(
            ControlPlaneLoader().repo_root,
            EngineeringCoreExtractRequest(
                output_root=args.output_root,
                overwrite=bool(args.overwrite),
            ),
        ),
    )
    if result is None:
        return 1

    next_steps = [
        (
            "Run watchtower-core pack apply-core --source-root "
            f"{result.output_root} --write --format json in the recipient repository, then run "
            "watchtower-core pack bootstrap --pack-settings-path <recipient-pack-settings> "
            "--replace-hosted-packs --write --sync-extra dev --format json there."
        )
    ]
    payload = {
        "command": "watchtower-core pack extract-core",
        "status": "ok",
        "passed": result.passed,
        "output_root": result.output_root,
        "copied_paths": list(result.copied_paths),
        "scrubbed_paths": list(result.scrubbed_paths),
        "changed_paths": list(result.changed_paths),
        "workspace_lock_removed": result.workspace_lock_removed,
        "readiness": {
            "passed": result.readiness_result.passed,
            "validator_id": result.readiness_result.validator_id,
            "target_path": result.readiness_result.target_path,
            "engine": result.readiness_result.engine,
            "schema_ids": list(result.readiness_result.schema_ids),
            "issue_count": result.readiness_result.issue_count,
            "issues": [
                {
                    "code": issue.code,
                    "message": issue.message,
                    "location": issue.location,
                    "schema_id": issue.schema_id,
                }
                for issue in result.readiness_result.issues
            ],
        },
        "next_steps": next_steps,
    }

    def _render_human() -> None:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status} {result.output_root}")
        print("Scope: engineering core extract")
        print("Copied Roots: " + ", ".join(result.copied_paths))
        print(f"Scrubbed Paths: {len(result.scrubbed_paths)}")
        if result.workspace_lock_removed:
            print(
                "Workspace Lock: removed core/python/uv.lock because shared "
                "workspace wiring changed."
            )
        readiness = result.readiness_result
        print(
            ("PASS" if readiness.passed else "FAIL")
            + f" readiness: {readiness.issue_count} issues"
        )
        if not readiness.passed:
            for issue in readiness.issues[:10]:
                location = f" ({issue.location})" if issue.location else ""
                print(f"- {issue.code}{location}: {issue.message}")
        print("Next Steps:")
        for step in next_steps:
            print(f"- {step}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
        exit_code=0 if result.passed else 1,
    )


def _run_pack_apply_core(args: argparse.Namespace) -> int:
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core pack apply-core",
        prefix="Pack apply error",
        operation=lambda: apply_engineering_core_extract(
            ControlPlaneLoader().repo_root,
            EngineeringCoreApplyRequest(
                source_root=args.source_root,
                write=bool(args.write),
            ),
        ),
    )
    if result is None:
        return 1

    next_steps = (
        [
            (
                "Re-run watchtower-core pack apply-core --source-root "
                f"{result.source_root} --write --format json to replace local core/ "
                "from the staged extract."
            )
        ]
        if not result.wrote
        else [
            (
                "Run watchtower-core pack bootstrap --pack-settings-path "
                "<recipient-pack-settings> --replace-hosted-packs --write "
                "--sync-extra dev --format json."
            )
        ]
    )
    payload = {
        "command": "watchtower-core pack apply-core",
        "status": "ok",
        "source_root": result.source_root,
        "source_core_root": result.source_core_root,
        "target_core_root": result.target_core_root,
        "source_readiness": {
            "passed": result.source_readiness_result.passed,
            "validator_id": result.source_readiness_result.validator_id,
            "target_path": result.source_readiness_result.target_path,
            "engine": result.source_readiness_result.engine,
            "schema_ids": list(result.source_readiness_result.schema_ids),
            "issue_count": result.source_readiness_result.issue_count,
            "issues": [
                {
                    "code": issue.code,
                    "message": issue.message,
                    "location": issue.location,
                    "schema_id": issue.schema_id,
                }
                for issue in result.source_readiness_result.issues
            ],
        },
        "changed_paths": list(result.changed_paths),
        "deleted_paths": list(result.deleted_paths),
        "preserved_paths": list(result.preserved_paths),
        "wrote": result.wrote,
        "next_steps": next_steps,
    }

    def _render_human() -> None:
        mode = "write mode" if result.wrote else "dry-run mode"
        print(f"Applied staged core extract from {result.source_root} in {mode}.")
        print(
            "Source Readiness: "
            + ("passed" if result.source_readiness_result.passed else "failed")
        )
        print(f"Changed Paths: {len(result.changed_paths)}")
        print(f"Deleted Paths: {len(result.deleted_paths)}")
        print(f"Preserved Paths: {len(result.preserved_paths)}")
        if result.deleted_paths:
            print("Deleted Paths:")
            for path in result.deleted_paths:
                print(f"- {path}")
        if result.preserved_paths:
            print("Preserved Paths:")
            for path in result.preserved_paths:
                print(f"- {path}")
        if next_steps:
            print("Next Steps:")
            for step in next_steps:
                print(f"- {step}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )


def _run_pack_export(args: argparse.Namespace) -> int:
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core pack export",
        prefix="Pack export error",
        operation=lambda: export_hosted_repository(
            ControlPlaneLoader().repo_root,
            PackExportRequest(
                output_root=args.output_root,
                included_pack_slugs=tuple(args.include_pack or ()),
                overwrite=bool(args.overwrite),
                pack_only=bool(args.pack_only),
            ),
        ),
    )
    if result is None:
        return 1

    payload = {
        "command": "watchtower-core pack export",
        "status": "ok",
        "passed": result.passed,
        "output_root": result.output_root,
        "export_scope": result.export_scope,
        "included_pack_slugs": list(result.included_pack_slugs),
        "default_pack_slug": result.default_pack_slug,
        "copied_paths": list(result.copied_paths),
        "scrubbed_paths": list(result.scrubbed_paths),
        "changed_paths": list(result.changed_paths),
        "workspace_lock_removed": result.workspace_lock_removed,
        "pack_validation_note": result.pack_validation_note,
        "pack_validations": [
            {
                "pack_slug": summary.pack_slug,
                "pack_settings_path": summary.pack_settings_path,
                "passed": summary.passed,
                "issue_count": summary.issue_count,
                "issues": [
                    {
                        "code": issue.code,
                        "message": issue.message,
                        "location": issue.location,
                        "schema_id": issue.schema_id,
                    }
                    for issue in summary.issues
                ],
            }
            for summary in result.pack_validations
        ],
        "portability": {
            "passed": result.portability_result.passed,
            "validator_id": result.portability_result.validator_id,
            "target_path": result.portability_result.target_path,
            "engine": result.portability_result.engine,
            "schema_ids": list(result.portability_result.schema_ids),
            "issue_count": result.portability_result.issue_count,
            "issues": [
                {
                    "code": issue.code,
                    "message": issue.message,
                    "location": issue.location,
                    "schema_id": issue.schema_id,
                }
                for issue in result.portability_result.issues
            ],
        },
    }

    def _render_human() -> None:
        status = "PASS" if result.passed else "FAIL"
        selected = (
            ", ".join(result.included_pack_slugs)
            if result.included_pack_slugs
            else "core-only"
        )
        print(f"{status} {result.output_root}")
        print(
            "Scope: "
            + (
                "pack-only bundle"
                if result.export_scope == PACK_BUNDLE_EXPORT_SCOPE
                else "repository bundle"
            )
        )
        print(f"Included Packs: {selected}")
        if result.default_pack_slug is not None:
            print(f"Default Pack: {result.default_pack_slug}")
        print("Copied Roots: " + ", ".join(result.copied_paths))
        print(f"Scrubbed Paths: {len(result.scrubbed_paths)}")
        if result.workspace_lock_removed:
            print(
                "Workspace Lock: removed core/python/uv.lock because shared "
                "workspace wiring changed."
            )
        for summary in result.pack_validations:
            status_label = "PASS" if summary.passed else "FAIL"
            print(
                f"{status_label} hosted-pack contract: {summary.pack_slug} "
                f"({summary.issue_count} issues)"
            )
        if result.pack_validation_note is not None:
            print("Pack Validation: " + result.pack_validation_note)
        portability = result.portability_result
        print(
            ("PASS" if portability.passed else "FAIL")
            + f" portability: {portability.issue_count} issues"
        )
        if not portability.passed:
            for issue in portability.issues[:10]:
                location = f" ({issue.location})" if issue.location else ""
                print(f"- {issue.code}{location}: {issue.message}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
        exit_code=0 if result.passed else 1,
    )


def _workspace_sync_command(sync_extras: tuple[str, ...]) -> str:
    if not sync_extras:
        return "`uv sync`"
    extras = " ".join(f"--extra {extra}" for extra in sync_extras)
    return f"`uv sync {extras}`"


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
                "Register the generated pack with "
                f"watchtower-core pack bootstrap --pack-settings-path "
                f"{result.pack_settings_path} --write --format json."
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
    try:
        return resolve_runtime_pack_registry_entry(loader, pack_slug)
    except KeyError:
        available = ", ".join(entry.pack_slug for entry in effective_pack_registry_entries(loader))
        raise ValueError(f"Unknown pack slug: {pack_slug}. Available packs: {available}") from None


def _resolve_describe_context(
    loader: ControlPlaneLoader,
    pack_slug: str | None,
) -> tuple[PackRegistryEntry, PackRuntimeManifest]:
    entry = _resolve_registry_entry(loader, pack_slug)
    pack_loader = loader.derive(active_pack_settings_path=entry.pack_settings_path)
    try:
        pack_loader.activate_pack_settings()
        manifest = pack_loader.load_pack_runtime_manifest()
    except (ControlPlaneError, ValueError) as exc:
        raise ValueError(
            f"Hosted-pack registry entry for {entry.pack_slug!r} is not usable: {exc}"
        ) from None
    return entry, manifest


def _render_pack_registry_entry(entry: PackRegistryEntry) -> None:
    default_suffix = " default=yes" if entry.default_repo_pack else ""
    print(
        f"- {entry.pack_slug} ({entry.pack_id}) "
        f"namespace={entry.command_namespace} "
        f"distribution={entry.python_distribution}{default_suffix}"
    )


__all__ = [
    "_run_pack_apply_core",
    "_run_pack_bootstrap",
    "_run_pack_describe",
    "_run_pack_extract_core",
    "_run_pack_list",
    "_run_pack_scaffold",
    "_run_pack_validate",
]
