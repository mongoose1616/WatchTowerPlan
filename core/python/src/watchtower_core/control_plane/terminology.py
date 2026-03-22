"""Helpers for pack-local terminology lookup, alias resolution, and deprecation awareness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    LifecycleStageEntry,
    LifecycleStageRegistry,
    ReviewStatusEntry,
    ReviewStatusRegistry,
    SourceTypeEntry,
    SourceTypeRegistry,
)

TerminologyMatchKind = Literal["canonical", "alias", "deprecated_alias"]


@dataclass(frozen=True, slots=True)
class TerminologyTerm:
    """One canonical terminology term plus its known aliases."""

    namespace: str
    canonical_value: str
    summary: str
    aliases: tuple[str, ...] = ()
    deprecated_aliases: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TerminologyResolution:
    """Resolved terminology result for one requested value."""

    namespace: str
    requested_value: str
    matched_value: str
    match_kind: TerminologyMatchKind
    term: TerminologyTerm

    @property
    def canonical_value(self) -> str:
        """Return the canonical value for the matched term."""

        return self.term.canonical_value

    @property
    def deprecated(self) -> bool:
        """Return whether the requested value matched a deprecated alias."""

        return self.match_kind == "deprecated_alias"


_PLAN_TASK_STATUS_TERMS = (
    TerminologyTerm(
        namespace="plan_task_status",
        canonical_value="planned",
        summary="The initiative-local task is captured but not yet execution-ready.",
    ),
    TerminologyTerm(
        namespace="plan_task_status",
        canonical_value="ready",
        summary="The initiative-local task is ready for execution.",
    ),
    TerminologyTerm(
        namespace="plan_task_status",
        canonical_value="in_progress",
        summary="The initiative-local task is actively executing.",
    ),
    TerminologyTerm(
        namespace="plan_task_status",
        canonical_value="in_review",
        summary="The initiative-local task is waiting on review or approval.",
    ),
    TerminologyTerm(
        namespace="plan_task_status",
        canonical_value="blocked",
        summary="The initiative-local task is blocked until a dependency is cleared.",
    ),
    TerminologyTerm(
        namespace="plan_task_status",
        canonical_value="completed",
        summary="The initiative-local task reached its intended outcome.",
    ),
    TerminologyTerm(
        namespace="plan_task_status",
        canonical_value="cancelled",
        summary="The initiative-local task ended before completing its intended outcome.",
    ),
)
_PLAN_TASK_STATUS_SURFACE_VALUES = {
    "planned": "planned",
    "ready": "ready",
    "in_progress": "in_progress",
    "in_review": "in_review",
    "blocked": "blocked",
    "completed": "completed",
    "cancelled": "cancelled",
}
_PLAN_TASK_STATUS_ORDER = {
    "ready": 0,
    "in_progress": 1,
    "in_review": 2,
    "planned": 3,
    "blocked": 4,
    "completed": 5,
    "cancelled": 6,
}


class TerminologyHelper:
    """Resolve governed pack-local terminology through one reusable helper."""

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
        self._terms_by_namespace = {
            "lifecycle_stage": tuple(
                TerminologyTerm(
                    namespace="lifecycle_stage",
                    canonical_value=entry.value,
                    summary=entry.summary,
                )
                for entry in lifecycle_stage_registry.entries
            ),
            "review_status": tuple(
                TerminologyTerm(
                    namespace="review_status",
                    canonical_value=entry.value,
                    summary=entry.summary,
                )
                for entry in review_status_registry.entries
            ),
            "source_type": tuple(
                TerminologyTerm(
                    namespace="source_type",
                    canonical_value=entry.value,
                    summary=entry.summary,
                )
                for entry in source_type_registry.entries
            ),
            "plan_task_status": _PLAN_TASK_STATUS_TERMS,
        }

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> TerminologyHelper:
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
            raise ValueError("Active pack settings do not declare a typed review_status_registry.")
        if not isinstance(source_registry, SourceTypeRegistry):
            raise ValueError("Active pack settings do not declare a typed source_type_registry.")
        return cls(
            lifecycle_stage_registry=lifecycle_registry,
            review_status_registry=review_registry,
            source_type_registry=source_registry,
        )

    def resolve(self, namespace: str, value: str) -> TerminologyResolution:
        """Resolve one term by namespace and value, including aliases."""

        for term in self._terms(namespace):
            if value == term.canonical_value:
                return TerminologyResolution(
                    namespace=namespace,
                    requested_value=value,
                    matched_value=value,
                    match_kind="canonical",
                    term=term,
                )
            if value in term.aliases:
                return TerminologyResolution(
                    namespace=namespace,
                    requested_value=value,
                    matched_value=value,
                    match_kind="alias",
                    term=term,
                )
            if value in term.deprecated_aliases:
                return TerminologyResolution(
                    namespace=namespace,
                    requested_value=value,
                    matched_value=value,
                    match_kind="deprecated_alias",
                    term=term,
                )
        raise KeyError(f"{namespace}:{value}")

    def canonical_value(self, namespace: str, value: str) -> str:
        """Return the canonical value for one term."""

        return self.resolve(namespace, value).canonical_value

    def term(self, namespace: str, canonical_value: str) -> TerminologyTerm:
        """Return one canonical term definition."""

        resolved = self.resolve(namespace, canonical_value)
        if resolved.match_kind != "canonical":
            raise KeyError(f"{namespace}:{canonical_value}")
        return resolved.term

    def lifecycle_stage(self, value: str) -> LifecycleStageEntry:
        """Return one lifecycle-stage entry by value."""

        return self._lifecycle_stage_registry.get(self.canonical_value("lifecycle_stage", value))

    def review_status(self, value: str) -> ReviewStatusEntry:
        """Return one review-status entry by value."""

        return self._review_status_registry.get(self.canonical_value("review_status", value))

    def source_type(self, value: str) -> SourceTypeEntry:
        """Return one source-type entry by value."""

        return self._source_type_registry.get(self.canonical_value("source_type", value))

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

    def surface_task_status(self, task_status: str) -> str:
        """Return the current derived-surface spelling for one plan task status."""

        canonical = self.canonical_value("plan_task_status", task_status)
        return _PLAN_TASK_STATUS_SURFACE_VALUES[canonical]

    def task_status_order(self, task_status: str) -> int:
        """Return the stable sort order for one plan task status."""

        canonical = self.canonical_value("plan_task_status", task_status)
        return _PLAN_TASK_STATUS_ORDER.get(canonical, 99)

    def _terms(self, namespace: str) -> tuple[TerminologyTerm, ...]:
        terms = self._terms_by_namespace.get(namespace)
        if terms is None:
            raise KeyError(namespace)
        return terms


class PlanningVocabularyHelper(TerminologyHelper):
    """Backward-compatible alias for callers that still import the older helper name."""


__all__ = [
    "PlanningVocabularyHelper",
    "TerminologyHelper",
    "TerminologyResolution",
    "TerminologyTerm",
]
