# Core Shared Language Deplanification Design Record

## Summary
Removes WatchTowerPlan and plan-flavored wording from shared core standards, registries, and reusable-core READMEs so core authority stays pack-neutral.

## Design Boundary
- The change is documentation- and registry-only. It should not alter Python runtime behavior, command surfaces, loader contracts, or pack manifests.
- Shared-core surfaces may still mention the current internal plan pack when the repository layout makes that necessary, but those mentions must be framed as current examples or concrete repo facts rather than policy defaults.
- Pack-neutral policy language should prefer terms such as `pack-owned`, `pack-local`, `hosted pack`, or `current internal pack` over language that makes `WatchTowerPlan` sound like the reusable-core design target.

## Editing Strategy
- Update the reusable-core standards first because they set contributor expectations for the package boundary.
- Align the closest reusable-core package READMEs and the shared Python workspace README in the same tranche so the package-facing docs do not drift behind the standards.
- Keep registry structure stable and limit registry edits to notes, summaries, and `updated_at` metadata unless a validator proves a structural change is required.

## Risks And Controls
- Risk: over-correcting and removing useful concrete examples of the current repository layout.
  - Control: keep real path examples where they improve operator clarity, but qualify them as current-repo examples instead of normative design rules.
- Risk: changing standards without reconciling adjacent contributor docs.
  - Control: update the shared Python workspace README and affected reusable-core READMEs in the same change set.
- Risk: changing governed docs or registries without refreshing dependent derived surfaces.
  - Control: rebuild the affected indexes after editing and run the standard validation commands before closeout.
