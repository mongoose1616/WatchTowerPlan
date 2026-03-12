---
id: "ref.example_reference"
title: "Reference Title"
summary: "One-sentence description."
type: "reference"
status: "active"
tags:
  - "reference"
owner: "repository_maintainer"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
audience: "shared"
authority: "reference"
applies_to:
  - "docs/references/<reference_file>.md"
aliases:
  - "alternate_term"
---

# <Reference Title>

> Use this template for repository reference documents that summarize a standard, framework, format, taxonomy, or working model.
> Write the document as native guidance for this repository.
> Governed references under `docs/references/**` should keep the front matter block and align it with [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md) and the reference front matter profile.
> When `applies_to` uses repo paths, files should omit a trailing slash and directories should end in `/`.
> Governed references under `docs/references/**` must include `## Canonical Upstream` and publish at least one official documentation, standards-body, vendor, RFC, or similar authoritative URL.
> If the topic has no canonical upstream authority, it does not belong in the governed `docs/references/**` family and should be authored in a more appropriate repo-native document family instead.
> Keep the document focused on durable lookup content. Reference lifecycle checks belong in the documentation-generation and documentation-refresh workflows rather than in each reference file.
> Authoring and review checklists belong in documentation workflows and standards, not in the reference document itself.
> Make `## Quick Reference or Distilled Reference` the main value of the document, not a thin preface to the upstream links.
> A reference that mostly acts as a bibliography or link index is incomplete. The distilled section should usually answer the recurring practical questions without forcing the reader back to the upstream source for every common case.
> For non-trivial topics, capture enough concrete detail that a maintainer can safely decide how to use, not use, configure, parse, validate, or compare the topic from the local reference alone.
> For standards-, security-, protocol-, format-, storage-, timestamp-, identifier-, or tooling-oriented topics, include explicit rules, defaults, required or disallowed patterns, edge cases, failure modes, and ambiguity notes when they materially affect correct use.
> Prefer concrete lookup structures such as rules lists, field tables, decision tables, syntax blocks, defaults, pitfalls, unsafe assumptions, and use-when versus do-not-use-when comparisons.
> If the upstream source is ambiguous, incomplete, or easy to misread, make that ambiguity explicit in the distilled section instead of smoothing it over.
> Delete any section that does not help the document stay focused on one succinct standard, topic, or area.

## Summary
<Give a short explanation of what this reference covers and why it exists in this repository.>

## Purpose
<Explain what problem this reference solves for maintainers, contributors, or reviewers.>

## Scope
- <Describe what this reference covers.>
- <Describe what it does not cover if that boundary matters.>

## Canonical Upstream
- <Official URL, standard, RFC, vendor doc, or spec page.>
- <Official URL, standard, RFC, vendor doc, or spec page.>
- <Optional internal authority doc if one exists.>

<Keep this section in governed reference docs under `docs/references/**`. Publish the authoritative upstream URLs that justify the local reference.>

## Related Standards and Sources
- <Related internal standard, template, workflow, or companion reference.>
- <Related internal standard, template, workflow, or companion reference.>

## Quick Reference or Distilled Reference
<Use this section for the dense lookup content the reader actually came for. It should usually let the reader answer the recurring practical questions without immediately leaving the repo for the upstream source. A reference that could be replaced by a short link list has failed this section. Distill enough content that the reader can safely understand the common cases, the important boundaries, and any local interpretation needed here. Tables, syntax, modes, rules, terms, decision points, defaults, edge cases, failure modes, and concise summaries usually belong here.>

### <Rules or Decision Points>
- <Concrete rule.>
- <Concrete rule.>
- <Concrete use-when or do-not-use-when boundary.>

### <Fields, Modes, or Terms>
| Item | Meaning | Notes |
|---|---|---|
| <Item> | <Meaning> | <Notes> |

### <Decision Table or Defaults>
| Question | Preferred Answer | Why |
|---|---|---|
| <Common decision> | <Preferred answer> | <Reason or tradeoff> |

### <Ambiguities, Failure Modes, or Pitfalls>
- <Concrete example, edge case, or common mistake.>
- <Concrete example, edge case, or common mistake.>

## Local Mapping in This Repository
- <Explain how this reference applies to current repository docs, workflows, standards, templates, or directories.>
- <Link the concept to actual repository surfaces when useful.>
- <State any local interpretation or usage boundary clearly.>

## Process or Workflow
1. <Describe how a contributor should apply this reference.>
2. <Describe how to classify or use the concept in this repository.>
3. <Describe any follow-up checks or companion updates that should happen.>

## Examples
- <Example document, example section, example command, example structure, or example usage.>
- <Example of correct local application.>

## References
- <Related internal document.>
- <Related internal document.>
- <Optional external standard or source.>

## Tooling and Automation
- <Relevant validator, generator, script, linter, or command if one exists.>
- <Delete this section if there is no useful tooling note.>

## Notes
- <Optional implementation note, caveat, interpretation boundary, or reminder.>

## Updated At
- `YYYY-MM-DDTHH:MM:SSZ`
