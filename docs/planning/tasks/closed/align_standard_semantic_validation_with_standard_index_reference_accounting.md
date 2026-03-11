---
id: task.internal_project_standards_review_and_hardening.standard_reference_alignment.001
trace_id: trace.internal_project_standards_review_and_hardening
title: Align standard semantic validation with standard-index reference accounting
summary: Make standard semantic validation and standard-index sync consume one shared
  external-authority and local-reference rule.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T18:00:36Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/standard_index.py
- core/python/tests/
related_ids:
- prd.internal_project_standards_review_and_hardening
- design.features.internal_project_standards_review_and_hardening
- design.implementation.internal_project_standards_review_and_hardening
- decision.internal_project_standards_review_and_hardening_direction
- contract.acceptance.internal_project_standards_review_and_hardening
---

# Align standard semantic validation with standard-index reference accounting

## Summary
Make standard semantic validation and standard-index sync consume one shared external-authority and local-reference rule.

## Scope
- Centralize standard reference accounting in core/python/src/watchtower_core/repo_ops/standards.py.
- Update standard semantic validation and standard-index sync to use the shared helper.
- Add regression coverage for valid and invalid external-authority cases across Related Standards and Sources and References.

## Done When
- Standard semantic validation and standard-index sync agree on governed local-reference requirements for external authority.
- Regression tests cover cross-section placement of local reference docs and raw external URLs.
- Affected planning and acceptance surfaces are refreshed.
