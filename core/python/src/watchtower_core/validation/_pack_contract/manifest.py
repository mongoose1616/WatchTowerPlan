"""Manifest and registry consistency checks for pack contracts."""

from __future__ import annotations

from typing import Any

from watchtower_core.control_plane.loader import PACK_REGISTRY_PATH
from watchtower_core.pack_integration import pack_command_entry_doc_path
from watchtower_core.validation.models import ValidationIssue


def matching_field_issues(
    *,
    pack_id: str,
    registry_pack_id: str,
    manifest_pack_id: str,
    pack_slug: str,
    manifest_pack_slug: str,
    command_namespace: str,
    manifest_command_namespace: str,
    python_distribution: str,
    manifest_python_distribution: str,
    python_package: str,
    manifest_python_package: str,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for field_name, left, right in (
        ("pack_id", pack_id, registry_pack_id),
        ("pack_id", pack_id, manifest_pack_id),
        ("pack_slug", pack_slug, manifest_pack_slug),
        ("command_namespace", command_namespace, manifest_command_namespace),
        ("python_distribution", python_distribution, manifest_python_distribution),
        ("python_package", python_package, manifest_python_package),
    ):
        if left == right:
            continue
        issues.append(
            ValidationIssue(
                code=f"pack_contract_{field_name}_mismatch",
                message=f"Pack contract field mismatch for {field_name}: {left} != {right}",
            )
        )
    return tuple(issues)


def registry_collision_issues(
    pack_registry: Any,
    registry_entry: Any,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    conflicting_entries = tuple(
        entry
        for entry in pack_registry.packs
        if entry.command_namespace == registry_entry.command_namespace
    )
    if len(conflicting_entries) > 1:
        conflicting_pack_slugs = ", ".join(sorted(entry.pack_slug for entry in conflicting_entries))
        issues.append(
            ValidationIssue(
                code="pack_registry_command_namespace_conflict",
                message=(
                    "Hosted-pack command namespaces must be unique across the pack registry: "
                    f"{registry_entry.command_namespace} is shared by {conflicting_pack_slugs}"
                ),
                location=PACK_REGISTRY_PATH,
            )
        )
    return tuple(issues)


def command_doc_issues(
    context: Any,
    runtime_manifest: Any,
) -> tuple[ValidationIssue, ...]:
    command_doc_path = pack_command_entry_doc_path(
        command_namespace=runtime_manifest.command_namespace,
        docs_root=runtime_manifest.owned_roots.docs_root,
    )
    if context.loader.resolve_path(command_doc_path).is_file():
        return ()
    return (
        ValidationIssue(
            code="pack_command_doc_missing",
            message=(
                "Pack contract is missing the pack-owned namespace command page: "
                f"{command_doc_path}"
            ),
            location=command_doc_path,
        ),
    )


def expected_python_root(workspace_root: str) -> str:
    return f"{workspace_root}/python"


def expected_manifest_path(machine_root: str, filename: str) -> str:
    return f"{machine_root}/manifests/{filename}"


def manifest_path_issues(
    context: Any,
    runtime_manifest: Any,
) -> tuple[ValidationIssue, ...]:
    expected_pack_settings_path = expected_manifest_path(
        context.workspace_roots.machine_root,
        "pack_settings.json",
    )
    expected_runtime_manifest_path = expected_manifest_path(
        runtime_manifest.owned_roots.machine_root,
        "pack_runtime_manifest.json",
    )
    issues: list[ValidationIssue] = []
    if context.pack_settings_path != expected_pack_settings_path:
        issues.append(
            ValidationIssue(
                code="pack_settings_path_not_under_machine_root",
                message=(
                    "Pack settings must live directly under the declared machine-root "
                    f"manifest directory: {context.pack_settings_path} != "
                    f"{expected_pack_settings_path}"
                ),
                location=context.pack_settings_path,
            )
        )
    actual_runtime_manifest_path = context.loader.pack_runtime_manifest_path(
        context.pack_settings_path
    )
    if actual_runtime_manifest_path != expected_runtime_manifest_path:
        issues.append(
            ValidationIssue(
                code="pack_runtime_manifest_path_not_under_machine_root",
                message=(
                    "Pack runtime manifest must live directly under the declared "
                    f"machine-root manifest directory: {actual_runtime_manifest_path} "
                    f"!= {expected_runtime_manifest_path}"
                ),
                location=actual_runtime_manifest_path,
            )
        )
    return tuple(issues)
