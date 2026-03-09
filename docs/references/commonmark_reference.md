---
id: "ref.commonmark"
title: "CommonMark Reference"
summary: "This document provides a working reference for CommonMark as the Markdown compatibility baseline for repository documents."
type: "reference"
status: "active"
tags:
  - "reference"
  - "commonmark"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# CommonMark Reference
## Summary
This document provides a working reference for CommonMark as the Markdown compatibility baseline for repository documents.

## Purpose
Provide a stable Markdown baseline so docs render predictably across tools and do not rely on engine-specific shortcuts.

## Scope
- Covers CommonMark as a document-formatting baseline.
- Does not define every local writing preference or documentation structure rule.

## Canonical Upstream
- `https://spec.commonmark.org/0.31.2/` - verified 2026-03-09; CommonMark Spec.

## Related Standards and Sources
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [templates](/home/j/WatchTowerPlan/docs/templates/)

## Quick Reference or Distilled Reference
### Portable Markdown Rules
- Prefer headings, lists, blockquotes, links, emphasis, and fenced code blocks that render consistently across tools.
- Treat raw HTML and renderer-specific extensions as compatibility risks unless the repository explicitly accepts them.
- Remember that tables are not part of core CommonMark; if the repo relies on GitHub-style tables, that is an additional renderer assumption.

### Safe Syntax Choices
| Need | Prefer | Be Careful With |
|---|---|---|
| code samples | fenced code blocks | indentation-sensitive blocks for long snippets |
| links and emphasis | standard CommonMark forms | renderer-specific shortcut syntax |
| layout | plain Markdown structure | embedded HTML for presentational control |
| tables | only when the renderer contract allows them | assuming tables are portable CommonMark |

### Common Pitfalls
- Depending on one renderer's HTML or CSS behavior.
- Calling a document "CommonMark compatible" while it actually depends on non-CommonMark extensions.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [templates](/home/j/WatchTowerPlan/docs/templates/)

### Why It Matters Here
- Use this reference when shaping Markdown-heavy templates in `docs/templates/**`.
- Use it when documentation standards need a format baseline without tying the repo to one renderer.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [templates](/home/j/WatchTowerPlan/docs/templates/)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
