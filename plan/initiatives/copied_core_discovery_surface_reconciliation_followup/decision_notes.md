# Copied Core Discovery Surface Reconciliation Followup Decision Notes

## Summary
Locks the reusable-core decisions for the copied-core bootstrap reconciliation followup.

## Decisions
- The repeated copied-core portability issue is fixed in reusable core, not deferred to downstream repos.
- `watchtower-core pack bootstrap --write` remains the explicit copied-core reconciliation boundary.
- Bootstrap reconciliation must rebuild all shared discovery surfaces that are materially pack-composition dependent:
  - `core/control_plane/indexes/commands/command_index.json`
  - `core/control_plane/indexes/repository_paths/repository_path_index.json`
  - `core/control_plane/indexes/references/reference_index.json`
  - `core/control_plane/indexes/standards/standard_index.json`
  - `core/control_plane/indexes/workflows/workflow_index.json`
  - `core/control_plane/indexes/routes/route_index.json`
- The broader rebuild only runs when the hosted-pack registry actually changes.
- Bootstrap rollback must restore the additional shared indexes if any later step fails.
- Copy-forward documentation must explicitly exclude `core/python/.venv`, editable-install metadata, caches, and pack runtime state from the supported copy contract.

## Deferred Decisions
- Whether copied-core bootstrap should also regenerate other derived shared artifacts beyond the discovery surfaces above is deferred until another portability defect proves it is needed.
- Whether shared query/read paths should prefer more runtime-effective discovery over persisted indexes in broader bootstrap-mode scenarios remains deferred.
