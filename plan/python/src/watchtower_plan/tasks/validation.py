"""Task lifecycle validation and gating helpers."""

from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.terminology import TerminologyHelper
from watchtower_plan.tasks.models import TaskUpdateParams
from watchtower_plan.tasks.state import (
    PlanInitiativeState,
    find_initiative_by_slug,
    find_initiative_by_trace_id,
)
from watchtower_plan.tasks.support import normalize_list, normalize_required_string
from watchtower_plan.workspace.service import PLAN_PACK_SETTINGS_PATH

_EXECUTION_START_TASK_STATUSES = frozenset({"in_progress", "in_review", "completed"})
_IMMUTABLE_INITIATIVE_LIFECYCLE_STAGES = frozenset(
    {"closing", "completed", "superseded", "cancelled"}
)


def canonical_task_status(helper: TerminologyHelper, value: str) -> str:
    return helper.canonical_value(
        "plan_task_status",
        normalize_required_string(value, label="task_status"),
    )


def required_items(values: tuple[str, ...], *, label: str) -> tuple[str, ...]:
    normalized = normalize_list(values)
    if not normalized:
        raise ValueError(f"{label} requires at least one non-empty item.")
    return normalized


def resolve_initiative_state(
    loader: ControlPlaneLoader,
    *,
    task_id: str,
    trace_id: str | None,
) -> PlanInitiativeState:
    if trace_id is not None:
        return find_initiative_by_trace_id(
            loader,
            normalize_required_string(trace_id, label="trace_id"),
        )
    initiative_slug = task_id_initiative_slug(task_id)
    if initiative_slug is None:
        raise ValueError(
            "Live task creation requires --trace-id when task_id does not identify an initiative."
        )
    return find_initiative_by_slug(loader, initiative_slug)


def task_id_initiative_slug(task_id: str) -> str | None:
    parts = task_id.split(".")
    if len(parts) < 3 or parts[0] != "task":
        return None
    return parts[1]


def require_mutable_initiative(
    loader: ControlPlaneLoader,
    initiative: PlanInitiativeState,
) -> None:
    initiative = reload_initiative_state(loader, initiative)
    if str(initiative.document.get("status", "active")) != "active":
        raise ValueError(
            f"Live task mutation requires an active initiative package: {initiative.trace_id}"
        )
    lifecycle_stage = str(
        initiative.document.get("lifecycle_stage", "capture_incomplete")
    )
    if lifecycle_stage in _IMMUTABLE_INITIATIVE_LIFECYCLE_STAGES:
        raise ValueError(
            "Live task mutation requires a non-terminal initiative package: "
            f"{initiative.trace_id} is {lifecycle_stage}."
        )


def require_execution_ready_initiative(
    loader: ControlPlaneLoader,
    *,
    initiative: PlanInitiativeState,
    task_status: str,
) -> None:
    if task_status not in _EXECUTION_START_TASK_STATUSES:
        return

    initiative = reload_initiative_state(loader, initiative)
    gate_state = initiative.document.get("gate_state")
    approval_status = (
        str(gate_state.get("approval_status"))
        if isinstance(gate_state, dict)
        and gate_state.get("approval_status") is not None
        else "pending"
    )
    ready_for_execution = (
        bool(gate_state.get("ready_for_execution"))
        if isinstance(gate_state, dict)
        else False
    )
    lifecycle_stage = str(
        initiative.document.get("lifecycle_stage", "capture_incomplete")
    )
    if approval_status == "approved" and (
        initiative_execution_started(loader, initiative)
        or lifecycle_stage == "in_progress"
        or (ready_for_execution and lifecycle_stage == "ready_for_execution")
    ):
        return

    raise ValueError(
        "Task status "
        f"{task_status} requires initiative {initiative.trace_id} to be approved and "
        "marked ready_for_execution before execution starts."
    )


def validate_task_references(
    *,
    task_id: str,
    depends_on: tuple[str, ...],
    blocked_by: tuple[str, ...],
    existing_task_ids: set[str],
) -> None:
    for key, values in (("depends_on", depends_on), ("blocked_by", blocked_by)):
        for value in values:
            if value == task_id:
                raise ValueError(f"{key} cannot reference the current task: {task_id}")
            if value not in existing_task_ids:
                raise ValueError(f"{key} references unknown task ID: {value}")


def validate_trace_linkage(
    *,
    trace_id: str,
    related_ids: tuple[str, ...],
    relative_path: str,
) -> None:
    traced_related_ids = tuple(
        value for value in related_ids if value.startswith("trace.")
    )
    if traced_related_ids and trace_id not in traced_related_ids:
        joined = ", ".join(traced_related_ids)
        raise ValueError(
            f"{relative_path} trace_id {trace_id} must match one of its traced related_ids: "
            f"{joined}."
        )


def validate_update_flags(params: TaskUpdateParams) -> None:
    reject_conflicting_clear(
        params.trace_id is not None, params.clear_trace_id, key="trace_id"
    )
    reject_conflicting_clear(
        params.applies_to is not None,
        params.clear_applies_to,
        key="applies_to",
    )
    reject_conflicting_clear(
        params.related_ids is not None,
        params.clear_related_ids,
        key="related_ids",
    )
    reject_conflicting_clear(
        params.depends_on is not None,
        params.clear_depends_on,
        key="depends_on",
    )
    reject_conflicting_clear(
        params.blocked_by is not None,
        params.clear_blocked_by,
        key="blocked_by",
    )


def initiative_execution_started(
    loader: ControlPlaneLoader,
    initiative: PlanInitiativeState,
) -> bool:
    events_root = loader.repo_root / initiative.relative_root / ".wt" / "events"
    if not events_root.exists():
        return False
    for path in sorted(events_root.glob("*.json")):
        document = loader.load_json_object(str(path.relative_to(loader.repo_root)))
        if str(document.get("event_type")) == "execution_started":
            return True
    return False


def reload_initiative_state(
    loader: ControlPlaneLoader,
    initiative: PlanInitiativeState,
) -> PlanInitiativeState:
    relative_path = initiative_state_relative_path(initiative)
    document = loader.derive(
        active_pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    ).load_validated_document(relative_path)
    return PlanInitiativeState(
        relative_root=initiative.relative_root,
        document=document,
    )


def initiative_state_relative_path(initiative: PlanInitiativeState) -> str:
    return f"{initiative.relative_root}/.wt/initiative.json"


def reject_conflicting_clear(has_values: bool, clear: bool, *, key: str) -> None:
    if has_values and clear:
        raise ValueError(
            f"Cannot provide replacement values and clear {key} in the same call."
        )
