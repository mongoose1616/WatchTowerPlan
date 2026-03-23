# Copy-Forward Pack Runtime Hardening Decision Notes

## Summary
This initiative changes reusable-core runtime behavior for copied-core adoption without changing the current authored `plan` steady-state contract in this repository.

## Locked Decisions
- Keep the current authored `pack.plan` registry entry and the current `watchtower-plan` shared workspace registration intact in `WatchTowerPlan`.
- Add a bootstrap-mode runtime fallback for copied-core repositories instead of removing the steady-state shared workspace contract.
- Treat manifest discovery as the fallback runtime source for hosted-pack visibility when authored registry entries are stale, missing, or donor-specific in a consuming repository.
- Keep the authored hosted-pack registry as the persisted canonical inventory after bootstrap. Fallback discovery exists to keep copied-core adoption operable before local rewiring, not to replace the authored registry long-term.
- Prefer deterministic manifest discovery from first-party/root pack roots and nested `packs/<slug>/` roots over donor-name assumptions.
- Improve stale-registry and missing-manifest failures by returning structured command errors instead of tracebacks.
- Keep output-contract changes additive and minimal. Do not break existing JSON or human stdout payloads merely to surface fallback state.
- Update shared docs and standards in the same change set if runtime behavior now distinguishes bootstrap-mode fallback from steady-state authored registration.

## Explicit Non-Decisions
- This initiative does not declare that all consuming repositories may skip `pack bootstrap` permanently.
- This initiative does not remove pack-contract checks for shared `core/python` workspace registration.
- This initiative does not rewrite Oversight-owned pack artifacts, registries, or tests.
