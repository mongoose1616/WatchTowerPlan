"""Pack-owned integration descriptor for the WatchTower plan pack."""

from __future__ import annotations

from typing import Any

from watchtower_core.pack_integration import PackIntegration


def _command_registration(*args: Any, **kwargs: Any) -> None:
    """Placeholder registration hook until the host runtime cutover lands."""


def _query_runtime(*args: Any, **kwargs: Any) -> dict[str, object]:
    """Placeholder query hook for pack-contract validation."""

    return {}


def _sync_targets(*args: Any, **kwargs: Any) -> tuple[str, ...]:
    """Placeholder sync-target hook for pack-contract validation."""

    return ()


def _validation_provider(*args: Any, **kwargs: Any) -> dict[str, object]:
    """Placeholder validation hook for pack-contract validation."""

    return {}


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
    command_registration=_command_registration,
    query_runtime=_query_runtime,
    sync_targets=_sync_targets,
    validation_provider=_validation_provider,
)


__all__ = ["PACK_INTEGRATION"]
