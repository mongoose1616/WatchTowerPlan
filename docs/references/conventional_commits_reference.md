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
updated: "2026-03-09"
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
- `https://www.conventionalcommits.org/en/v1.0.0/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use a type prefix such as `feat`, `fix`, `docs`, or `refactor` to signal intent.
- Use the optional scope when it materially improves clarity.
- Use breaking-change markers intentionally rather than casually.

## Local Mapping in This Repository
- Use this reference as supporting context for [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md).
- Pair it with semantic versioning guidance when release semantics matter.

## Process or Workflow
1. Read this reference before changing [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md) or related commit automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. Keep this file as supporting context and place normative repository policy in `docs/standards/**`.

## Examples
- Use this reference when deciding how commit-message policy should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules now live in [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md).

## Last Synced
- `2026-03-09`
