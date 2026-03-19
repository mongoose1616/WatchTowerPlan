---
trace_id: trace.guidance.plan_guidance_promotion_helper_foundation_initiative_brief
id: reference.plan_guidance_promotion_helper_foundation_initiative_brief
title: Guidance Promotion Reference
summary: Durable reference for governed guidance promotion. Describes how initiative-local authored inputs become durable plan guidance while provenance lives in machine indexes rather than in source-package references.
type: reference
status: active
owner: repository_maintainer
updated_at: '2026-03-19T10:10:00Z'
audience: shared
authority: reference
applies_to:
- plan/docs/references/plan_guidance_promotion_helper_foundation_initiative_brief.md
- core/python/src/watchtower_core/plan_runtime/guidance_promotion.py
- plan/.wt/registries/promotion_policy_registry.json
- plan/.wt/indexes/guidance_index.json
- plan/.wt/indexes/promotion_index.json
tags:
- promoted_guidance
- reference
- guidance_promotion
- initiative_brief
---

# Subject Summary

This reference captures the durable operating model for governed guidance promotion. Use it when initiative-local authored inputs need to become durable plan guidance without leaving live-package references embedded in the resulting document.

## Usage Guidance

- Use this reference when implementing or reviewing promotion of initiative-local inputs into `plan/docs/**`.
- Treat `plan/.wt/registries/promotion_policy_registry.json`, `plan/.wt/indexes/guidance_index.json`, and `plan/.wt/indexes/promotion_index.json` as the machine companions for this document.

## Boundaries

- Durable guidance belongs in `plan/docs/**`.
- Live execution state, closeout artifacts, and evidence bundles remain under initiative-local `plan/**` roots.

## Related Surfaces

- `plan/docs/references/plan_guidance_promotion_helper_foundation_initiative_brief.md`
- `core/python/src/watchtower_core/plan_runtime/guidance_promotion.py`
- `plan/.wt/indexes/guidance_index.json`
- `plan/.wt/indexes/promotion_index.json`

## Notes

- Keep this document durable; initiative-local authored inputs are temporary proof surfaces, not long-term guidance roots.
