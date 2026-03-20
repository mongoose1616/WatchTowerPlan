"""Synthetic hosted-pack integration used by pack-contract tests."""

from __future__ import annotations

from typing import Any

from watchtower_core.pack_integration import (
    PackIntegration,
    PackQueryRuntime,
    PackSyncRuntime,
    PackValidationRuntime,
)
from watchtower_core.validation.pack_targets import resolve_pack_validation_suite_targets


class OversightFixtureDocumentSemanticsValidationService:
    """Trivial callable factory target for synthetic pack-validation tests."""

    def __init__(self, loader: object) -> None:
        self.loader = loader


def _register_oversight_namespace(*args: Any, **kwargs: Any) -> None:
    subparsers = args[0]
    parser = subparsers.add_parser(
        "oversight",
        help="Synthetic oversight namespace used to prove hosted-pack extensibility.",
    )
    parser.set_defaults(handler=lambda _parsed_args: 0)


def _query_runtime(*args: Any, **kwargs: Any) -> PackQueryRuntime:
    return PackQueryRuntime(commands=("assessments", "reviews"))


def _sync_targets(*args: Any, **kwargs: Any) -> PackSyncRuntime:
    return PackSyncRuntime(targets=("oversight-index", "review-index"))


def _validation_provider(*args: Any, **kwargs: Any) -> PackValidationRuntime:
    return PackValidationRuntime(
        document_semantics_factory=OversightFixtureDocumentSemanticsValidationService,
        suite_target_resolver=resolve_pack_validation_suite_targets,
    )


PACK_INTEGRATION = PackIntegration(
    pack_id="pack.oversight",
    pack_slug="oversight",
    command_namespace="oversight",
    python_package="watchtower_oversight_fixture",
    declared_capabilities=(
        "command_registration",
        "query_runtime",
        "sync_targets",
        "validation_provider",
    ),
    command_implementation_path=(
        "core/python/tests/fixtures/python/watchtower_oversight_fixture/integration.py"
    ),
    command_registration=_register_oversight_namespace,
    query_runtime=_query_runtime,
    sync_targets=_sync_targets,
    validation_provider=_validation_provider,
)
