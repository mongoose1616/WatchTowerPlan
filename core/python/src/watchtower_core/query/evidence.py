"""Query helpers for governed validation-evidence artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ValidationEvidenceArtifact


@dataclass(frozen=True, slots=True)
class ValidationEvidenceSearchParams:
    """Search filters for validation-evidence lookups."""

    trace_id: str | None = None
    overall_result: str | None = None
    acceptance_id: str | None = None
    validator_id: str | None = None


class ValidationEvidenceQueryService:
    """Search governed validation-evidence artifacts."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(
        self,
        params: ValidationEvidenceSearchParams,
    ) -> tuple[ValidationEvidenceArtifact, ...]:
        """Return matching validation-evidence artifacts."""
        results: list[ValidationEvidenceArtifact] = []
        for artifact in self._loader.load_validation_evidence_artifacts():
            if params.trace_id is not None and artifact.trace_id != params.trace_id:
                continue
            if (
                params.overall_result is not None
                and artifact.overall_result != params.overall_result
            ):
                continue
            if params.acceptance_id is not None and not any(
                params.acceptance_id in check.acceptance_ids for check in artifact.checks
            ):
                continue
            if params.validator_id is not None and not any(
                check.validator_id == params.validator_id for check in artifact.checks
            ):
                continue
            results.append(artifact)
        return tuple(results)
