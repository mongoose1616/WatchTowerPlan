---
id: task.governed_front_matter_directory_canonicalization.compact_fixture_hardening.003
trace_id: trace.governed_front_matter_directory_canonicalization
title: Harden compact authoring fixture support
summary: Materialize applies_to targets in compact-authoring temp-repo tests so governed
  document loading stays aligned with canonical path enforcement.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T03:17:13Z'
audience: shared
authority: authoritative
applies_to:
- docs/
- core/python/src/watchtower_core/
related_ids:
- prd.governed_front_matter_directory_canonicalization
- design.features.governed_front_matter_directory_canonicalization
- design.implementation.governed_front_matter_directory_canonicalization
- decision.governed_front_matter_directory_canonicalization.direction
- contract.acceptance.governed_front_matter_directory_canonicalization
---

# Harden compact authoring fixture support

## Summary
Materialize applies_to targets in compact-authoring temp-repo tests so governed document loading stays aligned with canonical path enforcement.

## Scope
- Update compact-authoring temp-repo tests to materialize governed applies_to targets before loading governed documents.
- Keep the governed loader strict and prove the fix with targeted regression coverage plus the full test baseline.

## Done When
- The compact-authoring decision and task fixtures load successfully under the current governed applies_to rules.
- Targeted regressions and the full repository test baseline pass without relaxing canonical path enforcement.
