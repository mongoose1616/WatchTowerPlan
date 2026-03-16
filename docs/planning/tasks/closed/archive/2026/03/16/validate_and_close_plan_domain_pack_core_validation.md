---
id: task.plan_domain_pack_core_validation.validation_closeout.006
trace_id: trace.plan_domain_pack_core_validation
title: Validate and close plan domain pack core validation
summary: Refreshes derived surfaces, runs the final validation stack, updates evidence,
  and closes the trace.
type: task
status: active
task_status: done
task_kind: governance
priority: medium
owner: repository_maintainer
updated_at: '2026-03-16T21:41:48Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
related_ids:
- prd.plan_domain_pack_core_validation
- design.implementation.plan_domain_pack_core_validation
- contract.acceptance.plan_domain_pack_core_validation
depends_on:
- task.plan_domain_pack_core_validation.plan_fixture_pack.004
- task.plan_domain_pack_core_validation.repo_migration.005
---

# Validate and close plan domain pack core validation

## Summary
Refreshes derived surfaces, runs the final validation stack, updates evidence, and closes the trace.

## Scope
- Run the final sync, validate all, pytest, mypy, and ruff checks for the initiative.
- Refresh acceptance, evidence, task, initiative, and coordination closeout surfaces.

## Done When
- The final validation stack passes and the initiative can close cleanly.
- Acceptance, evidence, task, and coordination surfaces reflect the completed initiative state.

## Outcome
- `watchtower-core sync all --write --format json`, `watchtower-core validate acceptance --trace-id trace.plan_domain_pack_core_validation --format json`, and `watchtower-core validate all --format json` passed after the reusable-core validation migration and task closeout landed.
- `python -m pytest`, `python -m mypy src`, and `ruff check src tests/unit tests/integration` all passed after the final lint-only cleanup on the validation CLI and test imports.
- `watchtower-core closeout initiative --trace-id trace.plan_domain_pack_core_validation --initiative-status completed --closure-reason "Delivered reusable-core pack-aware validation loading, suite orchestration, the plan fixture pack, and repo validation migration with clean sync, acceptance, validation, test, typecheck, and lint passes." --closed-at 2026-03-16T21:41:48Z --write --format json` completed with zero acceptance issues and zero open tasks, and the coordination surface returned to `ready_for_bootstrap`.
