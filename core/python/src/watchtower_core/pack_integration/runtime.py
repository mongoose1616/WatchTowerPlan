"""Runtime helpers for loading declared pack integrations generically."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    PackRegistryEntry,
    PackRuntimeManifest,
    PackSettings,
)
from watchtower_core.pack_integration import (
    PackIntegration,
    PackQueryRuntime,
    PackSyncRuntime,
    PackValidationRuntime,
)
from watchtower_core.telemetry import telemetry_operation


@dataclass(frozen=True, slots=True)
class LoadedPackIntegration:
    """Resolved hosted-pack integration plus its governing machine contracts."""

    pack_settings: PackSettings
    registry_entry: PackRegistryEntry
    runtime_manifest: PackRuntimeManifest
    integration: PackIntegration


def load_active_pack_integration(
    loader: ControlPlaneLoader,
    *,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> LoadedPackIntegration:
    """Load the declared integration for one active pack settings surface."""

    with telemetry_operation(
        "pack_runtime",
        "load_active_pack_integration",
        attributes={"pack_settings_path": pack_settings_path},
    ) as operation:
        pack_settings = loader.load_pack_settings(pack_settings_path)
        registry_entry = loader.load_pack_registry().get_by_pack_id(pack_settings.pack_id)
        runtime_manifest = loader.load_pack_runtime_manifest(pack_settings_path=pack_settings_path)
        descriptor = _load_pack_integration_descriptor(runtime_manifest)
        loaded = LoadedPackIntegration(
            pack_settings=pack_settings,
            registry_entry=registry_entry,
            runtime_manifest=runtime_manifest,
            integration=descriptor,
        )
        if operation is not None:
            operation.set_result(
                status="ok",
                pack_slug=registry_entry.pack_slug,
                command_namespace=runtime_manifest.command_namespace,
                integration_module=runtime_manifest.integration_module,
            )
        return loaded


def load_registered_pack_integrations(
    loader: ControlPlaneLoader,
) -> tuple[LoadedPackIntegration, ...]:
    """Load every hosted-pack integration declared in the shared pack registry."""

    with telemetry_operation("pack_runtime", "load_registered_pack_integrations") as operation:
        registry = loader.load_pack_registry()
        loaded: list[LoadedPackIntegration] = []
        for entry in registry.packs:
            pack_settings = loader.load_pack_settings(entry.pack_settings_path)
            runtime_manifest = loader.load_pack_runtime_manifest(
                pack_settings_path=entry.pack_settings_path
            )
            descriptor = _load_pack_integration_descriptor(runtime_manifest)
            loaded.append(
                LoadedPackIntegration(
                    pack_settings=pack_settings,
                    registry_entry=entry,
                    runtime_manifest=runtime_manifest,
                    integration=descriptor,
                )
            )
        result = tuple(loaded)
        if operation is not None:
            operation.set_result(
                status="ok",
                pack_count=len(result),
                pack_slugs=[item.registry_entry.pack_slug for item in result],
            )
        return result


def load_pack_validation_runtime(
    loader: ControlPlaneLoader,
    *,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> PackValidationRuntime:
    """Load the declared validation runtime for one active pack."""

    with telemetry_operation(
        "pack_runtime",
        "load_pack_validation_runtime",
        attributes={"pack_settings_path": pack_settings_path},
    ) as operation:
        loaded = load_active_pack_integration(loader, pack_settings_path=pack_settings_path)
        provider = loaded.integration.validation_provider
        if provider is None:
            raise ValueError(
                "Pack integration is missing its validation_provider hook: "
                f"{loaded.runtime_manifest.integration_module}"
            )
        runtime = provider()
        validated = validate_pack_validation_runtime(
            runtime,
            integration_module=loaded.runtime_manifest.integration_module,
        )
        if operation is not None:
            operation.set_result(
                status="ok",
                pack_slug=loaded.registry_entry.pack_slug,
                integration_module=loaded.runtime_manifest.integration_module,
            )
        return validated


def load_pack_query_runtime(
    loader: ControlPlaneLoader,
    *,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> PackQueryRuntime:
    """Load the declared query runtime for one active pack."""

    with telemetry_operation(
        "pack_runtime",
        "load_pack_query_runtime",
        attributes={"pack_settings_path": pack_settings_path},
    ) as operation:
        loaded = load_active_pack_integration(loader, pack_settings_path=pack_settings_path)
        provider = loaded.integration.query_runtime
        if provider is None:
            raise ValueError(
                "Pack integration is missing its query_runtime hook: "
                f"{loaded.runtime_manifest.integration_module}"
            )
        runtime = provider()
        validated = validate_pack_query_runtime(
            runtime,
            integration_module=loaded.runtime_manifest.integration_module,
        )
        if operation is not None:
            operation.set_result(
                status="ok",
                pack_slug=loaded.registry_entry.pack_slug,
                integration_module=loaded.runtime_manifest.integration_module,
                command_count=len(validated.commands),
            )
        return validated


def load_pack_sync_runtime(
    loader: ControlPlaneLoader,
    *,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> PackSyncRuntime:
    """Load the declared sync runtime for one active pack."""

    with telemetry_operation(
        "pack_runtime",
        "load_pack_sync_runtime",
        attributes={"pack_settings_path": pack_settings_path},
    ) as operation:
        loaded = load_active_pack_integration(loader, pack_settings_path=pack_settings_path)
        provider = loaded.integration.sync_targets
        if provider is None:
            raise ValueError(
                "Pack integration is missing its sync_targets hook: "
                f"{loaded.runtime_manifest.integration_module}"
            )
        runtime = provider()
        validated = validate_pack_sync_runtime(
            runtime,
            integration_module=loaded.runtime_manifest.integration_module,
        )
        if operation is not None:
            operation.set_result(
                status="ok",
                pack_slug=loaded.registry_entry.pack_slug,
                integration_module=loaded.runtime_manifest.integration_module,
                target_count=len(validated.targets),
            )
        return validated


def _load_pack_integration_descriptor(runtime_manifest: PackRuntimeManifest) -> PackIntegration:
    with telemetry_operation(
        "pack_runtime_import",
        runtime_manifest.integration_module,
        attributes={
            "pack_slug": runtime_manifest.pack_slug,
            "command_namespace": runtime_manifest.command_namespace,
        },
    ) as operation:
        module = import_module(runtime_manifest.integration_module)
        descriptor = getattr(module, "PACK_INTEGRATION", None)
        if not isinstance(descriptor, PackIntegration):
            raise ValueError(
                "Pack integration module must export PACK_INTEGRATION as a "
                "watchtower_core.pack_integration.PackIntegration instance: "
                f"{runtime_manifest.integration_module}"
            )
        if operation is not None:
            operation.set_result(
                status="ok",
                capability_count=len(runtime_manifest.declared_capabilities),
            )
        return descriptor


def validate_pack_validation_runtime(
    runtime: object,
    *,
    integration_module: str,
) -> PackValidationRuntime:
    if not isinstance(runtime, PackValidationRuntime):
        raise ValueError(
            f"Pack validation_provider must return PackValidationRuntime: {integration_module}"
        )
    if not callable(runtime.document_semantics_factory):
        raise ValueError(
            "Pack validation_provider must return a callable document_semantics_factory: "
            f"{integration_module}"
        )
    if runtime.suite_target_resolver is not None and not callable(runtime.suite_target_resolver):
        raise ValueError(
            "Pack validation_provider must return a callable suite_target_resolver when "
            f"declared: {integration_module}"
        )
    return runtime


def validate_pack_query_runtime(
    runtime: object,
    *,
    integration_module: str,
) -> PackQueryRuntime:
    if not isinstance(runtime, PackQueryRuntime):
        raise ValueError(
            f"Pack query_runtime hook must return PackQueryRuntime: {integration_module}"
        )
    if not runtime.commands or not all(
        isinstance(command, str) and command for command in runtime.commands
    ):
        raise ValueError(
            "Pack query_runtime hook must return one or more non-empty command names: "
            f"{integration_module}"
        )
    return runtime


def validate_pack_sync_runtime(
    runtime: object,
    *,
    integration_module: str,
) -> PackSyncRuntime:
    if not isinstance(runtime, PackSyncRuntime):
        raise ValueError(
            f"Pack sync_targets hook must return PackSyncRuntime: {integration_module}"
        )
    if not runtime.targets or not all(
        isinstance(target, str) and target for target in runtime.targets
    ):
        raise ValueError(
            "Pack sync_targets hook must return one or more non-empty target names: "
            f"{integration_module}"
        )
    return runtime


__all__ = [
    "LoadedPackIntegration",
    "load_active_pack_integration",
    "load_pack_query_runtime",
    "load_pack_sync_runtime",
    "load_registered_pack_integrations",
    "load_pack_validation_runtime",
    "validate_pack_query_runtime",
    "validate_pack_sync_runtime",
    "validate_pack_validation_runtime",
]
