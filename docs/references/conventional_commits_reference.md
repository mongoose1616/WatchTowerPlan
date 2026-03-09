---
id: "ref.conventional_commits"
title: "Conventional Commits Reference"
summary: "This document provides a working reference for Conventional Commits as a parseable commit-message convention."
type: "reference"
status: "active"
tags:
  - "reference"
  - "conventional_commits"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# Conventional Commits Reference
## Summary
This document provides a working reference for Conventional Commits as a parseable commit-message convention.

## Purpose
Provide a consistent commit-message baseline that supports readable history and automation-friendly change classification.

## Scope
- Covers the Conventional Commits commit-message pattern.
- Does not by itself define this repository's full commit policy.

## Canonical Upstream
- `https://www.conventionalcommits.org/en/v1.0.0/` - verified 2026-03-09; Conventional Commits.

## Related Standards and Sources
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

## Quick Reference or Distilled Reference
### Core Rules
- Start the subject with a type such as `feat`, `fix`, `docs`, or another governed type.
- Add a scope only when it materially improves clarity.
- Mark breaking changes explicitly instead of burying them in body text.

### Common Shapes
| Pattern | Use When | Notes |
|---|---|---|
| `type: subject` | most commits | simplest readable form |
| `type(scope): subject` | subsystem context matters | keep scope short and stable |
| breaking marker or footer | compatibility changes | use intentionally and consistently |

### Common Pitfalls
- Inventing many custom types without governance.
- Using scope as a dumping ground for context that belongs in the body.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

### Why It Matters Here
- Use this reference as supporting context for [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md).
- Pair it with semantic versioning guidance when release semantics matter.

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
