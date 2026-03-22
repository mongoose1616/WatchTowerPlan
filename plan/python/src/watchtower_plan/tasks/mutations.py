"""Task lifecycle mutation and event helpers."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.event_stream import (
    EventStreamDescriptor,
    EventStreamHelper,
    EventStreamWriteRequest,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.tasks.state import (
    PlanInitiativeState,
    load_task_documents_by_id,
    task_event_directory,
)
from watchtower_plan.tasks.validation import (
    initiative_execution_started,
    initiative_state_relative_path,
    reload_initiative_state,
)
from watchtower_plan.workspace.service import PLAN_PACK_SETTINGS_PATH

_LIVE_TASK_ARTIFACT_STATUS = "active"
_EXECUTION_START_TASK_STATUSES = frozenset({"in_progress", "in_review", "completed"})
_IMMUTABLE_INITIATIVE_LIFECYCLE_STAGES = frozenset(
    {"closing", "completed", "superseded", "cancelled"}
)


def closeout_recommended(
    loader: ControlPlaneLoader,
    *,
    task_id: str,
    trace_id: str,
    candidate_status: str,
) -> bool:
    if candidate_status not in {"completed", "cancelled"}:
        return False
    for document in load_task_documents_by_id(loader).values():
        if document.trace_id != trace_id:
            continue
        effective_status = (
            candidate_status if document.task_id == task_id else document.task_status
        )
        if effective_status not in {"completed", "cancelled"}:
            return False
    return True


def load_task_document_payload(
    loader: ControlPlaneLoader,
    relative_path: str,
) -> dict[str, object]:
    return loader.derive(
        active_pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    ).load_validated_document(relative_path)


def task_document(
    *,
    task_id: str,
    slug: str,
    initiative_id: str,
    title: str,
    summary: str,
    task_status: str,
    task_kind: str,
    priority: str,
    owner: str,
    created_at: str,
    updated_at: str,
    depends_on: tuple[str, ...],
    blocked_by: tuple[str, ...],
    related_ids: tuple[str, ...],
    applies_to: tuple[str, ...],
    scope_items: tuple[str, ...],
    done_when_items: tuple[str, ...],
) -> dict[str, object]:
    document: dict[str, object] = {
        "$schema": "urn:watchtower:schema:artifacts:plan:task-state:v1",
        "task_id": task_id,
        "slug": slug,
        "initiative_id": initiative_id,
        "title": title,
        "summary": summary,
        "status": _LIVE_TASK_ARTIFACT_STATUS,
        "task_status": task_status,
        "task_kind": task_kind,
        "priority": priority,
        "owner": owner,
        "created_at": created_at,
        "updated_at": updated_at,
    }
    if depends_on:
        document["dependency_task_ids"] = list(depends_on)
    if blocked_by:
        document["blocker_task_ids"] = list(blocked_by)
    if related_ids:
        document["related_ids"] = list(related_ids)
    if applies_to:
        document["applies_to"] = list(applies_to)
    if scope_items:
        document["scope_items"] = list(scope_items)
    if done_when_items:
        document["done_when_items"] = list(done_when_items)
    return document


def update_initiative_state_for_task(
    loader: ControlPlaneLoader,
    initiative: PlanInitiativeState,
    *,
    task_id: str,
    updated_at: str,
) -> None:
    initiative_document = dict(reload_initiative_state(loader, initiative).document)
    task_id_values = initiative_document.get("task_ids", ())
    task_ids = (
        [str(value) for value in task_id_values]
        if isinstance(task_id_values, list)
        else []
    )
    if task_id not in task_ids:
        task_ids.append(task_id)
        task_ids.sort()
        initiative_document["task_ids"] = task_ids
    initiative_document["updated_at"] = updated_at
    loader.artifact_store.write_json_object(
        f"{initiative.relative_root}/.wt/initiative.json",
        initiative_document,
    )


def touch_initiative_state(
    loader: ControlPlaneLoader,
    initiative: PlanInitiativeState,
    *,
    updated_at: str,
) -> None:
    initiative_document = dict(reload_initiative_state(loader, initiative).document)
    initiative_document["updated_at"] = updated_at
    loader.artifact_store.write_json_object(
        f"{initiative.relative_root}/.wt/initiative.json",
        initiative_document,
    )


def append_task_event(
    loader: ControlPlaneLoader,
    *,
    initiative: PlanInitiativeState,
    task_id: str,
    task_slug: str,
    event_type: str,
    recorded_at: str,
    summary: str,
    payload: dict[str, object],
) -> None:
    helper = EventStreamHelper.from_loader(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )
    helper.append_event(
        EventStreamDescriptor.task(
            relative_dir=task_event_directory(
                f"{initiative.relative_root}/.wt/tasks/{task_slug}/task.json"
            ),
            event_id_prefix=f"event.{Path(initiative.relative_root).name}.{task_slug}",
            initiative_id=initiative.initiative_id,
            task_id=task_id,
        ),
        EventStreamWriteRequest(
            event_type=event_type,
            actor_id="actor.watchtower_core",
            recorded_at=recorded_at,
            summary=summary,
            payload=payload,
        ),
    )


def mark_initiative_execution_started(
    loader: ControlPlaneLoader,
    *,
    initiative: PlanInitiativeState,
    task_id: str,
    task_status: str,
    updated_at: str,
    task_doc_path: str,
) -> None:
    if task_status not in _EXECUTION_START_TASK_STATUSES:
        return

    initiative = reload_initiative_state(loader, initiative)
    initiative_relative_path = initiative_state_relative_path(initiative)
    initiative_document = dict(initiative.document)
    execution_started = initiative_execution_started(loader, initiative)
    changed = False
    if not execution_started:
        helper = EventStreamHelper.from_loader(
            loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        helper.append_event(
            EventStreamDescriptor.initiative(
                relative_dir=f"{initiative.relative_root}/.wt/events",
                event_id_prefix=f"event.{Path(initiative.relative_root).name}",
                initiative_id=initiative.initiative_id,
                trace_id=initiative.trace_id,
            ),
            EventStreamWriteRequest(
                event_type="execution_started",
                actor_id="actor.watchtower_core",
                recorded_at=updated_at,
                summary=(
                    f"Execution started after task {task_id} entered {task_status}."
                ),
                payload={
                    "task_id": task_id,
                    "task_status": task_status,
                },
                related_paths=(task_doc_path,),
            ),
        )
        changed = True

    lifecycle_stage = str(
        initiative_document.get("lifecycle_stage", "capture_incomplete")
    )
    if lifecycle_stage not in {
        "in_progress",
        *tuple(_IMMUTABLE_INITIATIVE_LIFECYCLE_STAGES),
    }:
        initiative_document["lifecycle_stage"] = "in_progress"
        changed = True

    if changed:
        initiative_document["updated_at"] = updated_at
        loader.artifact_store.write_json_object(
            initiative_relative_path,
            initiative_document,
        )
