---
id: task.core_split_compatibility_wrapper_retirement.validation_closeout.004
trace_id: trace.core_split_compatibility_wrapper_retirement
title: Validate and close core split compatibility wrapper retirement
summary: Run targeted and full validation, refresh derived planning surfaces, and
  close the compatibility-wrapper retirement trace once the boundary lands cleanly.
type: task
status: active
task_status: backlog
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T03:31:47Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
related_ids:
- prd.core_split_compatibility_wrapper_retirement
- design.features.core_split_compatibility_wrapper_retirement
- design.implementation.core_split_compatibility_wrapper_retirement
- decision.core_split_compatibility_wrapper_retirement_direction
- contract.acceptance.core_split_compatibility_wrapper_retirement
depends_on:
- task.core_split_compatibility_wrapper_retirement.boundary_proof.003
---

# Validate and close core split compatibility wrapper retirement

## Summary
Run targeted and full validation, refresh derived planning surfaces, and close the compatibility-wrapper retirement trace once the boundary lands cleanly.

## Scope
- Run targeted boundary tests plus the broader Python validation baseline after the wrapper retirement and boundary-proof work land.
- Refresh acceptance evidence and derived planning surfaces with the canonical repo-native sync plus validation reruns.
- Close the remaining tasks and the initiative only after the package boundary returns a clean state.

## Done When
- Targeted boundary validation and the full repository validation loop pass without a new package-boundary issue.
- Acceptance evidence covers the final implementation acceptance IDs.
- The derived planning surfaces and initiative state reflect the clean closeout after the final sync and validation reruns.
