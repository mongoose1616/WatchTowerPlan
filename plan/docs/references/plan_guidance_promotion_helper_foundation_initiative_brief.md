---
id: reference.plan_guidance_promotion_helper_foundation_initiative_brief
title: Guidance Promotion Reference
summary: Durable reference for governed guidance promotion. Describes how initiative-local authored inputs become durable plan guidance while provenance lives in machine indexes rather than in source-package references.
type: reference
status: active
owner: repository_maintainer
updated_at: '2026-03-28T23:55:00Z'
audience: shared
authority: reference
applies_to:
- plan/python/src/watchtower_plan/promotion/service.py
- plan/.wt/registries/promotion_policy_registry.json
- plan/.wt/indexes/guidance_index.json
- plan/.wt/indexes/promotion_index.json
tags:
- promoted_guidance
- reference
- guidance_promotion
- initiative_brief
---

# Guidance Promotion Reference

This reference captures the durable operating model for governed guidance promotion. Use it when initiative-local authored inputs need to become durable plan guidance without leaving live-package references embedded in the resulting document.

## Canonical Upstream

- [Guidance promotion service](https://github.com/mongoose1616/WatchTowerPlan/blob/HEAD/plan/python/src/watchtower_plan/promotion/service.py)
- [Promotion policy registry](https://github.com/mongoose1616/WatchTowerPlan/blob/HEAD/plan/.wt/registries/promotion_policy_registry.json)

## Quick Reference or Distilled Reference

- The promotion model turns initiative-local authored inputs into durable
  `plan/docs/**` guidance while keeping promotion provenance and execution state
  in machine indexes rather than in the promoted document body.
- Treat the promotion service and policy registry as the source of truth for
  what can be promoted, while this reference explains the durable operating
  boundary for reviewers and maintainers.

### Usage Guidance

- Use this reference when implementing or reviewing promotion of initiative-local inputs into `plan/docs/**`.
- Treat `plan/.wt/registries/promotion_policy_registry.json`, `plan/.wt/indexes/guidance_index.json`, and `plan/.wt/indexes/promotion_index.json` as the machine companions for this document.

### Boundaries

- Durable guidance belongs in `plan/docs/**`.
- Live execution state, closeout artifacts, and evidence bundles remain under initiative-local `plan/**` roots.

## Local Mapping in This Repository

### Current Repository Status

- Supporting authority for current plan guidance-promotion policy, machine
  provenance, and durable documentation layout decisions.

### Current Touchpoints

- `plan/python/src/watchtower_plan/promotion/service.py`
- `plan/.wt/registries/promotion_policy_registry.json`
- `plan/.wt/indexes/guidance_index.json`
- `plan/.wt/indexes/promotion_index.json`

### Why It Matters Here

- Reviewers need one durable description of why promoted guidance belongs under
  `plan/docs/**` while promotion provenance remains in the machine surfaces.
- The reference keeps that operating model stable even as initiative-local
  authored inputs and promotion runs change over time.

### If Local Policy Tightens

- Update `plan/python/src/watchtower_plan/promotion/service.py`,
  `plan/.wt/registries/promotion_policy_registry.json`, and the affected
  guidance-index surfaces in the same change set when promotion eligibility,
  provenance requirements, or destination rules change materially.

## References

- [Guidance promotion service](https://github.com/mongoose1616/WatchTowerPlan/blob/HEAD/plan/python/src/watchtower_plan/promotion/service.py)
- [Promotion policy registry](https://github.com/mongoose1616/WatchTowerPlan/blob/HEAD/plan/.wt/registries/promotion_policy_registry.json)
- `plan/.wt/indexes/guidance_index.json`
- `plan/.wt/indexes/promotion_index.json`

## Notes

- Keep this document durable; initiative-local authored inputs are temporary proof surfaces, not long-term guidance roots.

## Updated At

- `2026-03-28T23:55:00Z`
