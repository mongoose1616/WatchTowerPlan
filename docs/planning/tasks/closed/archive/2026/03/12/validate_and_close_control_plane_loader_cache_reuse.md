---
id: task.control_plane_loader_cache_reuse.validation_closeout.003
trace_id: trace.control_plane_loader_cache_reuse
title: Validate and close control plane loader cache reuse
summary: Run the final validation baseline, refresh evidence, and close the initiative
  once the loader cache change and follow-up review land cleanly.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T19:37:54Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/validation/
- core/python/tests/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
related_ids:
- prd.control_plane_loader_cache_reuse
- design.implementation.control_plane_loader_cache_reuse
- decision.control_plane_loader_cache_reuse_direction
- contract.acceptance.control_plane_loader_cache_reuse
depends_on:
- task.control_plane_loader_cache_reuse.loader_cache.002
---

# Validate and close control plane loader cache reuse

## Summary
Run the final validation baseline, refresh evidence, and close the initiative once the loader
cache change and follow-up review land cleanly.

## Scope
- Run targeted measurements, targeted regressions, and the full repository baseline after the
  loader cache implementation lands.
- Refresh acceptance evidence, close the execution tasks, close the initiative, and confirm a
  no-new-issues follow-up review pass.

## Done When
- Acceptance evidence and planning closeout surfaces reflect the delivered loader cache slice.
- `watchtower-core validate all`, `pytest -q`, `mypy`, and `ruff` pass after the change set
  lands.
- A final follow-up review pass of adjacent loader and validation surfaces finds no additional
  actionable issues.
