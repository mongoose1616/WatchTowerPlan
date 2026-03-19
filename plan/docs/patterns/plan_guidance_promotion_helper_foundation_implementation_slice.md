---
trace_id: trace.guidance.plan_guidance_promotion_helper_foundation_implementation_slice
id: pattern.plan_guidance_promotion_helper_foundation_implementation_slice
title: 'Guidance Promotion Pattern: Implementation Slice'
summary: Durable pattern for governed guidance promotion. Shows how validated initiative-local authored inputs become self-contained plan guidance without preserving source-package references in the guidance body.
type: pattern
status: active
owner: repository_maintainer
updated_at: '2026-03-19T10:10:00Z'
audience: shared
authority: authoritative
applies_to:
- plan/docs/patterns/plan_guidance_promotion_helper_foundation_implementation_slice.md
- core/python/src/watchtower_core/plan_runtime/guidance_promotion.py
- plan/.wt/registries/promotion_policy_registry.json
- plan/.wt/indexes/guidance_index.json
- plan/.wt/indexes/promotion_index.json
---

# Scenario

Use this pattern when one initiative-local authored input needs to become durable shared guidance without turning `plan/docs/` into a second live workspace. Promotion should yield a self-contained durable document while the machine indexes retain provenance and review history.

## Recommended Structure

- Resolve the promotion policy from source artifact kind and target family.
- Write the durable document under the governed target root with valid front matter and template headings.
- Rebuild the guidance and promotion indexes in the same change.

## Boundaries or Constraints

- Promotion is not a substitute for live initiative state or rendered plan views.
- Mirrored foundations must update all required roots in the same change set.

## Usage Notes

- Use this pattern for implementation-slice promotion into durable guidance families.
- Keep durable guidance self-contained and rely on machine indexes for provenance.

## Illustrative Example

- Promote a validated initiative-local implementation slice into `plan/docs/patterns/` and keep the guidance and promotion indexes synchronized with the result.
