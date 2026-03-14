---
id: task.structural_rewrite_program.phase0_phase1_package.002
trace_id: trace.structural_rewrite_program
title: Complete structural rewrite program Phase 0 and Phase 1 package
summary: Refresh the live rewrite baseline, publish the rewrite governance surfaces, classify critical and compatibility surfaces, and prepare the Phase 2 entry review package.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-14T02:37:25Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/governance/rewrite_surface_classification_standard.md
- docs/standards/governance/rewrite_execution_control_standard.md
- docs/planning/design/implementation/structural_rewrite_program.md
- core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json
- core/control_plane/ledgers/migrations/structural_rewrite_program_phase0_phase1_ready.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_program_phase0_phase1_baseline.v1.json
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.bootstrap.001
---

# Complete structural rewrite program Phase 0 and Phase 1 package

## Summary
Refresh the live rewrite baseline, publish the rewrite governance surfaces, classify critical and compatibility surfaces, and prepare the Phase 2 entry review package.

## Scope
- Re-run the required baseline commands and refresh the live hotspot inventory.
- Publish the rewrite classification and execution-control standards plus the public planning-authority parity contract.
- Publish critical-surface classification, history and compatibility consumer maps, support-level classifications, retention reasons, no-go conditions, rollback expectations, and Phase 2 entry conditions.
- Fix exactly one Phase 2 pilot family and stop with the review package complete.

## Done When
- Phase 0 and Phase 1 deliverables are published in repo-native homes.
- The implementation plan names the chosen Phase 2 pilot family and the review question explicitly.
- No Phase 2 implementation work has begun.
