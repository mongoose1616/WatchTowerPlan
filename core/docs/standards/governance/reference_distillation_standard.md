---
id: "std.governance.reference_distillation"
title: "Reference Distillation Standard"
summary: "This standard defines how externally published source material is distilled into durable local reference guidance and, when needed, translated into explicit repository policy."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "reference_distillation"
owner: "repository_maintainer"
updated_at: "2026-03-30T05:10:00Z"
audience: "shared"
authority: "authoritative"
---

# Reference Distillation Standard

## Summary
This standard defines how externally published source material is distilled into durable local reference guidance and, when needed, translated into explicit repository policy.

## Purpose
- Prevent raw research notes, copied source blobs, and unstable interpretations from becoming de facto repository guidance.
- Keep a clear boundary between external source material, local distilled references, and normative repository standards.
- Make local reference distillations accurate, attributable, maintainable, and useful without requiring repeated browsing for the same practical questions.

## Scope
- Applies when external standards, specifications, framework guidance, vendor documentation, or other published source material is converted into local repository references or used to shape local standards.
- Covers source selection, attribution, version or baseline capture, local mapping, policy separation, and refresh expectations.
- Does not define the full document structure for references or the full execution workflow for documentation work.

## Use When
- Creating a new local reference from external source material.
- Refreshing an existing distilled reference after upstream or repository changes.
- Reviewing whether a repository reference faithfully represents external source material.
- Turning repeated research on an external topic into a durable repository artifact.

## Related Standards and Sources
- [front_matter_standard.md](/core/docs/standards/metadata/front_matter_standard.md): governed references and standards still need the correct metadata contracts when distillation becomes a durable repository document.
- [reference_md_standard.md](/core/docs/standards/documentation/reference_md_standard.md): distilled external guidance should land in the governed reference family when the output is a reusable lookup surface.
- [source_and_citation_standard.md](/core/docs/standards/governance/source_and_citation_standard.md): distillation must keep observed source facts, local mapping, and adopted policy clearly separated.
- [reference_template.md](/core/docs/templates/reference_template.md): authoring scaffold that should stay aligned with this standard.
- [external_guidance_research.md](/core/workflows/modules/external_guidance_research.md): upstream research should narrow the open question before distillation begins.
- [reference_distillation.md](/core/workflows/modules/reference_distillation.md): workflow surface that operationalizes this standard.
- [documentation_generation.md](/core/workflows/modules/documentation_generation.md): use this after distillation when the result becomes a new durable repository document.

## Guidance
- Prefer authoritative primary sources over secondhand summaries when the topic is standards-driven, version-sensitive, or materially affects repository behavior.
- Always capture the canonical upstream source for externally governed topics.
- Record the relevant version, baseline, publication date, or last-checked date when the source is time-sensitive or version-sensitive.
- Keep each distillation bounded to one external topic or tightly related topic cluster rather than mixing multiple unrelated standards or frameworks into one artifact.
- Separate three concerns clearly:
  - external source facts or rules
  - local interpretation or mapping
  - normative repository policy
- Keep supporting lookup content in `core/docs/references/**` when the output is shared or cross-pack, or in the owning pack's references root when the output is pack-applied.
- Shared core may retain external reference topics when they support reusable-core behavior or multiple hosted packs.
- Owning packs may intentionally publish the same upstream topic as a pack-owned reference when the local operator mapping, touchpoints, or enforcement posture differ materially from the shared-core reference.
- Make the distilled reference operationally sufficient for repeated repository use. Future readers should not need to reopen the upstream source for every common question or basic decision.
- Do not collapse a local reference into a bibliography or link index. A distilled reference should carry concrete working content, not just source attribution.
- Move normative repository rules into `core/docs/standards/**` or the owning pack's `docs/standards/**` when the repository is adopting, narrowing, or enforcing the distilled guidance as local policy.
- Use the reference template and reference-document standard when the output is a reference document.
- Preserve the meaning of the source material without copying long passages into the repository.
- Use repository-native terminology and examples when mapping the source locally, but do not rewrite the source so aggressively that the original meaning becomes unclear.
- Distill the practical content that repeated readers will actually need: key terms, required or disallowed patterns, defaults, decision boundaries, edge cases, and common failure modes when the topic warrants them.
- Do not suppress materially distinct upstream exceptions, ambiguities, or decision branches just to keep the distilled output short.
- Include a concrete local mapping to real repository surfaces when the distilled guidance affects workflows, standards, templates, architecture, tooling, or implementation patterns.
- If the upstream source is incomplete, conflicting, ambiguous, or not directly applicable, record the uncertainty explicitly rather than normalizing it into false certainty.
- If ambiguity remains material after source review, route to clarification or decision capture instead of burying the unresolved interpretation inside the distillation.
- When durable outside guidance becomes repository-local policy, flow it through `external_guidance_research.md`, then `reference_distillation.md`, then `documentation_generation.md` or `documentation_refresh.md` rather than skipping directly from one-off research into a standard.
- When a distillation changes the effective local guidance, update affected standards, workflows, templates, or companion references in the same change set when practical.

## Structure or Data Model
- Distillation goal or target question
- Source scope boundary
- Canonical upstream sources
- Source version, baseline, or last-checked notes when relevant
- Distilled rules, decision points, or lookup guidance
- Local mapping in this repository
- Local policy differences, narrowing, or adoption notes when applicable
- Open questions, ambiguity, or confidence notes
- Related repository artifacts affected by the distillation

## Operationalization
- `Modes`: `workflow`; `documentation`
- `Operational Surfaces`: `core/workflows/modules/external_guidance_research.md`; `core/workflows/modules/reference_distillation.md`; `core/workflows/modules/documentation_generation.md`; `core/workflows/modules/documentation_refresh.md`; `core/docs/templates/reference_template.md`; `core/docs/standards/documentation/reference_md_standard.md`

## Validation
- The distilled artifact points to the canonical upstream source when the topic depends on external authority.
- Version-sensitive or time-sensitive topics include enough baseline information to keep the distillation interpretable later.
- The distillation preserves the source meaning without copying large source passages into the repository.
- The distilled reference is dense enough to answer recurring practical questions rather than only pointing the reader to upstream links.
- Local interpretation is distinguished clearly from direct source guidance.
- Normative repository policy is not left only inside a reference artifact when the repository is actually enforcing it.
- Local mappings point to real repository surfaces rather than abstract placeholders.
- Unresolved ambiguity, source conflict, or known uncertainty is called out explicitly.
- Reviewers should reject distillations that are effectively link-only or that omit material ambiguity for a topic where misinterpretation could be risky.

## Change Control
- Update this standard when the repository changes how external source material is distilled or promoted into local policy.
- Update the reference-distillation workflow, reference template, and affected reference or standards documents in the same change set when this standard changes materially.
- Refresh affected local references or standards when upstream source material changes in ways that materially affect local guidance.

## References
- [reference_md_standard.md](/core/docs/standards/documentation/reference_md_standard.md)
- [reference_template.md](/core/docs/templates/reference_template.md)
- [reference_distillation.md](/core/workflows/modules/reference_distillation.md)
- [external_guidance_research.md](/core/workflows/modules/external_guidance_research.md)
- [documentation_generation.md](/core/workflows/modules/documentation_generation.md)

## Notes
- Distillation is not the same as policy adoption. A local reference may summarize an external source without making every part of that source a mandatory repository rule.
- A good distillation reduces repeat research while keeping the reader one step away from the canonical upstream source when deeper detail is needed.

## Updated At
- `2026-03-30T05:10:00Z`
