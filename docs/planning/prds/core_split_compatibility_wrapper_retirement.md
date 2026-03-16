---
trace_id: trace.core_split_compatibility_wrapper_retirement
id: prd.core_split_compatibility_wrapper_retirement
title: Core Split Compatibility Wrapper Retirement PRD
summary: Retire repo-specific compatibility wrapper modules from export-safe
  `watchtower_core` namespaces so a future core split exposes only reusable surfaces.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-16T02:06:53Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/query/
- core/python/src/watchtower_core/sync/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/README.md
- core/python/src/watchtower_core/query/README.md
- core/python/src/watchtower_core/sync/README.md
- core/python/src/watchtower_core/validation/README.md
- core/python/src/watchtower_core/cli/
- core/python/README.md
- core/python/tests/unit/test_repo_ops_compatibility.py
---

# Core Split Compatibility Wrapper Retirement PRD

## Record Metadata
- `Trace ID`: `trace.core_split_compatibility_wrapper_retirement`
- `PRD ID`: `prd.core_split_compatibility_wrapper_retirement`
- `Status`: `active`
- `Linked Decisions`: `decision.core_split_compatibility_wrapper_retirement_direction`
- `Linked Designs`: `design.features.core_split_compatibility_wrapper_retirement`
- `Linked Implementation Plans`: `design.implementation.core_split_compatibility_wrapper_retirement`
- `Updated At`: `2026-03-16T02:06:53Z`

## Summary
Retire repo-specific compatibility wrapper modules from export-safe `watchtower_core` namespaces so a future core split exposes only reusable surfaces.

## Problem Statement
- The export-readiness and export-hardening traces established the reusable-versus-`repo_ops` boundary, but they intentionally stopped short of compatibility-wrapper retirement.
- The live package still carries explicit repo-local forwarding modules such as `watchtower_core.query.commands`, `watchtower_core.sync.command_index`, and `watchtower_core.validation.all`, each of which simply re-exports `repo_ops` behavior from an export-safe namespace.
- The current compatibility test suite still locks those wrappers in place, which means a future `core/` split would either copy repo-specific forwarding surfaces into the extracted package or require another cleanup pass immediately before extraction.
- That leftover compatibility layer is now extraction debt rather than migration help. Internal code already understands the `repo_ops` boundary, and future reusable-core consumers should not learn repo-specific imports through top-level module names that appear export-safe.

## Goals
- Remove repo-specific leaf compatibility wrappers from top-level export-safe `watchtower_core` namespaces before a future core split.
- Move any remaining repo-local callers and tests onto `watchtower_core.repo_ops.*` or truly reusable validation services.
- Publish package-boundary docs and regression checks that prove the split-ready surface after the wrapper retirement.

## Non-Goals
- Extracting `core/` into a separate package or repository in this trace.
- Redesigning CLI behavior, command names, or control-plane schemas.
- Reopening the older export-readiness or export-hardening traces instead of recording a new bounded follow-up.

## Target Users or Actors
- Maintainers preparing the reusable core surface for future extraction.
- Engineers working inside `core/python/` who need a clean import boundary between reusable services and `WatchTowerPlan`-specific orchestration.
- Future `WatchTower` consumers that should only see reusable package surfaces.

## Key Scenarios
- A maintainer splits reusable core code out of `WatchTowerPlan` and wants the extracted package to avoid carrying repo-specific forwarding modules.
- A contributor adds or updates repo-local query, sync, or validation logic and should import `repo_ops` directly instead of learning a compatibility wrapper path.
- A reviewer inspects the package boundary and needs tests and README docs to prove which namespaces remain reusable and which are repo-local.

## Requirements
- `req.core_split_compatibility_wrapper_retirement.001`: The trace must publish an explicit coverage map and bounded task chain for retiring repo-specific compatibility wrappers from `watchtower_core.query`, `watchtower_core.sync`, and repo-wide aggregate validation surfaces.
- `req.core_split_compatibility_wrapper_retirement.002`: Repo-local callers and tests must stop depending on top-level compatibility wrapper modules for query, sync, and aggregate validation behavior.
- `req.core_split_compatibility_wrapper_retirement.003`: The top-level package boundary must only retain reusable services or explicit guardrails; repo-specific leaf wrappers must be removed or replaced with fail-closed boundary signals.
- `req.core_split_compatibility_wrapper_retirement.004`: Runtime-boundary docs, package READMEs, and regression tests must prove the post-retirement boundary clearly enough that a future core split does not need to rediscover it.
- `req.core_split_compatibility_wrapper_retirement.005`: The slice must close through targeted and full validation plus refreshed derived planning surfaces once the current repo command path is healthy again.

## Acceptance Criteria
- `ac.core_split_compatibility_wrapper_retirement.001`: The planning corpus for `trace.core_split_compatibility_wrapper_retirement` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, and bounded open execution tasks.
- `ac.core_split_compatibility_wrapper_retirement.002`: Repo-specific compatibility wrapper modules no longer define the effective import path for query, sync, or aggregate validation behavior inside `watchtower_core`.
- `ac.core_split_compatibility_wrapper_retirement.003`: Package-boundary docs and tests show that repo-local behavior lives under `repo_ops` while the remaining top-level validation surface stays reusable and explicit.
- `ac.core_split_compatibility_wrapper_retirement.004`: Targeted boundary tests, full repository validation, evidence refresh, and initiative closeout complete without a new actionable package-boundary issue.

## Success Metrics
- A future extracted core package can exclude repo-specific query and sync forwarding modules without another cleanup pass.
- Repo-local callers and tests use `watchtower_core.repo_ops.*` or reusable validators directly.
- Package README guidance and boundary tests agree on the same export-safe surface.

## Risks and Dependencies
- Wrapper retirement could break tests or hidden internal imports that still rely on the legacy module paths.
- Boundary cleanup can drift from runtime docs if package READMEs and workspace guidance are not updated in the same change.
- The slice depends on the earlier `repo_ops` split already being structurally correct; if a wrapper is still masking true reusable behavior, retirement may expose another boundary problem.

## Open Questions
- Whether a later extracted package should ship its own one-release deprecation shim after this in-repo retirement lands cleanly.

## Foundations References Applied
- `docs/foundations/repository_scope.md`: repo-specific behavior must stay explicit instead of leaking into reusable surfaces.
- `docs/foundations/product_direction.md`: future product work should consume a clean shared core rather than a package that still forwards `WatchTowerPlan`-specific services.
- `docs/foundations/engineering_design_principles.md`: prefer explicit, deterministic boundaries over convenience indirection.

## References
- `docs/planning/prds/core_export_readiness_and_optimization.md`
- `docs/planning/prds/core_export_hardening_followup.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
- `docs/planning/design/features/core_export_hardening.md`
- `core/python/src/watchtower_core/README.md`
- `core/python/src/watchtower_core/query/README.md`
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/validation/README.md`
