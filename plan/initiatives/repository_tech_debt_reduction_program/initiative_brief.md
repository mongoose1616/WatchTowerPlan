# Repository Tech Debt Reduction Program

## Summary
Makes tech-debt reduction the active repository priority, starting with legacy residue removal, integration-tail reduction, and stale compatibility cleanup across core, host, and pack-owned code.

## Identity
- `initiative_id`: `initiative.repository_tech_debt_reduction_program`
- `trace_id`: `trace.repository_tech_debt_reduction_program`
- `scope_type`: `pack_wide`

## Problem
- The repository is functionally green, but a growing share of maintenance cost now comes from residual technical debt rather than missing features.
- The Python test suite still spends disproportionate wall time in a small number of integration-heavy and end-to-end paths, which slows normal iteration and obscures real regressions.
- Several compatibility shims, migration-era surfaces, duplicated registry declarations, and stale edge-case tests still exist because earlier architecture and cutover work favored correctness first and cleanup later.
- If new work resumes without a debt-first tranche, the repository will continue to accumulate avoidable complexity across `core`, `host`, and `plan`.

## Desired Outcome
- Make tech-debt removal the active repository priority until the highest-cost residue is reduced or explicitly deferred with evidence.
- Remove or narrow the remaining highest-cost legacy and compatibility surfaces without changing core-host-pack contracts.
- Reduce the full Python suite runtime materially below the current long-tail behavior by cutting redundant or low-signal integration coverage and tiering slower cases.
- Leave behind a clearer boundary map of which debt was removed, which debt remains, and what rules prevent it from growing again.

## In Scope
- Integration-test tail reduction, fixture reuse, and retirement of redundant end-to-end coverage.
- Compatibility shims, migration residue, duplicated registry declarations, and stale contract glue across `core/**`, `core/python/**`, `plan/.wt/**`, and `plan/python/**`.
- Dead or low-signal code paths, test helpers, and edge-case coverage that no longer protect active contracts.
- Documentation and initiative tracking updates required to explain the debt removed and any bounded deferrals.

## Out Of Scope
- New feature delivery that is unrelated to debt reduction.
- Large architectural rewrites unless the existing debt inventory proves one is required to remove a concentrated source of drag.
- OpenTelemetry expansion, multi-user concurrency work, or unrelated new standards authoring beyond the debt-removal boundaries.
- Removing valid contract coverage merely to make the test suite faster.

## Operator Requirements
- Prefer deleting or collapsing obsolete paths over adding more compatibility layers.
- Preserve existing external command behavior, public import surfaces, and governed artifact contracts unless a controlled contract change is explicitly captured.
- Keep each debt-reduction slice evidence-backed: before-versus-after runtime, coverage intent, or residue inventory.
- Treat tests as first-class debt surfaces. Slow, duplicated, or migration-only tests should be challenged rather than preserved by inertia.

## Acceptance Criteria
- The initiative produces a concrete debt inventory ranked by maintenance cost, runtime impact, or boundary confusion.
- The highest-value test tail and legacy residue slices are reduced or removed with validation evidence.
- Shared-core and plan-pack registries or validators no longer carry avoidable duplicate or stale declarations introduced by migration-era work.
- The full repo validation gate remains green after every landed slice.
- The closeout summary records removed debt, retained debt, explicit deferrals, and the next recommended tranche if any high-cost residue remains.

## Non-Goals
- This initiative does not keep every historical edge case simply because it once existed.
- This initiative does not optimize for abstract cleanliness without measurable usability or maintainability gain.
- This initiative does not merge reusable core and pack-owned code just to make cleanup easier.

## Planned Task Set
- `task.repository_tech_debt_reduction_program.bootstrap_repository_tech_debt_reduction_program`: Finish bootstrap, author the detailed debt-removal plan, confirm inputs, approve the initiative, and seed the execution tasks.
- `task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt`: Capture the current debt inventory across tests, compatibility shims, duplicate registries, and migration residue, then rank the first removal slices.
- `task.repository_tech_debt_reduction_program.reduce_integration_tail_and_tier_tests`: Reduce the slow integration tail, remove redundant end-to-end cases, and define a clearer fast-versus-slow suite boundary.
- `task.repository_tech_debt_reduction_program.remove_stale_compatibility_and_migration_residue`: Remove stale compatibility imports, migration-era glue, and dead edge-case support that no longer protects an active contract.
- `task.repository_tech_debt_reduction_program.reconcile_duplicate_registry_and_contract_declarations`: Collapse avoidable duplicated registry or schema declarations between shared core and the active plan pack where one contract surface should remain authoritative.
- `task.repository_tech_debt_reduction_program.validate_and_close_first_tech_debt_tranche`: Run the final repo gate, record the debt removed and the remaining residue, and close the initiative cleanly.
