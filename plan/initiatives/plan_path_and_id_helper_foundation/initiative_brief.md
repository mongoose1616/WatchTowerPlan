# Plan Path And ID Helper Foundation

## Summary
Adds reusable path and id helpers so plan initiative, project, task, and companion artifact naming stops living in scattered repo-local string conventions.

## Identity
- `initiative_id`: `initiative.plan_path_and_id_helper_foundation`
- `trace_id`: `trace.plan_path_and_id_helper_foundation`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_path_and_id_helper_foundation.add_path_and_id_helper`: Implement a reusable-core helper for canonical slugs, ids, and plan-workspace root paths.
- `task.plan_path_and_id_helper_foundation.refactor_plan_runtime_callers`: Adopt the helper in initiative, project, and related runtime surfaces that currently hand-roll canonical names and paths.
- `task.plan_path_and_id_helper_foundation.validate_helper_and_reconcile_requirements`: Add focused tests for the helper and align requirements.md with the implemented runtime seam.
