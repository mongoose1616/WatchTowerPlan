---
trace_id: trace.plan_guidance_promotion_helper_foundation
id: standard.plan_guidance_promotion_helper_foundation_decision_notes
title: 'Plan Guidance Promotion Helper Foundation Standard: Plan Guidance Promotion
  Helper Foundation Decision Notes'
summary: Promoted standard extracted from the decision notes for Plan Guidance Promotion
  Helper Foundation. Optional decision notes seeded during initiative bootstrap.
type: standard
status: active
owner: repository_maintainer
updated_at: '2026-03-17T22:19:46Z'
audience: shared
authority: authoritative
applies_to:
- initiative.plan_guidance_promotion_helper_foundation
- plan/initiatives/plan_guidance_promotion_helper_foundation/decision_notes.md
- promotion.plan_guidance_promotion_helper_foundation.bootstrap_shell
- plan/.wt/indexes/guidance_index.json
---

# Purpose

This standard captures the rule-bearing obligations for durable guidance promotion proven by `Plan Guidance Promotion Helper Foundation`. Optional decision notes seeded during initiative bootstrap.

## Applicability

- Applies when initiative-local outputs are promoted into `plan/docs/**` guidance roots.
- Applies to both pack-wide and project-scoped initiatives when promotion records exist.

## Required or Prohibited Rules

- Require one governed promotion record with source, evidence, approval, and target-path metadata.
- Require target roots and mirror behavior to match the active promotion policy registry.
- Do not promote durable guidance directly into `plan/docs/**` without a recorded initiative-local promotion artifact.

## Enforcement or Validation Implications

- Promotion records and promoted docs must pass schema-backed validation.
- Guidance and promotion indexes must rebuild cleanly after promotion.

## Examples

- `plan/initiatives/plan_guidance_promotion_helper_foundation/decision_notes.md` -> `plan/docs/standards/plan_guidance_promotion_helper_foundation_decision_notes.md`

## Notes

- Source initiative: `initiative.plan_guidance_promotion_helper_foundation` (`trace.plan_guidance_promotion_helper_foundation`)
- Source artifact: `plan/initiatives/plan_guidance_promotion_helper_foundation/decision_notes.md`
- Promotion record: `promotion.plan_guidance_promotion_helper_foundation.bootstrap_shell`
- Evidence refs: `evidence.plan_guidance_promotion_helper_foundation.bootstrap_validation_bundle`
