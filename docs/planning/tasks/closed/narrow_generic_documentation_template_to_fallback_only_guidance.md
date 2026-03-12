---
id: task.standards_lookup_and_generic_template_alignment.generic_template_scope.001
trace_id: trace.standards_lookup_and_generic_template_alignment
title: Narrow generic documentation template to fallback-only guidance
summary: Rewrite the generic documentation template and templates inventory so
  they stop advertising the template as a substitute for governed family-specific
  scaffolds.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T00:20:44Z'
audience: shared
authority: authoritative
applies_to:
- docs/templates/documentation_template.md
- docs/templates/README.md
- core/python/tests/integration/test_control_plane_artifacts.py
depends_on:
- task.standards_lookup_and_generic_template_alignment.bootstrap.001
related_ids:
- prd.standards_lookup_and_generic_template_alignment
- design.features.standards_lookup_and_generic_template_alignment
- design.implementation.standards_lookup_and_generic_template_alignment
- decision.standards_lookup_and_generic_template_alignment_direction
- contract.acceptance.standards_lookup_and_generic_template_alignment
---

# Narrow generic documentation template to fallback-only guidance

## Summary
Rewrite the generic documentation template and templates inventory so they stop
advertising the template as a substitute for governed family-specific
scaffolds.

## Scope
- Narrow the documentation template guidance to docs without a narrower family
  template.
- Update the templates README so the inventory description matches that
  fallback-only boundary.
- Add artifact regression coverage for the narrowed template contract.

## Done When
- The generic documentation template no longer advertises use for standards,
  references, or planning design docs with dedicated governed templates.
- The templates inventory describes the template as a fallback scaffold rather
  than a broad governed-family substitute.
- Regression coverage fails if the broad stale guidance returns.
