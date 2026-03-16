---
id: task.reference_and_workflow_standards_alignment.workflow_additional_load_alignment.001
trace_id: trace.reference_and_workflow_standards_alignment
title: Tighten workflow additional-load generic baseline enforcement
summary: Reject generic workflow standards in Additional Files to Load,
  including routing_and_context_loading_standard.md, and add matching
  regression coverage.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T23:25:32Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/workflow_md_standard.md
- docs/templates/workflow_template.md
- core/python/src/watchtower_core/repo_ops/sync/workflow_index.py
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_workflow_index_sync.py
depends_on:
- task.reference_and_workflow_standards_alignment.reference_authoring_alignment.001
related_ids:
- prd.reference_and_workflow_standards_alignment
- design.features.reference_and_workflow_standards_alignment
- design.implementation.reference_and_workflow_standards_alignment
- decision.reference_and_workflow_standards_alignment_direction
- contract.acceptance.reference_and_workflow_standards_alignment
---

# Tighten workflow additional-load generic baseline enforcement

## Summary
Reject generic workflow standards in Additional Files to Load, including
routing_and_context_loading_standard.md, and add matching regression
coverage.

## Scope
- Extend the workflow additional-load disallow set to cover the missing generic
  workflow standard.
- Keep unit and integration workflow checks aligned with the published
  workflow-standard boundary.
- Preserve acceptance of legitimate task-specific repo-local load paths.

## Done When
- Workflow validation and sync reject generic workflow standards that should
  stay implicit.
- Regression coverage fails closed if the disallow set weakens.
- No unrelated workflow additional-load behavior regresses.
