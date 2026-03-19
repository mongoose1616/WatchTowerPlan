# Plan Workflow Execution Harness Foundation Implementation Slice

## Summary
Adds a reusable workflow execution harness over routed workflow selection with mode checks, gate checks, runner callbacks, and event recording hooks.

## Work Breakdown
- `task.plan_workflow_execution_harness_foundation.define_generic_workflow_execution_contract`: Add the export-safe workflow execution models and harness under watchtower_core.workflow_execution.
- `task.plan_workflow_execution_harness_foundation.add_workflow_execution_boundary_coverage`: Lock the new execution seam through focused unit coverage and package-root boundary tests.
- `task.plan_workflow_execution_harness_foundation.reconcile_requirements_and_package_docs`: Update requirements.md and package documentation to mark workflow execution current at the reusable-core boundary.

## Acceptance Shape
- `watchtower_core.workflow_execution` exposes typed workflow-step, event, gate, and result contracts plus a reusable harness.
- The harness executes selected workflows in deterministic order using routed workflow metadata, callback-based mode and gate checks, and callback-based step runners.
- Requirements and package docs mark the workflow execution runtime seam current without leaking repo-local orchestration into the package root.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
