---
id: "ref.git_commit_message_guidance"
title: "Git Commit Message Guidance Reference"
summary: "This document provides a working reference for general Git commit message quality guidance from cbea.ms."
type: "reference"
status: "active"
tags:
  - "reference"
  - "git_commit_message_guidance"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# Git Commit Message Guidance Reference
## Summary
This document provides a working reference for general Git commit message quality guidance from cbea.ms.

## Purpose
Provide human-readable commit-writing guidance that complements formal commit conventions.

## Scope
- Covers commit message clarity and structure guidance.
- Does not replace a formal repository commit standard.

## Canonical Upstream
- `https://cbea.ms/git-commit/` - verified 2026-03-09; How to Write a Git Commit Message.

## Related Standards and Sources
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

## Quick Reference or Distilled Reference
### Commit Message Shape
| Part | Role | Notes |
|---|---|---|
| subject line | state the change clearly | keep it concise and action-oriented |
| blank line | separates summary from detail | improves parser and reader behavior |
| body | explain rationale, caveats, or side effects | use when the subject is not enough |

### Core Rules
- Write the subject around what changed and why it matters, not just the file touched.
- Use the body when reviewers need reasoning, risks, or migration context.
- Keep the first line scannable in history views.

### Common Pitfalls
- Using subjects like `update stuff` or file-only descriptions.
- Hiding important compatibility or behavior changes outside the commit body.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

### Why It Matters Here
- Use this reference as supporting guidance for [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md).
- Treat it as style guidance layered on top of any formal commit convention.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

## Notes
- Repository-specific rules now live in [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md).
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
