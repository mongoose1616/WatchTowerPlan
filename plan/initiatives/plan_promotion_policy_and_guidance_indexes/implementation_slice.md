# Plan Promotion Policy and Guidance Indexes Implementation Slice

## Summary
Adds the missing promotion policy registry and pack-level promotion and guidance indexes so initiative-local promotion records and approved plan guidance are machine-queryable under plan/.wt.

## Initial Work Breakdown
- `task.plan_promotion_policy_and_guidance_indexes.publish_promotion_policy_schema_and_registry`: Add the governed promotion-policy registry contract and seed the initial plan-pack promotion policy entries.
- `task.plan_promotion_policy_and_guidance_indexes.build_promotion_and_guidance_index_runtime`: Aggregate initiative-local promotion records and approved plan guidance into derived plan/.wt index surfaces.
- `task.plan_promotion_policy_and_guidance_indexes.validate_promotion_and_guidance_lookup`: Add validation coverage proving the new promotion policy registry and aggregate indexes stay aligned with live promotion records and plan/docs guidance.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
