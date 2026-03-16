---
id: task.validation_test_hotspot_rebalancing.validation_closeout.004
trace_id: trace.validation_test_hotspot_rebalancing
title: Validate and close validation test hotspot rebalancing
summary: Run targeted and full validation, repeat same-theme confirmation passes,
  refresh evidence, and close the validation-hotspot trace once the split stays clean.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T19:18:52Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
- docs/planning/
related_ids:
- prd.validation_test_hotspot_rebalancing
- design.implementation.validation_test_hotspot_rebalancing
- decision.validation_test_hotspot_rebalancing_direction
- contract.acceptance.validation_test_hotspot_rebalancing
depends_on:
- task.validation_test_hotspot_rebalancing.integration_suite_split.002
- task.validation_test_hotspot_rebalancing.document_semantics_suite_split.003
---

# Validate and close validation test hotspot rebalancing

## Summary
Run targeted and full validation, repeat same-theme confirmation passes, refresh evidence, and close the validation-hotspot trace once the split stays clean.

## Scope
- Run targeted validation and then full repository validation on the final split layout.
- Repeat post-fix, second-angle, and adversarial confirmation passes under the same validation-hotspot theme.
- Refresh acceptance, evidence, tracker, and initiative closeout surfaces only after the final clean-state evidence is in hand.

## Done When
- Targeted and full validation pass after the split.
- Repeated confirmation passes find no new actionable issue under the same theme.
- Acceptance, evidence, task, and initiative surfaces align with the final closeout state.
