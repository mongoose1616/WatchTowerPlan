---
trace_id: trace.unit_test_hardening_and_rebalancing
id: prd.unit_test_hardening_and_rebalancing
title: Unit Test Hardening and Rebalancing PRD
summary: Harden under-covered executable test surfaces, rebalance the unit suite structure,
  and tighten unit-suite documentation so WatchTowerPlan has a more reliable and maintainable
  test foundation before WatchTower product implementation begins.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T02:46:38Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/planning/
aliases:
- unit_test_review_followup
- test_suite_hardening
---

# Unit Test Hardening and Rebalancing PRD

## Record Metadata
- `Trace ID`: `trace.unit_test_hardening_and_rebalancing`
- `PRD ID`: `prd.unit_test_hardening_and_rebalancing`
- `Status`: `active`
- `Linked Decisions`: `None`
- `Linked Designs`: `design.features.unit_test_hardening_and_rebalancing`
- `Linked Implementation Plans`: `design.implementation.unit_test_hardening_and_rebalancing`
- `Updated At`: `2026-03-12T02:46:38Z`

## Summary
Harden under-covered executable test surfaces, rebalance the unit suite structure, and tighten unit-suite documentation so WatchTowerPlan has a more reliable and maintainable test foundation before WatchTower product implementation begins.

## Problem Statement
The current unit suite is useful but uneven. Fresh verification on March 10, 2026 found `28` unit test files and `176` tests passing, with `75%` overall coverage, but the suite still under-covers critical executable surfaces and over-concentrates cost in a small set of broad orchestration tests. The most important remaining gaps are GitHub integration behavior, GitHub task-sync write paths, closeout handler behavior, task and planning lifecycle handlers, and branch-heavy lifecycle services such as initiative and task derivation. The suite is also still structurally misleading: [README.md](/home/j/WatchTowerPlan/core/python/tests/unit/README.md) describes these as "fast unit tests" even though the suite materially depends on authored repository state, and [test_cli.py](/home/j/WatchTowerPlan/core/python/tests/unit/test_cli.py) now carries `78` tests and `1495` lines while still leaving large handler surfaces weakly covered.

## Goals
- Raise confidence in the most important executable and mutation-heavy Python surfaces before WatchTower product implementation begins.
- Rebalance the unit suite so broad CLI smoke coverage does not dominate runtime or maintenance cost.
- Add shared test helpers and clearer suite boundaries so future test work uses consistent fixture patterns.
- Keep the repository green on the current validation baseline while materially improving targeted subsystem coverage.

## Non-Goals
- Replacing the current repository-governed contract style with fully isolated mock-only tests.
- Introducing a second parallel test harness outside `core/python/tests/`.
- Solving every thin compatibility-wrapper coverage gap if the wrapper is intentionally trivial and already protected by narrower compatibility checks.
- Building hosted CI automation that depends on infrastructure outside this repository.

## Requirements
- `req.unit_test_hardening_and_rebalancing.001`: The initiative must publish a traced planning chain, acceptance contract, planning-baseline evidence artifact, closed bootstrap task, and bounded execution tasks for the verified unit-test follow-up.
- `req.unit_test_hardening_and_rebalancing.002`: Critical executable coverage must materially improve for GitHub integration, GitHub task-sync write behavior, closeout handlers, and the low-coverage route, plan, and task handler families.
- `req.unit_test_hardening_and_rebalancing.003`: The unit suite must gain better direct coverage for handler-level query behavior and branch-heavy lifecycle services where the current CLI smoke tests are too shallow.
- `req.unit_test_hardening_and_rebalancing.004`: The unit suite structure must be rebalanced through shared fixture support and family-oriented CLI test files instead of continuing to grow one oversized `test_cli.py`.
- `req.unit_test_hardening_and_rebalancing.005`: Orchestration and lifecycle failure coverage must expand for `sync all`, `validate all`, initiative closeout, and coordination or initiative derivation edge states.
- `req.unit_test_hardening_and_rebalancing.006`: Unit-test documentation must describe the suite boundary honestly and document the shared fixture pattern contributors should follow.
- `req.unit_test_hardening_and_rebalancing.007`: The repository must remain green on unit, integration, lint, typecheck, sync, validation, and doctor baselines while the test-suite work lands.

## Acceptance Criteria
- `ac.unit_test_hardening_and_rebalancing.001`: The planning corpus publishes the PRD, feature design, implementation plan, acceptance contract, planning-baseline evidence artifact, closed bootstrap task, and bounded execution tasks for this initiative.
- `ac.unit_test_hardening_and_rebalancing.002`: GitHub integration, GitHub task sync, closeout, route, plan, and task command surfaces have direct unit coverage for success and failure branches that were previously shallow or missing.
- `ac.unit_test_hardening_and_rebalancing.003`: The unit suite no longer centers its CLI coverage in one oversized file; shared fixture support exists and command-family tests are split into more focused modules.
- `ac.unit_test_hardening_and_rebalancing.004`: Orchestration and lifecycle tests cover meaningful failure or edge states for aggregate validation, aggregate sync, initiative closeout, and derived coordination or initiative projections.
- `ac.unit_test_hardening_and_rebalancing.005`: The unit-test README and companion guidance describe the suite as a hybrid unit or contract surface, explain shared fixture expectations, and stay aligned with the implemented test layout.
- `ac.unit_test_hardening_and_rebalancing.006`: `pytest`, `mypy`, `ruff`, `watchtower-core validate all --format json`, and `watchtower-core doctor --format json` pass after the initiative lands.

## Risks and Dependencies
- Coverage work can bloat quickly if it keeps testing broad orchestration paths at the wrong layer instead of moving assertions closer to handlers and services.
- Test infrastructure refactors can create noisy diffs if file moves and helper extraction are mixed with too many behavior changes in one slice.
- GitHub integration tests must stay deterministic and must not perform live network calls.
- Lifecycle and coordination tests still depend on authored repository fixtures, so helper design must preserve realistic behavior without increasing flake risk.

## Target Users or Actors
- Maintainers who need faster, more reliable confidence in mutation-heavy command and sync behavior.
- Agents adding new commands, sync surfaces, or governed artifacts that need a clear testing pattern.
- Future WatchTower product work that will rely on `watchtower_core` behavior staying stable while the product repo begins implementation.

## Key Scenarios
- A contributor changes GitHub task sync logic and needs deterministic tests for create, update, label, project, and error paths.
- A contributor changes task or planning lifecycle commands and needs direct handler tests instead of only parser-level smoke checks.
- A contributor changes closeout or initiative derivation logic and needs failure-path coverage for open tasks, supersession, and coordination updates.
- A contributor adds a new CLI family and can follow a shared family-test pattern instead of expanding one monolithic CLI test file.

## Success Metrics
- Critical executable surfaces named in the verified review move materially upward from their current low-coverage baselines.
- The largest CLI test file no longer dominates the unit suite.
- The unit test README no longer misdescribes the suite as purely fast isolated unit tests.

## References
- User-supplied WatchTower unit-test review dated `2026-03-10`

## Updated At
- `2026-03-12T02:46:38Z`
