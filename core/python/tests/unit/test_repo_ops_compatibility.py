from watchtower_core.query.acceptance import (
    AcceptanceContractQueryService as LegacyAcceptanceContractQueryService,
)
from watchtower_core.query.evidence import (
    ValidationEvidenceQueryService as LegacyValidationEvidenceQueryService,
)
from watchtower_core.query.initiatives import (
    InitiativeQueryService as LegacyInitiativeQueryService,
)
from watchtower_core.query.tasks import TaskQueryService as LegacyTaskQueryService
from watchtower_core.query.traceability import (
    TraceabilityQueryService as LegacyTraceabilityQueryService,
)
from watchtower_core.repo_ops.query.acceptance import AcceptanceContractQueryService
from watchtower_core.repo_ops.query.evidence import ValidationEvidenceQueryService
from watchtower_core.repo_ops.query.initiatives import InitiativeQueryService
from watchtower_core.repo_ops.query.tasks import TaskQueryService
from watchtower_core.repo_ops.query.traceability import TraceabilityQueryService
from watchtower_core.repo_ops.validation.document_semantics import (
    DocumentSemanticsValidationService,
)
from watchtower_core.validation.document_semantics import (
    DocumentSemanticsValidationService as LegacyDocumentSemanticsValidationService,
)


def test_repo_ops_query_services_remain_available_via_compatibility_wrappers() -> None:
    assert LegacyAcceptanceContractQueryService is AcceptanceContractQueryService
    assert LegacyValidationEvidenceQueryService is ValidationEvidenceQueryService
    assert LegacyInitiativeQueryService is InitiativeQueryService
    assert LegacyTaskQueryService is TaskQueryService
    assert LegacyTraceabilityQueryService is TraceabilityQueryService


def test_repo_ops_document_semantics_service_remains_available_via_compatibility_wrapper() -> None:
    assert LegacyDocumentSemanticsValidationService is DocumentSemanticsValidationService
