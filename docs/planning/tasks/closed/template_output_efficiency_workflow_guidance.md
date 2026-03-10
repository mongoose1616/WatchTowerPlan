---
id: "task.template_and_output_efficiency.workflow_guidance.001"
trace_id: "trace.template_and_output_efficiency"
title: "Tighten workflow guidance for proportional output"
summary: "Update planning and documentation workflow modules so they prefer the smallest useful output and stop encouraging low-value meta content."
type: "task"
status: "active"
task_status: "done"
task_kind: "documentation"
priority: "medium"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:34:28Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "workflows/modules/"
  - "docs/templates/"
  - "docs/standards/workflows/"
related_ids:
  - "prd.template_and_output_efficiency"
  - "design.features.compact_document_authoring_and_tracking"
  - "design.implementation.template_and_output_efficiency_execution"
depends_on:
  - "task.template_and_output_efficiency.compact_authoring.001"
---

# Tighten workflow guidance for proportional output

## Summary
Update planning and documentation workflow modules so they prefer the smallest useful output and stop encouraging low-value meta content.

## Context
- Current workflow modules can nudge contributors toward verbose "data structure" and "outputs" thinking that leaks into the resulting repository documents.
- The new compact-authoring rule needs companion workflow guidance or the old verbose patterns will keep getting regenerated.

## Scope
- Update the relevant planning and documentation workflow modules plus any adjacent template or workflow standards that need alignment.
- Keep the workflow module structure stable while tightening the execution guidance inside it.

## Done When
- Workflow guidance explicitly prefers proportional output and no longer implies that meta drafting records should appear in the repository artifact by default.

## Links
- [template_and_output_efficiency.md](/home/j/WatchTowerPlan/docs/planning/prds/template_and_output_efficiency.md)
- [compact_document_authoring_and_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/features/compact_document_authoring_and_tracking.md)
- [template_and_output_efficiency_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/template_and_output_efficiency_execution.md)

## Updated At
- `2026-03-10T16:34:28Z`
