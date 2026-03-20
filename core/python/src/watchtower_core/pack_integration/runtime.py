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
from watchtower_core.pack_integration import PackIntegration, PackValidationRuntime


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

    pack_settings = loader.load_pack_settings(pack_settings_path)
    registry_entry = loader.load_pack_registry().get_by_pack_id(pack_settings.pack_id)
    runtime_manifest = loader.load_pack_runtime_manifest(pack_settings_path=pack_settings_path)
    descriptor = _load_pack_integration_descriptor(runtime_manifest)
    return LoadedPackIntegration(
        pack_settings=pack_settings,
        registry_entry=registry_entry,
        runtime_manifest=runtime_manifest,
        integration=descriptor,
    )


def load_pack_validation_runtime(
    loader: ControlPlaneLoader,
    *,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> PackValidationRuntime:
    """Load the declared validation runtime for one active pack."""

    loaded = load_active_pack_integration(loader, pack_settings_path=pack_settings_path)
    provider = loaded.integration.validation_provider
    if provider is None:
        raise ValueError(
            "Pack integration is missing its validation_provider hook: "
            f"{loaded.runtime_manifest.integration_module}"
        )
    runtime = provider()
    return _validated_pack_validation_runtime(
        runtime,
        integration_module=loaded.runtime_manifest.integration_module,
    )


def _load_pack_integration_descriptor(runtime_manifest: PackRuntimeManifest) -> PackIntegration:
    module = import_module(runtime_manifest.integration_module)
    descriptor = getattr(module, "PACK_INTEGRATION", None)
    if not isinstance(descriptor, PackIntegration):
        raise ValueError(
            "Pack integration module must export PACK_INTEGRATION as a "
            "watchtower_core.pack_integration.PackIntegration instance: "
            f"{runtime_manifest.integration_module}"
        )
    return descriptor


def _validated_pack_validation_runtime(
    runtime: object,
    *,
    integration_module: str,
) -> PackValidationRuntime:
    if not isinstance(runtime, PackValidationRuntime):
        raise ValueError(
            "Pack validation_provider must return PackValidationRuntime: "
            f"{integration_module}"
        )
    if not callable(runtime.document_semantics_factory):
        raise ValueError(
            "Pack validation_provider must return a callable document_semantics_factory: "
            f"{integration_module}"
        )
    if runtime.suite_target_resolver is not None and not callable(
        runtime.suite_target_resolver
    ):
        raise ValueError(
            "Pack validation_provider must return a callable suite_target_resolver when "
            f"declared: {integration_module}"
        )
    return runtime


__all__ = [
    "LoadedPackIntegration",
    "load_active_pack_integration",
    "load_pack_validation_runtime",
]
