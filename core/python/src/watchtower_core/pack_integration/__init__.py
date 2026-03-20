"""Reusable pack-integration contracts for host and pack composition."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from watchtower_core.control_plane.loader import ControlPlaneLoader
    from watchtower_core.validation.suite import ValidationSuiteTargetResolver

REQUIRED_PACK_CAPABILITIES: tuple[str, ...] = (
    "command_registration",
    "query_runtime",
    "sync_targets",
    "validation_provider",
)
OPTIONAL_PACK_CAPABILITIES: tuple[str, ...] = (
    "bootstrap",
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
PackDocumentSemanticsFactory = Callable[["ControlPlaneLoader"], object]


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
    suite_target_resolver: "ValidationSuiteTargetResolver | None" = None


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


__all__ = [
    "OPTIONAL_PACK_CAPABILITIES",
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
    "REQUIRED_PACK_CAPABILITIES",
    "SUPPORTED_PACK_CAPABILITIES",
]
