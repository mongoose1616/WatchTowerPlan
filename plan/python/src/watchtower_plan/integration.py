"""Pack-owned integration descriptor for the WatchTower plan pack."""

from __future__ import annotations

from typing import Any

from watchtower_core.pack_integration import (
    PackIntegration,
    PackQueryRuntime,
    PackSyncRuntime,
    PackValidationRuntime,
)
from watchtower_core.validation.pack_targets import (
    resolve_pack_validation_suite_targets,
)
from watchtower_plan.export_cleanup import scrub_plan_export
from watchtower_plan.validation.document_semantics import (
    DocumentSemanticsValidationService,
)


def _command_registration(*args: Any, **kwargs: Any) -> None:
    """Register the pack-owned `plan` namespace lazily to avoid import cycles."""

    from watchtower_plan.cli.namespace import register_plan_namespace

    register_plan_namespace(*args, **kwargs)


def _query_runtime(*args: Any, **kwargs: Any) -> PackQueryRuntime:
    """Return the plan-owned query command surface exposed under `watchtower-core plan query`."""

    return PackQueryRuntime(
        commands=(
            "artifacts",
            "authority",
            "closeouts",
            "coordination",
            "discrepancies",
            "initiatives",
            "plan-evidence",
            "project-context",
            "projects",
            "readiness",
            "reviews",
            "tasks",
            "trace",
        )
    )


def _sync_targets(*args: Any, **kwargs: Any) -> PackSyncRuntime:
    """Return the plan-owned sync targets exposed under `watchtower-core plan sync`."""

    return PackSyncRuntime(
        targets=(
            "all",
            "coordination",
            "reference-index",
            "foundation-index",
            "standard-index",
            "workflow-index",
            "initiative-index",
            "initiative-tracking",
            "task-index",
            "task-tracking",
            "traceability-index",
            "github-tasks",
        )
    )


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
        "export_cleanup",
    ),
    command_implementation_path="plan/python/src/watchtower_plan/cli/namespace.py",
    command_subcommand_implementation_paths=(
        ("bootstrap", "plan/python/src/watchtower_plan/cli/handlers.py"),
        ("confirm-inputs", "plan/python/src/watchtower_plan/cli/handlers.py"),
        ("approve", "plan/python/src/watchtower_plan/cli/handlers.py"),
        ("query", "plan/python/src/watchtower_plan/cli/query.py"),
        ("sync", "plan/python/src/watchtower_plan/cli/sync.py"),
        ("closeout", "plan/python/src/watchtower_plan/cli/closeout.py"),
        ("task", "plan/python/src/watchtower_plan/cli/tasks.py"),
    ),
    command_registration=_command_registration,
    query_runtime=_query_runtime,
    sync_targets=_sync_targets,
    validation_provider=_validation_provider,
    export_cleanup=scrub_plan_export,
)


__all__ = ["PACK_INTEGRATION"]
