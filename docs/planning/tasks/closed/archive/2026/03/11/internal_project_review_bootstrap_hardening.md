---
id: task.internal_project_review_and_hardening.bootstrap_hardening.001
trace_id: trace.internal_project_review_and_hardening
title: Harden planning bootstrap for validation-compatible traces
summary: Makes bootstrap write mode publish repository-compliant docs, acceptance
  contract, and baseline evidence.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T15:36:35Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py
- core/python/src/watchtower_core/repo_ops/planning_scaffolds.py
- core/python/src/watchtower_core/evidence/validation_evidence.py
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
related_ids:
- prd.internal_project_review_and_hardening
- decision.internal_project_review_and_hardening_direction
- design.features.internal_project_review_and_hardening
- design.implementation.internal_project_review_and_hardening
---

# Harden planning bootstrap for validation-compatible traces

## Summary
Makes bootstrap write mode publish repository-compliant docs, acceptance contract, and baseline evidence.

## Scope
- Add compliant applied-reference sections to scaffolded design docs.
- Publish the acceptance contract and planning-baseline evidence during bootstrap write mode.
- Keep bootstrap command docs, payloads, and tests aligned with the expanded write output.

## Done When
- Bootstrap write mode leaves the repository validation-compatible for a new traced initiative.
- Planning scaffold and bootstrap tests cover the new contract and evidence outputs.
