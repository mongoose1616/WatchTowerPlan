"""Pack-owned integration descriptor for the WatchTower plan pack."""

from __future__ import annotations

from typing import Any

from watchtower_core.pack_integration import PackIntegration, PackValidationRuntime
from watchtower_plan.validation.document_semantics import DocumentSemanticsValidationService
from watchtower_plan.validation.targets import resolve_pack_validation_suite_targets


def _command_registration(*args: Any, **kwargs: Any) -> None:
    """Register the pack-owned `plan` namespace lazily to avoid import cycles."""

    from watchtower_plan.cli.namespace import register_plan_namespace

    register_plan_namespace(*args, **kwargs)


def _query_runtime(*args: Any, **kwargs: Any) -> dict[str, object]:
    """Placeholder query hook for pack-contract validation."""

    return {}


def _sync_targets(*args: Any, **kwargs: Any) -> tuple[str, ...]:
    """Placeholder sync-target hook for pack-contract validation."""

    return ()


def _validation_provider(*args: Any, **kwargs: Any) -> PackValidationRuntime:
    """Return the plan-pack validation runtime declared through the contract."""

    return PackValidationRuntime(
        document_semantics_factory=DocumentSemanticsValidationService,
        suite_target_resolver=resolve_pack_validation_suite_targets,
    )


PACK_INTEGRATION = PackIntegration(
    pack_id="pack.plan",
    pack_slug="plan",
    command_namespace="plan",
    python_package="watchtower_plan",
    declared_capabilities=(
        "command_registration",
        "query_runtime",
        "sync_targets",
        "validation_provider",
    ),
    command_implementation_path="plan/python/src/watchtower_plan/cli/namespace.py",
    command_subcommand_implementation_paths=(
        ("bootstrap", "plan/python/src/watchtower_plan/cli/handlers.py"),
        ("confirm-inputs", "plan/python/src/watchtower_plan/cli/handlers.py"),
        ("approve", "plan/python/src/watchtower_plan/cli/handlers.py"),
    ),
    command_registration=_command_registration,
    query_runtime=_query_runtime,
    sync_targets=_sync_targets,
    validation_provider=_validation_provider,
)


__all__ = ["PACK_INTEGRATION"]
