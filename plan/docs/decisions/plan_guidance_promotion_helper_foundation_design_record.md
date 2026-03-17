---
trace_id: trace.plan_guidance_promotion_helper_foundation
id: decision.plan_guidance_promotion_helper_foundation_design_record
title: 'Plan Guidance Promotion Helper Foundation Decision Record: Plan Guidance Promotion
  Helper Foundation Design Record'
summary: Promoted decision record extracted from the design record for Plan Guidance
  Promotion Helper Foundation. Adds governed promotion-policy and guidance-promotion
  helpers, then extracts approved initiative-local outputs into durable plan/docs
  guidance surfaces so requirements.md and decisions.md no longer stop at promotion
  shells.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-17T22:19:46Z'
audience: shared
authority: authoritative
applies_to:
- initiative.plan_guidance_promotion_helper_foundation
- plan/initiatives/plan_guidance_promotion_helper_foundation/design_record.md
- promotion.plan_guidance_promotion_helper_foundation.bootstrap_shell
- plan/.wt/indexes/guidance_index.json
---

# Context

`Plan Guidance Promotion Helper Foundation` required a durable decision about how live initiative outputs become approved guidance. Adds governed promotion-policy and guidance-promotion helpers, then extracts approved initiative-local outputs into durable plan/docs guidance surfaces so requirements.md and decisions.md no longer stop at promotion shells.

## Decision

- Durable guidance must be promoted through governed policy, family, and template contracts rather than being copied ad hoc from live initiative inputs.
- Promotion records must retain source initiative, evidence, review, and target-path provenance.

## Consequences

- Promotion output stays aligned with machine-readable policy and indexing surfaces.
- Durable guidance can move out of initiative-local planning state without losing traceability.
- Future closeout and retention flows can treat promoted docs as authority and initiative artifacts as temporary state.

## Current Status or Supersession Notes

- Active via `promotion.plan_guidance_promotion_helper_foundation.bootstrap_shell`.
- Source initiative: `initiative.plan_guidance_promotion_helper_foundation` (`trace.plan_guidance_promotion_helper_foundation`)
- Source artifact: `plan/initiatives/plan_guidance_promotion_helper_foundation/design_record.md`
- Promotion record: `promotion.plan_guidance_promotion_helper_foundation.bootstrap_shell`
- Evidence refs: `evidence.plan_guidance_promotion_helper_foundation.bootstrap_validation_bundle`
