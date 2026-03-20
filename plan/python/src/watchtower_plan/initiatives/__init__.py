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
    "DeferredItemSpec": "watchtower_plan.initiatives.service",
    "InitiativeBootstrapParams": "watchtower_plan.initiatives.service",
    "InitiativePackageResult": "watchtower_plan.initiatives.service",
    "InitiativePackageService": "watchtower_plan.initiatives.service",
    "InitiativeReadinessResult": "watchtower_plan.initiatives.service",
    "InitiativeTaskSpec": "watchtower_plan.initiatives.service",
    "InitiativeTerminalCloseoutResult": "watchtower_plan.initiatives.service",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
