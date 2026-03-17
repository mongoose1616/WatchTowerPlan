---
id: task.capture_first_plan_workspace_bootstrap.history_retention_reconciliation.007
trace_id: trace.capture_first_plan_workspace_bootstrap
title: Reconcile legacy history and retention with clean endstate
summary: Defines the follow-up tranche for historical docs handling, archive retention,
  and the clean-endstate purge policy after first-tranche cutover.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-17T09:40:00Z'
audience: shared
authority: authoritative
related_ids:
- prd.capture_first_plan_workspace_bootstrap
- design.features.capture_first_plan_workspace_bootstrap
- design.implementation.capture_first_plan_workspace_bootstrap
- decision.capture_first_plan_workspace_bootstrap_direction
- contract.acceptance.capture_first_plan_workspace_bootstrap
depends_on:
- task.capture_first_plan_workspace_bootstrap.cutover_proof_follow_up.006
---

# Reconcile legacy history and retention with clean endstate

## Summary
Defines the follow-up tranche for historical docs handling, archive retention, and the clean-endstate purge policy after first-tranche cutover.

## Scope
- Define how the retained docs/planning corpus should remain archived, ignored, migrated, or purged after the first tranche.
- Reconcile transitional full-package archive retention with the clean-endstate promotion-before-deletion rules in requirements.md.

## Done When
- A named follow-up implementation slice exists for legacy history handling, archive retention, and clean-endstate purge alignment.
- The follow-up slice is linked from the active bootstrap planning package so history cleanup is explicit rather than implied.
