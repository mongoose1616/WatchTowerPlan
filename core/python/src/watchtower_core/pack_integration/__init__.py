"""Reusable pack-integration contracts for host and pack composition."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from watchtower_core.control_plane.loader import ControlPlaneLoader
    from watchtower_core.pack_integration.bootstrap import (
        PackBootstrapRequest,
        PackBootstrapResult,
    )
    from watchtower_core.pack_integration.export import (
        PackExportCleanupRequest,
        PackExportCleanupResult,
        PackExportRequest,
        PackExportResult,
        PackExportValidationSummary,
    )
    from watchtower_core.pack_integration.scaffold import (
        PackScaffoldRequest,
        PackScaffoldResult,
    )
    from watchtower_core.pack_integration.workspace_registration import (
        CORE_PYPROJECT_RELATIVE_PATH,
        CORE_UV_LOCK_RELATIVE_PATH,
        CorePythonWorkspaceRegistration,
        reconcile_core_python_workspace_pyproject,
    )
    from watchtower_core.pack_integration.factory import (
        PackIntegrationConfig,
        PackValidationConfig,
    )
    from watchtower_core.validation.models import ValidationIssue
    from watchtower_core.validation.suite import (
        DocumentSemanticsValidationService,
        ValidationSuiteTargetResolver,
    )

REQUIRED_PACK_CAPABILITIES: tuple[str, ...] = (
    "command_registration",
    "query_runtime",
    "sync_targets",
    "validation_provider",
)
OPTIONAL_PACK_CAPABILITIES: tuple[str, ...] = (
    "bootstrap",
    "export_cleanup",
    "task_lifecycle",
    "initiative_lifecycle",
    "project_context",
    "promotion",
    "closeout",
    "review_lifecycle",
    "rendered_views",
)
SUPPORTED_PACK_CAPABILITIES: tuple[str, ...] = (
    *REQUIRED_PACK_CAPABILITIES,
    *OPTIONAL_PACK_CAPABILITIES,
)


class PackCommandRegistrar(Protocol):
    """Register pack-owned CLI commands with the host runtime."""

    def __call__(self, *args: Any, **kwargs: Any) -> object: ...


class PackQueryProvider(Protocol):
    """Expose pack-owned query behavior to the host runtime."""

    def __call__(self, *args: Any, **kwargs: Any) -> PackQueryRuntime: ...


class PackSyncTargetProvider(Protocol):
    """Expose pack-owned sync targets to the host runtime."""

    def __call__(self, *args: Any, **kwargs: Any) -> PackSyncRuntime: ...


class PackValidationProvider(Protocol):
    """Expose pack-owned validation adapters to the host runtime."""

    def __call__(self, *args: Any, **kwargs: Any) -> PackValidationRuntime: ...


PackLifecycleHook = Callable[..., object]
PackDocumentSemanticsFactory = Callable[
    ["ControlPlaneLoader"], "DocumentSemanticsValidationService"
]
PackContractIssueProvider = Callable[
    ["ControlPlaneLoader", str],
    tuple["ValidationIssue", ...],
]


@dataclass(frozen=True, slots=True)
class PackQueryRuntime:
    """Pack-owned query hooks consumed through the integration contract."""

    commands: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PackSyncRuntime:
    """Pack-owned sync hooks consumed through the integration contract."""

    targets: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PackValidationRuntime:
    """Pack-owned validation hooks consumed through the integration contract."""

    document_semantics_factory: PackDocumentSemanticsFactory
    suite_target_resolver: ValidationSuiteTargetResolver | None = None
    pack_contract_issue_provider: PackContractIssueProvider | None = None


@dataclass(frozen=True, slots=True)
class PackIntegration:
    """Pack-owned integration descriptor exported for host composition."""

    pack_id: str
    pack_slug: str
    command_namespace: str
    python_package: str
    declared_capabilities: tuple[str, ...]
    command_implementation_path: str | None = None
    command_subcommand_implementation_paths: tuple[tuple[str, str], ...] = ()
    command_registration: PackCommandRegistrar | None = None
    query_runtime: PackQueryProvider | None = None
    sync_targets: PackSyncTargetProvider | None = None
    validation_provider: PackValidationProvider | None = None
    bootstrap: PackLifecycleHook | None = None
    export_cleanup: PackLifecycleHook | None = None
    task_lifecycle: PackLifecycleHook | None = None
    initiative_lifecycle: PackLifecycleHook | None = None
    project_context: PackLifecycleHook | None = None
    promotion: PackLifecycleHook | None = None
    closeout: PackLifecycleHook | None = None
    review_lifecycle: PackLifecycleHook | None = None
    rendered_views: PackLifecycleHook | None = None

    def hook_for_capability(self, capability: str) -> object | None:
        """Return the registered hook for one declared capability."""

        return getattr(self, capability, None)


_EXPORTS: dict[str, tuple[str, str]] = {
    "CORE_PYPROJECT_RELATIVE_PATH": (
        "watchtower_core.pack_integration.workspace_registration",
        "CORE_PYPROJECT_RELATIVE_PATH",
    ),
    "CORE_UV_LOCK_RELATIVE_PATH": (
        "watchtower_core.pack_integration.workspace_registration",
        "CORE_UV_LOCK_RELATIVE_PATH",
    ),
    "CorePythonWorkspaceRegistration": (
        "watchtower_core.pack_integration.workspace_registration",
        "CorePythonWorkspaceRegistration",
    ),
    "PackBootstrapRequest": (
        "watchtower_core.pack_integration.bootstrap",
        "PackBootstrapRequest",
    ),
    "PackBootstrapResult": (
        "watchtower_core.pack_integration.bootstrap",
        "PackBootstrapResult",
    ),
    "EngineeringCoreApplyRequest": (
        "watchtower_core.pack_integration.export",
        "EngineeringCoreApplyRequest",
    ),
    "EngineeringCoreApplyResult": (
        "watchtower_core.pack_integration.export",
        "EngineeringCoreApplyResult",
    ),
    "PackExportRequest": (
        "watchtower_core.pack_integration.export",
        "PackExportRequest",
    ),
    "PackExportCleanupRequest": (
        "watchtower_core.pack_integration.export",
        "PackExportCleanupRequest",
    ),
    "PackExportCleanupResult": (
        "watchtower_core.pack_integration.export",
        "PackExportCleanupResult",
    ),
    "PackExportResult": (
        "watchtower_core.pack_integration.export",
        "PackExportResult",
    ),
    "PackExportValidationSummary": (
        "watchtower_core.pack_integration.export",
        "PackExportValidationSummary",
    ),
    "PackScaffoldRequest": (
        "watchtower_core.pack_integration.scaffold",
        "PackScaffoldRequest",
    ),
    "PackScaffoldResult": (
        "watchtower_core.pack_integration.scaffold",
        "PackScaffoldResult",
    ),
    "bootstrap_hosted_pack": (
        "watchtower_core.pack_integration.bootstrap",
        "bootstrap_hosted_pack",
    ),
    "apply_engineering_core_extract": (
        "watchtower_core.pack_integration.export",
        "apply_engineering_core_extract",
    ),
    "export_hosted_repository": (
        "watchtower_core.pack_integration.export",
        "export_hosted_repository",
    ),
    "core_python_workspace_registration": (
        "watchtower_core.pack_integration.workspace_registration",
        "core_python_workspace_registration",
    ),
    "ensure_core_python_workspace_registration": (
        "watchtower_core.pack_integration.workspace_registration",
        "ensure_core_python_workspace_registration",
    ),
    "hosted_pack_workspace_registrations": (
        "watchtower_core.pack_integration.workspace_registration",
        "hosted_pack_workspace_registrations",
    ),
    "load_core_python_workspace_state": (
        "watchtower_core.pack_integration.workspace_registration",
        "load_core_python_workspace_state",
    ),
    "pack_command_docs_root": (
        "watchtower_core.pack_integration.docs",
        "pack_command_docs_root",
    ),
    "pack_command_entry_doc_path": (
        "watchtower_core.pack_integration.docs",
        "pack_command_entry_doc_path",
    ),
    "parse_core_python_workspace_state": (
        "watchtower_core.pack_integration.workspace_registration",
        "parse_core_python_workspace_state",
    ),
    "reconcile_core_python_workspace_pyproject": (
        "watchtower_core.pack_integration.workspace_registration",
        "reconcile_core_python_workspace_pyproject",
    ),
    "render_core_python_workspace_pyproject": (
        "watchtower_core.pack_integration.workspace_registration",
        "render_core_python_workspace_pyproject",
    ),
    "scaffold_hosted_pack": (
        "watchtower_core.pack_integration.scaffold",
        "scaffold_hosted_pack",
    ),
    "PackIntegrationConfig": (
        "watchtower_core.pack_integration.factory",
        "PackIntegrationConfig",
    ),
    "PackValidationConfig": (
        "watchtower_core.pack_integration.factory",
        "PackValidationConfig",
    ),
    "build_pack_integration": (
        "watchtower_core.pack_integration.factory",
        "build_pack_integration",
    ),
}


__all__ = [
    "OPTIONAL_PACK_CAPABILITIES",
    "CORE_PYPROJECT_RELATIVE_PATH",
    "CORE_UV_LOCK_RELATIVE_PATH",
    "CorePythonWorkspaceRegistration",
    "EngineeringCoreApplyRequest",
    "EngineeringCoreApplyResult",
    "PackBootstrapRequest",
    "PackBootstrapResult",
    "PackExportRequest",
    "PackExportCleanupRequest",
    "PackExportCleanupResult",
    "PackExportResult",
    "PackExportValidationSummary",
    "PackCommandRegistrar",
    "PackDocumentSemanticsFactory",
    "PackIntegration",
    "PackLifecycleHook",
    "PackQueryProvider",
    "PackQueryRuntime",
    "PackSyncRuntime",
    "PackSyncTargetProvider",
    "PackValidationRuntime",
    "PackValidationProvider",
    "PackScaffoldRequest",
    "PackScaffoldResult",
    "REQUIRED_PACK_CAPABILITIES",
    "SUPPORTED_PACK_CAPABILITIES",
    "apply_engineering_core_extract",
    "bootstrap_hosted_pack",
    "export_hosted_repository",
    "core_python_workspace_registration",
    "ensure_core_python_workspace_registration",
    "hosted_pack_workspace_registrations",
    "load_core_python_workspace_state",
    "pack_command_docs_root",
    "pack_command_entry_doc_path",
    "parse_core_python_workspace_state",
    "reconcile_core_python_workspace_pyproject",
    "render_core_python_workspace_pyproject",
    "scaffold_hosted_pack",
    "PackIntegrationConfig",
    "PackValidationConfig",
    "build_pack_integration",
]


def __getattr__(name: str) -> object:
    try:
        module_name, attribute_name = _EXPORTS[name]
    except KeyError as exc:  # pragma: no cover - Python import protocol
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc
    value = getattr(import_module(module_name), attribute_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
