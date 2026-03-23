"""Public sync namespace for export-safe generic harness surfaces."""

from __future__ import annotations

from watchtower_core.sync.harness import (
    SyncHarness,
    SyncRecord,
    SyncResult,
    SyncTargetSpec,
)
from watchtower_core.utils.module_exports import fail_closed_package_getattr

__all__ = ["SyncHarness", "SyncRecord", "SyncResult", "SyncTargetSpec"]

__getattr__ = fail_closed_package_getattr(
    "watchtower_core.sync exports only the generic sync harness from the package root. "
    "Repo-shared sync services live under explicit watchtower_core.sync.* modules, and "
    "pack-local orchestration remains under the owning watchtower_<pack>.sync package."
)
