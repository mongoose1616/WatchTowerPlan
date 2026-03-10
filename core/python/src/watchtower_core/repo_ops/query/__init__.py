"""Repository-specific query services."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "AcceptanceContractQueryService",
    "AcceptanceContractSearchParams",
    "CommandQueryService",
    "CommandSearchParams",
    "DecisionQueryService",
    "DecisionSearchParams",
    "DesignDocumentQueryService",
    "DesignDocumentSearchParams",
    "ValidationEvidenceQueryService",
    "ValidationEvidenceSearchParams",
    "FoundationQueryService",
    "FoundationSearchParams",
    "InitiativeQueryService",
    "InitiativeSearchParams",
    "PrdQueryService",
    "PrdSearchParams",
    "ReferenceQueryService",
    "ReferenceSearchParams",
    "RepositoryPathQueryService",
    "RepositoryPathSearchParams",
    "StandardQueryService",
    "StandardSearchParams",
    "TaskQueryService",
    "TaskSearchParams",
    "TraceabilityQueryService",
    "WorkflowQueryService",
    "WorkflowSearchParams",
]

_EXPORT_MODULES = {
    "AcceptanceContractQueryService": "watchtower_core.repo_ops.query.acceptance",
    "AcceptanceContractSearchParams": "watchtower_core.repo_ops.query.acceptance",
    "CommandQueryService": "watchtower_core.repo_ops.query.commands",
    "CommandSearchParams": "watchtower_core.repo_ops.query.commands",
    "DecisionQueryService": "watchtower_core.repo_ops.query.decisions",
    "DecisionSearchParams": "watchtower_core.repo_ops.query.decisions",
    "DesignDocumentQueryService": "watchtower_core.repo_ops.query.designs",
    "DesignDocumentSearchParams": "watchtower_core.repo_ops.query.designs",
    "ValidationEvidenceQueryService": "watchtower_core.repo_ops.query.evidence",
    "ValidationEvidenceSearchParams": "watchtower_core.repo_ops.query.evidence",
    "FoundationQueryService": "watchtower_core.repo_ops.query.foundations",
    "FoundationSearchParams": "watchtower_core.repo_ops.query.foundations",
    "InitiativeQueryService": "watchtower_core.repo_ops.query.initiatives",
    "InitiativeSearchParams": "watchtower_core.repo_ops.query.initiatives",
    "PrdQueryService": "watchtower_core.repo_ops.query.prds",
    "PrdSearchParams": "watchtower_core.repo_ops.query.prds",
    "ReferenceQueryService": "watchtower_core.repo_ops.query.references",
    "ReferenceSearchParams": "watchtower_core.repo_ops.query.references",
    "RepositoryPathQueryService": "watchtower_core.repo_ops.query.repository",
    "RepositoryPathSearchParams": "watchtower_core.repo_ops.query.repository",
    "StandardQueryService": "watchtower_core.repo_ops.query.standards",
    "StandardSearchParams": "watchtower_core.repo_ops.query.standards",
    "TaskQueryService": "watchtower_core.repo_ops.query.tasks",
    "TaskSearchParams": "watchtower_core.repo_ops.query.tasks",
    "TraceabilityQueryService": "watchtower_core.repo_ops.query.traceability",
    "WorkflowQueryService": "watchtower_core.repo_ops.query.workflows",
    "WorkflowSearchParams": "watchtower_core.repo_ops.query.workflows",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(import_module(module_name), name)
