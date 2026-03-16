---
id: task.design_document_index_relationship_alignment.implementation_plan_source_paths.001
trace_id: trace.design_document_index_relationship_alignment
title: Broaden implementation-plan source paths beyond source designs
summary: Derive implementation-plan source_paths from linked PRDs and repo-local source
  surfaces, then align companion tracking and standards guidance.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T19:36:07Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/
- docs/standards/data_contracts/design_document_index_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/implementation_plan_template.md
- core/control_plane/examples/valid/indexes/design_document_index.v1.example.json
- core/python/src/watchtower_core/repo_ops/sync/design_document_index.py
- core/python/src/watchtower_core/repo_ops/sync/design_tracking.py
- core/python/tests/
related_ids:
- prd.design_document_index_relationship_alignment
- design.features.design_document_index_relationship_alignment
- design.implementation.design_document_index_relationship_alignment
- decision.design_document_index_relationship_alignment_direction
- contract.acceptance.design_document_index_relationship_alignment
---

# Broaden implementation-plan source paths beyond source designs

## Summary
Derive implementation-plan source_paths from linked PRDs and repo-local source surfaces, then align companion tracking and standards guidance.

## Scope
- Broaden implementation-plan source-path derivation beyond Source Designs in design-document index sync.
- Align design-tracking wording, standards text, and template guidance with the broader source model.
- Add regression coverage for PRD-backed and repo-local-source-backed implementation plans.

## Done When
- Implementation-plan entries can derive source_paths from Source Designs, linked PRDs, or repo-local source surfaces in Source Request or Design.
- Sync still fails clearly when no traceable source surface exists.
- Tracker wording, standards docs, and regression tests reflect the updated source model.
