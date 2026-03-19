---
trace_id: trace.guidance.plan_guidance_promotion_helper_foundation_decision_notes
id: standard.plan_guidance_promotion_helper_foundation_decision_notes
title: Guidance Promotion Standard
summary: Durable operational standard for governed guidance promotion. Defines the required machine contracts and durable-document expectations that allow source initiative packages to be purged cleanly.
type: standard
status: active
owner: repository_maintainer
updated_at: '2026-03-19T10:10:00Z'
audience: shared
authority: authoritative
applies_to:
- plan/docs/standards/plan_guidance_promotion_helper_foundation_decision_notes.md
- core/python/src/watchtower_core/plan_runtime/guidance_promotion.py
- plan/.wt/registries/promotion_policy_registry.json
- plan/.wt/indexes/guidance_index.json
- plan/.wt/indexes/promotion_index.json
---

# Purpose

This standard captures the rule-bearing obligations for durable guidance promotion. Durable guidance should remain authoritative after the source initiative package is closed and purged.

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

- `plan/initiatives/example/decision_notes.md` -> `plan/docs/standards/example_decision_notes.md`

## Notes

- Durable guidance should stand on its own after the source initiative package is closed and purged.
- Promotion indexes carry the machine-readable provenance for the guidance family.
