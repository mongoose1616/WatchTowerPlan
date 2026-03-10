import watchtower_core.query as public_query
import watchtower_core.sync as public_sync
import watchtower_core.validation as public_validation
from watchtower_core.query.commands import CommandQueryService as LegacyCommandQueryService
from watchtower_core.repo_ops.query.commands import CommandQueryService
from watchtower_core.repo_ops.sync.command_index import CommandIndexSyncService
from watchtower_core.repo_ops.validation import ValidationAllService
from watchtower_core.repo_ops.validation.document_semantics import (
    DocumentSemanticsValidationService,
)
from watchtower_core.sync.command_index import (
    CommandIndexSyncService as LegacyCommandIndexSyncService,
)
from watchtower_core.validation.all import ValidationAllService as LegacyValidationAllService
from watchtower_core.validation.document_semantics import (
    DocumentSemanticsValidationService as LegacyDocumentSemanticsValidationService,
)


def test_public_query_and_sync_packages_do_not_advertise_repo_specific_services() -> None:
    assert not hasattr(public_query, "CommandQueryService")
    assert not hasattr(public_sync, "CommandIndexSyncService")


def test_public_validation_package_does_not_advertise_repo_wide_aggregate_validation() -> None:
    assert not hasattr(public_validation, "ValidationAllService")
    assert not hasattr(public_validation, "VALIDATION_FAMILY_SPECS")


def test_repo_ops_leaf_compatibility_wrappers_remain_available() -> None:
    assert LegacyCommandQueryService is CommandQueryService
    assert LegacyCommandIndexSyncService is CommandIndexSyncService
    assert LegacyValidationAllService is ValidationAllService
    assert LegacyDocumentSemanticsValidationService is DocumentSemanticsValidationService
