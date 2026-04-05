"""Factory helpers for building pack integration descriptors from configuration."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from watchtower_core.pack_integration import (
    PackIntegration,
    PackQueryRuntime,
    PackSyncRuntime,
    PackValidationRuntime,
)


@dataclass(frozen=True, slots=True)
class PackValidationConfig:
    """Declarative configuration for pack-owned validation runtime construction."""

    document_semantics_module: str
    document_semantics_attr: str
    suite_target_resolver_module: str | None = None
    suite_target_resolver_attr: str | None = None
    pack_contract_issue_module: str | None = None
    pack_contract_issue_attr: str | None = None


@dataclass(frozen=True, slots=True)
class PackIntegrationConfig:
    """Declarative configuration for one pack integration descriptor."""

    pack_id: str
    pack_slug: str
    command_namespace: str
    python_package: str
    declared_capabilities: tuple[str, ...]

    # Command registration.
    command_registration_module: str
    command_registration_attr: str
    command_implementation_path: str | None = None
    command_subcommand_implementation_paths: tuple[tuple[str, str], ...] = ()

    # Query.
    query_commands: tuple[str, ...] = ()

    # Sync.
    sync_target_names: tuple[str, ...] = ()

    # Validation.
    validation_config: PackValidationConfig | None = None

    # Export cleanup.
    export_cleanup_module: str | None = None
    export_cleanup_attr: str | None = None


def build_pack_integration(config: PackIntegrationConfig) -> PackIntegration:
    """Construct a ``PackIntegration`` from one declarative configuration."""

    return PackIntegration(
        pack_id=config.pack_id,
        pack_slug=config.pack_slug,
        command_namespace=config.command_namespace,
        python_package=config.python_package,
        declared_capabilities=config.declared_capabilities,
        command_implementation_path=config.command_implementation_path,
        command_subcommand_implementation_paths=config.command_subcommand_implementation_paths,
        command_registration=_lazy_command_registrar(
            config.command_registration_module,
            config.command_registration_attr,
        ),
        query_runtime=(
            _lazy_query_provider(config.query_commands) if config.query_commands else None
        ),
        sync_targets=(
            _lazy_sync_provider(config.sync_target_names) if config.sync_target_names else None
        ),
        validation_provider=(
            _lazy_validation_provider(config.validation_config)
            if config.validation_config
            else None
        ),
        export_cleanup=(
            _lazy_export_cleanup(config.export_cleanup_module, config.export_cleanup_attr)
            if config.export_cleanup_module and config.export_cleanup_attr
            else None
        ),
    )


# ---------------------------------------------------------------------------
# Internal lazy-wrapper builders
# ---------------------------------------------------------------------------


def _lazy_command_registrar(module_name: str, attr_name: str) -> Any:
    def _registrar(*args: Any, **kwargs: Any) -> None:
        func = getattr(import_module(module_name), attr_name)
        func(*args, **kwargs)

    return _registrar


def _lazy_query_provider(commands: tuple[str, ...]) -> Any:
    def _provider(*args: Any, **kwargs: Any) -> PackQueryRuntime:
        return PackQueryRuntime(commands=commands)

    return _provider


def _lazy_sync_provider(targets: tuple[str, ...]) -> Any:
    def _provider(*args: Any, **kwargs: Any) -> PackSyncRuntime:
        return PackSyncRuntime(targets=targets)

    return _provider


def _lazy_validation_provider(validation_config: PackValidationConfig) -> Any:
    def _provider(*args: Any, **kwargs: Any) -> PackValidationRuntime:
        doc_semantics = getattr(
            import_module(validation_config.document_semantics_module),
            validation_config.document_semantics_attr,
        )
        suite_resolver = None
        if (
            validation_config.suite_target_resolver_module
            and validation_config.suite_target_resolver_attr
        ):
            suite_resolver = getattr(
                import_module(validation_config.suite_target_resolver_module),
                validation_config.suite_target_resolver_attr,
            )
        contract_provider = None
        if (
            validation_config.pack_contract_issue_module
            and validation_config.pack_contract_issue_attr
        ):
            contract_provider = getattr(
                import_module(validation_config.pack_contract_issue_module),
                validation_config.pack_contract_issue_attr,
            )
        return PackValidationRuntime(
            document_semantics_factory=doc_semantics,
            suite_target_resolver=suite_resolver,
            pack_contract_issue_provider=contract_provider,
        )

    return _provider


def _lazy_export_cleanup(module_name: str, attr_name: str) -> Any:
    def _cleanup(*args: Any, **kwargs: Any) -> object:
        func = getattr(import_module(module_name), attr_name)
        return func(*args, **kwargs)

    return _cleanup
