"""Validation services and result models for governed artifacts."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "AcceptanceReconciliationService",
    "ArtifactValidationService",
    "DocumentSemanticsValidationService",
    "FrontMatterValidationService",
    "ValidationAllRecord",
    "ValidationAllResult",
    "ValidationAllService",
    "VALIDATION_FAMILY_SPECS",
    "ValidationExecutionError",
    "ValidationFamilySpec",
    "ValidationFamilySummary",
    "ValidationIssue",
    "ValidationResult",
    "ValidationSelectionError",
]

_EXPORT_MODULES = {
    "AcceptanceReconciliationService": "watchtower_core.validation.acceptance",
    "ArtifactValidationService": "watchtower_core.validation.artifact",
    "DocumentSemanticsValidationService": "watchtower_core.validation.document_semantics",
    "FrontMatterValidationService": "watchtower_core.validation.front_matter",
    "ValidationAllRecord": "watchtower_core.validation.all",
    "ValidationAllResult": "watchtower_core.validation.all",
    "ValidationAllService": "watchtower_core.validation.all",
    "VALIDATION_FAMILY_SPECS": "watchtower_core.validation.registry",
    "ValidationExecutionError": "watchtower_core.validation.errors",
    "ValidationFamilySpec": "watchtower_core.validation.registry",
    "ValidationFamilySummary": "watchtower_core.validation.all",
    "ValidationIssue": "watchtower_core.validation.models",
    "ValidationResult": "watchtower_core.validation.models",
    "ValidationSelectionError": "watchtower_core.validation.errors",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(import_module(module_name), name)
