# Plan Workflow Execution Harness Foundation

## Summary
Adds a reusable workflow execution harness over routed workflow selection with mode checks, gate checks, runner callbacks, and event recording hooks.

## Scope
- Add an export-safe `watchtower_core.workflow_execution` package that turns governed route selection plus workflow metadata into executable ordered workflow steps.
- Keep the harness generic by delegating step execution, mode checks, gate checks, and event persistence to injected callbacks rather than embedding repo-local planning behavior.
- Update the requirements and package docs so the reusable-core workflow execution boundary is no longer marked missing.

## Out Of Scope
- Repo-local execution of workflow module documents as first-class planning mutations.
- New workflow metadata fields or route schema expansion beyond what the current generic harness needs.
- Broader closeout, evidence, or rendered-view refactors.

## Identity
- `initiative_id`: `initiative.plan_workflow_execution_harness_foundation`
- `trace_id`: `trace.plan_workflow_execution_harness_foundation`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_workflow_execution_harness_foundation.define_generic_workflow_execution_contract`: Add the export-safe workflow execution models and harness under watchtower_core.workflow_execution.
- `task.plan_workflow_execution_harness_foundation.add_workflow_execution_boundary_coverage`: Lock the new execution seam through focused unit coverage and package-root boundary tests.
- `task.plan_workflow_execution_harness_foundation.reconcile_requirements_and_package_docs`: Update requirements.md and package documentation to mark workflow execution current at the reusable-core boundary.
