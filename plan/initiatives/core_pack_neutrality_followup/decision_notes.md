# Core Pack Neutrality Followup Decision Notes

## Summary
This document captures the design decisions that keep shared core exportable without falsifying current `WatchTowerPlan` repository facts.

## Locked Decisions
- Shared-core tests may use synthetic fixture packs and synthetic pack-owned paths, but they must not require a live `watchtower_plan` import or a live `plan/**` workspace unless they are explicitly moved under `plan/python/tests/**`.
- Shared-core standards and references should express generic hosted-pack behavior with canonical repo-relative globs or neutral prose, not with `plan/**` operationalization paths, unless the reference is intentionally describing the current repository as a fact.
- Current shared foundations may continue to mention the live `plan` pack where they are documenting the actual repository layout or mirror contract. This initiative does not rewrite those foundations into abstract templates.
- If a test exercises rendered-surface IDs, initiative indexes, or other live planning artifacts owned by `plan`, that test belongs under `plan/python/tests/**`.
- The shared fixture-pack template should be neutral source data. It may still be generated from test-owned fixture files inside `core/python/tests/fixtures/**`, but those files must not encode donor pack identity as the authored contract.
- Documentation updates must include explicit split-test maintenance guidance so future developers and agents do not drift plan-only tests back into shared core.

## Deferred Decisions
- Whether shared foundations should eventually move to a separate export-ready corpus independent of repository-specific current-state facts.
- Whether the synthetic source Python package under `core/python/tests/fixtures/python/**` also needs renaming away from `oversight` terminology in a later cleanup.
