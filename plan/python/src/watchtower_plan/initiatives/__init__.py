"""Feature-owned initiative services for the plan pack."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "DeferredItemSpec",
    "InitiativeBootstrapParams",
    "InitiativePackageResult",
    "InitiativePackageService",
    "InitiativeReadinessResult",
    "InitiativeTaskSpec",
    "InitiativeTerminalCloseoutResult",
]

_EXPORT_MODULES = {
    "DeferredItemSpec": "watchtower_plan.initiatives.models",
    "InitiativeBootstrapParams": "watchtower_plan.initiatives.models",
    "InitiativePackageResult": "watchtower_plan.initiatives.models",
    "InitiativePackageService": "watchtower_plan.initiatives.service",
    "InitiativeReadinessResult": "watchtower_plan.initiatives.models",
    "InitiativeTaskSpec": "watchtower_plan.initiatives.models",
    "InitiativeTerminalCloseoutResult": "watchtower_plan.initiatives.models",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
