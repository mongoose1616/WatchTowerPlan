"""Feature-owned guidance promotion services for the plan pack."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "GuidancePromotionOutput",
    "GuidancePromotionResult",
    "GuidancePromotionService",
    "build_guidance_front_matter",
    "default_mirror_target_paths",
    "default_target_family_for_source_kind",
    "default_target_path",
    "extract_markdown_summary",
    "extract_markdown_title",
    "guidance_id_for_target_path",
    "guidance_summary",
    "guidance_title",
    "guidance_trace_id_for_target_path",
    "readable_source_artifact_kind",
    "render_guidance_body",
    "source_artifact_kind_for_path",
]

_EXPORT_MODULES = {
    "GuidancePromotionOutput": "watchtower_plan.promotion.models",
    "GuidancePromotionResult": "watchtower_plan.promotion.models",
    "GuidancePromotionService": "watchtower_plan.promotion.service",
    "build_guidance_front_matter": "watchtower_plan.promotion.rendering",
    "default_mirror_target_paths": "watchtower_plan.promotion.targets",
    "default_target_family_for_source_kind": "watchtower_plan.promotion.targets",
    "default_target_path": "watchtower_plan.promotion.targets",
    "extract_markdown_summary": "watchtower_plan.promotion.rendering",
    "extract_markdown_title": "watchtower_plan.promotion.rendering",
    "guidance_id_for_target_path": "watchtower_plan.promotion.targets",
    "guidance_summary": "watchtower_plan.promotion.rendering",
    "guidance_title": "watchtower_plan.promotion.rendering",
    "guidance_trace_id_for_target_path": "watchtower_plan.promotion.targets",
    "readable_source_artifact_kind": "watchtower_plan.promotion.rendering",
    "render_guidance_body": "watchtower_plan.promotion.rendering",
    "source_artifact_kind_for_path": "watchtower_plan.promotion.targets",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
