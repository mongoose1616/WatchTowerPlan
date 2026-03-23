# Core Portability Follow-up Root Pack And Query Typing Decision Notes

## Summary
Records the bounded decisions for the copied-core portability follow-up slice.

## Locked Decisions
- Treat `WatchTowerPlan` steady-state `plan` ownership as intentional, not as donor residue to remove in this initiative.
- Prefer first-party root-pack examples such as `oversight/` in shared help, docs, and generic tests. Keep `packs/<slug>` documented as supported, but not as the only topology.
- Keep one explicit externalized-pack test family where the purpose is to prove multi-pack or externalized-pack behavior.
- Fix the host query handler type baseline through explicit local typed helper boundaries rather than broad `cast()` spray or `# type: ignore`.
- Limit code changes to reusable-core and host-owned files under `core/**`; do not patch `WatchTowerOversight`.
- Keep validation bounded to the touched host query handlers, affected shared-core tests, and the repo validation gate needed for changed docs and artifacts.

## Deferred Items
- Full removal of `watchtower_plan` imports from every shared-core test
- Changing `core/python/pyproject.toml` away from the current repo-local `watchtower-plan` dependency
- Converting derived indexes and current repo command surfaces to copied-core consumer state
