"""Pack-owned integration descriptor for the WatchTower plan pack."""

from __future__ import annotations

from watchtower_core.pack_integration import (
    PackIntegrationConfig,
    PackValidationConfig,
    build_pack_integration,
)

PACK_INTEGRATION = build_pack_integration(
    PackIntegrationConfig(
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
        command_registration_module="watchtower_plan.cli.namespace",
        command_registration_attr="register_plan_namespace",
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
        query_commands=(
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
        ),
        sync_target_names=(
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
        ),
        validation_config=PackValidationConfig(
            document_semantics_module="watchtower_plan.validation.document_semantics",
            document_semantics_attr="DocumentSemanticsValidationService",
            suite_target_resolver_module="watchtower_core.validation.pack_targets",
            suite_target_resolver_attr="resolve_pack_validation_suite_targets",
        ),
        export_cleanup_module="watchtower_plan.export_cleanup",
        export_cleanup_attr="scrub_plan_export",
    )
)

__all__ = ["PACK_INTEGRATION"]
