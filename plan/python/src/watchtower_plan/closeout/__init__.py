"""Plan-domain closeout services and initiative-package helpers."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "CloseoutArtifactDocument",
    "InitiativeCloseoutResult",
    "InitiativeCloseoutService",
    "InitiativePackageCloseoutHelper",
    "InitiativePackageCloseoutPlan",
    "TERMINAL_INITIATIVE_PACKAGE_STATUSES",
]

_EXPORT_MODULES = {
    "CloseoutArtifactDocument": "watchtower_plan.closeout.initiative_package",
    "InitiativeCloseoutResult": "watchtower_plan.closeout.initiative",
    "InitiativeCloseoutService": "watchtower_plan.closeout.initiative",
    "InitiativePackageCloseoutHelper": "watchtower_plan.closeout.initiative_package",
    "InitiativePackageCloseoutPlan": "watchtower_plan.closeout.initiative_package",
    "TERMINAL_INITIATIVE_PACKAGE_STATUSES": "watchtower_plan.closeout.initiative_package",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
