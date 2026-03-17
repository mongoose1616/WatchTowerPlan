# Plan Generic Query Harness Export Foundation

## Summary
Exports a reusable generic query surface from watchtower_core.query and refactors export-safe query services onto that public boundary so requirements.md and decisions.md no longer depend on a guardrail-only query root.

## Identity
- `initiative_id`: `initiative.plan_generic_query_harness_export_foundation`
- `trace_id`: `trace.plan_generic_query_harness_export_foundation`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_generic_query_harness_export_foundation.publish_generic_query_harness_contracts`: Add export-safe query modules, search parameter types, and reusable query services under watchtower_core.query.
- `task.plan_generic_query_harness_export_foundation.refactor_repo_query_services_onto_public_query_surface`: Move generic repo-local query implementations onto the reusable-core query surface without moving plan-live query services out of repo_ops.
- `task.plan_generic_query_harness_export_foundation.validate_query_harness_export_and_guidance`: Add boundary tests and package guidance proving watchtower_core.query now exports reusable generic query services aligned to requirements.md and decisions.md.
