"""Pack-contract validation services."""

from __future__ import annotations

from watchtower_core.control_plane.errors import ControlPlaneError
from watchtower_core.control_plane.loader import (
    PACK_SETTINGS_PATH,
    ControlPlaneLoader,
)
from watchtower_core.validation._pack_contract.boundaries import dependency_boundary_issues
from watchtower_core.validation._pack_contract.manifest import (
    command_doc_issues,
    manifest_path_issues,
    matching_field_issues,
    registry_collision_issues,
)
from watchtower_core.validation._pack_contract.runtime import integration_issues
from watchtower_core.validation._pack_contract.workspace import (
    core_python_workspace_issues,
    owned_root_issues,
    surface_path_issues,
    validation_suite_issues,
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
            matching_field_issues(
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
        issues.extend(registry_collision_issues(pack_registry, registry_entry))
        issues.extend(manifest_path_issues(context, runtime_manifest))
        issues.extend(owned_root_issues(context, runtime_manifest))
        issues.extend(surface_path_issues(context))
        issues.extend(command_doc_issues(context, runtime_manifest))
        issues.extend(core_python_workspace_issues(context, runtime_manifest))
        issues.extend(validation_suite_issues(context, runtime_manifest))
        issues.extend(integration_issues(runtime_manifest))
        issues.extend(dependency_boundary_issues(context, runtime_manifest))

        return ValidationResult(
            validator_id=PACK_CONTRACT_VALIDATOR_ID,
            target_path=pack_settings_path,
            engine="python",
            schema_ids=(),
            passed=not issues,
            issues=tuple(issues),
        )
