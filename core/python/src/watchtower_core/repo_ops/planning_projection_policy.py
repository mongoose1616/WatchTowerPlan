"""Private helpers for planning projection phase and next-step policy."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.models import (
    DecisionIndexEntry,
    DesignDocumentIndexEntry,
    PrdIndexEntry,
    TaskIndexEntry,
    TraceabilityEntry,
)
from watchtower_core.repo_ops.planning_projection_task_selection import (
    TracePlanningTaskSelection,
    _select_coordination_task,
)

VALIDATE_ACCEPTANCE_COMMAND_DOC = (
    "docs/commands/core_python/watchtower_core_validate_acceptance.md"
)
CLOSEOUT_INITIATIVE_COMMAND_DOC = (
    "docs/commands/core_python/watchtower_core_closeout_initiative.md"
)
DESIGN_DIRECTORY = "docs/planning/design/features/"
IMPLEMENTATION_PLAN_DIRECTORY = "docs/planning/design/implementation/"
TASK_OPEN_DIRECTORY = "docs/planning/tasks/open/"


@dataclass(frozen=True, slots=True)
class TracePlanningPolicySnapshot:
    """Derived phase and next-step policy for one planning trace."""

    current_phase: str
    key_surface_path: str
    next_action: str
    next_surface_path: str


def build_trace_planning_policy_snapshot(
    *,
    trace_entry: TraceabilityEntry,
    prd_entries: tuple[PrdIndexEntry, ...],
    design_entries: tuple[DesignDocumentIndexEntry, ...],
    decision_entries: tuple[DecisionIndexEntry, ...],
    task_entries: tuple[TaskIndexEntry, ...],
    active_tasks: tuple[TaskIndexEntry, ...],
    task_lookup: dict[str, TaskIndexEntry],
    task_selection: TracePlanningTaskSelection,
) -> TracePlanningPolicySnapshot:
    """Derive the private policy view used by planning projections."""

    current_phase = _determine_current_phase(
        trace_entry=trace_entry,
        prd_entries=prd_entries,
        design_entries=design_entries,
        active_tasks=active_tasks,
    )
    key_surface_path = _key_surface_path(
        trace_entry=trace_entry,
        prd_entries=prd_entries,
        design_entries=design_entries,
        decision_entries=decision_entries,
        task_entries=task_entries,
    )
    next_action, next_surface_path = _next_step(
        current_phase=current_phase,
        initiative_status=trace_entry.initiative_status,
        active_tasks=active_tasks,
        task_lookup=task_lookup,
        blocked_task_count=task_selection.blocked_task_count,
        key_surface_path=key_surface_path,
    )
    return TracePlanningPolicySnapshot(
        current_phase=current_phase,
        key_surface_path=key_surface_path,
        next_action=next_action,
        next_surface_path=next_surface_path,
    )


def _feature_designs(
    entries: tuple[DesignDocumentIndexEntry, ...],
) -> tuple[DesignDocumentIndexEntry, ...]:
    return tuple(entry for entry in entries if entry.family == "feature_design")


def _implementation_plans(
    entries: tuple[DesignDocumentIndexEntry, ...],
) -> tuple[DesignDocumentIndexEntry, ...]:
    return tuple(entry for entry in entries if entry.family == "implementation_plan")


def _determine_current_phase(
    *,
    trace_entry: TraceabilityEntry,
    prd_entries: tuple[PrdIndexEntry, ...],
    design_entries: tuple[DesignDocumentIndexEntry, ...],
    active_tasks: tuple[TaskIndexEntry, ...],
) -> str:
    if trace_entry.initiative_status != "active":
        return "closed"

    feature_designs = _feature_designs(design_entries)
    implementation_plans = _implementation_plans(design_entries)
    if active_tasks and _has_non_bootstrap_active_tasks(active_tasks):
        return "execution"
    if active_tasks and _has_only_bootstrap_active_tasks(active_tasks):
        return _determine_pre_execution_phase(
            prd_entries=prd_entries,
            feature_designs=feature_designs,
            implementation_plans=implementation_plans,
        )

    has_validation_inputs = bool(
        trace_entry.acceptance_ids or trace_entry.acceptance_contract_ids
    )
    has_evidence = bool(trace_entry.evidence_ids)

    pre_execution_phase = _determine_pre_execution_phase(
        prd_entries=prd_entries,
        feature_designs=feature_designs,
        implementation_plans=implementation_plans,
    )
    if pre_execution_phase == "prd":
        return "prd"
    if pre_execution_phase == "design":
        return "design"
    if (
        pre_execution_phase == "implementation_planning"
        and not has_validation_inputs
        and not has_evidence
    ):
        return "implementation_planning"
    if implementation_plans and has_validation_inputs and not has_evidence:
        return "validation"
    if has_evidence:
        return "closeout"
    return pre_execution_phase


def _determine_pre_execution_phase(
    *,
    prd_entries: tuple[PrdIndexEntry, ...],
    feature_designs: tuple[DesignDocumentIndexEntry, ...],
    implementation_plans: tuple[DesignDocumentIndexEntry, ...],
) -> str:
    if prd_entries and not feature_designs:
        return "prd"
    if feature_designs and not implementation_plans:
        return "design"
    if implementation_plans:
        return "implementation_planning"
    if feature_designs:
        return "design"
    if prd_entries:
        return "prd"
    return "closeout"


def _has_non_bootstrap_active_tasks(active_tasks: tuple[TaskIndexEntry, ...]) -> bool:
    return any(not _task_is_bootstrap(entry) for entry in active_tasks)


def _has_only_bootstrap_active_tasks(active_tasks: tuple[TaskIndexEntry, ...]) -> bool:
    return bool(active_tasks) and all(_task_is_bootstrap(entry) for entry in active_tasks)


def _task_is_bootstrap(entry: TaskIndexEntry) -> bool:
    """Bootstrap tasks keep a trace owned during planning but do not imply execution."""

    return ".bootstrap." in entry.task_id


def _key_surface_path(
    *,
    trace_entry: TraceabilityEntry,
    prd_entries: tuple[PrdIndexEntry, ...],
    design_entries: tuple[DesignDocumentIndexEntry, ...],
    decision_entries: tuple[DecisionIndexEntry, ...],
    task_entries: tuple[TaskIndexEntry, ...],
) -> str:
    if prd_entries:
        return sorted(entry.doc_path for entry in prd_entries)[0]
    feature_designs = _feature_designs(design_entries)
    if feature_designs:
        return sorted(entry.doc_path for entry in feature_designs)[0]
    implementation_plans = _implementation_plans(design_entries)
    if implementation_plans:
        return sorted(entry.doc_path for entry in implementation_plans)[0]
    if decision_entries:
        return sorted(entry.doc_path for entry in decision_entries)[0]
    if task_entries:
        return sorted(entry.doc_path for entry in task_entries)[0]
    if trace_entry.related_paths:
        return sorted(trace_entry.related_paths)[0]
    return "docs/planning/initiatives/initiative_tracking.md"


def _next_step(
    *,
    current_phase: str,
    initiative_status: str,
    active_tasks: tuple[TaskIndexEntry, ...],
    task_lookup: dict[str, TaskIndexEntry],
    blocked_task_count: int,
    key_surface_path: str,
) -> tuple[str, str]:
    if initiative_status != "active":
        return (
            f"No further default action. Initiative is {initiative_status}.",
            key_surface_path,
        )
    if current_phase == "prd":
        return (
            (
                "Create or update a feature design so the initiative has a "
                "reviewed technical direction."
            ),
            DESIGN_DIRECTORY,
        )
    if current_phase == "design":
        return (
            (
                "Create or update an implementation plan so the approved "
                "design becomes executable work."
            ),
            IMPLEMENTATION_PLAN_DIRECTORY,
        )
    if current_phase == "implementation_planning":
        return (
            (
                "Create execution tasks and assign an owner so work can move "
                "from planning into execution."
            ),
            TASK_OPEN_DIRECTORY,
        )
    if current_phase == "execution":
        focus_task = _select_coordination_task(active_tasks, task_lookup)
        next_task_path = focus_task.doc_path if focus_task is not None else TASK_OPEN_DIRECTORY
        if blocked_task_count > 0:
            return (
                (
                    "Resolve blockers on the active task set and keep task "
                    "state current before opening new follow-up work."
                ),
                next_task_path,
            )
        if any(entry.task_status in {"backlog", "ready"} for entry in active_tasks):
            return (
                (
                    "Start or continue the active task set and keep the "
                    "current task records aligned with execution progress."
                ),
                next_task_path,
            )
        if any(entry.task_status == "in_review" for entry in active_tasks):
            return (
                (
                    "Review the active task set, land any follow-up changes, "
                    "and close completed tasks explicitly."
                ),
                next_task_path,
            )
        return (
            (
                "Continue the active task set and keep planning, traceability, "
                "and derived surfaces aligned as work lands."
            ),
            next_task_path,
        )
    if current_phase == "validation":
        return (
            (
                "Run initiative validation and record durable evidence before "
                "moving the initiative into closeout."
            ),
            VALIDATE_ACCEPTANCE_COMMAND_DOC,
        )
    if current_phase == "closeout":
        return (
            (
                "Run initiative closeout or create explicit follow-up tasks "
                "before marking the initiative complete."
            ),
            CLOSEOUT_INITIATIVE_COMMAND_DOC,
        )
    return (
        "Inspect the initiative source surfaces and decide the next bounded planning step.",
        key_surface_path,
    )
