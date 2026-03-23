# Core Portability Follow-up Root Pack And Query Typing Design Record

## Summary
Cleans up copied-core portability debt in shared help, command docs, tests, and host query typing without changing WatchTowerPlan's current steady-state plan workspace contract.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/core_portability_followup_root_pack_and_query_typing/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Design Approach
- Separate copied-core portability concerns from current donor-repo facts.
- Only change reusable-core and host-owned surfaces where the current behavior is intended to be pack-generic:
  - CLI examples and help text
  - shared core command docs and authoring references
  - generic fixture and test defaults
  - host query handler typing
- Leave current repo truths untouched when they are the active `WatchTowerPlan` contract:
  - `pack.plan` as the current default hosted pack
  - the live `watchtower-core plan ...` command family
  - the current shared `watchtower-plan` workspace installation entry

## Root-Pack Documentation Strategy
- Use a first-party root pack such as `oversight/` as the primary example in generic shared-core help and docs.
- Phrase externalized `packs/<slug>` roots as an allowed alternative topology, not the assumed default.
- Update the pack family help, root parser examples, validate family examples, and core-owned pack command docs together so help and docs stay aligned.

## Test Strategy
- Convert generic scaffold/bootstrap expectations to first-party root-pack examples where the test is proving generic hosted-pack support.
- Keep the explicit externalized-pack integration file focused on multi-pack or externalized-pack behavior, because that topology is still supported and should remain covered.
- Reuse the existing fixture support, which already knows how to rewrite copied fixtures for both first-party root packs and `packs/<slug>` pack roots.

## Typing Strategy
- Introduce local typed payload helper aliases or protocols in the host query handler modules so render helpers accept concrete entry types instead of `object`.
- Keep the handlers thin and avoid moving query-service behavior just to satisfy typing.
- Use type boundaries that reflect the query-service return models already exported by `watchtower_core.query`.

## Validation Strategy
- Run targeted `mypy` over the three host query handler files during implementation.
- Run targeted pytest over the edited shared-core tests.
- Run `watchtower-core validate all --skip-acceptance --format json` after documentation updates.
- If command-doc metadata or governed surfaces drift, run the minimum necessary reconciliation/sync before closeout.
