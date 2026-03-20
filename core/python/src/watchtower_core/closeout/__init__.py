"""Fail-closed boundary guard for moved plan-domain closeout services."""

from __future__ import annotations

from watchtower_core.utils.module_exports import fail_closed_package_getattr

__all__: list[str] = []

__getattr__ = fail_closed_package_getattr(
    "watchtower_core.closeout exposes no supported imports. "
    "Import repo-local closeout services from watchtower_plan.closeout."
)
