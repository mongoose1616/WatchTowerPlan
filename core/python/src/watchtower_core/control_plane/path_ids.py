"""Canonical plan-workspace path and identifier helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

PlanScopeType = Literal["pack_wide", "project_scoped"]

_SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True, slots=True)
class PlanInitiativeLocation:
    """Resolved plan-workspace initiative placement for one scope root."""

    initiative_slug: str
    initiative_root_relative: str
    scope_type: PlanScopeType
    project_slug: str | None = None
    project_id: str | None = None

    @property
    def discrepancy_namespace(self) -> str:
        """Return the canonical discrepancy namespace for this initiative."""

        if self.project_slug is None:
            return self.initiative_slug
        return f"{self.project_slug}.{self.initiative_slug}"

    def relative_path(self, suffix: str) -> str:
        """Return one path beneath this initiative root."""

        return PlanPathIdHelper.join_relative(self.initiative_root_relative, suffix)


class PlanPathIdHelper:
    """Centralized plan-workspace slug, identifier, and root-path helpers."""

    @classmethod
    def slugify(cls, value: str, *, label: str = "value") -> str:
        """Return one canonical snake_case slug."""

        normalized = _SLUG_PATTERN.sub("_", value.strip().casefold()).strip("_")
        if not normalized:
            raise ValueError(f"{label} resolved to an empty canonical slug.")
        return normalized

    @classmethod
    def normalize_slug(cls, value: str, *, label: str = "slug") -> str:
        """Validate that one slug already uses the canonical snake_case form."""

        candidate = value.strip()
        if not candidate:
            raise ValueError(f"{label} must be a non-empty string.")
        normalized = cls.slugify(candidate, label=label)
        if candidate != normalized:
            raise ValueError(f"{label} must already use canonical snake_case.")
        return candidate

    @classmethod
    def trace_suffix(cls, trace_id: str) -> str:
        """Return the canonical slug suffix for one trace identifier."""

        normalized = trace_id.strip()
        if not normalized:
            raise ValueError("trace_id must be a non-empty string.")
        if not normalized.startswith("trace."):
            raise ValueError("trace_id must use the canonical trace.<slug> form.")
        suffix = normalized.removeprefix("trace.")
        if not suffix:
            raise ValueError("trace_id must include a suffix after trace.")
        return cls.normalize_slug(suffix, label="trace_id suffix")

    @classmethod
    def initiative_slug(
        cls,
        *,
        trace_id: str,
        initiative_slug: str | None = None,
    ) -> str:
        """Return the canonical initiative slug for one trace."""

        trace_slug = cls.trace_suffix(trace_id)
        if initiative_slug is None:
            return trace_slug
        normalized = cls.normalize_slug(initiative_slug, label="initiative_slug")
        if normalized != trace_slug:
            raise ValueError("initiative_slug must match the trace stem derived from trace_id.")
        return normalized

    @classmethod
    def canonical_initiative_id(cls, initiative_slug: str) -> str:
        """Return the canonical initiative identifier for one initiative slug."""

        return cls._canonical_prefixed_id(
            "initiative",
            cls.normalize_slug(initiative_slug, label="initiative_slug"),
        )

    @classmethod
    def canonical_project_id(cls, project_slug: str) -> str:
        """Return the canonical project identifier for one project slug."""

        return cls._canonical_prefixed_id(
            "project",
            cls.normalize_slug(project_slug, label="project_slug"),
        )

    @classmethod
    def canonical_repository_id(cls, project_slug: str, repository_role: str) -> str:
        """Return the canonical repository identifier for one project-role pair."""

        return cls._canonical_prefixed_id(
            "repository",
            cls.normalize_slug(project_slug, label="project_slug"),
            cls.normalize_slug(repository_role, label="repository_role"),
        )

    @classmethod
    def canonical_task_id(cls, initiative_slug: str, task_slug: str) -> str:
        """Return the canonical task identifier for one initiative-local task."""

        return cls._canonical_prefixed_id(
            "task",
            cls.normalize_slug(initiative_slug, label="initiative_slug"),
            cls.normalize_slug(task_slug, label="task_slug"),
        )

    @classmethod
    def canonical_deferred_item_id(cls, initiative_slug: str, deferred_slug: str) -> str:
        """Return the canonical deferred-item identifier for one initiative-local record."""

        return cls._canonical_prefixed_id(
            "deferred",
            cls.normalize_slug(initiative_slug, label="initiative_slug"),
            cls.normalize_slug(deferred_slug, label="deferred_slug"),
        )

    @classmethod
    def canonical_acceptance_id(cls, initiative_slug: str, acceptance_slug: str) -> str:
        """Return the canonical acceptance identifier for one initiative-local contract."""

        return cls._canonical_prefixed_id(
            "acceptance",
            cls.normalize_slug(initiative_slug, label="initiative_slug"),
            cls.normalize_slug(acceptance_slug, label="acceptance_slug"),
        )

    @classmethod
    def canonical_evidence_id(cls, initiative_slug: str, evidence_slug: str) -> str:
        """Return the canonical evidence identifier for one initiative-local bundle."""

        return cls._canonical_prefixed_id(
            "evidence",
            cls.normalize_slug(initiative_slug, label="initiative_slug"),
            cls.normalize_slug(evidence_slug, label="evidence_slug"),
        )

    @classmethod
    def canonical_closeout_id(cls, initiative_slug: str, closeout_slug: str) -> str:
        """Return the canonical closeout identifier for one initiative-local recap."""

        return cls._canonical_prefixed_id(
            "closeout",
            cls.normalize_slug(initiative_slug, label="initiative_slug"),
            cls.normalize_slug(closeout_slug, label="closeout_slug"),
        )

    @classmethod
    def canonical_promotion_id(cls, initiative_slug: str, promotion_slug: str) -> str:
        """Return the canonical promotion identifier for one initiative-local record."""

        return cls._canonical_prefixed_id(
            "promotion",
            cls.normalize_slug(initiative_slug, label="initiative_slug"),
            cls.normalize_slug(promotion_slug, label="promotion_slug"),
        )

    @classmethod
    def canonical_entry_id(cls, initiative_slug: str, entry_slug: str) -> str:
        """Return the canonical entry identifier for one initiative-local companion entry."""

        return cls._canonical_prefixed_id(
            "entry",
            cls.normalize_slug(initiative_slug, label="initiative_slug"),
            cls.normalize_slug(entry_slug, label="entry_slug"),
        )

    @classmethod
    def packwide_initiative_location(
        cls,
        *,
        trace_id: str | None = None,
        initiative_slug: str | None = None,
    ) -> PlanInitiativeLocation:
        """Return the canonical pack-wide initiative location."""

        slug = cls._resolve_initiative_slug(trace_id=trace_id, initiative_slug=initiative_slug)
        return PlanInitiativeLocation(
            initiative_slug=slug,
            initiative_root_relative=f"plan/initiatives/{slug}",
            scope_type="pack_wide",
        )

    @classmethod
    def project_scoped_initiative_location(
        cls,
        project_slug: str,
        *,
        trace_id: str | None = None,
        initiative_slug: str | None = None,
    ) -> PlanInitiativeLocation:
        """Return the canonical project-scoped initiative location."""

        normalized_project_slug = cls.normalize_slug(project_slug, label="project_slug")
        slug = cls._resolve_initiative_slug(trace_id=trace_id, initiative_slug=initiative_slug)
        return PlanInitiativeLocation(
            initiative_slug=slug,
            initiative_root_relative=(
                f"{cls.project_initiatives_root_relative(normalized_project_slug)}/{slug}"
            ),
            scope_type="project_scoped",
            project_slug=normalized_project_slug,
            project_id=cls.canonical_project_id(normalized_project_slug),
        )

    @classmethod
    def project_root_relative(cls, project_slug: str) -> str:
        """Return the canonical relative root for one project container."""

        normalized = cls.normalize_slug(project_slug, label="project_slug")
        return f"plan/projects/{normalized}"

    @classmethod
    def project_machine_root_relative(cls, project_slug: str) -> str:
        """Return the canonical machine root for one project container."""

        return cls.join_relative(cls.project_root_relative(project_slug), ".wt")

    @classmethod
    def project_initiatives_root_relative(cls, project_slug: str) -> str:
        """Return the canonical initiatives root for one project container."""

        return cls.join_relative(cls.project_root_relative(project_slug), "initiatives")

    @staticmethod
    def join_relative(root: str, suffix: str) -> str:
        """Join one repository-relative root with a relative suffix."""

        normalized_root = root.strip().strip("/")
        normalized_suffix = suffix.strip().strip("/")
        if not normalized_suffix:
            return normalized_root
        return f"{normalized_root}/{normalized_suffix}"

    @classmethod
    def _resolve_initiative_slug(
        cls,
        *,
        trace_id: str | None,
        initiative_slug: str | None,
    ) -> str:
        if trace_id is not None:
            return cls.initiative_slug(trace_id=trace_id, initiative_slug=initiative_slug)
        if initiative_slug is None:
            raise ValueError("trace_id or initiative_slug is required.")
        return cls.normalize_slug(initiative_slug, label="initiative_slug")

    @staticmethod
    def _canonical_prefixed_id(prefix: str, *components: str) -> str:
        return ".".join((prefix, *components))


__all__ = ["PlanInitiativeLocation", "PlanPathIdHelper"]
