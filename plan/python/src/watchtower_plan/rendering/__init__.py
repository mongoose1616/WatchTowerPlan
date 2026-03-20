"""Feature-owned rendering helpers for live plan surfaces."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "serialize_active_task_summary",
    "serialize_initiative_entry",
]

_EXPORT_MODULES = {
    "serialize_active_task_summary": "watchtower_plan.rendering.serialization",
    "serialize_initiative_entry": "watchtower_plan.rendering.serialization",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
