"""Internal helper functions for workspace indexing and rendering."""

from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import InitiativeActiveTaskSummary
from watchtower_core.control_plane.terminology import TerminologyHelper
from watchtower_plan.workspace.constants import (
    PHASE_ORDER,
    PLAN_PACK_SETTINGS_PATH,
    PRIORITY_ORDER,
    TERMINAL_TASK_STATUSES,
)
from watchtower_plan.workspace.models import PlanReadinessIndexEntry


def task_status_for_id(
    task_documents: tuple[dict[str, object], ...],
    task_id: str,
) -> str | None:
    for task_document in task_documents:
        if task_document["task_id"] == task_id:
            return str(task_document["task_status"])
    return None


def initiative_status(
    document: dict[str, object],
    vocabulary: TerminologyHelper,
) -> str:
    lifecycle_stage = str(document["lifecycle_stage"])
    if vocabulary.is_terminal_lifecycle(lifecycle_stage):
        return lifecycle_stage
    return "active"


def current_phase_for_lifecycle(
    lifecycle_stage: str,
    vocabulary: TerminologyHelper,
) -> str:
    return vocabulary.current_phase_for_lifecycle(lifecycle_stage)


def current_phase_for_snapshot(
    initiative: dict[str, object],
    active_task_summaries: tuple[InitiativeActiveTaskSummary, ...],
    vocabulary: TerminologyHelper,
) -> str:
    lifecycle_stage = str(initiative["lifecycle_stage"])
    if (
        not active_task_summaries
        and initiative.get("status") == "active"
        and not vocabulary.is_terminal_lifecycle(lifecycle_stage)
    ):
        return "closeout"
    return current_phase_for_lifecycle(lifecycle_stage, vocabulary)


def next_action(
    snapshot: Any,
    readiness: PlanReadinessIndexEntry,
    vocabulary: TerminologyHelper,
) -> str:
    lifecycle_stage = str(snapshot.initiative_document["lifecycle_stage"])
    active_task_statuses = {
        str(task_document["task_status"])
        for task_document in snapshot.task_documents
        if str(task_document["task_status"]) not in TERMINAL_TASK_STATUSES
    }
    if vocabulary.is_terminal_lifecycle(lifecycle_stage):
        return f"No further default action. Initiative is {lifecycle_stage}."
    if readiness.blocking_reasons:
        return "Resolve blocking reasons and rebuild derived surfaces before execution."
    if not active_task_statuses:
        return "Finalize closeout, evidence, and promotion decisions."
    if snapshot.initiative_document["lifecycle_stage"] == "closing":
        return "Finalize closeout, evidence, and promotion decisions."
    if (
        not vocabulary.allows_execution(readiness.review_status)
        and not readiness.ready_for_execution
    ):
        return "Review and approve the initiative package for execution."
    if readiness.ready_for_execution:
        if "ready" in active_task_statuses:
            return "Start the highest-priority ready task from the initiative package."
        if "in_progress" in active_task_statuses:
            return (
                "Advance the current in-progress task set and keep initiative-local task "
                "state current."
            )
        if "in_review" in active_task_statuses:
            return "Close the current in-review task set before opening follow-up work."
        if "blocked" in active_task_statuses:
            return "Resolve blocked task dependencies before opening follow-up work."
        if "planned" in active_task_statuses:
            return (
                "Promote the next planned task to ready before opening follow-up work."
            )
    return "Keep initiative-local task state current before opening follow-up work."


def next_surface_path(
    snapshot: Any,
    readiness: PlanReadinessIndexEntry,
) -> str:
    if str(snapshot.initiative_document["lifecycle_stage"]) in {
        "completed",
        "superseded",
        "cancelled",
    }:
        return f"{snapshot.initiative_root}/summary.md"
    if readiness.blocking_reasons:
        return f"{snapshot.initiative_root}/progress.md"
    if not any(
        str(task_document["task_status"]) not in TERMINAL_TASK_STATUSES
        for task_document in snapshot.task_documents
    ):
        return f"{snapshot.initiative_root}/summary.md"
    if snapshot.initiative_document["lifecycle_stage"] == "closing":
        return f"{snapshot.initiative_root}/summary.md"
    if readiness.ready_for_execution:
        return f"{snapshot.initiative_root}/plan.md"
    return f"{snapshot.initiative_root}/progress.md"


@lru_cache(maxsize=1)
def plan_terminology() -> TerminologyHelper:
    """Return one cached terminology helper for module-level query helpers."""

    return TerminologyHelper.from_loader(
        ControlPlaneLoader(),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def task_status_order(task_status: str) -> int:
    """Return the stable sort order for plan task index statuses."""

    return plan_terminology().task_status_order(task_status)


def plan_markdown_issue_summary(issue_code: str, relative_path: str) -> str:
    if issue_code == "missing_expected_content":
        return f"Required rendered surface is missing from the expected build: {relative_path}."
    if issue_code == "missing_output":
        return f"Required rendered surface is missing: {relative_path}."
    return f"Rendered surface drift detected for {relative_path}."


def json_document(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return value


def markdown_content(value: object) -> str:
    assert isinstance(value, str)
    return value


def ordered_unique_strings(values: Iterable[object]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value)
        if text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return tuple(ordered)


def joined_or_dash(values: object) -> str:
    if not isinstance(values, Iterable) or isinstance(values, (str, bytes)):
        return "-"
    items = [str(value) for value in values if str(value)]
    return ", ".join(items) if items else "-"


__all__ = [
    "PHASE_ORDER",
    "PRIORITY_ORDER",
    "TERMINAL_TASK_STATUSES",
    "current_phase_for_lifecycle",
    "current_phase_for_snapshot",
    "initiative_status",
    "joined_or_dash",
    "json_document",
    "markdown_content",
    "next_action",
    "next_surface_path",
    "ordered_unique_strings",
    "plan_markdown_issue_summary",
    "task_status_for_id",
    "task_status_order",
]
