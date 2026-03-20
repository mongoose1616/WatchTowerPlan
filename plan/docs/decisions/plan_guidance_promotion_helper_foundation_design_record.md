---
trace_id: trace.guidance.plan_guidance_promotion_helper_foundation_design_record
id: decision.plan_guidance_promotion_helper_foundation_design_record
title: Guidance Promotion Decision Record
summary: Durable decision record for governed guidance promotion. Defines how validated initiative-local outputs become durable plan guidance without retaining live-package references in the durable document.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-19T10:10:00Z'
audience: shared
authority: authoritative
applies_to:
- plan/docs/decisions/plan_guidance_promotion_helper_foundation_design_record.md
- plan/python/src/watchtower_plan/promotion/service.py
- plan/.wt/registries/promotion_policy_registry.json
- plan/.wt/indexes/guidance_index.json
- plan/.wt/indexes/promotion_index.json
---

# Context

This decision defines how validated initiative-local outputs become durable plan guidance. Durable guidance must survive initiative closeout and purge without keeping source-package paths, source trace IDs, or live promotion records embedded in the document itself.

## Decision

- Durable guidance must be promoted through governed policy, family, and template contracts rather than being copied ad hoc from live initiative inputs.
- Machine-readable promotion and guidance indexes must preserve provenance without forcing durable docs to retain live initiative package references.

## Consequences

- Promotion output stays aligned with machine-readable policy and indexing surfaces.
- Durable guidance can move out of initiative-local planning state without blocking purge of closed initiative packages.
- Future closeout and retention flows can treat promoted docs as authority and initiative artifacts as temporary state.

## Current Status or Supersession Notes

- Active as durable guidance under `plan/docs/**`.
- Promotion policy and promotion-index records carry the machine-readable provenance for this guidance family.
