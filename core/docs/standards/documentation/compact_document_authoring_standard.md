---
id: "std.documentation.compact_document_authoring"
title: "Proportional Document Authoring Standard"
summary: "This standard defines the repository rule that authored documents should include the detail and structure needed for real human review without normalizing low-value boilerplate."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "compact_authoring"
owner: "repository_maintainer"
updated_at: "2026-03-30T05:10:00Z"
audience: "shared"
authority: "authoritative"
---

# Proportional Document Authoring Standard

## Summary
This standard defines the repository rule that authored human-readable documents and generated Markdown outputs must include every materially distinct detail needed for correct interpretation, execution, or review without normalizing low-value boilerplate.

## Purpose
Prevent arbitrary low-count output, symmetry-driven compression, and “short for its own sake” authoring from hiding materially distinct repository detail, while still removing sections or prose that add no non-derivable value.

## Scope
- Applies to repository-authored templates under `core/docs/templates/`.
- Applies to pack-owned rendered trackers and initiative-local or project-local authored planning packages under hosted pack roots such as `<pack>/tracking/`, `<pack>/initiatives/`, and `<pack>/projects/`.
- Applies to generic documentation and workflow guidance when that guidance materially shapes authored output size.
- Does not replace family-specific front matter, traceability, or schema requirements.

## Use When
- Creating or refreshing a repository template.
- Deciding whether a document section should be required, optional, or omitted by default.
- Reviewing whether a generated human-readable output is duplicating machine-readable authority without adding human value.

## Related Standards and Sources
- [front_matter_standard.md](/core/docs/standards/metadata/front_matter_standard.md): proportional authoring must preserve governed front matter where the document family requires machine-readable metadata.
- [workflow_design_standard.md](/core/docs/standards/workflows/workflow_design_standard.md): workflow modules keep their structural sections, but their execution guidance should still prefer proportional repository output.
- Pack-owned task and initiative tracking standards under `<pack>/docs/standards/governance/`: human tracking remains derived from authoritative records, but still needs browseable active and terminal tables.

## Guidance
- Default every authored template to the section set that usually carries the non-derivable value for that family.
- Keep optional sections out of the default body scaffold unless they are needed in most real documents for that family, but add them whenever omission would hide a materially distinct boundary, exception, example, or handoff.
- Document every materially distinct input, assumption, branch, exception, handoff, output, finding, and open question needed for correct interpretation, execution, or review.
- Let section count, bullet count, table count, and example count follow the source material. Do not normalize sibling sections to the same size for convenience or symmetry.
- Do not delete examples, branches, or edge cases merely to keep a document short. Delete only material that adds no non-derivable value for the reader.
- When a document family already has machine-readable front matter or a governed index, do not duplicate that machine detail in verbose body prose unless the duplication materially helps the human reader.
- Prefer section guidance that is proportional to the real material the document needs to carry rather than placeholder inventories or arbitrary caps.
- Treat front matter as the primary machine surface for stable identity, lifecycle state, ownership, and timestamps when the document family uses governed front matter.
- A body `Updated At` section is optional when the family already carries `updated_at` in front matter and `Updated At` in record metadata.
- Generated human-readable trackers should prefer dense tables, clear headings, and explicit zero-state text over placeholder `None` rows or repeated footer prose.
- Summary-first entrypoints are acceptable only when richer companion trackers still expose the underlying terminal and historical rows that humans need for review.
- Do not replace browseable terminal history with count-only summaries when the generated surface can render the rows directly.
- Use tables and section structure deliberately so generated Markdown remains readable as a document, not just as a wrapper around machine output.
- Use ordered lists only when order is semantically required. Otherwise choose the structure that most clearly distinguishes the source material.
- Remove sections, bullets, or notes that restate obvious context without helping review, routing, or execution.

## Operationalization
- `Modes`: `documentation`
- `Operational Surfaces`: `core/docs/templates/`; `core/docs/templates/README.md`; `core/docs/templates/pack/README.md`; `core/docs/references/domain_pack_authoring_reference.md`

## Validation
- Reviewers should reject templates that normalize low-value optional sections into every new document.
- Reviewers should reject authoring guidance that implies a preferred fixed count, “short by default” output, or symmetry-driven compression when the source material requires more detail.
- Reviewers should reject workflow guidance that encourages meta drafting records in repository artifacts when those records do not materially help the project.
- Generated human-readable outputs should stay scan-first, but reviewers should reject output that becomes too shallow to support real human review or omits materially distinct branches, exceptions, or outputs.

## Change Control
- Update this standard together with affected templates, family-specific documentation standards, workflow guidance, and sync renderers when proportional-authoring rules change materially.
- Update validators or index builders in the same change set when a proportional-authoring rule changes the required body shape for a governed family.

## References
- [core/docs/templates/README.md](/core/docs/templates/README.md)
- [front_matter_standard.md](/core/docs/standards/metadata/front_matter_standard.md)
- Pack-owned tracking standards under `<pack>/docs/standards/governance/`

## Updated At
- `2026-03-30T05:10:00Z`
