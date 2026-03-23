# Core Pack Neutral Portability Cleanup Design Record

## Summary
Removes remaining shared-core plan-specific test and documentation coupling so copied core works with any hosted pack.

## Design Boundary
- Shared-core behavior stays in `core/**`.
- Pack-owned direct-runtime assertions move to `plan/python/tests/**`.
- Current-repository foundations and current live pack-owned docs remain where they are when they state real repo facts rather than generic reusable-core policy.

## Test Split Design
- `core/python/tests/**` proves reusable-core loaders, validators, host composition, synthetic pack fixtures, and pack-neutral runtime contracts.
- `plan/python/tests/**` proves direct `watchtower_plan` behavior, current live `plan` command/doc surfaces, and current-repository pack-owned contracts.
- Shared-core tests that need pack context should build it through synthetic fixture packs or copied pack roots, not through the live `plan` workspace.

## Helper Strategy
- Keep `tests.pack_fixture_support` as the shared-core synthetic pack fixture helper, but replace donor-pack defaults with neutral example defaults.
- Keep pack-owned test support under `watchtower_plan.testing` when the helper is only meaningful for plan-owned tests.
- Generic helper records that currently use `pack.plan` as example data should become neutral example pack identifiers.

## Documentation Strategy
- Remove unnecessary direct links to `plan/python/tests/` from shared-core reference and standards docs.
- Use generic forms such as `<pack-root>/python/tests/` in core-owned guidance unless the line is explicitly documenting the current internal pack.
- Update shared test-suite docs and validation standards to say that pack-owned tests live under the owning pack root and that live-pack assumptions must not remain in the shared-core suite.
