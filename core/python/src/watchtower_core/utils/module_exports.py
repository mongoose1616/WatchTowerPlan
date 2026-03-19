"""Shared package-root export helpers for lazy imports and fail-closed guards."""

from __future__ import annotations

from collections.abc import Mapping
from importlib import import_module
from typing import Any


def fail_closed_package_getattr(message: str) -> Any:
    """Return one module-level ``__getattr__`` that always fails closed."""

    def _getattr(name: str) -> Any:
        raise AttributeError(message)

    return _getattr


def lazy_module_getattr(
    *,
    module_name: str,
    export_modules: Mapping[str, str],
    blocked_messages: Mapping[str, str] | None = None,
) -> Any:
    """Return one module-level ``__getattr__`` over a lazy export map."""

    blocked = blocked_messages or {}

    def _getattr(name: str) -> Any:
        message = blocked.get(name)
        if message is not None:
            raise AttributeError(message)
        target_module = export_modules.get(name)
        if target_module is None:
            raise AttributeError(f"module {module_name!r} has no attribute {name!r}")
        return getattr(import_module(target_module), name)

    return _getattr
