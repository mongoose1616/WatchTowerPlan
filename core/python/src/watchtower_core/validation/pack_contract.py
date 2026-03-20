"""Pack-contract validation services."""

from __future__ import annotations

import importlib
from pathlib import Path

from watchtower_core.control_plane.errors import ControlPlaneError
from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.pack_integration import (
    REQUIRED_PACK_CAPABILITIES,
    SUPPORTED_PACK_CAPABILITIES,
    PackIntegration,
    pack_command_entry_doc_path,
)
from watchtower_core.pack_integration.runtime import (
    validate_pack_query_runtime,
    validate_pack_sync_runtime,
    validate_pack_validation_runtime,
)
from watchtower_core.validation.context import PackValidationContext
from watchtower_core.validation.models import ValidationIssue, ValidationResult

PACK_CONTRACT_VALIDATOR_ID = "validator.pack.contract"


class PackContractValidationService:
    """Validate that a pack publishes the governed surfaces core expects."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def validate(self, pack_settings_path: str = PACK_SETTINGS_PATH) -> ValidationResult:
        """Validate one pack settings surface and its declared validation context."""

        issues: list[ValidationIssue] = []
        try:
            context = PackValidationContext.from_loader(
                self._loader,
                pack_settings_path=pack_settings_path,
            )
            pack_registry = context.loader.load_pack_registry()
            registry_entry = pack_registry.get_by_pack_id(context.pack_settings.pack_id)
            runtime_manifest = context.loader.load_pack_runtime_manifest(
                pack_settings_path=context.pack_settings_path
            )
        except (ControlPlaneError, ValueError) as exc:
            return ValidationResult(
                validator_id=PACK_CONTRACT_VALIDATOR_ID,
                target_path=pack_settings_path,
                engine="python",
                schema_ids=(),
                passed=False,
                issues=(
                    ValidationIssue(
                        code="pack_contract_invalid",
                        message=str(exc),
                        location=pack_settings_path,
                    ),
                ),
            )

        if registry_entry.pack_settings_path != context.pack_settings_path:
            issues.append(
                ValidationIssue(
                    code="pack_registry_settings_path_mismatch",
                    message=(
                        "Pack registry entry does not match the active pack settings path: "
                        f"{registry_entry.pack_settings_path} != {context.pack_settings_path}"
                    ),
                    location=context.pack_settings_path,
                )
            )
        effective_runtime_manifest_path = context.loader.pack_runtime_manifest_path(
            context.pack_settings_path
        )
        if registry_entry.pack_runtime_manifest_path != effective_runtime_manifest_path:
            issues.append(
                ValidationIssue(
                    code="pack_registry_runtime_manifest_path_mismatch",
                    message=(
                        "Pack registry entry does not match the active runtime manifest path: "
                        f"{registry_entry.pack_runtime_manifest_path} "
                        f"!= {effective_runtime_manifest_path}"
                    ),
                    location=effective_runtime_manifest_path,
                )
            )

        issues.extend(
            _matching_field_issues(
                pack_id=context.pack_settings.pack_id,
                registry_pack_id=registry_entry.pack_id,
                manifest_pack_id=runtime_manifest.pack_id,
                pack_slug=registry_entry.pack_slug,
                manifest_pack_slug=runtime_manifest.pack_slug,
                command_namespace=registry_entry.command_namespace,
                manifest_command_namespace=runtime_manifest.command_namespace,
                python_distribution=registry_entry.python_distribution,
                manifest_python_distribution=runtime_manifest.python_distribution,
                python_package=registry_entry.python_package,
                manifest_python_package=runtime_manifest.python_package,
            )
        )
        issues.extend(_owned_root_issues(context, runtime_manifest))
        issues.extend(_command_doc_issues(context, runtime_manifest))
        issues.extend(_validation_suite_issues(context, runtime_manifest))
        issues.extend(_integration_issues(runtime_manifest))

        return ValidationResult(
            validator_id=PACK_CONTRACT_VALIDATOR_ID,
            target_path=pack_settings_path,
            engine="python",
            schema_ids=(),
            passed=not issues,
            issues=tuple(issues),
        )


def _matching_field_issues(
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


def _owned_root_issues(
    context: PackValidationContext,
    runtime_manifest,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    workspace_roots = context.workspace_roots
    owned_roots = runtime_manifest.owned_roots
    for field_name, expected, actual in (
        ("workspace_root", workspace_roots.workspace_root, owned_roots.workspace_root),
        ("machine_root", workspace_roots.machine_root, owned_roots.machine_root),
        ("docs_root", workspace_roots.docs_root, owned_roots.docs_root),
        ("workflows_root", workspace_roots.workflows_root, owned_roots.workflows_root),
        ("tracking_root", workspace_roots.tracking_root, owned_roots.tracking_root),
        ("python_root", _expected_python_root(workspace_roots.workspace_root), owned_roots.python_root),
        ("initiatives_root", workspace_roots.initiatives_root, owned_roots.initiatives_root),
        ("projects_root", workspace_roots.projects_root, owned_roots.projects_root),
    ):
        if expected != actual:
            issues.append(
                ValidationIssue(
                    code=f"pack_owned_roots_{field_name}_mismatch",
                    message=(
                        f"Pack owned_roots field mismatch for {field_name}: {expected} != {actual}"
                    ),
                    location=actual,
                )
            )
        issues.extend(
            _owned_root_location_issues(
                workspace_root=owned_roots.workspace_root,
                field_name=field_name,
                relative_path=actual,
                repo_root=context.loader.repo_root,
            )
        )
    return tuple(issues)


def _command_doc_issues(
    context: PackValidationContext,
    runtime_manifest,
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


def _expected_python_root(workspace_root: str) -> str:
    return f"{workspace_root}/python"


def _owned_root_location_issues(
    *,
    workspace_root: str,
    field_name: str,
    relative_path: str | None,
    repo_root: Path,
) -> tuple[ValidationIssue, ...]:
    if not relative_path:
        return ()
    issues: list[ValidationIssue] = []
    if relative_path != workspace_root and not relative_path.startswith(f"{workspace_root}/"):
        issues.append(
            ValidationIssue(
                code="pack_owned_root_not_pack_local",
                message=(
                    "Pack owned root must stay under the pack workspace root: "
                    f"{field_name} -> {relative_path}"
                ),
                location=relative_path,
            )
        )
    if not (repo_root / relative_path).exists():
        issues.append(
            ValidationIssue(
                code="pack_owned_root_missing",
                message=f"Pack owned root is missing from the repository: {relative_path}",
                location=relative_path,
            )
        )
    return tuple(issues)


def _validation_suite_issues(
    context: PackValidationContext,
    runtime_manifest,
) -> tuple[ValidationIssue, ...]:
    available_suite_ids = {
        suite.suite_id for suite in context.validation_suite_registry.suites
    }
    issues: list[ValidationIssue] = []
    for suite_id in runtime_manifest.required_validation_suite_ids:
        if suite_id in available_suite_ids:
            continue
        issues.append(
            ValidationIssue(
                code="pack_required_validation_suite_missing",
                message=(
                    "Pack runtime manifest declares a missing validation suite: "
                    f"{suite_id}"
                ),
                location=context.pack_settings_path,
            )
        )
    return tuple(issues)


def _integration_issues(runtime_manifest) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
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
                message=f"Pack integration descriptor mismatch for {field_name}: {expected} != {actual}",
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
                _runtime_hook_issues(
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
                _runtime_hook_issues(
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
                _runtime_hook_issues(
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


def _runtime_hook_issues(
    *,
    hook,
    integration_module: str,
    validator,
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
