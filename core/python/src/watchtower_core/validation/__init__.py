"""Validation services and result models for governed artifacts."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "AcceptanceReconciliationService",
    "ArtifactValidationService",
    "FrontMatterValidationService",
    "PackContractValidationService",
    "PackValidationContext",
    "ValidationExecutionError",
    "ValidationIssue",
    "ValidationResult",
    "ValidationSuiteRecord",
    "ValidationSuiteResult",
    "ValidationSuiteService",
    "ValidationSuiteStepSummary",
    "ValidationSelectionError",
]

_EXPORT_MODULES = {
    "AcceptanceReconciliationService": "watchtower_core.validation.acceptance",
    "ArtifactValidationService": "watchtower_core.validation.artifact",
    "FrontMatterValidationService": "watchtower_core.validation.front_matter",
    "PackContractValidationService": "watchtower_core.validation.pack_contract",
    "PackValidationContext": "watchtower_core.validation.context",
    "ValidationExecutionError": "watchtower_core.validation.errors",
    "ValidationIssue": "watchtower_core.validation.models",
    "ValidationResult": "watchtower_core.validation.models",
    "ValidationSuiteRecord": "watchtower_core.validation.models",
    "ValidationSuiteResult": "watchtower_core.validation.models",
    "ValidationSuiteService": "watchtower_core.validation.suite",
    "ValidationSuiteStepSummary": "watchtower_core.validation.models",
    "ValidationSelectionError": "watchtower_core.validation.errors",
}

_REPO_OPS_EXPORTS = {
    "DocumentSemanticsValidationService",
    "ValidationAllRecord",
    "ValidationAllResult",
    "ValidationAllService",
    "VALIDATION_FAMILY_SPECS",
    "ValidationFamilySpec",
    "ValidationFamilySummary",
}


def __getattr__(name: str) -> Any:
    if name in _REPO_OPS_EXPORTS:
        raise AttributeError(
            "watchtower_core.validation exposes only reusable validation services. "
            "Import repo-local document semantics and aggregate validation helpers "
            "from watchtower_core.repo_ops.validation."
        )
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(import_module(module_name), name)
