# Plan Workflow Execution Harness Foundation Design Record

## Summary
Adds a reusable workflow execution harness over routed workflow selection with mode checks, gate checks, runner callbacks, and event recording hooks.

## Design Boundary
- The generic harness should depend only on reusable route selection and workflow-catalog helpers, not on repo-local CLI handlers or plan initiative state.
- Because workflow modules are authored docs rather than executable code units, the harness should expose injected runner callbacks for actual step execution while still owning ordered step preparation, mode checks, gate checks, and event emission.
- Event recording should stay callback-based so the generic contract can work with pack-local event stores later without hard-coding one event artifact family now.
- The result contract should preserve route warnings, step outcomes, and emitted event payloads in one typed surface.

## Validation Boundary
- Focused unit tests should cover explicit task-type execution, mode-blocked steps, gate-blocked steps, runner success, and recorded event ordering.
- Package-boundary tests should prove `watchtower_core.workflow_execution` exports only the reusable harness surfaces and fails closed for repo-local callers.
