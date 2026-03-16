---
id: task.foundation_document_standard_boundary_alignment.contract.001
trace_id: trace.foundation_document_standard_boundary_alignment
title: Align foundation document standard boundary and lookup coverage
summary: Narrow the foundation document standard to governed foundation docs only
  and add fail-closed lookup coverage for the foundations family boundary.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T23:48:07Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/foundation_md_standard.md
- docs/foundations/README.md
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/tests/unit/
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
related_ids:
- prd.foundation_document_standard_boundary_alignment
- design.features.foundation_document_standard_boundary_alignment
- decision.foundation_document_standard_boundary_alignment_direction
- contract.acceptance.foundation_document_standard_boundary_alignment
---

# Align foundation document standard boundary and lookup coverage

## Summary
Narrow the foundation document standard to governed foundation docs only and add fail-closed lookup coverage for the foundations family boundary.

## Scope
- Replace the over-broad foundations directory operationalization boundary with explicit governed foundation-document coverage that excludes the family README.
- Add regression coverage proving every governed foundation document resolves std.documentation.foundation_md while docs/foundations/README.md does not.

## Done When
- The foundation document standard no longer resolves from docs/foundations/README.md and still resolves from every governed foundation document.
- Targeted tests fail closed on the repaired foundations-family lookup boundary.
