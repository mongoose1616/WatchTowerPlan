---
id: "<document_id>"
title: "<Document Title>"
summary: "<One-sentence description.>"
type: "<document_type>"
status: "<document_status>"
tags:
  - "<tag>"
owner: "<document_owner>"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
audience: "<document_audience>"
authority: "<document_authority>"
applies_to:
  - "<repo-surface-or-concept>"
aliases:
  - "<alternate_term>"
---

# <Document Title>

> Use this template for standards, guides, design docs, reference docs, local working references, and overview docs.
> Prefer the smallest useful section set for the document's actual job.
> Write the document as native to this repository rather than as a description of where the idea came from.
> Keep the YAML front matter when the document family requires governed metadata or when metadata is operationally useful. Delete it otherwise.
> If you keep front matter, align the keys and allowed values with [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md) and the matching document-family profile.
> Delete any front matter keys that the chosen profile does not permit.
> Delete any optional section that adds no non-derivable information.

## Summary
<Give a short plain-language explanation of what this document is for and how it should be used.>

## Purpose
<Explain why this document exists and what problem it solves.>

## Guidance
- <Primary rule, recommendation, or design statement.>
- <Primary rule, recommendation, or design statement.>
- <Primary rule, recommendation, or design statement.>

## References
- <Related internal document or artifact.>
- <Related formal standard or source, if applicable.>

## Optional Sections
Add only when they materially improve the document:
- `Scope`
- `Use When`
- `Related Standards and Sources`
- `Structure or Data Model`
- `Quick Reference or Distilled Reference`
- `Process or Workflow`
- `Examples`
- `Validation`
- `Change Control`
- `Tooling and Automation`
- `Notes`
- `Updated At`
