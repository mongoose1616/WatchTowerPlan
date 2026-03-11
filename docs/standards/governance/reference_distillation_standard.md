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
updated_at: "2026-03-11T06:00:00Z"
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
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md): authoring scaffold that should stay aligned with this standard.
- [reference_distillation.md](/home/j/WatchTowerPlan/workflows/modules/reference_distillation.md): workflow surface that operationalizes or depends on this standard.
- [documentation_generation.md](/home/j/WatchTowerPlan/workflows/modules/documentation_generation.md): workflow surface that operationalizes or depends on this standard.
- [documentation_refresh.md](/home/j/WatchTowerPlan/workflows/modules/documentation_refresh.md): workflow surface that operationalizes or depends on this standard.

## Guidance
- Prefer authoritative primary sources over secondhand summaries when the topic is standards-driven, version-sensitive, or materially affects repository behavior.
- Always capture the canonical upstream source for externally governed topics.
- Record the relevant version, baseline, publication date, or last-checked date when the source is time-sensitive or version-sensitive.
- Keep each distillation focused on one succinct external topic rather than mixing multiple unrelated standards or frameworks into one artifact.
- Separate three concerns clearly:
  - external source facts or rules
  - local interpretation or mapping
  - normative repository policy
- Keep supporting lookup content in `docs/references/**` when the output is mainly a reusable working reference.
- Make the distilled reference operationally sufficient for repeated repository use. Future readers should not need to reopen the upstream source for every common question or basic decision.
- Do not collapse a local reference into a bibliography or link index. A distilled reference should carry concrete working content, not just source attribution.
- Move normative repository rules into `docs/standards/**` when the repository is adopting, narrowing, or enforcing the distilled guidance as local policy.
- Use the reference template and reference-document standard when the output is a reference document.
- When the output becomes a governed reference under `docs/references/**`, apply the front matter standard and the reference front matter profile in the same change set.
- Preserve the meaning of the source material without copying long passages into the repository.
- Use repository-native terminology and examples when mapping the source locally, but do not rewrite the source so aggressively that the original meaning becomes unclear.
- Distill the practical content that repeated readers will actually need: key terms, required or disallowed patterns, defaults, decision boundaries, edge cases, and common failure modes when the topic warrants them.
- Include a concrete local mapping to real repository surfaces when the distilled guidance affects workflows, standards, templates, architecture, tooling, or implementation patterns.
- If the upstream source is incomplete, conflicting, ambiguous, or not directly applicable, record the uncertainty explicitly rather than normalizing it into false certainty.
- For high-stakes or easy-to-misread topics such as security controls, parsing rules, timestamps, identifiers, storage behavior, schema contracts, or tooling configuration, make non-obvious constraints and unsafe assumptions explicit in the distillation.
- If ambiguity remains material after source review, route to clarification or decision capture instead of burying the unresolved interpretation inside the distillation.
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

## Process or Workflow
1. Choose the correct output boundary before drafting.
   - Use `docs/references/**` for supporting lookup guidance.
   - Use `docs/standards/**` when the repository is adopting or enforcing the guidance as local policy.
2. Keep source facts, local mapping, and normative repository policy visibly separate.
3. Carry forward the required companion standards for the chosen output shape.
   - Apply the reference-document standard, reference template, and front matter standard when the result is a governed reference.
   - Apply the relevant local standards and companion workflows when the result changes repository policy.
4. Record canonical upstream sources plus version, baseline, or date context when those details materially affect interpretation.
5. Update affected standards, references, templates, or workflows in the same change set when the distillation changes effective local guidance.

## Operationalization
- `Modes`: `workflow`; `documentation`
- `Operational Surfaces`: `workflows/modules/documentation_refresh.md`; `workflows/modules/reference_distillation.md`; `workflows/modules/documentation_generation.md`; `docs/templates/reference_template.md`

## Validation
- The distilled artifact points to the canonical upstream source when the topic depends on external authority.
- Version-sensitive or time-sensitive topics include enough baseline information to keep the distillation interpretable later.
- The distillation preserves the source meaning without copying large source passages into the repository.
- The distilled reference is dense enough to answer the recurring practical questions rather than only pointing the reader to upstream links.
- Local interpretation is distinguished clearly from direct source guidance.
- Normative repository policy is not left only inside a reference artifact when the repository is actually enforcing it.
- Local mappings point to real repository surfaces rather than abstract placeholders.
- Unresolved ambiguity, source conflict, or known uncertainty is called out explicitly.
- Reviewers should reject distillations that are effectively link-only or that omit material ambiguity for a topic where misinterpretation could be risky.
- The result is concise enough to maintain and useful enough that future contributors do not need to re-derive the same interpretation from scratch.

## Change Control
- Update this standard when the repository changes how external source material is distilled or promoted into local policy.
- Update the reference-distillation workflow, reference template, and affected reference or standards documents in the same change set when this standard changes materially.
- Refresh affected local references or standards when upstream source material changes in ways that materially affect local guidance.

## References
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md)
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [reference_distillation.md](/home/j/WatchTowerPlan/workflows/modules/reference_distillation.md)
- [diataxis_local_reference.md](/home/j/WatchTowerPlan/docs/references/diataxis_local_reference.md)

## Notes
- Distillation is not the same as policy adoption. A local reference may summarize an external source without making every part of that source a mandatory repository rule.
- A good distillation reduces repeat research while keeping the reader one step away from the canonical upstream source when deeper detail is needed.

## Refresh Procedure
1. Re-check whether the canonical upstream links, version notes, and local mappings are still accurate.
2. Update affected references, standards, workflows, or templates when the upstream change materially affects local guidance.
3. Re-read the distilled output to confirm that source facts, local interpretation, and normative repository policy are still clearly separated.

## Updated At
- `2026-03-11T06:00:00Z`
