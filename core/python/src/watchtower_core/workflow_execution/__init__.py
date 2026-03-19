"""Public workflow execution namespace for export-safe routed workflow orchestration."""

from __future__ import annotations

from watchtower_core.utils.module_exports import fail_closed_package_getattr
from watchtower_core.workflow_execution.harness import (
    WorkflowEventRecorder,
    WorkflowExecutionEvent,
    WorkflowExecutionGateResult,
    WorkflowExecutionHarness,
    WorkflowExecutionResult,
    WorkflowExecutionStep,
    WorkflowExecutionStepResult,
    WorkflowGateCheck,
    WorkflowModeCheck,
    WorkflowStepRunner,
    WorkflowStepStatus,
)

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
__getattr__ = fail_closed_package_getattr(
    "watchtower_core.workflow_execution exports only reusable workflow execution surfaces. "
    "Repo-specific workflow behavior still lives under watchtower_core.repo_ops."
)
