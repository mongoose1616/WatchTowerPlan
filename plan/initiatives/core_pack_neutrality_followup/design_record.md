# Core Pack Neutrality Followup Design Record

## Summary
Removes remaining donor-style plan assumptions from shared core tests, fixtures, and core-owned standards while keeping legitimate current-repo pack facts scoped to plan-owned boundaries.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/core_pack_neutrality_followup/.wt/`.
- The code changes are limited to `WatchTowerPlan/core/**`, plus plan-owned test destinations when a shared-core test is deliberately moved out of core.
- The purpose is shared-core portability, not a repo-wide rename of the active `plan` pack.

## Architecture
### Shared Fixture Contract
- Replace the current donor-style hosted-pack fixture template with a neutral fixture-pack template under `core/python/tests/fixtures/packs/`.
- The fixture helper will materialize requested pack IDs, slugs, namespaces, distributions, packages, and integration modules from neutral placeholders.
- The helper should not special-case `watchtower_plan.integration`.

### Test Boundary
- Keep reusable-core tests under `core/python/tests/**` only when they can run against shared control-plane state, synthetic pack fixtures, or generic sample paths.
- Move tests to `plan/python/tests/**` when they require live rendered surface IDs, live plan initiative indexes, or other plan-owned artifact families.
- Add or refresh boundary documentation so the split remains explicit for future maintainers and agents.

### Documentation Contract
- For standards operationalization, prefer canonical repo-relative glob patterns such as `*/workflows/modules/`, `*/docs/standards/*/*_standard.md`, `*/docs/commands/`, and `*/tracking/` when the guidance applies to hosted-pack families generically.
- For front-matter `applies_to`, use only canonical existing repo-relative paths or non-path scope tokens. Do not use `plan/**` paths unless the document intentionally applies to the live `plan` workspace as a repository fact.
- Keep current-repository foundation statements out of scope unless they are directly blocking shared-core portability validation.

## Validation Strategy
- Run targeted pytest over touched shared-core tests and any relocated plan-owned tests.
- Run `ruff` and `mypy` on the touched shared-core and plan-owned test roots.
- Run `watchtower-core validate all --skip-acceptance --format json`.
- Run at least one broad pytest pass spanning `core/python/tests` and `plan/python/tests` for regression confidence after the moves.
