"""Feature-owned task state and lifecycle services for the plan pack."""

from __future__ import annotations

from watchtower_core.utils.module_exports import lazy_module_getattr

__all__ = [
    "TASK_KIND_CHOICES",
    "TASK_PRIORITY_CHOICES",
    "TASK_STATUS_CHOICES",
    "PlanInitiativeState",
    "PlanTaskStateDocument",
    "TaskCreateParams",
    "TaskLifecycleService",
    "TaskMutationResult",
    "TaskTransitionParams",
    "TaskUpdateParams",
    "find_initiative_by_slug",
    "find_initiative_by_trace_id",
    "iter_initiative_states",
    "iter_task_documents",
    "load_task_document",
    "load_task_documents_by_id",
    "task_event_directory",
    "update_task_document",
    "write_task_document",
]

_EXPORT_MODULES = {
    "TASK_KIND_CHOICES": "watchtower_plan.tasks.support",
    "TASK_PRIORITY_CHOICES": "watchtower_plan.tasks.support",
    "TASK_STATUS_CHOICES": "watchtower_plan.tasks.lifecycle",
    "PlanInitiativeState": "watchtower_plan.tasks.state",
    "PlanTaskStateDocument": "watchtower_plan.tasks.state",
    "TaskCreateParams": "watchtower_plan.tasks.lifecycle",
    "TaskLifecycleService": "watchtower_plan.tasks.lifecycle",
    "TaskMutationResult": "watchtower_plan.tasks.lifecycle",
    "TaskTransitionParams": "watchtower_plan.tasks.lifecycle",
    "TaskUpdateParams": "watchtower_plan.tasks.lifecycle",
    "find_initiative_by_slug": "watchtower_plan.tasks.state",
    "find_initiative_by_trace_id": "watchtower_plan.tasks.state",
    "iter_initiative_states": "watchtower_plan.tasks.state",
    "iter_task_documents": "watchtower_plan.tasks.state",
    "load_task_document": "watchtower_plan.tasks.state",
    "load_task_documents_by_id": "watchtower_plan.tasks.state",
    "task_event_directory": "watchtower_plan.tasks.state",
    "update_task_document": "watchtower_plan.tasks.state",
    "write_task_document": "watchtower_plan.tasks.state",
}

__getattr__ = lazy_module_getattr(
    module_name=__name__,
    export_modules=_EXPORT_MODULES,
)
