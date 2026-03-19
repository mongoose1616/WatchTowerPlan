from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.workflow_execution import (
    WorkflowExecutionGateResult,
    WorkflowExecutionHarness,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _harness() -> WorkflowExecutionHarness:
    return WorkflowExecutionHarness(ControlPlaneLoader(REPO_ROOT))


def test_workflow_execution_harness_executes_selected_workflow_chain_in_order() -> None:
    executed: list[str] = []
    recorded_events: list[str] = []

    result = _harness().execute(
        task_type="Code Implementation",
        mode="execute",
        runner=lambda step: executed.append(step.workflow_id) or {"workflow_id": step.workflow_id},
        event_recorder=lambda event: recorded_events.append(event.event_type),
    )

    assert result.succeeded is True
    assert [step.workflow_id for step in result.steps] == [
        "workflow.core",
        "workflow.task_scope_definition",
        "workflow.current_state_inspection",
        "workflow.internal_context_review",
        "workflow.external_guidance_research",
        "workflow.code_implementation",
        "workflow.code_validation",
        "workflow.task_handoff_review",
    ]
    assert executed == [step.workflow_id for step in result.steps]
    assert result.step_results[-1].status == "completed"
    assert recorded_events[0] == "workflow_chain_selected"
    assert recorded_events.count("workflow_executed") == len(result.steps)


def test_workflow_execution_harness_blocks_steps_on_mode_check() -> None:
    executed: list[str] = []

    result = _harness().execute(
        task_type="Code Review",
        mode="review_only",
        mode_check=lambda step, mode: (
            "Execution mode required for code review."
            if step.workflow_id == "workflow.code_review" and mode == "review_only"
            else None
        ),
        runner=lambda step: executed.append(step.workflow_id),
    )

    blocked = next(
        step_result
        for step_result in result.step_results
        if step_result.step.workflow_id == "workflow.code_review"
    )
    assert result.succeeded is False
    assert blocked.status == "mode_blocked"
    assert blocked.reason == "Execution mode required for code review."
    assert "workflow.code_review" not in executed


def test_workflow_execution_harness_blocks_steps_on_gate_check() -> None:
    result = _harness().execute(
        task_type="Documentation Review",
        mode="execute",
        gate_check=lambda step: (
            WorkflowExecutionGateResult(
                allowed=False,
                reason="Documentation review is waiting on an approval gate.",
            )
            if step.workflow_id == "workflow.documentation_review"
            else None
        ),
    )

    blocked = next(
        step_result
        for step_result in result.step_results
        if step_result.step.workflow_id == "workflow.documentation_review"
    )
    assert result.succeeded is False
    assert blocked.status == "gate_blocked"
    assert blocked.reason == "Documentation review is waiting on an approval gate."


def test_workflow_execution_harness_records_runner_failures_without_crashing_chain_result() -> None:
    result = _harness().execute(
        task_type="Code Review",
        mode="execute",
        runner=lambda step: (
            (_ for _ in ()).throw(RuntimeError("runner failed"))
            if step.workflow_id == "workflow.code_review"
            else None
        ),
    )

    failed = next(
        step_result
        for step_result in result.step_results
        if step_result.step.workflow_id == "workflow.code_review"
    )
    assert result.succeeded is False
    assert failed.status == "failed"
    assert failed.reason == "runner failed"
