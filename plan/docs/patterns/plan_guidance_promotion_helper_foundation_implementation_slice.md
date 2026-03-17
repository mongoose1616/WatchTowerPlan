---
trace_id: trace.plan_guidance_promotion_helper_foundation
id: pattern.plan_guidance_promotion_helper_foundation_implementation_slice
title: 'Plan Guidance Promotion Helper Foundation Pattern: Plan Guidance Promotion
  Helper Foundation Implementation Slice'
summary: Promoted pattern extracted from the implementation slice for Plan Guidance
  Promotion Helper Foundation. Adds governed promotion-policy and guidance-promotion
  helpers, then extracts approved initiative-local outputs into durable plan/docs
  guidance surfaces so requirements.md and decisions.md no longer stop at promotion
  shells.
type: pattern
status: active
owner: repository_maintainer
updated_at: '2026-03-17T22:19:46Z'
audience: shared
authority: authoritative
applies_to:
- initiative.plan_guidance_promotion_helper_foundation
- plan/initiatives/plan_guidance_promotion_helper_foundation/implementation_slice.md
- promotion.plan_guidance_promotion_helper_foundation.bootstrap_shell
- plan/.wt/indexes/guidance_index.json
---

# Scenario

Use this pattern when one initiative-local authored input needs to become durable shared guidance without turning `plan/docs/` into a second live workspace. Adds governed promotion-policy and guidance-promotion helpers, then extracts approved initiative-local outputs into durable plan/docs guidance surfaces so requirements.md and decisions.md no longer stop at promotion shells.

## Recommended Structure

- Resolve the promotion policy from source artifact kind and target family.
- Write the durable document under the governed target root with valid front matter and template headings.
- Update the initiative-local promotion record with approval, evidence, and target-path metadata in the same change.

## Boundaries or Constraints

- Promotion is not a substitute for live initiative state or rendered plan views.
- Mirrored foundations must update all required roots in the same change set.

## Usage Notes

- This pattern was promoted from `plan/initiatives/plan_guidance_promotion_helper_foundation/implementation_slice.md` in `Plan Guidance Promotion Helper Foundation`.
- Source initiative: `initiative.plan_guidance_promotion_helper_foundation` (`trace.plan_guidance_promotion_helper_foundation`)
- Source artifact: `plan/initiatives/plan_guidance_promotion_helper_foundation/implementation_slice.md`
- Promotion record: `promotion.plan_guidance_promotion_helper_foundation.bootstrap_shell`
- Evidence refs: `evidence.plan_guidance_promotion_helper_foundation.bootstrap_validation_bundle`

## Illustrative Example

- Promote `plan/initiatives/plan_guidance_promotion_helper_foundation/implementation_slice.md` to `plan/docs/patterns/plan_guidance_promotion_helper_foundation_implementation_slice.md` and keep the promotion record synchronized with the resulting guidance path.
