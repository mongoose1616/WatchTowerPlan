---
id: "<document_id>"
title: "<Document Title>"
summary: "<One-sentence description.>"
type: "<document_type>"
status: "<document_status>"
tags:
  - "<tag>"
owner: "<document_owner>"
updated: "YYYY-MM-DD"
audience: "<document_audience>"
authority: "<document_authority>"
applies_to:
  - "<repo-surface-or-concept>"
aliases:
  - "<alternate_term>"
---

# <Document Title>

> Use this template for standards, guides, design docs, reference docs, local working references, and overview docs.
> Keep the sections that apply, rename sections when needed, and delete any section that does not fit the document.
> Write the document as native to this repository rather than as a description of where the idea came from.
> Keep the YAML front matter when the document family requires governed metadata or when metadata is operationally useful. Delete it otherwise.
> If you keep front matter, align the keys and allowed values with [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md) and the matching document-family profile.
> Delete any front matter keys that the chosen profile does not permit.
> Add an `Inputs` section only when the document needs an explicit dependency list that is not already clear from `Use When`, `Related Standards and Sources`, or the artifact model itself.

## Summary
<Give a short plain-language explanation of what this document is for and how it should be used.>

## Choose a Shape
- Use the structured authority sections below for standards, policies, specs, operational docs, and other documents that define rules or process.
- Use the reference sections for local working references, concise standards summaries, terminology guides, and lookup docs that support this repo.
- Use the scoped application sections at the bottom for overview docs that explain how the same concept applies to `Core`, `Both`, and `Domain Packs`.
- Use both patterns together when the document needs formal rules and an applied breakdown.

## Purpose
<Explain why this document exists and what problem it solves.>

## Scope
- <What is in scope.>
- <What is out of scope, if useful.>

## Use When
- <When this document should be consulted.>
- <What kinds of decisions or work it should guide.>

## Related Standards and Sources
- <Related internal document, formal standard, or primary source if it materially helps.>
- <Related internal document, formal standard, or primary source if it materially helps.>

<Use this section when the document depends on a formal standard, a companion policy, or a source the reader may need to check. Omit it when the document is fully repo-native.>

## Guidance
- <Primary rule, recommendation, or design statement.>
- <Primary rule, recommendation, or design statement.>
- <Primary rule, recommendation, or design statement.>

## Structure or Data Model
- <Use this section when the document defines required sections, fields, tables, schemas, IDs, or artifact shapes.>
- <Delete this section if the document is purely narrative or policy-oriented.>

## Quick Reference or Distilled Reference
<Use this section for dense factual lookup content, distilled concepts, tables, syntax, command formats, taxonomy summaries, or concise guidance.>

## Process or Workflow
1. <Step or ordered guidance.>
2. <Step or ordered guidance.>
3. <Step or ordered guidance.>

## Examples
- <Example scenario, example command, example artifact, or example output.>
- <Delete this section if examples are not needed.>

## Checklist
- [ ] <Validation or authoring checklist item.>
- [ ] <Validation or authoring checklist item.>
- [ ] <Delete this section if a checklist is not useful.>

## Validation
- <How to verify the document is being followed.>
- <What checks, tests, reviews, or evidence should exist.>

## Change Control
- <What kinds of changes require review or approval.>
- <What other docs or artifacts must be updated in the same change set.>

## References
- <Related internal document or artifact.>
- <Related formal standard or source, if applicable.>

## Tooling and Automation
- <Relevant commands, scripts, hooks, validators, or automation notes.>
- <Delete this section if no tooling guidance is needed.>

## Notes
- <Optional implementation notes, caveats, migration guidance, or open questions.>

## Refresh Procedure
1. <Describe how to re-check related standards, repository structure, or companion docs.>
2. <Describe how to update this document.>
3. <Describe what validation, indexing, changelog, or related-doc updates should happen after changes.>

## Last Synced
- `YYYY-MM-DD`

## Optional Scoped Application

### Core
- <How this concept applies to core-only concerns.>

### Both
- <How this concept applies across both core and domain packs.>

### Domain Packs
- <How this concept applies to domain-specific or user-facing pack concerns.>
