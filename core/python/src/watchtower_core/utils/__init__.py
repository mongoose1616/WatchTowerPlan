"""Narrow shared helpers for the core Python package."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "GitHygieneRequest",
    "GitHygieneResult",
    "GitHygieneService",
    "utc_timestamp_now",
]

_EXPORT_MODULES = {
    "GitHygieneRequest": "watchtower_core.utils.git_hygiene",
    "GitHygieneResult": "watchtower_core.utils.git_hygiene",
    "GitHygieneService": "watchtower_core.utils.git_hygiene",
    "utc_timestamp_now": "watchtower_core.utils.timestamps",
}

__getattr__ = lazy_module_getattr(module_name=__name__, export_modules=_EXPORT_MODULES)
