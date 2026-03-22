"""Structured lifecycle helpers for initiative-local live task state."""

from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.terminology import TerminologyHelper
from watchtower_core.documentation.front_matter_paths import (
    normalize_governed_applies_to_values,
)
from watchtower_core.utils import utc_timestamp_now
from watchtower_plan.sync.coordination import CoordinationSyncService
from watchtower_plan.tasks.models import (
    TaskCreateParams,
    TaskMutationResult,
    TaskTransitionParams,
    TaskUpdateParams,
)
from watchtower_plan.tasks.mutations import (
    append_task_event,
    closeout_recommended,
    load_task_document_payload,
    mark_initiative_execution_started,
    task_document,
    touch_initiative_state,
    update_initiative_state_for_task,
)
from watchtower_plan.tasks.state import (
    find_initiative_by_trace_id,
    load_task_documents_by_id,
    write_task_document,
)
from watchtower_plan.tasks.support import (
    TASK_KIND_CHOICES,
    TASK_PRIORITY_CHOICES,
    apply_optional_list_field,
    normalize_choice,
    pick_choice,
    pick_string,
    slugify_file_stem,
)
from watchtower_plan.tasks.support import (
    TASK_STATUS_CHOICES as _TASK_STATUS_CHOICES,
)
from watchtower_plan.tasks.validation import (
    canonical_task_status,
    require_execution_ready_initiative,
    require_mutable_initiative,
    required_items,
    resolve_initiative_state,
    validate_task_references,
    validate_trace_linkage,
    validate_update_flags,
)
from watchtower_plan.workspace.service import (
    PLAN_PACK_SETTINGS_PATH,
    PlanWorkspaceService,
)

_LIVE_TASK_ARTIFACT_STATUS = "active"
TASK_STATUS_CHOICES = _TASK_STATUS_CHOICES
__all__ = ["TASK_STATUS_CHOICES", "TaskLifecycleService", "find_initiative_by_trace_id"]


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
        task_id = params.task_id.strip()
        if task_id in existing_documents:
            raise ValueError(f"Task ID already exists: {task_id}")

        initiative = resolve_initiative_state(
            self._loader,
            task_id=task_id,
            trace_id=params.trace_id,
        )
        require_mutable_initiative(self._loader, initiative)

        updated_at = params.updated_at or utc_timestamp_now()
        task_status = canonical_task_status(self._terminology, params.task_status)
        require_execution_ready_initiative(
            self._loader,
            initiative=initiative,
            task_status=task_status,
        )
        task_kind = normalize_choice(
            params.task_kind, TASK_KIND_CHOICES, label="task_kind"
        )
        priority = normalize_choice(
            params.priority, TASK_PRIORITY_CHOICES, label="priority"
        )
        title = params.title.strip()
        summary = params.summary.strip()
        owner = params.owner.strip()
        if not title:
            raise ValueError("title is required.")
        if not summary:
            raise ValueError("summary is required.")
        if not owner:
            raise ValueError("owner is required.")
        slug = slugify_file_stem(params.file_stem or title)
        relative_path = f"{initiative.relative_root}/.wt/tasks/{slug}/task.json"
        if (self._loader.repo_root / relative_path).exists():
            raise ValueError(f"Task document path already exists: {relative_path}")

        scope_items = required_items(params.scope_items, label="scope")
        done_when_items = required_items(params.done_when_items, label="done-when")
        applies_to = normalize_governed_applies_to_values(
            params.applies_to,
            origin=f"task create {task_id} applies_to",
            repo_root=self._loader.repo_root,
        )
        related_ids = tuple(
            value.strip() for value in params.related_ids if value.strip()
        )
        depends_on = tuple(
            value.strip() for value in params.depends_on if value.strip()
        )
        blocked_by = tuple(
            value.strip() for value in params.blocked_by if value.strip()
        )
        validate_task_references(
            task_id=task_id,
            depends_on=depends_on,
            blocked_by=blocked_by,
            existing_task_ids=set(existing_documents),
        )
        validate_trace_linkage(
            trace_id=initiative.trace_id,
            related_ids=related_ids,
            relative_path=relative_path,
        )

        document = task_document(
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
            update_initiative_state_for_task(
                self._loader,
                initiative,
                task_id=task_id,
                updated_at=updated_at,
            )
            append_task_event(
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
            mark_initiative_execution_started(
                self._loader,
                initiative=initiative,
                task_id=task_id,
                task_status=task_status,
                updated_at=updated_at,
                task_doc_path=relative_path,
            )
            PlanWorkspaceService(self._loader).sync(write=True)
            CoordinationSyncService(self._loader).run_workspace_follow_up_outputs(
                write=True
            )

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
            closeout_recommended=closeout_recommended(
                self._loader,
                task_id=task_id,
                trace_id=initiative.trace_id,
                candidate_status=task_status,
            ),
        )

    def update(self, params: TaskUpdateParams, *, write: bool) -> TaskMutationResult:
        validate_update_flags(params)
        task_id = params.task_id.strip()
        if not task_id:
            raise ValueError("task_id is required.")
        documents = load_task_documents_by_id(self._loader)
        try:
            document = documents[task_id]
        except KeyError as exc:
            raise ValueError(f"Unknown task ID: {task_id}") from exc

        initiative = resolve_initiative_state(
            self._loader,
            task_id=document.task_id,
            trace_id=document.trace_id,
        )
        require_mutable_initiative(self._loader, initiative)
        if params.clear_trace_id:
            raise ValueError(
                "Live initiative-local tasks inherit trace_id from the initiative package and "
                "cannot clear it."
            )
        if params.trace_id is not None and params.trace_id.strip() != document.trace_id:
            raise ValueError(
                "Live initiative-local tasks inherit trace_id from the initiative package and "
                "cannot move between traces."
            )
        if (
            params.file_stem is not None
            and slugify_file_stem(params.file_stem) != document.slug
        ):
            raise ValueError(
                "file_stem renames are not supported for live initiative-local task state."
            )

        task_state = load_task_document_payload(self._loader, document.relative_path)
        changed = False

        title = pick_string(params.title, current=document.title, label="title")
        if title != document.title:
            task_state["title"] = title
            changed = True

        summary = pick_string(params.summary, current=document.summary, label="summary")
        if summary != document.summary:
            task_state["summary"] = summary
            changed = True

        task_kind = pick_choice(
            params.task_kind,
            current=document.task_kind,
            allowed=TASK_KIND_CHOICES,
            label="task_kind",
        )
        if task_kind != document.task_kind:
            task_state["task_kind"] = task_kind
            changed = True

        priority = pick_choice(
            params.priority,
            current=document.priority,
            allowed=TASK_PRIORITY_CHOICES,
            label="priority",
        )
        if priority != document.priority:
            task_state["priority"] = priority
            changed = True

        owner = pick_string(params.owner, current=document.owner, label="owner")
        if owner != document.owner:
            task_state["owner"] = owner
            changed = True

        task_status = (
            canonical_task_status(self._terminology, params.task_status)
            if params.task_status is not None
            else document.task_status
        )
        require_execution_ready_initiative(
            self._loader,
            initiative=initiative,
            task_status=task_status,
        )
        if task_status != document.task_status:
            task_state["task_status"] = task_status
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
            task_state,
            "applies_to",
            values=applies_to,
            clear=params.clear_applies_to,
        )
        changed |= apply_optional_list_field(
            task_state,
            "related_ids",
            values=params.related_ids,
            clear=params.clear_related_ids,
        )
        changed |= apply_optional_list_field(
            task_state,
            "dependency_task_ids",
            values=params.depends_on,
            clear=params.clear_depends_on,
        )
        changed |= apply_optional_list_field(
            task_state,
            "blocker_task_ids",
            values=params.blocked_by,
            clear=params.clear_blocked_by,
        )

        if params.scope_items is not None:
            normalized_scope_items = required_items(params.scope_items, label="scope")
            if (
                string_tuple_field(task_state.get("scope_items"))
                != normalized_scope_items
            ):
                task_state["scope_items"] = list(normalized_scope_items)
                changed = True
        if params.done_when_items is not None:
            normalized_done_when_items = required_items(
                params.done_when_items,
                label="done-when",
            )
            if (
                string_tuple_field(task_state.get("done_when_items"))
                != normalized_done_when_items
            ):
                task_state["done_when_items"] = list(normalized_done_when_items)
                changed = True

        validate_task_references(
            task_id=document.task_id,
            depends_on=string_tuple_field(task_state.get("dependency_task_ids")),
            blocked_by=string_tuple_field(task_state.get("blocker_task_ids")),
            existing_task_ids=set(documents),
        )
        validate_trace_linkage(
            trace_id=document.trace_id,
            related_ids=string_tuple_field(task_state.get("related_ids")),
            relative_path=document.relative_path,
        )

        updated_at = params.updated_at or (
            utc_timestamp_now() if changed else document.updated_at
        )
        if updated_at != document.updated_at:
            task_state["updated_at"] = updated_at
            changed = True

        if write and changed:
            write_task_document(self._loader, document.relative_path, task_state)
            touch_initiative_state(self._loader, initiative, updated_at=updated_at)
            append_task_event(
                self._loader,
                initiative=initiative,
                task_id=document.task_id,
                task_slug=document.slug,
                event_type=(
                    "status_changed"
                    if task_status != document.task_status
                    else "updated"
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
            mark_initiative_execution_started(
                self._loader,
                initiative=initiative,
                task_id=document.task_id,
                task_status=task_status,
                updated_at=updated_at,
                task_doc_path=document.relative_path,
            )
            PlanWorkspaceService(self._loader).sync(write=True)
            CoordinationSyncService(self._loader).run_workspace_follow_up_outputs(
                write=True
            )

        return TaskMutationResult(
            task_id=document.task_id,
            title=str(task_state["title"]),
            summary=str(task_state["summary"]),
            trace_id=document.trace_id,
            task_status=str(task_state["task_status"]),
            task_kind=str(task_state["task_kind"]),
            priority=str(task_state["priority"]),
            owner=str(task_state["owner"]),
            updated_at=str(task_state["updated_at"]),
            doc_path=document.relative_path,
            previous_doc_path=None,
            moved=False,
            changed=changed,
            wrote=bool(write and changed),
            coordination_refreshed=bool(write and changed),
            closeout_recommended=closeout_recommended(
                self._loader,
                task_id=document.task_id,
                trace_id=document.trace_id,
                candidate_status=str(task_state["task_status"]),
            ),
        )

    def transition(
        self, params: TaskTransitionParams, *, write: bool
    ) -> TaskMutationResult:
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


def string_tuple_field(value: object) -> tuple[str, ...]:
    """Normalize one optional list-like task field into a string tuple."""

    if not isinstance(value, list):
        return ()
    return tuple(str(item) for item in value)
