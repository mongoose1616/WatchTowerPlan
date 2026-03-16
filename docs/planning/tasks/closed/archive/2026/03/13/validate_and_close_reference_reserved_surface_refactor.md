---
id: task.reference_and_reserved_surface_maturity_signaling.validation_closeout.004
trace_id: trace.reference_and_reserved_surface_maturity_signaling
title: Validate and close reference/reserved-surface refactor
summary: Run targeted and full validation, perform repeated no-new-issues review passes,
  refresh evidence, and close the initiative when the slice stays clean.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T16:13:27Z'
audience: shared
authority: authoritative
applies_to:
- docs/references/
- core/control_plane/indexes/references/
- core/control_plane/indexes/registries/README.md
- core/control_plane/indexes/schemas/README.md
- core/control_plane/policies/README.md
- core/control_plane/policies/execution/README.md
- core/control_plane/policies/validation/README.md
- core/python/tests/
- docs/planning/
related_ids:
- trace.reference_and_reserved_surface_maturity_signaling
- prd.reference_and_reserved_surface_maturity_signaling
- design.features.reference_and_reserved_surface_maturity_signaling
- design.implementation.reference_and_reserved_surface_maturity_signaling
- decision.reference_and_reserved_surface_maturity_signaling_direction
- contract.acceptance.reference_and_reserved_surface_maturity_signaling
depends_on:
- task.reference_and_reserved_surface_maturity_signaling.reference_maturity_signaling.002
- task.reference_and_reserved_surface_maturity_signaling.reserved_family_signaling.003
---

# Validate and close reference/reserved-surface refactor

## Summary
Run targeted and full validation, perform repeated no-new-issues review passes, refresh evidence, and close the initiative when the slice stays clean.

## Scope
- Run targeted tests and sync or semantic checks for reference docs, reference index behavior, query surfaces, and reserved-family guidance.
- Run full repository validation plus post-fix, second-angle, and adversarial review passes over touched and adjacent surfaces.
- Refresh evidence, close the bounded tasks, and close the initiative only after no new actionable issue remains.

## Done When
- Targeted validation and full repository validation are green for the slice.
- Post-fix, second-angle, and adversarial confirmation passes find no new actionable issue or any findings are looped back and resolved in the same trace.
- Evidence, task state, initiative state, and closeout surfaces are aligned and ready for commit.
