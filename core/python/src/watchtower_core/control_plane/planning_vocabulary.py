"""Helpers for plan-runtime lifecycle, review, and provenance vocabulary resolution."""

from __future__ import annotations

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    LifecycleStageEntry,
    LifecycleStageRegistry,
    ReviewStatusEntry,
    ReviewStatusRegistry,
    SourceTypeEntry,
    SourceTypeRegistry,
)


class PlanningVocabularyHelper:
    """Resolve governed lifecycle, review, and provenance vocabulary for the plan pack."""

    def __init__(
        self,
        *,
        lifecycle_stage_registry: LifecycleStageRegistry,
        review_status_registry: ReviewStatusRegistry,
        source_type_registry: SourceTypeRegistry,
    ) -> None:
        self._lifecycle_stage_registry = lifecycle_stage_registry
        self._review_status_registry = review_status_registry
        self._source_type_registry = source_type_registry

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> PlanningVocabularyHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        lifecycle_registry = context.registries.get("lifecycle_stage_registry")
        review_registry = context.registries.get("review_status_registry")
        source_registry = context.registries.get("source_type_registry")
        if not isinstance(lifecycle_registry, LifecycleStageRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed lifecycle_stage_registry."
            )
        if not isinstance(review_registry, ReviewStatusRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed review_status_registry."
            )
        if not isinstance(source_registry, SourceTypeRegistry):
            raise ValueError("Active pack settings do not declare a typed source_type_registry.")
        return cls(
            lifecycle_stage_registry=lifecycle_registry,
            review_status_registry=review_registry,
            source_type_registry=source_registry,
        )

    def lifecycle_stage(self, value: str) -> LifecycleStageEntry:
        """Return one lifecycle-stage entry by value."""

        return self._lifecycle_stage_registry.get(value)

    def review_status(self, value: str) -> ReviewStatusEntry:
        """Return one review-status entry by value."""

        return self._review_status_registry.get(value)

    def source_type(self, value: str) -> SourceTypeEntry:
        """Return one source-type entry by value."""

        return self._source_type_registry.get(value)

    def current_phase_for_lifecycle(self, lifecycle_stage: str) -> str:
        """Return the rendered/query phase that corresponds to one lifecycle stage."""

        return self.lifecycle_stage(lifecycle_stage).current_phase

    def is_terminal_lifecycle(self, lifecycle_stage: str) -> bool:
        """Return whether one lifecycle stage is terminal."""

        return self.lifecycle_stage(lifecycle_stage).terminal

    def allows_execution(self, review_status: str) -> bool:
        """Return whether one review status allows execution to proceed."""

        return self.review_status(review_status).allows_execution

    def source_class_for(self, source_type: str) -> str:
        """Return the broad provenance class for one source-type value."""

        return self.source_type(source_type).source_class


__all__ = ["PlanningVocabularyHelper"]
