# Plan Project Context Runtime Standardization Implementation Slice

## Summary
Promotes project-scoped context loading into a first-class runtime surface layered on always-loaded pack context and proves it through a narrow query path.

## Initial Work Breakdown
- `task.plan_project_context_runtime_standardization.extract_project_context_runtime_helper`: Move project-scoped context loading behind a first-class runtime surface that builds on project record and repository map artifacts.
- `task.plan_project_context_runtime_standardization.expose_project_context_query_surface`: Add a bounded CLI query path that loads pack context and project context explicitly for one project-scoped target.
- `task.plan_project_context_runtime_standardization.validate_project_context_load_contract`: Add integration and command coverage proving separate project-context loading and scope-aware query behavior.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
