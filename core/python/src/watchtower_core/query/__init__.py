"""Public query namespace for export-safe surfaces."""

from __future__ import annotations

__all__: list[str] = []


def __getattr__(name: str) -> object:
    raise AttributeError(
        "watchtower_core.query does not export repo-specific query services. "
        "Import from watchtower_core.repo_ops.query or from an explicit "
        "watchtower_core.query.<module> compatibility wrapper instead."
    )
