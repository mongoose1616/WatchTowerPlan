"""Runtime integration checks for pack contracts."""

from __future__ import annotations

import importlib
from typing import Any

from watchtower_core.pack_integration import (
    REQUIRED_PACK_CAPABILITIES,
    SUPPORTED_PACK_CAPABILITIES,
    PackIntegration,
)
from watchtower_core.pack_integration.runtime import (
    validate_pack_query_runtime,
    validate_pack_sync_runtime,
    validate_pack_validation_runtime,
)
from watchtower_core.validation.models import ValidationIssue


def integration_issues(runtime_manifest: Any) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    if runtime_manifest.integration_module != runtime_manifest.python_package and not (
        runtime_manifest.integration_module.startswith(f"{runtime_manifest.python_package}.")
    ):
        issues.append(
            ValidationIssue(
                code="pack_integration_module_not_pack_local",
                message=(
                    "Pack runtime manifest integration_module must stay inside the "
                    "declared pack python package."
                ),
                location=runtime_manifest.integration_module,
            )
        )
    unsupported_capabilities = set(runtime_manifest.declared_capabilities).difference(
        SUPPORTED_PACK_CAPABILITIES
    )
    if unsupported_capabilities:
        issues.append(
            ValidationIssue(
                code="pack_capability_unsupported",
                message=(
                    "Pack runtime manifest declares unsupported capabilities: "
                    + ", ".join(sorted(unsupported_capabilities))
                ),
            )
        )
        return tuple(issues)

    missing_required_capabilities = set(REQUIRED_PACK_CAPABILITIES).difference(
        runtime_manifest.declared_capabilities
    )
    if missing_required_capabilities:
        issues.append(
            ValidationIssue(
                code="pack_required_capability_missing",
                message=(
                    "Pack runtime manifest is missing required capabilities: "
                    + ", ".join(sorted(missing_required_capabilities))
                ),
            )
        )
    try:
        module = importlib.import_module(runtime_manifest.integration_module)
    except ModuleNotFoundError:
        return (
            *issues,
            ValidationIssue(
                code="pack_integration_module_missing",
                message=(
                    "Pack runtime manifest integration module is not importable: "
                    f"{runtime_manifest.integration_module}"
                ),
                location=runtime_manifest.integration_module,
            ),
        )
    except Exception as exc:
        return (
            *issues,
            ValidationIssue(
                code="pack_integration_module_import_error",
                message=(
                    "Pack runtime manifest integration module raised an import-time error: "
                    f"{type(exc).__name__}: {exc}"
                ),
                location=runtime_manifest.integration_module,
            ),
        )

    descriptor = getattr(module, "PACK_INTEGRATION", None)
    if not isinstance(descriptor, PackIntegration):
        return (
            *issues,
            ValidationIssue(
                code="pack_integration_descriptor_missing",
                message=(
                    "Pack integration module must export PACK_INTEGRATION as a "
                    "watchtower_core.pack_integration.PackIntegration instance."
                ),
                location=runtime_manifest.integration_module,
            ),
        )

    for field_name, expected, actual in (
        ("pack_id", runtime_manifest.pack_id, descriptor.pack_id),
        ("pack_slug", runtime_manifest.pack_slug, descriptor.pack_slug),
        ("command_namespace", runtime_manifest.command_namespace, descriptor.command_namespace),
        ("python_package", runtime_manifest.python_package, descriptor.python_package),
    ):
        if expected == actual:
            continue
        issues.append(
            ValidationIssue(
                code=f"pack_integration_{field_name}_mismatch",
                message=(
                    f"Pack integration descriptor mismatch for {field_name}: {expected} != {actual}"
                ),
                location=runtime_manifest.integration_module,
            )
        )

    descriptor_capabilities = set(descriptor.declared_capabilities)
    manifest_capabilities = set(runtime_manifest.declared_capabilities)
    if descriptor_capabilities != manifest_capabilities:
        issues.append(
            ValidationIssue(
                code="pack_integration_capability_mismatch",
                message=(
                    "Pack integration descriptor capabilities do not match the runtime manifest."
                ),
                location=runtime_manifest.integration_module,
            )
        )

    for capability in runtime_manifest.declared_capabilities:
        hook = descriptor.hook_for_capability(capability)
        if hook is None:
            issues.append(
                ValidationIssue(
                    code="pack_integration_hook_missing",
                    message=f"Pack integration descriptor is missing the {capability} hook.",
                    location=runtime_manifest.integration_module,
                )
            )
            continue
        if capability == "validation_provider":
            issues.extend(
                runtime_hook_issues(
                    hook=hook,
                    integration_module=runtime_manifest.integration_module,
                    validator=validate_pack_validation_runtime,
                    error_code="pack_validation_provider_error",
                    invalid_code="pack_validation_provider_invalid",
                    invalid_message=(
                        "Pack validation_provider hook must return "
                        "watchtower_core.pack_integration.PackValidationRuntime."
                    ),
                )
            )
            continue
        if capability == "query_runtime":
            issues.extend(
                runtime_hook_issues(
                    hook=hook,
                    integration_module=runtime_manifest.integration_module,
                    validator=validate_pack_query_runtime,
                    error_code="pack_query_runtime_error",
                    invalid_code="pack_query_runtime_invalid",
                    invalid_message=(
                        "Pack query_runtime hook must return "
                        "watchtower_core.pack_integration.PackQueryRuntime."
                    ),
                )
            )
            continue
        if capability == "sync_targets":
            issues.extend(
                runtime_hook_issues(
                    hook=hook,
                    integration_module=runtime_manifest.integration_module,
                    validator=validate_pack_sync_runtime,
                    error_code="pack_sync_runtime_error",
                    invalid_code="pack_sync_runtime_invalid",
                    invalid_message=(
                        "Pack sync_targets hook must return "
                        "watchtower_core.pack_integration.PackSyncRuntime."
                    ),
                )
            )
            continue

    return tuple(issues)


def runtime_hook_issues(
    *,
    hook: Any,
    integration_module: str,
    validator: Any,
    error_code: str,
    invalid_code: str,
    invalid_message: str,
) -> tuple[ValidationIssue, ...]:
    try:
        runtime = hook()
    except Exception as exc:  # pragma: no cover - fail-closed guard
        return (
            ValidationIssue(
                code=error_code,
                message=f"Pack integration hook raised an error: {exc}",
                location=integration_module,
            ),
        )
    try:
        validator(runtime, integration_module=integration_module)
        return ()
    except ValueError:
        pass
    return (
        ValidationIssue(
            code=invalid_code,
            message=invalid_message,
            location=integration_module,
        ),
    )
