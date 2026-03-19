"""Structured lifecycle helpers for initiative-local live task state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.event_stream import (
    EventStreamDescriptor,
    EventStreamHelper,
    EventStreamWriteRequest,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.terminology import TerminologyHelper
from watchtower_core.plan_runtime.front_matter_paths import (
    normalize_governed_applies_to_values,
)
from watchtower_core.plan_runtime.plan_task_state import (
    PlanInitiativeState,
    find_initiative_by_slug,
    find_initiative_by_trace_id,
    load_task_documents_by_id,
    task_event_directory,
    write_task_document,
)
from watchtower_core.plan_runtime.plan_workspace import (
    PLAN_PACK_SETTINGS_PATH,
    PlanWorkspaceService,
)
from watchtower_core.plan_runtime.sync.coordination import CoordinationSyncService
from watchtower_core.plan_runtime.task_lifecycle_support import (
    TASK_KIND_CHOICES,
    TASK_PRIORITY_CHOICES,
    apply_optional_list_field,
    normalize_choice,
    normalize_list,
    normalize_required_string,
    pick_choice,
    pick_string,
    slugify_file_stem,
)
from watchtower_core.plan_runtime.task_lifecycle_support import (
    TASK_STATUS_CHOICES as _TASK_STATUS_CHOICES,
)
from watchtower_core.utils import utc_timestamp_now

_LIVE_TASK_ARTIFACT_STATUS = "active"
_EXECUTION_START_TASK_STATUSES = frozenset({"in_progress", "in_review", "completed"})
_IMMUTABLE_INITIATIVE_LIFECYCLE_STAGES = frozenset(
    {"closing", "completed", "superseded", "cancelled"}
)
TASK_STATUS_CHOICES = _TASK_STATUS_CHOICES


@dataclass(frozen=True, slots=True)
class TaskCreateParams:
    """Inputs for one task creation operation."""

    task_id: str
    title: str
    summary: str
    task_kind: str
    priority: str
    owner: str
    scope_items: tuple[str, ...]
    done_when_items: tuple[str, ...]
    task_status: str = "planned"
    trace_id: str | None = None
    applies_to: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()
    file_stem: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class TaskUpdateParams:
    """Inputs for one task update operation."""

    task_id: str
    title: str | None = None
    summary: str | None = None
    task_kind: str | None = None
    priority: str | None = None
    owner: str | None = None
    task_status: str | None = None
    trace_id: str | None = None
    clear_trace_id: bool = False
    scope_items: tuple[str, ...] | None = None
    done_when_items: tuple[str, ...] | None = None
    applies_to: tuple[str, ...] | None = None
    clear_applies_to: bool = False
    related_ids: tuple[str, ...] | None = None
    clear_related_ids: bool = False
    depends_on: tuple[str, ...] | None = None
    clear_depends_on: bool = False
    blocked_by: tuple[str, ...] | None = None
    clear_blocked_by: bool = False
    file_stem: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class TaskTransitionParams:
    """Inputs for one task handoff or phase-transition operation."""

    task_id: str
    task_status: str
    next_owner: str | None = None
    depends_on: tuple[str, ...] | None = None
    clear_depends_on: bool = False
    blocked_by: tuple[str, ...] | None = None
    clear_blocked_by: bool = False
    file_stem: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class TaskMutationResult:
    """Result summary for one task lifecycle command."""

    task_id: str
    title: str
    summary: str
    trace_id: str | None
    task_status: str
    task_kind: str
    priority: str
    owner: str
    updated_at: str
    doc_path: str
    previous_doc_path: str | None
    moved: bool
    changed: bool
    wrote: bool
    coordination_refreshed: bool
    closeout_recommended: bool


class TaskLifecycleService:
    """Create, update, and transition initiative-local live task state."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._terminology = TerminologyHelper.from_loader(
            loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def create(self, params: TaskCreateParams, *, write: bool) -> TaskMutationResult:
        existing_documents = load_task_documents_by_id(self._loader)
        task_id = normalize_required_string(params.task_id, label="task_id")
        if task_id in existing_documents:
            raise ValueError(f"Task ID already exists: {task_id}")

        initiative = _resolve_initiative_state(
            self._loader,
            task_id=task_id,
            trace_id=params.trace_id,
        )
        _require_mutable_initiative(initiative)

        updated_at = params.updated_at or utc_timestamp_now()
        task_status = _canonical_task_status(self._terminology, params.task_status)
        _require_execution_ready_initiative(
            self._loader,
            initiative=initiative,
            task_status=task_status,
        )
        task_kind = normalize_choice(params.task_kind, TASK_KIND_CHOICES, label="task_kind")
        priority = normalize_choice(params.priority, TASK_PRIORITY_CHOICES, label="priority")
        title = normalize_required_string(params.title, label="title")
        summary = normalize_required_string(params.summary, label="summary")
        owner = normalize_required_string(params.owner, label="owner")
        slug = slugify_file_stem(params.file_stem or title)
        relative_path = f"{initiative.relative_root}/.wt/tasks/{slug}/task.json"
        if (self._loader.repo_root / relative_path).exists():
            raise ValueError(f"Task document path already exists: {relative_path}")

        scope_items = _required_items(params.scope_items, label="scope")
        done_when_items = _required_items(params.done_when_items, label="done-when")
        applies_to = normalize_governed_applies_to_values(
            params.applies_to,
            origin=f"task create {task_id} applies_to",
            repo_root=self._loader.repo_root,
        )
        related_ids = normalize_list(params.related_ids)
        depends_on = normalize_list(params.depends_on)
        blocked_by = normalize_list(params.blocked_by)
        _validate_task_references(
            task_id=task_id,
            depends_on=depends_on,
            blocked_by=blocked_by,
            existing_task_ids=set(existing_documents),
        )
        _validate_trace_linkage(
            trace_id=initiative.trace_id,
            related_ids=related_ids,
            relative_path=relative_path,
        )

        document = _task_document(
            task_id=task_id,
            slug=slug,
            initiative_id=initiative.initiative_id,
            title=title,
            summary=summary,
            task_status=task_status,
            task_kind=task_kind,
            priority=priority,
            owner=owner,
            created_at=updated_at,
            updated_at=updated_at,
            depends_on=depends_on,
            blocked_by=blocked_by,
            related_ids=related_ids,
            applies_to=applies_to,
            scope_items=scope_items,
            done_when_items=done_when_items,
        )

        if write:
            write_task_document(self._loader, relative_path, document)
            _update_initiative_state_for_task(
                self._loader,
                initiative,
                task_id=task_id,
                updated_at=updated_at,
            )
            _append_task_event(
                self._loader,
                initiative=initiative,
                task_id=task_id,
                task_slug=slug,
                event_type="created",
                recorded_at=updated_at,
                summary=f"Created live task {task_id}.",
                payload={
                    "status": _LIVE_TASK_ARTIFACT_STATUS,
                    "task_status": task_status,
                    "owner": owner,
                    "doc_path": relative_path,
                },
            )
            _mark_initiative_execution_started(
                self._loader,
                initiative=initiative,
                task_id=task_id,
                task_status=task_status,
                updated_at=updated_at,
                task_doc_path=relative_path,
            )
            PlanWorkspaceService(self._loader).sync(write=True)
            CoordinationSyncService(self._loader).run(write=True)

        return TaskMutationResult(
            task_id=task_id,
            title=title,
            summary=summary,
            trace_id=initiative.trace_id,
            task_status=task_status,
            task_kind=task_kind,
            priority=priority,
            owner=owner,
            updated_at=updated_at,
            doc_path=relative_path,
            previous_doc_path=None,
            moved=False,
            changed=True,
            wrote=write,
            coordination_refreshed=write,
            closeout_recommended=_closeout_recommended(
                self._loader,
                task_id=task_id,
                trace_id=initiative.trace_id,
                candidate_status=task_status,
            ),
        )

    def update(self, params: TaskUpdateParams, *, write: bool) -> TaskMutationResult:
        _validate_update_flags(params)
        task_id = normalize_required_string(params.task_id, label="task_id")
        documents = load_task_documents_by_id(self._loader)
        try:
            document = documents[task_id]
        except KeyError as exc:
            raise ValueError(f"Unknown task ID: {task_id}") from exc

        initiative = find_initiative_by_trace_id(self._loader, document.trace_id)
        _require_mutable_initiative(initiative)
        if params.clear_trace_id:
            raise ValueError(
                "Live initiative-local tasks inherit trace_id from the initiative package and "
                "cannot clear it."
            )
        if params.trace_id is not None:
            requested_trace_id = normalize_required_string(params.trace_id, label="trace_id")
            if requested_trace_id != document.trace_id:
                raise ValueError(
                    "Live initiative-local tasks inherit trace_id from the initiative package and "
                    "cannot move between traces."
                )
        if params.file_stem is not None and slugify_file_stem(params.file_stem) != document.slug:
            raise ValueError(
                "file_stem renames are not supported for live initiative-local task state."
            )

        task_document = _load_task_document_payload(self._loader, document.relative_path)
        changed = False

        title = pick_string(params.title, current=document.title, label="title")
        if title != document.title:
            task_document["title"] = title
            changed = True

        summary = pick_string(params.summary, current=document.summary, label="summary")
        if summary != document.summary:
            task_document["summary"] = summary
            changed = True

        task_kind = pick_choice(
            params.task_kind,
            current=document.task_kind,
            allowed=TASK_KIND_CHOICES,
            label="task_kind",
        )
        if task_kind != document.task_kind:
            task_document["task_kind"] = task_kind
            changed = True

        priority = pick_choice(
            params.priority,
            current=document.priority,
            allowed=TASK_PRIORITY_CHOICES,
            label="priority",
        )
        if priority != document.priority:
            task_document["priority"] = priority
            changed = True

        owner = pick_string(params.owner, current=document.owner, label="owner")
        if owner != document.owner:
            task_document["owner"] = owner
            changed = True

        task_status = (
            _canonical_task_status(self._terminology, params.task_status)
            if params.task_status is not None
            else document.task_status
        )
        _require_execution_ready_initiative(
            self._loader,
            initiative=initiative,
            task_status=task_status,
        )
        if task_status != document.task_status:
            task_document["task_status"] = task_status
            changed = True

        applies_to = (
            normalize_governed_applies_to_values(
                params.applies_to,
                origin=f"task update {document.task_id} applies_to",
                repo_root=self._loader.repo_root,
            )
            if params.applies_to is not None
            else None
        )
        changed |= apply_optional_list_field(
            task_document,
            "applies_to",
            values=applies_to,
            clear=params.clear_applies_to,
        )
        changed |= apply_optional_list_field(
            task_document,
            "related_ids",
            values=params.related_ids,
            clear=params.clear_related_ids,
        )
        changed |= apply_optional_list_field(
            task_document,
            "dependency_task_ids",
            values=params.depends_on,
            clear=params.clear_depends_on,
        )
        changed |= apply_optional_list_field(
            task_document,
            "blocker_task_ids",
            values=params.blocked_by,
            clear=params.clear_blocked_by,
        )

        if params.scope_items is not None:
            normalized_scope_items = _required_items(params.scope_items, label="scope")
            if tuple(task_document.get("scope_items", ())) != normalized_scope_items:
                task_document["scope_items"] = list(normalized_scope_items)
                changed = True
        if params.done_when_items is not None:
            normalized_done_when_items = _required_items(
                params.done_when_items,
                label="done-when",
            )
            if tuple(task_document.get("done_when_items", ())) != normalized_done_when_items:
                task_document["done_when_items"] = list(normalized_done_when_items)
                changed = True

        _validate_task_references(
            task_id=document.task_id,
            depends_on=tuple(task_document.get("dependency_task_ids", ())),
            blocked_by=tuple(task_document.get("blocker_task_ids", ())),
            existing_task_ids=set(documents),
        )
        _validate_trace_linkage(
            trace_id=document.trace_id,
            related_ids=tuple(str(value) for value in task_document.get("related_ids", ())),
            relative_path=document.relative_path,
        )

        updated_at = (
            params.updated_at
            or (utc_timestamp_now() if changed else document.updated_at)
        )
        if updated_at != document.updated_at:
            task_document["updated_at"] = updated_at
            changed = True

        if write and changed:
            write_task_document(self._loader, document.relative_path, task_document)
            _touch_initiative_state(self._loader, initiative, updated_at=updated_at)
            _append_task_event(
                self._loader,
                initiative=initiative,
                task_id=document.task_id,
                task_slug=document.slug,
                event_type=(
                    "status_changed" if task_status != document.task_status else "updated"
                ),
                recorded_at=updated_at,
                summary=(
                    f"Updated live task {document.task_id}."
                    if task_status == document.task_status
                    else (
                        f"Changed {document.task_id} status from {document.task_status} "
                        f"to {task_status}."
                    )
                ),
                payload={
                    "status": _LIVE_TASK_ARTIFACT_STATUS,
                    "task_status": task_status,
                    "owner": owner,
                    "doc_path": document.relative_path,
                },
            )
            _mark_initiative_execution_started(
                self._loader,
                initiative=initiative,
                task_id=document.task_id,
                task_status=task_status,
                updated_at=updated_at,
                task_doc_path=document.relative_path,
            )
            PlanWorkspaceService(self._loader).sync(write=True)
            CoordinationSyncService(self._loader).run(write=True)

        return TaskMutationResult(
            task_id=document.task_id,
            title=str(task_document["title"]),
            summary=str(task_document["summary"]),
            trace_id=document.trace_id,
            task_status=str(task_document["task_status"]),
            task_kind=str(task_document["task_kind"]),
            priority=str(task_document["priority"]),
            owner=str(task_document["owner"]),
            updated_at=str(task_document["updated_at"]),
            doc_path=document.relative_path,
            previous_doc_path=None,
            moved=False,
            changed=changed,
            wrote=bool(write and changed),
            coordination_refreshed=bool(write and changed),
            closeout_recommended=_closeout_recommended(
                self._loader,
                task_id=document.task_id,
                trace_id=document.trace_id,
                candidate_status=str(task_document["task_status"]),
            ),
        )

    def transition(self, params: TaskTransitionParams, *, write: bool) -> TaskMutationResult:
        return self.update(
            TaskUpdateParams(
                task_id=params.task_id,
                task_status=params.task_status,
                owner=params.next_owner,
                depends_on=params.depends_on,
                clear_depends_on=params.clear_depends_on,
                blocked_by=params.blocked_by,
                clear_blocked_by=params.clear_blocked_by,
                file_stem=params.file_stem,
                updated_at=params.updated_at,
            ),
            write=write,
        )


def _canonical_task_status(helper: TerminologyHelper, value: str) -> str:
    return helper.canonical_value(
        "plan_task_status",
        normalize_required_string(value, label="task_status"),
    )


def _closeout_recommended(
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
        effective_status = candidate_status if document.task_id == task_id else document.task_status
        if effective_status not in {"completed", "cancelled"}:
            return False
    return True


def _load_task_document_payload(
    loader: ControlPlaneLoader,
    relative_path: str,
) -> dict[str, object]:
    return loader.derive(
        active_pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    ).load_validated_document(relative_path)


def _required_items(values: tuple[str, ...], *, label: str) -> tuple[str, ...]:
    normalized = normalize_list(values)
    if not normalized:
        raise ValueError(f"{label} requires at least one non-empty item.")
    return normalized


def _resolve_initiative_state(
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
    initiative_slug = _task_id_initiative_slug(task_id)
    if initiative_slug is None:
        raise ValueError(
            "Live task creation requires --trace-id when task_id does not identify an initiative."
        )
    return find_initiative_by_slug(loader, initiative_slug)


def _task_id_initiative_slug(task_id: str) -> str | None:
    parts = task_id.split(".")
    if len(parts) < 3 or parts[0] != "task":
        return None
    return parts[1]


def _require_mutable_initiative(initiative: PlanInitiativeState) -> None:
    if str(initiative.document.get("status", "active")) != "active":
        raise ValueError(
            f"Live task mutation requires an active initiative package: {initiative.trace_id}"
        )
    lifecycle_stage = str(initiative.document.get("lifecycle_stage", "capture_incomplete"))
    if lifecycle_stage in _IMMUTABLE_INITIATIVE_LIFECYCLE_STAGES:
        raise ValueError(
            "Live task mutation requires a non-terminal initiative package: "
            f"{initiative.trace_id} is {lifecycle_stage}."
        )


def _require_execution_ready_initiative(
    loader: ControlPlaneLoader,
    *,
    initiative: PlanInitiativeState,
    task_status: str,
) -> None:
    if task_status not in _EXECUTION_START_TASK_STATUSES:
        return

    gate_state = initiative.document.get("gate_state")
    approval_status = (
        str(gate_state.get("approval_status"))
        if isinstance(gate_state, dict) and gate_state.get("approval_status") is not None
        else "pending"
    )
    ready_for_execution = (
        bool(gate_state.get("ready_for_execution"))
        if isinstance(gate_state, dict)
        else False
    )
    lifecycle_stage = str(initiative.document.get("lifecycle_stage", "capture_incomplete"))
    if approval_status == "approved" and (
        _initiative_execution_started(loader, initiative)
        or lifecycle_stage == "in_progress"
        or (ready_for_execution and lifecycle_stage == "ready_for_execution")
    ):
        return

    raise ValueError(
        "Task status "
        f"{task_status} requires initiative {initiative.trace_id} to be approved and "
        "marked ready_for_execution before execution starts."
    )


def _validate_task_references(
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


def _validate_trace_linkage(
    *,
    trace_id: str,
    related_ids: tuple[str, ...],
    relative_path: str,
) -> None:
    traced_related_ids = tuple(value for value in related_ids if value.startswith("trace."))
    if traced_related_ids and trace_id not in traced_related_ids:
        joined = ", ".join(traced_related_ids)
        raise ValueError(
            f"{relative_path} trace_id {trace_id} must match one of its traced related_ids: "
            f"{joined}."
        )


def _task_document(
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


def _update_initiative_state_for_task(
    loader: ControlPlaneLoader,
    initiative: PlanInitiativeState,
    *,
    task_id: str,
    updated_at: str,
) -> None:
    initiative_document = dict(initiative.document)
    task_ids = [str(value) for value in initiative_document.get("task_ids", ())]
    if task_id not in task_ids:
        task_ids.append(task_id)
        task_ids.sort()
        initiative_document["task_ids"] = task_ids
    initiative_document["updated_at"] = updated_at
    loader.artifact_store.write_json_object(
        f"{initiative.relative_root}/.wt/initiative.json",
        initiative_document,
    )


def _touch_initiative_state(
    loader: ControlPlaneLoader,
    initiative: PlanInitiativeState,
    *,
    updated_at: str,
) -> None:
    initiative_document = dict(initiative.document)
    initiative_document["updated_at"] = updated_at
    loader.artifact_store.write_json_object(
        f"{initiative.relative_root}/.wt/initiative.json",
        initiative_document,
    )


def _append_task_event(
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


def _mark_initiative_execution_started(
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

    initiative_relative_path = f"{initiative.relative_root}/.wt/initiative.json"
    initiative_document = loader.derive(
        active_pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    ).load_validated_document(initiative_relative_path)
    execution_started = _initiative_execution_started(loader, initiative)
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

    lifecycle_stage = str(initiative_document.get("lifecycle_stage", "capture_incomplete"))
    if lifecycle_stage not in {"in_progress", *tuple(_IMMUTABLE_INITIATIVE_LIFECYCLE_STAGES)}:
        initiative_document["lifecycle_stage"] = "in_progress"
        changed = True

    if changed:
        initiative_document["updated_at"] = updated_at
        loader.artifact_store.write_json_object(
            initiative_relative_path,
            initiative_document,
        )


def _validate_update_flags(params: TaskUpdateParams) -> None:
    _reject_conflicting_clear(params.trace_id is not None, params.clear_trace_id, key="trace_id")
    _reject_conflicting_clear(
        params.applies_to is not None,
        params.clear_applies_to,
        key="applies_to",
    )
    _reject_conflicting_clear(
        params.related_ids is not None,
        params.clear_related_ids,
        key="related_ids",
    )
    _reject_conflicting_clear(
        params.depends_on is not None,
        params.clear_depends_on,
        key="depends_on",
    )
    _reject_conflicting_clear(
        params.blocked_by is not None,
        params.clear_blocked_by,
        key="blocked_by",
    )


def _initiative_execution_started(
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


def _reject_conflicting_clear(has_values: bool, clear: bool, *, key: str) -> None:
    if has_values and clear:
        raise ValueError(f"Cannot provide replacement values and clear {key} in the same call.")
