---
id: task.design_document_index_relationship_alignment.feature_design_related_paths.001
trace_id: trace.design_document_index_relationship_alignment
title: Project feature-design affected surfaces into design-index related paths
summary: Derive feature-design related_paths from the required Affected Surfaces section
  and preserve the result in derived planning surfaces.
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
- docs/standards/documentation/feature_design_md_standard.md
- core/python/src/watchtower_core/repo_ops/sync/design_document_index.py
- core/python/tests/
related_ids:
- prd.design_document_index_relationship_alignment
- design.features.design_document_index_relationship_alignment
- design.implementation.design_document_index_relationship_alignment
- decision.design_document_index_relationship_alignment_direction
- contract.acceptance.design_document_index_relationship_alignment
---

# Project feature-design affected surfaces into design-index related paths

## Summary
Derive feature-design related_paths from the required Affected Surfaces section and preserve the result in derived planning surfaces.

## Scope
- Add feature-design related-path derivation from Affected Surfaces in design-document index sync.
- Normalize document-relative repo-local affected-surface links to repository-relative paths.
- Add regression coverage proving design-index and derived planning surfaces retain the projected paths.

## Done When
- Feature-design entries publish normalized related_paths from Affected Surfaces without regressing existing linked-plan relationships.
- Regression tests cover the reproduced related-path drift.
- Affected planning and acceptance surfaces are refreshed.
