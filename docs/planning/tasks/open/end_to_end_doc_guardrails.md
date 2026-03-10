---
id: "task.end_to_end_repo_review_and_rationalization.doc_guardrails.001"
trace_id: "trace.end_to_end_repo_review_and_rationalization"
title: "Add documentation guardrails for repo-local link integrity"
summary: "Extend document-semantics validation so repo-local markdown links fail closed and keep documentation-coherence drift from recurring silently."
type: "task"
status: "active"
task_status: "ready"
task_kind: "governance"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:43:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/repo_ops/validation/"
  - "core/python/tests/"
  - "docs/standards/documentation/"
  - "workflows/"
related_ids:
  - "prd.end_to_end_repo_review_and_rationalization"
  - "design.features.end_to_end_repo_rationalization"
  - "design.implementation.end_to_end_repo_rationalization_execution"
depends_on:
  - "task.end_to_end_repo_review_and_rationalization.bootstrap.001"
---

# Add documentation guardrails for repo-local link integrity

## Summary
Extend document-semantics validation so repo-local markdown links fail closed and keep documentation-coherence drift from recurring silently.

## Scope
- Add repo-local markdown-link validation for docs and workflow modules.
- Add targeted tests for valid and invalid repo-local links.
- Update the relevant documentation semantics standard and any nearby guidance.

## Done When
- Broken repo-local links fail validation.
- The current documentation corpus passes the stronger rule.
- The standard and tests explain the narrow scope clearly.

## Links
- [end_to_end_repo_rationalization.md](/home/j/WatchTowerPlan/docs/planning/design/features/end_to_end_repo_rationalization.md)
- [end_to_end_repo_rationalization_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/end_to_end_repo_rationalization_execution.md)

## Updated At
- `2026-03-10T19:43:34Z`
