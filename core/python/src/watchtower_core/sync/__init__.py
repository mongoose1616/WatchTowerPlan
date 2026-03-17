"""Public sync namespace for export-safe generic harness surfaces."""

from __future__ import annotations

from watchtower_core.sync.harness import (
    SyncHarness,
    SyncRecord,
    SyncResult,
    SyncTargetSpec,
)

__all__ = ["SyncHarness", "SyncRecord", "SyncResult", "SyncTargetSpec"]


def __getattr__(name: str) -> object:
    raise AttributeError(
        "watchtower_core.sync exports only generic sync harness surfaces. "
        "Repo-specific sync services still live under watchtower_core.repo_ops.sync."
    )
