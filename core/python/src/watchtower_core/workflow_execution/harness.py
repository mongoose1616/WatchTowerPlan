"""Reusable workflow-execution harness over governed route and workflow metadata."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.workflow_catalog import WorkflowCatalogHelper
from watchtower_core.routing import RoutingEngine, RoutingSelection

WorkflowStepStatus = Literal["completed", "mode_blocked", "gate_blocked", "failed"]
WorkflowModeCheck = Callable[
    ["WorkflowExecutionStep", str],
    "WorkflowExecutionGateResult | bool | str | None",
]
WorkflowGateCheck = Callable[
    ["WorkflowExecutionStep"],
    "WorkflowExecutionGateResult | bool | str | None",
]
WorkflowStepRunner = Callable[["WorkflowExecutionStep"], object | None]
WorkflowEventRecorder = Callable[["WorkflowExecutionEvent"], None]


@dataclass(frozen=True, slots=True)
class WorkflowExecutionStep:
    """One executable workflow step derived from routing and workflow metadata."""

    workflow_id: str
    title: str
    doc_path: str
    phase_type: str
    task_family: str
    route_ids: tuple[str, ...]
    companion_workflow_ids: tuple[str, ...]
    primary_risks: tuple[str, ...]
    trigger_tags: tuple[str, ...]
    related_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class WorkflowExecutionGateResult:
    """Normalized outcome for one mode or gate check."""

    allowed: bool
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class WorkflowExecutionEvent:
    """One emitted workflow execution event."""

    sequence: int
    event_type: str
    mode: str
    workflow_id: str | None = None
    route_ids: tuple[str, ...] = ()
    detail: str | None = None


@dataclass(frozen=True, slots=True)
class WorkflowExecutionStepResult:
    """Outcome for one workflow execution step."""

    step: WorkflowExecutionStep
    status: WorkflowStepStatus
    output: object | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class WorkflowExecutionResult:
    """Aggregated output for one workflow execution run."""

    mode: str
    selection: RoutingSelection
    steps: tuple[WorkflowExecutionStep, ...]
    step_results: tuple[WorkflowExecutionStepResult, ...]
    recorded_events: tuple[WorkflowExecutionEvent, ...]
    succeeded: bool
    warnings: tuple[str, ...] = ()


class WorkflowExecutionHarness:
    """Execute routed workflow chains through reusable callback-based orchestration."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._routing = RoutingEngine(loader)
        self._catalog = WorkflowCatalogHelper.from_loader(loader)

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> WorkflowExecutionHarness:
        """Build one execution harness from a repository root."""

        return cls(ControlPlaneLoader(repo_root))

    def execute(
        self,
        *,
        mode: str,
        request_text: str | None = None,
        task_type: str | None = None,
        mode_check: WorkflowModeCheck | None = None,
        gate_check: WorkflowGateCheck | None = None,
        runner: WorkflowStepRunner | None = None,
        event_recorder: WorkflowEventRecorder | None = None,
    ) -> WorkflowExecutionResult:
        """Execute the routed workflow chain for one request or explicit task type."""

        selection = self._routing.select(request_text=request_text, task_type=task_type)
        steps = self._build_steps(selection)
        events: list[WorkflowExecutionEvent] = []

        def record(
            event_type: str,
            *,
            workflow_id: str | None = None,
            route_ids: tuple[str, ...] = (),
            detail: str | None = None,
        ) -> None:
            event = WorkflowExecutionEvent(
                sequence=len(events) + 1,
                event_type=event_type,
                mode=mode,
                workflow_id=workflow_id,
                route_ids=route_ids,
                detail=detail,
            )
            events.append(event)
            if event_recorder is not None:
                event_recorder(event)

        record(
            "workflow_chain_selected",
            route_ids=tuple(route.route_id for route in selection.selected_routes),
            detail=("; ".join(selection.warnings) if selection.warnings else None),
        )

        step_results: list[WorkflowExecutionStepResult] = []
        succeeded = True
        for step in steps:
            mode_result = _normalize_check_result(
                mode_check(step, mode) if mode_check is not None else None,
                blocked_reason=f"Execution mode blocked workflow {step.workflow_id}.",
            )
            if not mode_result.allowed:
                succeeded = False
                record(
                    "workflow_mode_blocked",
                    workflow_id=step.workflow_id,
                    route_ids=step.route_ids,
                    detail=mode_result.reason,
                )
                step_results.append(
                    WorkflowExecutionStepResult(
                        step=step,
                        status="mode_blocked",
                        reason=mode_result.reason,
                    )
                )
                continue

            gate_result = _normalize_check_result(
                gate_check(step) if gate_check is not None else None,
                blocked_reason=f"Execution gate blocked workflow {step.workflow_id}.",
            )
            if not gate_result.allowed:
                succeeded = False
                record(
                    "workflow_gate_blocked",
                    workflow_id=step.workflow_id,
                    route_ids=step.route_ids,
                    detail=gate_result.reason,
                )
                step_results.append(
                    WorkflowExecutionStepResult(
                        step=step,
                        status="gate_blocked",
                        reason=gate_result.reason,
                    )
                )
                continue

            try:
                output = runner(step) if runner is not None else None
            except Exception as exc:
                succeeded = False
                detail = str(exc) or type(exc).__name__
                record(
                    "workflow_failed",
                    workflow_id=step.workflow_id,
                    route_ids=step.route_ids,
                    detail=detail,
                )
                step_results.append(
                    WorkflowExecutionStepResult(
                        step=step,
                        status="failed",
                        reason=detail,
                    )
                )
                continue

            record(
                "workflow_executed",
                workflow_id=step.workflow_id,
                route_ids=step.route_ids,
            )
            step_results.append(
                WorkflowExecutionStepResult(
                    step=step,
                    status="completed",
                    output=output,
                )
            )

        return WorkflowExecutionResult(
            mode=mode,
            selection=selection,
            steps=steps,
            step_results=tuple(step_results),
            recorded_events=tuple(events),
            succeeded=succeeded,
            warnings=selection.warnings,
        )

    def _build_steps(
        self,
        selection: RoutingSelection,
    ) -> tuple[WorkflowExecutionStep, ...]:
        route_ids_by_workflow_id = {
            workflow.workflow_id: tuple(
                route.route_id
                for route in selection.selected_routes
                if workflow.workflow_id in route.required_workflow_ids
            )
            for workflow in selection.selected_workflows
        }
        return tuple(
            WorkflowExecutionStep(
                workflow_id=snapshot.workflow.workflow_id,
                title=snapshot.workflow.title,
                doc_path=snapshot.workflow.doc_path,
                phase_type=snapshot.metadata.phase_type,
                task_family=snapshot.metadata.task_family,
                route_ids=route_ids_by_workflow_id.get(snapshot.workflow.workflow_id, ()),
                companion_workflow_ids=snapshot.metadata.companion_workflow_ids,
                primary_risks=snapshot.metadata.primary_risks,
                trigger_tags=snapshot.workflow.trigger_tags,
                related_paths=snapshot.workflow.related_paths,
            )
            for snapshot in (
                self._catalog.snapshot(workflow.workflow_id)
                for workflow in selection.selected_workflows
            )
        )


def _normalize_check_result(
    result: WorkflowExecutionGateResult | bool | str | None,
    *,
    blocked_reason: str,
) -> WorkflowExecutionGateResult:
    if result is None:
        return WorkflowExecutionGateResult(allowed=True)
    if isinstance(result, WorkflowExecutionGateResult):
        return result
    if isinstance(result, bool):
        return WorkflowExecutionGateResult(
            allowed=result,
            reason=None if result else blocked_reason,
        )
    if isinstance(result, str):
        return WorkflowExecutionGateResult(allowed=False, reason=result)
    raise TypeError(f"Unsupported workflow execution check result: {type(result).__name__}")


__all__ = [
    "WorkflowExecutionEvent",
    "WorkflowExecutionGateResult",
    "WorkflowExecutionHarness",
    "WorkflowExecutionResult",
    "WorkflowExecutionStep",
    "WorkflowExecutionStepResult",
    "WorkflowEventRecorder",
    "WorkflowGateCheck",
    "WorkflowModeCheck",
    "WorkflowStepRunner",
    "WorkflowStepStatus",
]
