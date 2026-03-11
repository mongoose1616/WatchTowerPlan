---
id: task.reference_and_workflow_standards_alignment.reference_authoring_alignment.001
trace_id: trace.reference_and_workflow_standards_alignment
title: Align reference authoring contract with governed enforcement
summary: Update reference authoring guidance and regression coverage so governed
  reference docs require Canonical Upstream just like the live validator and
  reference index already do.
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
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_document_semantics_validation.py
related_ids:
- prd.reference_and_workflow_standards_alignment
- design.features.reference_and_workflow_standards_alignment
- design.implementation.reference_and_workflow_standards_alignment
- decision.reference_and_workflow_standards_alignment_direction
- contract.acceptance.reference_and_workflow_standards_alignment
---

# Align reference authoring contract with governed enforcement

## Summary
Update reference authoring guidance and regression coverage so governed
reference docs require Canonical Upstream just like the live validator and
reference index already do.

## Scope
- Make the reference document standard and template publish `Canonical
  Upstream` as a required governed section for `docs/references/**`.
- Clarify the reference-family boundary so repo-native-only lookup content is
  not implied to belong in the governed reference family without upstream
  authority.
- Add regression checks that fail if the standard or template weakens the
  canonical-upstream contract again.

## Done When
- Reference authoring guidance matches the live validator and reference-index
  contract.
- Regression coverage protects the required Canonical Upstream section.
- Companion planning and control-plane surfaces are ready for final validation.
