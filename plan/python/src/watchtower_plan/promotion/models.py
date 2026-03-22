"""Public promotion result models."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.models import ExtractionOutputEnvelopeArtifact


@dataclass(frozen=True, slots=True)
class GuidancePromotionOutput:
    """One promoted guidance output emitted from an initiative-local candidate."""

    source_path: str
    source_artifact_kind: str
    target_family: str
    target_path: str
    guidance_id: str
    mirror_target_paths: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class GuidancePromotionResult:
    """Promotion result for one initiative-local promotion record."""

    promotion_id: str
    initiative_id: str
    trace_id: str
    status: str
    updated_at: str
    wrote: bool
    outputs: tuple[GuidancePromotionOutput, ...]
    extraction_envelopes: tuple[ExtractionOutputEnvelopeArtifact, ...] = ()
