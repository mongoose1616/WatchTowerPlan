"""Validation services and result models for governed artifacts."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

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

_PLAN_DOMAIN_EXPORTS = {
    "DocumentSemanticsValidationService",
}
_SUBMODULE_ONLY_EXPORTS = {
    "ValidationAllRecord": "watchtower_core.validation.all",
    "ValidationAllResult": "watchtower_core.validation.all",
    "ValidationAllService": "watchtower_core.validation.all",
    "ValidationFamilySummary": "watchtower_core.validation.all",
    "VALIDATION_ALL_FAMILIES": "watchtower_core.validation.all",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
    blocked_messages=(
        dict.fromkeys(
            _PLAN_DOMAIN_EXPORTS,
            "watchtower_core.validation exposes only reusable validation services. "
            "Import repo-local document semantics from watchtower_plan.validation.",
        )
        | dict.fromkeys(
            _SUBMODULE_ONLY_EXPORTS,
            "watchtower_core.validation keeps aggregate validate-all helpers out of the "
            "package root. Import them from watchtower_core.validation.all.",
        )
    ),
)
