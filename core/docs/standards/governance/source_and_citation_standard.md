---
id: "std.governance.source_and_citation"
title: "Source And Citation Standard"
summary: "This standard defines shared authority order, citation discipline, and fact-versus-inference expectations for repository work."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "source_and_citation"
owner: "repository_maintainer"
updated_at: "2026-03-27T15:00:00Z"
audience: "shared"
authority: "authoritative"
---

# Source And Citation Standard

## Summary
This standard defines shared authority order, citation discipline, and fact-versus-inference expectations for repository work.

## Purpose
- Keep repository conclusions auditable and explicit about what is observed, inferred, adopted as local policy, or still unknown.
- Prevent raw repo scanning, stale helper docs, and unsupported inference from displacing current governed authority.
- Make source-backed repository guidance easier for humans and agents to apply consistently.

## Scope
- Applies to analysis, standards, references, workflows, command pages, review outputs, and agent guidance that depend on current repository state or external authority.
- Covers authority order, when to use governed lookup surfaces, and how to label claims derived from source material.
- Does not replace narrower document-family structure rules or live pack-machine state contracts.

## Use When
- Writing analysis, findings, recommendations, standards, or gap assessments.
- Distilling external guidance into local references or promoting it into repository policy.
- Designing workflows, AGENTS instructions, command pages, or templates that guide repository discovery or evidence-backed claims.

## Related Standards and Sources
- [AGENTS.md](/AGENTS.md): repository-wide instructions should reinforce the source hierarchy and lookup order defined here.
- [routing_and_context_loading_standard.md](/core/docs/standards/workflows/routing_and_context_loading_standard.md): routed work should load the correct lookup surface before broad scanning.
- [reference_distillation_standard.md](/core/docs/standards/governance/reference_distillation_standard.md): externally governed material should be distilled before it becomes durable local policy.
- [reference_md_standard.md](/core/docs/standards/documentation/reference_md_standard.md): governed references must cite canonical upstream authority and make local mapping explicit.
- [standard_md_standard.md](/core/docs/standards/documentation/standard_md_standard.md): governed standards must keep source authority and applied local implications auditable.
- [current_state_inspection.md](/core/workflows/modules/current_state_inspection.md): current-state review should capture observed facts before recommendation or policy.

## Guidance
- Source authority order is:
  - current machine-readable authority for deterministic state and rules
  - current foundations and standards
  - current governed reference docs, command pages, workflow docs, and README surfaces
  - authoritative external sources when internal guidance is incomplete
  - bounded local inference last
- When the question is which governed surface is canonical, use `watchtower-core query authority` first.
- After authority resolution, use the narrow query surface for the governed family when one exists, then the exact canonical file, and only then raw repo search such as `rg` for unindexed detail or verification.
- Do not present inferred conclusions, recommendations, or open questions as if they were observed current-state facts.
- Distinguish these claim types explicitly when a task makes substantive claims:
  - observed facts
  - inferred implications
  - adopted local policy or recommendation
  - open questions or unknowns
- When a claim depends on current repository state, cite the exact repository path or governed artifact path that supports it.
- When a claim depends on outside authority, cite the canonical upstream source directly or the governed local reference that faithfully distills it.
- Prefer governed local references over scattering raw external URLs across multiple docs once the topic has been distilled locally.
- If a conclusion is not directly observed, state the confidence boundary plainly. Use compact qualifiers such as `confirmed`, `strong inference`, `tentative`, or `unknown` when a review or analysis surface benefits from graded certainty.
- If material uncertainty remains, keep the uncertainty visible instead of smoothing it over with vague summary language.
- When a workflow or AGENTS surface tells contributors how to discover repo facts, point to the governed lookup surface first instead of directing them to broad raw scanning.

## Operationalization
- `Modes`: `workflow`; `documentation`; `review`
- `Operational Surfaces`: `AGENTS.md`; `core/docs/AGENTS.md`; `core/workflows/modules/current_state_inspection.md`; `core/workflows/modules/internal_context_review.md`; `core/workflows/modules/reference_distillation.md`; `core/workflows/modules/documentation_generation.md`; `core/workflows/modules/documentation_refresh.md`; `core/docs/standards/documentation/reference_md_standard.md`; `core/docs/standards/documentation/standard_md_standard.md`; `core/docs/standards/workflows/routing_and_context_loading_standard.md`; `core/docs/standards/workflows/workflow_design_standard.md`; `core/docs/commands/core_python/watchtower_core_query_authority.md`

## Validation
- Source-backed claims include exact repo paths, governed artifact paths, canonical upstream URLs, or governed local references that support the claim.
- Inferences, recommendations, and open questions are not presented as observed facts.
- High-stakes or correctness-sensitive conclusions re-check current governed surfaces before finalization.
- Lookup-order guidance routes readers and agents to governed discovery surfaces before raw repo search when those lookup surfaces exist.

## Change Control
- Update companion AGENTS files, workflow modules, and document-family standards in the same change when the source hierarchy or claim-labeling model changes.
- Update the authority map and command docs in the same change when the canonical shared lookup order changes materially.

## References
- [AGENTS.md](/AGENTS.md)
- [current_state_inspection.md](/core/workflows/modules/current_state_inspection.md)
- [internal_context_review.md](/core/workflows/modules/internal_context_review.md)
- [reference_distillation_standard.md](/core/docs/standards/governance/reference_distillation_standard.md)

## Updated At
- `2026-03-27T15:00:00Z`
