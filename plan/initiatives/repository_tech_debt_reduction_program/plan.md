# Repository Tech Debt Reduction Program Plan

## Initiative Identity
- `initiative_id`: `initiative.repository_tech_debt_reduction_program`
- `trace_id`: `trace.repository_tech_debt_reduction_program`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `in_progress`
- `review_status`: `approved`
- `updated_at`: `2026-03-22T21:50:42Z`

## Scope and Non-Goals
Makes tech-debt reduction the active repository priority, starting with legacy residue removal, integration-tail reduction, and stale compatibility cleanup across core, host, and pack-owned code.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Repository Tech Debt Reduction Program: Bootstrap Repository Tech Debt Reduction Program live initiative package.
- Inventory High-Cost Technical Debt: Profiles the current debt inventory across slow tests, stale compatibility surfaces, migration residue, and duplicate authority declarations.
- Reconcile Duplicate Registry And Contract Declarations: Collapses avoidable duplicated schema, validator, and registry declarations where one authority surface should remain canonical.
- Reduce Integration Tail And Tier Tests: Cuts the slow integration tail by removing redundant end-to-end coverage, reusing prepared baselines, and clarifying fast-versus-slow test boundaries.
- Remove Stale Compatibility And Migration Residue: Deletes stale compatibility imports, migration-era glue, and dead edge-case support that no longer protects active contracts.
- Validate And Close First Tech Debt Tranche: Runs the final repo gate, records removed debt and bounded deferrals, and closes the first tech-debt tranche cleanly.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.repository_tech_debt_reduction_program.remove_stale_compatibility_and_migration_residue](/plan/initiatives/repository_tech_debt_reduction_program/.wt/tasks/remove_stale_compatibility_and_migration_residue/task.json) | `in_progress` | `high` | `repository_maintainer` | Deletes stale compatibility imports, migration-era glue, and dead edge-case support that no longer protects active contracts. | task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt |
| [task.repository_tech_debt_reduction_program.reconcile_duplicate_registry_and_contract_declarations](/plan/initiatives/repository_tech_debt_reduction_program/.wt/tasks/reconcile_duplicate_registry_and_contract_declarations/task.json) | `planned` | `high` | `repository_maintainer` | Collapses avoidable duplicated schema, validator, and registry declarations where one authority surface should remain canonical. | task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt |
| [task.repository_tech_debt_reduction_program.validate_and_close_first_tech_debt_tranche](/plan/initiatives/repository_tech_debt_reduction_program/.wt/tasks/validate_and_close_first_tech_debt_tranche/task.json) | `planned` | `high` | `repository_maintainer` | Runs the final repo gate, records removed debt and bounded deferrals, and closes the first tech-debt tranche cleanly. | task.repository_tech_debt_reduction_program.reduce_integration_tail_and_tier_tests, task.repository_tech_debt_reduction_program.remove_stale_compatibility_and_migration_residue, task.repository_tech_debt_reduction_program.reconcile_duplicate_registry_and_contract_declarations |
| [task.repository_tech_debt_reduction_program.bootstrap_repository_tech_debt_reduction_program](/plan/initiatives/repository_tech_debt_reduction_program/.wt/tasks/bootstrap_repository_tech_debt_reduction_program/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Repository Tech Debt Reduction Program live initiative package. | - |
| [task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt](/plan/initiatives/repository_tech_debt_reduction_program/.wt/tasks/inventory_high_cost_technical_debt/task.json) | `completed` | `high` | `repository_maintainer` | Profiles the current debt inventory across slow tests, stale compatibility surfaces, migration residue, and duplicate authority declarations. | - |
| [task.repository_tech_debt_reduction_program.reduce_integration_tail_and_tier_tests](/plan/initiatives/repository_tech_debt_reduction_program/.wt/tasks/reduce_integration_tail_and_tier_tests/task.json) | `completed` | `high` | `repository_maintainer` | Cuts the slow integration tail by removing redundant end-to-end coverage, reusing prepared baselines, and clarifying fast-versus-slow test boundaries. | task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt |

## Dependencies and Risks
- Discrepancy `discrepancy.repository_tech_debt_reduction_program.decision_notes_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/repository_tech_debt_reduction_program/decision_notes.md; machine confirmation is required.
- Discrepancy `discrepancy.repository_tech_debt_reduction_program.design_record_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/repository_tech_debt_reduction_program/design_record.md; machine confirmation is required.
- Discrepancy `discrepancy.repository_tech_debt_reduction_program.implementation_slice_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/repository_tech_debt_reduction_program/implementation_slice.md; machine confirmation is required.
- Discrepancy `discrepancy.repository_tech_debt_reduction_program.initiative_brief_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/repository_tech_debt_reduction_program/initiative_brief.md; machine confirmation is required.
- Discrepancy `discrepancy.repository_tech_debt_reduction_program.review_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/review_index.json.
- Task `task.repository_tech_debt_reduction_program.reconcile_duplicate_registry_and_contract_declarations` depends on `task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt`.
- Task `task.repository_tech_debt_reduction_program.reduce_integration_tail_and_tier_tests` depends on `task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt`.
- Task `task.repository_tech_debt_reduction_program.remove_stale_compatibility_and_migration_residue` depends on `task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt`.
- Task `task.repository_tech_debt_reduction_program.validate_and_close_first_tech_debt_tranche` depends on `task.repository_tech_debt_reduction_program.reduce_integration_tail_and_tier_tests`, `task.repository_tech_debt_reduction_program.remove_stale_compatibility_and_migration_residue`, `task.repository_tech_debt_reduction_program.reconcile_duplicate_registry_and_contract_declarations`.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `True`
- `blocking_reasons`: `none`
- Task count: `6`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/repository_tech_debt_reduction_program/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/repository_tech_debt_reduction_program/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/repository_tech_debt_reduction_program/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/repository_tech_debt_reduction_program/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/repository_tech_debt_reduction_program/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/repository_tech_debt_reduction_program/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/repository_tech_debt_reduction_program/summary.md)
