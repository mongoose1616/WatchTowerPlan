---
id: task.task_query_dependency_lookup_hardening.validation_closeout.003
trace_id: trace.task_query_dependency_lookup_hardening
title: Validate and close task query dependency lookup hardening
summary: Run the measured validation baseline, refresh evidence, complete the stop-condition
  review, and close the trace once task-query dependency lookup hardening lands cleanly.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T20:22:54Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
related_ids:
- prd.task_query_dependency_lookup_hardening
- design.implementation.task_query_dependency_lookup_hardening
- decision.task_query_dependency_lookup_hardening_direction
- contract.acceptance.task_query_dependency_lookup_hardening
depends_on:
- task.task_query_dependency_lookup_hardening.reverse_dependency_batching.002
---

# Validate and close task query dependency lookup hardening

## Summary
Run the measured validation baseline, refresh evidence, complete the stop-condition review, and close the trace once task-query dependency lookup hardening lands cleanly.

## Scope
- Run targeted measurement and targeted regressions for the task-query dependency lookup change.
- Run the repository validation baseline after the optimization lands.
- Refresh acceptance evidence, close tasks, close the initiative, and confirm a no-new-issues follow-up review pass.

## Done When
- Acceptance evidence reflects the delivered task-query optimization slice.
- Sync, validation, tests, mypy, and ruff are green after the change set lands.
- A final follow-up review of adjacent query and coordination surfaces finds no additional actionable issues.
