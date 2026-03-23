# Core Pack Neutral Portability Cleanup

## Summary
Removes remaining shared-core plan-specific test and documentation coupling so copied core works with any hosted pack.

## Identity
- `initiative_id`: `initiative.core_pack_neutral_portability_cleanup`
- `trace_id`: `trace.core_pack_neutral_portability_cleanup`
- `scope_type`: `pack_wide`

## Problem
- Shared-core tests under `core/python/tests/` still carry live `plan` assumptions in helpers, fixtures, and current-repository contract assertions.
- Shared reusable-core docs still include a small number of unnecessary `plan` examples or direct pack-root links where pack-neutral guidance is sufficient.
- Copied-core repositories should not need the donor repository's live `plan/` workspace just to validate shared-core behavior.

## Desired Outcome
- `core/python/tests/` proves reusable-core and host behavior without requiring the live `plan/` workspace or direct `watchtower_plan` imports.
- Pack-owned current-repository assertions live under `plan/python/tests/` instead of the shared-core suite.
- Shared reusable-core docs describe split-test and pack-root behavior in pack-neutral terms unless a current-repo fact is materially required.

## In Scope
- Shared-core test helpers, test defaults, and test-support fixtures.
- Shared-core docs and standards that still use unnecessary `plan` examples.
- Moving current-repository or pack-owned tests from `core/python/tests/` into `plan/python/tests/`.
- Tightening boundary guards so pack-owned tests do not drift back into `core/python/tests/`.

## Out Of Scope
- Rewriting current repository foundations that correctly describe `plan` as the active internal pack.
- Changing live `plan` runtime behavior or pack-owned docs beyond what is needed to receive moved tests.
- Any Oversight-local repair work inside `/home/j/WatchTowerOversight`.

## Acceptance Criteria
- Shared-core tests no longer require the live `plan/.wt/manifests/pack_settings.json` path unless the test is explicitly current-repository or pack-owned and has been moved.
- Shared-core synthetic fixture helpers no longer default to `pack.plan`, `watchtower-plan`, `watchtower_plan`, or `watchtower_plan.integration`.
- Core-owned docs and standards use pack-neutral examples where a direct `plan` reference is not required.
- The moved pack-owned tests pass from `plan/python/tests/`, the shared-core suite passes from `core/python/tests/`, and `watchtower-core validate all --skip-acceptance --format json` passes.

## Initial Task Set
- `task.core_pack_neutral_portability_cleanup.bootstrap_core_pack_neutral_portability_cleanup`: Bootstrap Core Pack Neutral Portability Cleanup live initiative package.
