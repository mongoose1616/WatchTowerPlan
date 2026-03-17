# Plan Guidance Promotion Helper Foundation Implementation Slice

## Summary
Adds governed promotion-policy and guidance-promotion helpers, then extracts approved initiative-local outputs into durable plan/docs guidance surfaces so requirements.md and decisions.md no longer stop at promotion shells.

## Initial Work Breakdown
- `task.plan_guidance_promotion_helper_foundation.publish_promotion_helper_contracts`: Add typed promotion-policy and guidance-promotion helper contracts for governed extraction flows.
- `task.plan_guidance_promotion_helper_foundation.implement_governed_guidance_promotion_flow`: Promote approved initiative outputs into plan/docs guidance roots with policy, template, and mirror enforcement.
- `task.plan_guidance_promotion_helper_foundation.validate_promoted_guidance_extraction_and_requirements_alignment`: Add coverage for promotion output, mirror handling, and touched requirements rows.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
