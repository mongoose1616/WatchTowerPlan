---
id: "std.<family>.<topic>"
title: "<Standard Title>"
summary: "<One-sentence description.>"
type: "standard"
status: "active"
tags:
  - "standard"
  - "<family>"
  - "<topic>"
owner: "repository_maintainer"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
audience: "shared"
authority: "authoritative"
---

# <Standard Title>

> Use this template for governed standard and best-practice documents under `docs/standards/`.
> Keep the front matter aligned with [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md) and the standard front matter profile.
> Keep one primary standard concern per document.
> Write `Related Standards and Sources` bullets in `source: implication` form so the local consequence of each authority is explicit.
> Publish `Operationalization` with metadata bullets for `Modes` and `Operational Surfaces`.
> Use repo-relative file paths for exact files, repo-relative directory paths ending in `/` for directories, and bounded repo-relative glob patterns for repeating families.
> Keep `Updated At` aligned with front matter `updated_at`.
> Leave one blank line between the last item in a bullet or numbered list and the next heading.
> Use repo-local Markdown links only when the target already exists or is being created in the same change.
> Keep the template compact, but do not mark contract-required sections as optional.

## Summary
<One short explanation of what this standard governs.>

## Purpose
<Explain why this rule exists.>

## Scope
- <Describe where this standard applies.>
- <Describe what this standard does not cover when that boundary matters.>

## Use When
- <Describe when maintainers should consult or update this standard.>

## Related Standards and Sources
- <Related standard, reference, template, or workflow>: <Why it materially shapes this standard.>
- <Related standard, reference, template, or workflow>: <Why it materially shapes this standard.>

## Guidance
- <Primary rule or best practice.>
- <Primary rule or best practice.>

## Operationalization
- `Modes`: `<mode>`; `<mode>`
- `Operational Surfaces`: `<repo/file.md>`; `<repo/directory/>`

## Validation
- <How reviewers or automation should verify compliance.>

## Change Control
- <What companion docs, indexes, schemas, or code must change with this standard.>

## References
- <Companion document, example, artifact, or supporting local reference.>

## Updated At
- `YYYY-MM-DDTHH:MM:SSZ`

## Optional Sections
Add only when they materially improve the standard:
- `Structure or Data Model`
- `Notes`
