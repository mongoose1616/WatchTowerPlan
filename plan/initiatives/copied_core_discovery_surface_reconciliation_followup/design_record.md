# Copied Core Discovery Surface Reconciliation Followup Design Record

## Summary
Extends copied-core bootstrap so shared discovery surfaces converge beyond command and repository-path indexes, and updates copy-forward guidance to exclude runtime environment artifacts.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/copied_core_discovery_surface_reconciliation_followup/.wt/`.
- The implementation boundary is reusable core plus core-owned docs. No Oversight-owned files are changed in this slice.

## Runtime Model
- `pack bootstrap` remains the explicit moment when a copied donor core becomes a locally authored shared-core steady state.
- The runtime discovery fallback already makes an unbootstrapped root pack visible enough for `pack list`, `pack describe`, and `pack validate`.
- The remaining gap is persisted discovery, not runtime pack loading. Bootstrap therefore needs to widen its write set rather than introducing another runtime-only layer.

## Bootstrap Reconciliation Model
- Bootstrap still starts from the candidate pack settings and runtime manifest, updates the shared hosted-pack registry, and reconciles shared workspace registration.
- When the shared hosted-pack registry changes, bootstrap must also rebuild the neighboring shared discovery surfaces that depend on:
  - current hosted-pack registration
  - current pack routing-table roots
  - current pack workflow-module roots
  - current citation and operationalization paths pointing into pack-owned docs
- The rebuilt surfaces are:
  - command index
  - repository-path index
  - reference index
  - standard index
  - workflow index
  - route index
- This keeps copied-core convergence as one explicit command instead of a hidden multi-command procedure.

## Rollback And Compatibility
- Bootstrap dry runs must preview the wider changed-path set without mutating any files.
- Write mode must snapshot and restore the wider set of derived artifacts if workspace sync or post-bootstrap validation fails.
- The stronger bootstrap path must not alter current `WatchTowerPlan` behavior because its authored `plan` pack remains valid and the rebuilt shared indexes should be semantically stable in the steady-state repo.

## Test Strategy
- Extend the copied-core bootstrap regression to inspect the additional shared indexes after bootstrapping an unbootstrapped first-party root pack into a donor-shaped temp repo.
- The fixture repo used by that regression must materialize the shared discovery sources needed for the additional index rebuilds.
- Keep at least one direct dry-run assertion so changed-path reporting stays accurate.

## Documentation Strategy
- Update the bootstrap command page to describe the full shared discovery-surface reconciliation contract.
- Update pack authoring and workspace guidance so downstream repos know:
  - raw `core/` copy is allowed as a source transfer
  - copied `.venv`, editable-install metadata, caches, and runtime state are unsupported residue
  - bootstrap is the required convergence step after the copy
