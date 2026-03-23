# Copied Core Doctor Pack Surface Neutrality Design Record

## Summary
Makes the generic doctor command tolerate copied-core repositories whose active pack does not publish plan-style live indexes such as task_index or initiative_index.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/copied_core_doctor_pack_surface_neutrality/.wt/`.
- The implementation boundary is reusable core plus core-owned command and pack-authoring docs. No Oversight-owned files change here.
- The goal is to remove one remaining generic-host `plan` assumption without weakening real pack-contract validation.

## Runtime Model
- `watchtower-core doctor` should always load shared core governed surfaces because that is its primary health signal.
- Pack-owned live indexes are secondary informational counts, not the command’s core availability contract.
- The active pack still comes from the normal default-pack resolution flow. This slice does not add a new fallback or alternate registry layer.

## Handler Strategy
- Load the active/default pack settings normally.
- Build the set of declared pack surfaces from that manifest.
- Only load `task_index` and `initiative_index` when the active pack explicitly declares them.
- Return count `0` when those optional surfaces are absent.
- Do not swallow unrelated loader or schema failures; if pack settings or shared governed surfaces are genuinely invalid, doctor should still fail.

## Neighbor-Surface Review Boundary
- Re-run the copied-core smoke using a scaffolded first-party root pack, not a plan-flavored test fixture.
- Check adjacent generic host surfaces after the doctor fix: `pack validate`, `validate all`, `query commands`, `query paths`, `query workflows`, `query references`, `query standards`, and `query foundations`.
- Treat zero-result query responses for a bare scaffolded pack as acceptable when the authored pack has not published those families yet.

## Documentation Strategy
- Update the doctor command page so operators understand that absent pack-owned live indexes now resolve to zero counts.
- Update the pack-interface contract and pack-authoring reference so future pack authors and future agent loops know these live indexes are optional and generic host commands must tolerate their absence.

## Validation Strategy
- Add one copied-core integration test that proves doctor succeeds after scaffolding and bootstrapping a root-pack without plan-style live indexes.
- Re-run targeted lint, typing, and pytest for the touched handler and new regression.
- Re-run copied-core smoke manually against the neighboring generic host surfaces.
- Finish with broad repository validation.
