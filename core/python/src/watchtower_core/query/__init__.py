"""Public query namespace for export-safe surfaces."""

from __future__ import annotations

__all__: list[str] = []


def __getattr__(name: str) -> object:
    raise AttributeError(
        "watchtower_core.query is a guardrail namespace root and does not export "
        "repo-specific query services. Import from watchtower_core.repo_ops.query."
    )
