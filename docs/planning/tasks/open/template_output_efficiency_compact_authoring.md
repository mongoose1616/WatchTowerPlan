---
id: "task.template_and_output_efficiency.compact_authoring.001"
trace_id: "trace.template_and_output_efficiency"
title: "Define compact authoring rules and align governed templates"
summary: "Add the compact-authoring standard, align templates with governed outputs, and relax low-value required sections without weakening machine-readable authority."
type: "task"
status: "active"
task_status: "ready"
task_kind: "governance"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:00:54Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/templates/"
  - "docs/standards/documentation/"
  - "core/python/src/watchtower_core/repo_ops/planning_documents.py"
  - "core/python/src/watchtower_core/repo_ops/validation/document_semantics.py"
related_ids:
  - "prd.template_and_output_efficiency"
  - "design.features.compact_document_authoring_and_tracking"
  - "design.implementation.template_and_output_efficiency_execution"
---

# Define compact authoring rules and align governed templates

## Summary
Add the compact-authoring standard, align templates with governed outputs, and relax low-value required sections without weakening machine-readable authority.

## Context
- PRD and decision templates currently fail to model the governed front matter their outputs need.
- Planning validators still require some sections that are better treated as optional when they do not add non-derivable information.

## Scope
- Add a repository standard for compact, high-signal authored documents.
- Update planning, decision, task, and generic documentation templates plus the validator logic and companion standards they depend on.

## Done When
- Compact-authored document rules are durable, templates match governed families, and leaner planning documents validate cleanly.

## Links
- [template_and_output_efficiency.md](/home/j/WatchTowerPlan/docs/planning/prds/template_and_output_efficiency.md)
- [compact_document_authoring_and_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/features/compact_document_authoring_and_tracking.md)
- [template_and_output_efficiency_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/template_and_output_efficiency_execution.md)

## Updated At
- `2026-03-10T16:00:54Z`
