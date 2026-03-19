"""Closeout helpers for traced initiatives and future release/report workflows."""

__all__ = [
    "CloseoutArtifactDocument",
    "InitiativeCloseoutResult",
    "InitiativeCloseoutService",
    "InitiativePackageCloseoutHelper",
    "InitiativePackageCloseoutPlan",
    "TERMINAL_INITIATIVE_PACKAGE_STATUSES",
    "TracePurgeResult",
    "TracePurgeService",
]


def __getattr__(name: str) -> object:
    if name in {
        "InitiativeCloseoutResult",
        "InitiativeCloseoutService",
    }:
        from watchtower_core.closeout.initiative import (
            InitiativeCloseoutResult,
            InitiativeCloseoutService,
        )

        return {
            "InitiativeCloseoutResult": InitiativeCloseoutResult,
            "InitiativeCloseoutService": InitiativeCloseoutService,
        }[name]
    if name in {
        "CloseoutArtifactDocument",
        "InitiativePackageCloseoutHelper",
        "InitiativePackageCloseoutPlan",
        "TERMINAL_INITIATIVE_PACKAGE_STATUSES",
    }:
        from watchtower_core.closeout.initiative_package import (
            TERMINAL_INITIATIVE_PACKAGE_STATUSES,
            CloseoutArtifactDocument,
            InitiativePackageCloseoutHelper,
            InitiativePackageCloseoutPlan,
        )

        return {
            "CloseoutArtifactDocument": CloseoutArtifactDocument,
            "InitiativePackageCloseoutHelper": InitiativePackageCloseoutHelper,
            "InitiativePackageCloseoutPlan": InitiativePackageCloseoutPlan,
            "TERMINAL_INITIATIVE_PACKAGE_STATUSES": TERMINAL_INITIATIVE_PACKAGE_STATUSES,
        }[name]
    if name in {"TracePurgeResult", "TracePurgeService"}:
        from watchtower_core.closeout.purge_trace import TracePurgeResult, TracePurgeService

        return {
            "TracePurgeResult": TracePurgeResult,
            "TracePurgeService": TracePurgeService,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
