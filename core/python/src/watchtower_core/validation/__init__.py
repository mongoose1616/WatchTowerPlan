"""Validation services and result models for governed artifacts."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "AcceptanceReconciliationService",
    "ArtifactValidationService",
    "DocumentSemanticsValidationService",
    "FrontMatterValidationService",
    "ValidationExecutionError",
    "ValidationIssue",
    "ValidationResult",
    "ValidationSelectionError",
]

_EXPORT_MODULES = {
    "AcceptanceReconciliationService": "watchtower_core.validation.acceptance",
    "ArtifactValidationService": "watchtower_core.validation.artifact",
    "DocumentSemanticsValidationService": "watchtower_core.validation.document_semantics",
    "FrontMatterValidationService": "watchtower_core.validation.front_matter",
    "ValidationExecutionError": "watchtower_core.validation.errors",
    "ValidationIssue": "watchtower_core.validation.models",
    "ValidationResult": "watchtower_core.validation.models",
    "ValidationSelectionError": "watchtower_core.validation.errors",
}

_REPO_OPS_EXPORTS = {
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
            "watchtower_core.validation does not export repo-wide aggregate validation "
            "helpers. Import from watchtower_core.repo_ops.validation or from "
            "watchtower_core.validation.all for the compatibility wrapper."
        )
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(import_module(module_name), name)
