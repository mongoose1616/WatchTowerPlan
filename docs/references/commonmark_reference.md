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
updated: "2026-03-09"
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
- `https://spec.commonmark.org/0.31.2/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Prefer standard headings, fenced code blocks, lists, blockquotes, and tables that are widely supported.
- Avoid depending on renderer-specific extensions when a portable CommonMark form exists.
- Treat CommonMark compatibility as a portability guardrail rather than as a visual-design system.

## Local Mapping in This Repository
- Use this reference when shaping Markdown-heavy templates in `docs/templates/**`.
- Use it when documentation standards need a format baseline without tying the repo to one renderer.

## Process or Workflow
1. Read this reference before codifying CommonMark Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how Markdown structure and syntax should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
