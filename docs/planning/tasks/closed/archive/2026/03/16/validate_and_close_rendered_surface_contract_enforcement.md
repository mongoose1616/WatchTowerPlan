---
id: task.rendered_surface_contract_enforcement.validation_and_closeout.003
trace_id: trace.rendered_surface_contract_enforcement
title: Validate and close Rendered Surface Contract Enforcement
summary: Refreshes rendered and machine-readable surfaces, validates the rendered-surface
  initiative, and closes the trace after a clean confirmation pass.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T17:34:52Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/
- docs/planning/
- docs/standards/
related_ids:
- prd.rendered_surface_contract_enforcement
- design.features.rendered_surface_contract_enforcement
- design.implementation.rendered_surface_contract_enforcement
- decision.rendered_surface_contract_enforcement_direction
- contract.acceptance.rendered_surface_contract_enforcement
depends_on:
- task.rendered_surface_contract_enforcement.rendered_registry_and_runtime_alignment.002
---

# Validate and close Rendered Surface Contract Enforcement

## Summary
Refreshes rendered and machine-readable surfaces, validates the rendered-surface initiative, and closes the trace after a clean confirmation pass.

## Scope
- Refresh current derived surfaces after the rendered-surface contract and runtime rename land.
- Run acceptance, validation, tests, typing, and linting for the rendered-surface trace and repair any final drift.
- Close the execution tasks and initiative once the bounded rendered-surface slice is confirmed clean.

## Done When
- Acceptance, repository validation, tests, typing, and linting pass for the rendered-surface trace.
- The rendered-surface task chain is terminal and the initiative closeout metadata records the bounded result.

## Outcome
- `watchtower-core sync all --write --format json`, `watchtower-core validate acceptance --trace-id trace.rendered_surface_contract_enforcement --format json`, and `watchtower-core validate all --format json` passed after the rendered-surface registry, runtime rename, and tracker refactor landed.
- `ruff check .`, `mypy src`, and the full `pytest` suite passed after the active-path and archive companion updates for the renamed rendered runtime modules.
- The final confirmation pass found no remaining active `projection` compatibility boundary in the scoped live runtime, command, standards, or tracker surfaces, so the trace is ready for terminal closeout as `completed`.
