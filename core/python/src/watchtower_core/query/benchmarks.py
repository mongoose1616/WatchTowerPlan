"""Reusable query helpers for retained benchmark record artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import BenchmarkRecordArtifact


@dataclass(frozen=True, slots=True)
class BenchmarkRecordSearchParams:
    """Search filters for retained benchmark records."""

    record_id: str | None = None
    suite_id: str | None = None
    limit: int | None = None


class BenchmarkRecordQueryService:
    """Search retained benchmark record artifacts."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(
        self,
        params: BenchmarkRecordSearchParams,
    ) -> tuple[BenchmarkRecordArtifact, ...]:
        """Return matching benchmark records."""

        results: list[BenchmarkRecordArtifact] = []
        for artifact in self._loader.load_benchmark_record_artifacts():
            if params.record_id is not None and artifact.record_id != params.record_id:
                continue
            if params.suite_id is not None and artifact.suite_id != params.suite_id:
                continue
            results.append(artifact)
        results.sort(key=lambda artifact: (artifact.recorded_at, artifact.record_id), reverse=True)
        if params.limit is not None:
            results = results[: params.limit]
        return tuple(results)


__all__ = ["BenchmarkRecordQueryService", "BenchmarkRecordSearchParams"]
