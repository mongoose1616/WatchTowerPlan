from watchtower_core.query.acceptance import (
    AcceptanceContractQueryService as LegacyAcceptanceContractQueryService,
)
from watchtower_core.query.commands import CommandQueryService as LegacyCommandQueryService
from watchtower_core.query.decisions import DecisionQueryService as LegacyDecisionQueryService
from watchtower_core.query.designs import (
    DesignDocumentQueryService as LegacyDesignDocumentQueryService,
)
from watchtower_core.query.evidence import (
    ValidationEvidenceQueryService as LegacyValidationEvidenceQueryService,
)
from watchtower_core.query.foundations import FoundationQueryService as LegacyFoundationQueryService
from watchtower_core.query.initiatives import (
    InitiativeQueryService as LegacyInitiativeQueryService,
)
from watchtower_core.query.prds import PrdQueryService as LegacyPrdQueryService
from watchtower_core.query.references import ReferenceQueryService as LegacyReferenceQueryService
from watchtower_core.query.repository import (
    RepositoryPathQueryService as LegacyRepositoryPathQueryService,
)
from watchtower_core.query.standards import StandardQueryService as LegacyStandardQueryService
from watchtower_core.query.tasks import TaskQueryService as LegacyTaskQueryService
from watchtower_core.query.traceability import (
    TraceabilityQueryService as LegacyTraceabilityQueryService,
)
from watchtower_core.query.workflows import WorkflowQueryService as LegacyWorkflowQueryService
from watchtower_core.repo_ops.query.acceptance import AcceptanceContractQueryService
from watchtower_core.repo_ops.query.commands import CommandQueryService
from watchtower_core.repo_ops.query.decisions import DecisionQueryService
from watchtower_core.repo_ops.query.designs import DesignDocumentQueryService
from watchtower_core.repo_ops.query.evidence import ValidationEvidenceQueryService
from watchtower_core.repo_ops.query.foundations import FoundationQueryService
from watchtower_core.repo_ops.query.initiatives import InitiativeQueryService
from watchtower_core.repo_ops.query.prds import PrdQueryService
from watchtower_core.repo_ops.query.references import ReferenceQueryService
from watchtower_core.repo_ops.query.repository import RepositoryPathQueryService
from watchtower_core.repo_ops.query.standards import StandardQueryService
from watchtower_core.repo_ops.query.tasks import TaskQueryService
from watchtower_core.repo_ops.query.traceability import TraceabilityQueryService
from watchtower_core.repo_ops.query.workflows import WorkflowQueryService
from watchtower_core.repo_ops.sync import (
    AllSyncService,
    CommandIndexSyncService,
    GitHubTaskSyncService,
    TaskTrackingSyncService,
    TraceabilityIndexSyncService,
)
from watchtower_core.repo_ops.validation.document_semantics import (
    DocumentSemanticsValidationService,
)
from watchtower_core.sync import (
    AllSyncService as LegacyAllSyncService,
)
from watchtower_core.sync import (
    CommandIndexSyncService as LegacyCommandIndexSyncService,
)
from watchtower_core.sync import (
    GitHubTaskSyncService as LegacyGitHubTaskSyncService,
)
from watchtower_core.sync import (
    TaskTrackingSyncService as LegacyTaskTrackingSyncService,
)
from watchtower_core.sync import (
    TraceabilityIndexSyncService as LegacyTraceabilityIndexSyncService,
)
from watchtower_core.validation.document_semantics import (
    DocumentSemanticsValidationService as LegacyDocumentSemanticsValidationService,
)


def test_repo_ops_query_services_remain_available_via_compatibility_wrappers() -> None:
    assert LegacyAcceptanceContractQueryService is AcceptanceContractQueryService
    assert LegacyCommandQueryService is CommandQueryService
    assert LegacyDecisionQueryService is DecisionQueryService
    assert LegacyDesignDocumentQueryService is DesignDocumentQueryService
    assert LegacyValidationEvidenceQueryService is ValidationEvidenceQueryService
    assert LegacyFoundationQueryService is FoundationQueryService
    assert LegacyInitiativeQueryService is InitiativeQueryService
    assert LegacyPrdQueryService is PrdQueryService
    assert LegacyReferenceQueryService is ReferenceQueryService
    assert LegacyRepositoryPathQueryService is RepositoryPathQueryService
    assert LegacyStandardQueryService is StandardQueryService
    assert LegacyTaskQueryService is TaskQueryService
    assert LegacyTraceabilityQueryService is TraceabilityQueryService
    assert LegacyWorkflowQueryService is WorkflowQueryService


def test_repo_ops_document_semantics_service_remains_available_via_compatibility_wrapper() -> None:
    assert LegacyDocumentSemanticsValidationService is DocumentSemanticsValidationService


def test_repo_ops_sync_services_remain_available_via_compatibility_wrappers() -> None:
    assert LegacyAllSyncService is AllSyncService
    assert LegacyCommandIndexSyncService is CommandIndexSyncService
    assert LegacyGitHubTaskSyncService is GitHubTaskSyncService
    assert LegacyTaskTrackingSyncService is TaskTrackingSyncService
    assert LegacyTraceabilityIndexSyncService is TraceabilityIndexSyncService
