"""Repo-shared governed-document helper package."""

from __future__ import annotations

from watchtower_core.utils.module_exports import fail_closed_package_getattr

__all__: list[str] = []

__getattr__ = fail_closed_package_getattr(
    "watchtower_core.documentation does not export a package-root wildcard surface. "
    "Import explicit documentation helper modules instead."
)
