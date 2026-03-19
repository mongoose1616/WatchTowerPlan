"""Shared serializers for live initiative rendered payloads."""

from __future__ import annotations

from watchtower_core.control_plane.models import InitiativeActiveTaskSummary, InitiativeIndexEntry
from watchtower_core.plan_runtime.planning_rendered_serialization_helpers import (
    _assign_scalar,
    _assign_sequence,
    _assign_serialized_collection,
)


def serialize_active_task_summary(
    task: InitiativeActiveTaskSummary,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "task_id": task.task_id,
        "title": task.title,
        "task_status": task.task_status,
        "priority": task.priority,
        "owner": task.owner,
        "doc_path": task.doc_path,
        "is_actionable": task.is_actionable,
    }
    _assign_sequence(payload, "blocked_by", task.blocked_by, compact=compact)
    _assign_sequence(payload, "depends_on", task.depends_on, compact=compact)
    return payload


def serialize_initiative_entry(
    entry: InitiativeIndexEntry,
    *,
    compact: bool,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "trace_id": entry.trace_id,
        "title": entry.title,
        "summary": entry.summary,
        "artifact_status": entry.artifact_status,
        "initiative_status": entry.initiative_status,
        "current_phase": entry.current_phase,
        "updated_at": entry.updated_at,
        "open_task_count": entry.open_task_count,
        "blocked_task_count": entry.blocked_task_count,
        "key_surface_path": entry.key_surface_path,
        "next_action": entry.next_action,
        "next_surface_path": entry.next_surface_path,
    }
    _assign_scalar(payload, "initiative_id", entry.initiative_id, compact=compact)
    _assign_scalar(payload, "slug", entry.slug, compact=compact)
    _assign_scalar(payload, "scope_type", entry.scope_type, compact=compact)
    _assign_scalar(payload, "project_id", entry.project_id, compact=compact)
    _assign_scalar(payload, "primary_owner", entry.primary_owner, compact=compact)
    _assign_sequence(payload, "active_owners", entry.active_owners, compact=compact)
    _assign_sequence(payload, "active_task_ids", entry.active_task_ids, compact=compact)
    _assign_serialized_collection(
        payload,
        "active_task_summaries",
        entry.active_task_summaries,
        compact=compact,
        serializer=lambda task: serialize_active_task_summary(task, compact=compact),
    )
    _assign_sequence(
        payload,
        "blocked_by_task_ids",
        entry.blocked_by_task_ids,
        compact=compact,
    )
    _assign_sequence(
        payload,
        "source_surface_paths",
        entry.source_surface_paths,
        compact=compact,
    )
    _assign_sequence(payload, "task_ids", entry.task_ids, compact=compact)
    _assign_sequence(payload, "acceptance_ids", entry.acceptance_ids, compact=compact)
    _assign_sequence(
        payload,
        "acceptance_contract_ids",
        entry.acceptance_contract_ids,
        compact=compact,
    )
    _assign_sequence(payload, "evidence_ids", entry.evidence_ids, compact=compact)
    _assign_scalar(payload, "closed_at", entry.closed_at, compact=compact)
    _assign_scalar(payload, "closure_reason", entry.closure_reason, compact=compact)
    _assign_scalar(
        payload,
        "superseded_by_trace_id",
        entry.superseded_by_trace_id,
        compact=compact,
    )
    _assign_sequence(payload, "related_paths", entry.related_paths, compact=compact)
    _assign_sequence(payload, "tags", entry.tags, compact=compact)
    _assign_scalar(payload, "notes", entry.notes, compact=compact)
    return payload
