---
id: "std.documentation.reference_md"
title: "Reference Document Standard"
summary: "This standard defines the role, structure, and quality expectations for reference documents, especially external reference documents under `docs/references/**`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "reference_md"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
---

# Reference Document Standard

## Summary
This standard defines the role, structure, and quality expectations for reference documents, especially external reference documents under `docs/references/**`.

## Purpose
Keep reference documents focused on durable lookup content by separating reader-facing reference material from authoring workflows, lifecycle checks, and broader process guidance.

## Scope
- Applies to reference documents in this repository, including external reference documents under `docs/references/**`.
- Covers what belongs in a reference document, what should stay optional, and what should be enforced by workflows or standards instead of the document body.
- Does not define the full authoring workflow for all documentation types.

## Use When
- Creating a new reference document.
- Refreshing an existing reference document.
- Reviewing whether a reference document is properly scoped and structured.

## Related Standards and Sources
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md): authoring scaffold that should stay aligned with this standard.
- [documentation_generation.md](/home/j/WatchTowerPlan/workflows/modules/documentation_generation.md): workflow surface that operationalizes or depends on this standard.
- [documentation_refresh.md](/home/j/WatchTowerPlan/workflows/modules/documentation_refresh.md): workflow surface that operationalizes or depends on this standard.
## Guidance
- A reference document should optimize for fast lookup, stable terminology, and clear local application.
- A reference document should cover one succinct standard, framework, format, specification, or working model.
- Use the reference template when creating new reference documents.
- When external published guidance materially shapes repository standards or design documents, prefer distilling it into `docs/references/**` and citing the local reference doc as the repo-native lookup surface rather than scattering raw vendor URLs across multiple docs.
- Include `Canonical Upstream` when the topic depends on authoritative external sources.
- Include `Local Mapping in This Repository` when the external topic needs a concrete connection to repository surfaces.
- Omit generic reader-orientation sections such as `Audience` and `Use When` unless a specific reference truly needs them to avoid ambiguity.
- `Quick Reference or Distilled Reference` should be useful enough that the reader can answer the common practical questions without immediately leaving the repo for the upstream source.
- `Quick Reference or Distilled Reference` is the core deliverable of a reference document, not filler between the summary and the link list.
- Prefer concrete lookup density over abstract summary. Use rules, decision points, field tables, syntax, examples, defaults, and pitfalls where they materially help.
- A reference that mostly restates scope and then points the reader to upstream links should be treated as incomplete.
- Avoid leaving the dense reference section as only a short `Core Guidance` summary unless the topic is so small that anything denser would be artificial.
- For topics with correctness, security, interoperability, parsing, storage, data-loss, or configuration risk, the quick-reference section should surface defaults, unsafe assumptions, disallowed patterns, edge cases, and failure modes explicitly.
- If the upstream source leaves material ambiguity, the reference should name the ambiguity and the local interpretation boundary instead of hiding it behind vague summary language.
- Keep process guidance brief and limited to how the reader should apply the reference locally.
- Keep examples focused on correct local use rather than broad tutorials.
- Keep lifecycle checks, refresh steps, change-control notes, and authoring checklists in documentation workflows or standards rather than in the reference document body.
- Use `Updated At` in the document body when the topic depends on time-sensitive or version-sensitive source material, and record it as an RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`.
- Update the governed reference index in the same change set when a reference document is added, renamed, removed, or materially retargeted.

## Structure or Data Model
- Title
- `Summary`
- `Purpose`
- `Scope`
- `Canonical Upstream` when applicable
- `Related Standards and Sources`
- `Quick Reference or Distilled Reference`
- `Local Mapping in This Repository`
- `Process or Workflow` when useful
- `Examples`
- `References`
- `Tooling and Automation` when useful
- `Notes` when useful
- `Updated At`

## Validation
- The document should be easy to scan as a lookup artifact.
- The document should stay focused on one topic and should not sprawl into a survey of loosely related subjects.
- Canonical upstream links should be present when the topic depends on external authority.
- Local mappings should point to real repository surfaces when they are included.
- The quick-reference section should contain concrete lookup content rather than only high-level summary language.
- The reader should be able to resolve the common local questions from the reference doc without needing the upstream source for every basic decision.
- Reviewers should reject references whose quick-reference section could be replaced by a bare link list without meaningful loss of information.
- For high-stakes or easy-to-misread topics, the reference should expose ambiguity, unsafe defaults, or important edge cases clearly enough that the reader does not need to rediscover them from scratch.
- The document should not contain embedded lifecycle sections or authoring-only checklist content that belongs in workflows or standards.

## Change Control
- Update this standard when the repository’s reference-document model changes materially.
- Update the reference template, the reference-index standard, and affected reference documents in the same change set when structural expectations change.
- Update documentation workflows in the same change set when reference-quality checks move between document bodies and workflow procedures.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md)
- [documentation_generation.md](/home/j/WatchTowerPlan/workflows/modules/documentation_generation.md)
- [documentation_refresh.md](/home/j/WatchTowerPlan/workflows/modules/documentation_refresh.md)

## Notes
- A good reference document helps the reader find stable facts quickly.
- If a document’s main value is action sequencing or concept explanation, it should probably not be a reference document.

## Updated At
- `2026-03-09T23:02:08Z`
