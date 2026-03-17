# Plan Lifecycle Review And Source Vocab Registries

## Summary
Adds the missing lifecycle-stage, review-status, and source-type registries plus typed helper coverage so plan-pack workflow semantics stop living only in scattered schema enums and runtime string literals.

## Identity
- `initiative_id`: `initiative.plan_lifecycle_review_and_source_vocab_registries`
- `trace_id`: `trace.plan_lifecycle_review_and_source_vocab_registries`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_lifecycle_review_and_source_vocab_registries.publish_lifecycle_review_and_source_registry_schemas`: Add governed schema contracts for the lifecycle-stage, review-status, and source-type registries.
- `task.plan_lifecycle_review_and_source_vocab_registries.seed_lifecycle_review_and_source_vocab_entries`: Seed active registry entries aligned to current plan-workspace lifecycle stages, review states, and provenance categories.
- `task.plan_lifecycle_review_and_source_vocab_registries.wire_typed_helper_and_validation_coverage`: Add typed loader support, a vocabulary helper, and tests proving the registries stay aligned with live schemas and runtime use.
