# Plan Terminology Helper Foundation

## Summary
Generalize the existing planning vocabulary seam into a reusable terminology helper with pack-local lookup, alias resolution, and deprecation awareness.

## Identity
- `initiative_id`: `initiative.plan_terminology_helper_foundation`
- `trace_id`: `trace.plan_terminology_helper_foundation`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_terminology_helper_foundation.define_terminology_helper_contract`: Add a reusable terminology helper for pack-local lifecycle, review, source, and task-status vocabulary lookup.
- `task.plan_terminology_helper_foundation.refactor_callers_and_add_terminology_coverage`: Route live plan vocabulary callers through the terminology helper and lock alias or deprecation behavior with focused tests.
- `task.plan_terminology_helper_foundation.reconcile_terminology_requirements_and_docs`: Update the authoritative requirements and control-plane package docs to reflect the terminology helper boundary.
