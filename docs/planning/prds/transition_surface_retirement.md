---
trace_id: trace.transition_surface_retirement
id: prd.transition_surface_retirement
title: Transition Surface Retirement PRD
summary: Retires the remaining live compatibility facades, re-export bridges, and
  marker-only test surfaces now that direct runtime and focused test consumers already
  exist.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-16T19:23:51Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/
- core/python/tests/
- docs/planning/
- docs/standards/
---

# Transition Surface Retirement PRD

## Record Metadata
- `Trace ID`: `trace.transition_surface_retirement`
- `PRD ID`: `prd.transition_surface_retirement`
- `Status`: `active`
- `Linked Decisions`: `decision.transition_surface_retirement_direction`
- `Linked Designs`: `design.features.transition_surface_retirement`
- `Linked Implementation Plans`: `design.implementation.transition_surface_retirement`
- `Updated At`: `2026-03-16T19:23:51Z`

## Summary
Retires the remaining live compatibility facades, re-export bridges, and marker-only test surfaces now that direct runtime and focused test consumers already exist.

## Problem Statement
- Earlier refactor traces already split the real owners for planning-query handlers, typed control-plane models, CLI query tests, document-semantics tests, and integration artifact tests.
- The live tree still carried leftover transition surfaces such as the retired `handlers.py`, `query_handlers.py`, `query_coordination_handlers.py`, and `planning.py` bridge plus the old marker-style hotspot tests.
- Those leftovers kept dead imports, dead test entrypoints, and stale planning or governed discovery references alive even though the direct owners and focused suites already existed.
- The product is still unreleased, so preserving these transition surfaces would only add review noise, path drift, and extraction debt rather than real compatibility value.

## Goals
- Remove the remaining facade modules, re-export bridge, and marker-only test files from the live tree.
- Move runtime, tests, docs, and governed discovery surfaces to the current direct owners and focused suites.
- Eliminate scoped stale references so current indexes, trackers, and repository-path discovery do not advertise retired paths.
- Prove the retirement with negative import coverage plus the full repository validation stack.

## Non-Goals
- Redesign the intentional guardrail roots under `watchtower_core.query`, `watchtower_core.sync`, or the reusable validation namespace.
- Preserve backward compatibility for retired in-repo import paths or deleted hotspot test filenames.
- Reopen unrelated historical traces except where a current governed or discovery surface must stop pointing at a retired path.

## Requirements
- `req.transition_surface_retirement.001`: The trace must publish a concrete PRD, accepted decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, and bounded task chain with no scaffold placeholder text left in the active planning corpus.
- `req.transition_surface_retirement.002`: The live runtime tree must remove the remaining transition facade modules and the retired control-plane model bridge so direct imports resolve only through the current authoritative owners.
- `req.transition_surface_retirement.003`: The live test tree must remove the marker-only hotspot files, keep focused suite coverage in place, and preserve only direct boundary-proof regressions that match the current architecture.
- `req.transition_surface_retirement.004`: Current docs, acceptance records, evidence ledgers, README inventories, and derived governed discovery surfaces must stop advertising the retired paths and must not retain temporary audit helpers after the rewrite lands.
- `req.transition_surface_retirement.005`: The initiative closes only after `sync all`, acceptance validation, `validate all`, `pytest`, `mypy`, `ruff`, and a scoped retired-path audit all pass on the final state.

## Acceptance Criteria
- `ac.transition_surface_retirement.001`: The active planning corpus for `trace.transition_surface_retirement` is concrete, linked, and free of scaffold placeholders.
- `ac.transition_surface_retirement.002`: The retired facade modules and the retired model bridge no longer exist in the live runtime tree, and negative import tests prove they do not come back silently.
- `ac.transition_surface_retirement.003`: The retired hotspot test files no longer exist, focused suites remain the only live test entrypoints, and the boundary proof test uses current naming and ownership.
- `ac.transition_surface_retirement.004`: Current docs, contracts, evidence, trackers, indexes, and repository-path discovery surfaces resolve only current owners or directories in scope and no longer point at the retired transition paths.
- `ac.transition_surface_retirement.005`: Full validation and test passes complete on the cleaned state, and the initiative closes without leaving active transition helpers, duplicate surfaces, or marker files in scope.

## Risks and Dependencies
- Hidden internal imports or planning references could still depend on retired paths and only surface during full-repo validation.
- The cleanup depends on regenerating derived planning and repository-path surfaces after source docs and tests are updated.
- Hard-cut retirement is only safe because the direct owners and focused suites are already present and exercised elsewhere in the repo.

## References
- [transition_surface_retirement.md](/docs/planning/design/features/transition_surface_retirement.md)
- [transition_surface_retirement.md](/docs/planning/design/implementation/transition_surface_retirement.md)
- [transition_surface_retirement_direction.md](/docs/planning/decisions/transition_surface_retirement_direction.md)
- [python_workspace_standard.md](/docs/standards/engineering/python_workspace_standard.md)
- [rewrite_surface_classification_standard.md](/docs/standards/governance/rewrite_surface_classification_standard.md)
