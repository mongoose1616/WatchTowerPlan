# Plan Artifact Index Runtime Foundation

## Summary
Publishes the missing live plan artifact index, removes legacy artifact-index field leakage, and exposes the cross-family query surface required by requirements.md and decisions.md.

## Identity
- `initiative_id`: `initiative.plan_artifact_index_runtime_foundation`
- `trace_id`: `trace.plan_artifact_index_runtime_foundation`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_artifact_index_runtime_foundation.publish_artifact_index_contract_and_neutralize_legacy_fields`: Update the generic pack artifact-index contract, typed models, and validation so challenge-specific and platform-specific leakage is replaced by plan-safe provenance fields.
- `task.plan_artifact_index_runtime_foundation.build_live_plan_artifact_index_and_query_surface`: Build plan/.wt/artifact_index.json from live plan artifact families and expose it through a first-class query command.
- `task.plan_artifact_index_runtime_foundation.validate_artifact_index_coverage_and_guidance`: Add tests, validator wiring, and command guidance proving the live artifact index stays aligned with requirements.md and decisions.md.
