"""Hosted-pack integration template."""

from __future__ import annotations

from watchtower_core.pack_integration import (
    PackIntegration,
    PackQueryRuntime,
    PackSyncRuntime,
    PackValidationRuntime,
)
from watchtower_core.validation.pack_targets import resolve_pack_validation_suite_targets


class PackDocumentSemanticsValidationService:
    """Replace this with the pack-owned document-semantics service if needed."""

    def __init__(self, loader: object) -> None:
        self.loader = loader


def _register_pack_namespace(subparsers) -> None:
    """Register the pack-owned namespace command family."""

    parser = subparsers.add_parser(
        "<command_namespace>",
        help="Describe the <pack_slug> namespace.",
    )
    parser.set_defaults(handler=lambda _parsed_args: 0)


def _query_runtime() -> PackQueryRuntime:
    """Return the non-empty pack-owned query command inventory."""

    return PackQueryRuntime(commands=("<first_query_command>",))


def _sync_targets() -> PackSyncRuntime:
    """Return the non-empty pack-owned sync target inventory."""

    return PackSyncRuntime(targets=("<first_sync_target>",))


def _validation_provider() -> PackValidationRuntime:
    """Return the pack-owned validation runtime hooks."""

    return PackValidationRuntime(
        document_semantics_factory=PackDocumentSemanticsValidationService,
        suite_target_resolver=resolve_pack_validation_suite_targets,
    )


PACK_INTEGRATION = PackIntegration(
    pack_id="pack.<pack_slug>",
    pack_slug="<pack_slug>",
    command_namespace="<command_namespace>",
    python_package="watchtower_<pack_slug>",
    declared_capabilities=(
        "command_registration",
        "query_runtime",
        "sync_targets",
        "validation_provider",
    ),
    command_implementation_path="<pack_root>/python/src/watchtower_<pack_slug>/integration.py",
    command_registration=_register_pack_namespace,
    query_runtime=_query_runtime,
    sync_targets=_sync_targets,
    validation_provider=_validation_provider,
)
