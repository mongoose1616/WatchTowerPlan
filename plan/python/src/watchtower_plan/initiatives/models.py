"""Public models for plan initiative package bootstrap and lifecycle flows."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.validation import ValidationResult


@dataclass(frozen=True, slots=True)
class InitiativeTaskSpec:
    """Bootstrap-time specification for one initiative-local task."""

    title: str
    summary: str
    slug: str | None = None
    task_id: str | None = None
    task_kind: str = "feature"
    priority: str = "high"
    owner: str = "repository_maintainer"
    depends_on: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    governing_document_paths: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DeferredItemSpec:
    """Bootstrap-time specification for one initiative-local deferred item."""

    category: str
    summary: str
    reason: str
    resolution_trigger: str
    blocks_ready_for_execution: bool = False
    slug: str | None = None
    deferred_item_id: str | None = None
    owner: str = "repository_maintainer"
    related_task_id: str | None = None


@dataclass(frozen=True, slots=True)
class InitiativeBootstrapParams:
    """Inputs for one pack-wide or project-scoped initiative package bootstrap."""

    trace_id: str
    title: str
    summary: str
    task_specs: tuple[InitiativeTaskSpec, ...]
    initiative_slug: str | None = None
    initiative_id: str | None = None
    owner: str = "repository_maintainer"
    deferred_items: tuple[DeferredItemSpec, ...] = ()
    include_decision_notes: bool = False
    governing_document_paths: tuple[str, ...] = ()
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class InitiativeReadinessResult:
    """Structured validation result for one initiative package."""

    initiative_id: str
    trace_id: str
    initiative_root: str
    passed: bool
    lifecycle_stage: str
    issue_messages: tuple[str, ...]
    artifact_results: tuple[ValidationResult, ...]
    open_discrepancy_ids: tuple[str, ...]
    blocking_reasons: tuple[str, ...]
    wrote: bool


@dataclass(frozen=True, slots=True)
class InitiativePackageResult:
    """Output summary for one initiative package mutation."""

    initiative_id: str
    trace_id: str
    initiative_root: str
    lifecycle_stage: str
    review_status: str
    ready_for_execution: bool
    validation_passed: bool
    wrote: bool


@dataclass(frozen=True, slots=True)
class InitiativeTerminalCloseoutResult:
    """Output summary for one terminal live-initiative closeout mutation."""

    initiative_id: str
    trace_id: str
    initiative_root: str
    initiative_status: str
    closed_at: str
    closure_reason: str
    scope_type: str
    superseded_by_trace_id: str | None
    wrote: bool


__all__ = [
    "DeferredItemSpec",
    "InitiativeBootstrapParams",
    "InitiativePackageResult",
    "InitiativeReadinessResult",
    "InitiativeTaskSpec",
    "InitiativeTerminalCloseoutResult",
]
