# Plan Rebuild Harness Export Foundation

## Summary
Exports a reusable rebuild harness and routes the existing plan and project derived-surface rebuilds through the new boundary.

## Scope
- Add an export-safe `watchtower_core.rebuild` package with reusable target and result models for deterministic derived-surface rebuilds.
- Keep repo-local rebuild catalogs and output shaping under `watchtower_core.repo_ops` while moving the generic orchestration seam to reusable core.
- Refactor the existing plan-workspace and project-workspace derived-surface writes to use the new rebuild harness without changing the current rendered or machine-readable outputs.
- Update the requirements and boundary coverage so `rebuild_harness` and `watchtower_core.rebuild` can move from `Missing` to `Current`.

## Out Of Scope
- Broader rendered-view registry unification beyond the current plan and project workspace rebuild callers.
- Generic workflow execution, closeout broadening, or evidence-model expansion.
- Status-vocabulary or artifact-index field cleanup beyond what is necessary to keep the rebuild slice coherent.

## Identity
- `initiative_id`: `initiative.plan_rebuild_harness_export_foundation`
- `trace_id`: `trace.plan_rebuild_harness_export_foundation`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_rebuild_harness_export_foundation.define_rebuild_harness_contract`: Add the export-safe rebuild target and result model under watchtower_core.rebuild.
- `task.plan_rebuild_harness_export_foundation.refactor_plan_and_project_rebuild_callers`: Route plan and project derived-surface rebuild writes through the new harness without changing the current outputs.
- `task.plan_rebuild_harness_export_foundation.validate_rebuild_boundary_and_requirements_alignment`: Add focused tests, boundary coverage, and update the authoritative requirements rows for the rebuild export.
