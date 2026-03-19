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
- plan/docs/standards/governance/plan_guidance_promotion_helper_foundation_decision_notes.md
- core/python/src/watchtower_core/plan_runtime/guidance_promotion.py
- plan/.wt/registries/promotion_policy_registry.json
- plan/.wt/indexes/guidance_index.json
- plan/.wt/indexes/promotion_index.json
---

# Guidance Promotion Standard

## Summary

Durable operational standard for governed guidance promotion. Defines the required machine contracts and durable-document expectations that allow source initiative packages to be purged cleanly.

## Purpose

Define the rule-bearing obligations for governed promotion of initiative-local authored inputs into durable plan guidance.

## Scope

- Applies to pack-wide and project-scoped initiatives that promote implementation slices or decision notes into durable plan-domain standards.
- Applies to the promotion runtime, policy registry, guidance index, promotion index, and the promoted standard documents written under `plan/docs/standards/**`.
- Does not replace the live initiative package as the execution workspace before promotion approval.

## Use When

- Promoting initiative-local authored inputs into durable plan-domain standards.
- Reviewing whether a promoted standard remains authoritative after the source initiative package is closed and purged.
- Auditing whether the machine-readable promotion policy and index surfaces still match the promoted standard outputs.

## Related Standards and Sources

- [standard_md_standard.md](/core/docs/standards/documentation/standard_md_standard.md): promoted standards under `plan/docs/standards/**` must satisfy the governed standard-document contract instead of using a reduced template-only shape.
- [planning_retention_and_purge_standard.md](/plan/docs/standards/governance/planning_retention_and_purge_standard.md): durable guidance must remain authoritative after initiative packages are eligible for purge.
- [guidance_promotion.py](/core/python/src/watchtower_core/plan_runtime/guidance_promotion.py): the promotion runtime must route outputs into governed roots and keep rendered documents aligned with the active validators.
- [promotion_policy_registry.json](/plan/.wt/registries/promotion_policy_registry.json): the promotion policy registry defines the sanctioned target family, root, review path, provenance, and mirror behavior.

## Guidance

- Require one governed promotion record with source, evidence, approval, and target-path metadata before durable promotion writes occur.
- Require promoted standards to land under a governed standards category path instead of directly under the `plan/docs/standards/` root.
- Require promoted standards to remain self-contained and validator-compliant so they can outlive the source initiative package cleanly.
- Do not promote durable standards directly into `plan/docs/**` without a recorded initiative-local promotion artifact and synchronized machine indexes.

## Operationalization

- `Modes`: `documentation`; `sync`; `validation`
- `Operational Surfaces`: `plan/docs/standards/governance/plan_guidance_promotion_helper_foundation_decision_notes.md`; `core/python/src/watchtower_core/plan_runtime/guidance_promotion.py`; `plan/.wt/registries/promotion_policy_registry.json`; `plan/.wt/indexes/guidance_index.json`; `plan/.wt/indexes/promotion_index.json`

## Validation

- Promotion records and promoted standard docs should pass schema-backed validation before closeout.
- Promoted standards should rebuild the guidance and promotion indexes cleanly in the same change set.
- Reviewers should reject promoted standards that bypass the governed category structure or fail the standard-document contract.

## Change Control

- Update this standard when promotion policy, durable target roots, or standard-document requirements change materially.
- Update the promotion runtime, promotion policy registry, guidance index, promotion index, and affected promoted docs in the same change set when this contract changes.

## References

- [standard_md_standard.md](/core/docs/standards/documentation/standard_md_standard.md)
- [planning_retention_and_purge_standard.md](/plan/docs/standards/governance/planning_retention_and_purge_standard.md)
- [promotion_policy_registry.json](/plan/.wt/registries/promotion_policy_registry.json)
- [guidance_index.json](/plan/.wt/indexes/guidance_index.json)
- [promotion_index.json](/plan/.wt/indexes/promotion_index.json)

## Updated At

- `2026-03-19T10:10:00Z`
