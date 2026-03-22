# Root Pack Schema Catalog Contract Alignment

## Summary
Extends the reusable-core schema catalog canonical-path contract to support first-party root pack machine roots such as <pack>/.wt without donor-specific exceptions.

## Identity
- `initiative_id`: `initiative.root_pack_schema_catalog_contract_alignment`
- `trace_id`: `trace.root_pack_schema_catalog_contract_alignment`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.root_pack_schema_catalog_contract_alignment.bootstrap_root_pack_schema_catalog_contract_alignment`: Bootstrap Root Pack Schema Catalog Contract Alignment live initiative package.

## Problem
- The reusable-core schema catalog artifact schema currently accepts canonical schema paths only under `core/control_plane`, `packs/<slug>/.wt`, or `plan/.wt`.
- Reusable core already supports first-party root pack operating mode for pack discovery and pack workspace roots, but the schema-catalog contract still rejects root-pack schema paths such as `oversight/.wt/schemas/...`.
- This creates a donor-specific mismatch: a copied root pack can satisfy the pack manifest and discovery rules while still failing schema-catalog validation.

## Desired Outcome
- Reusable core accepts canonical schema paths for both supported pack layouts:
  - first-party root packs at `<pack>/.wt/...`
  - nested packs at `packs/<slug>/.wt/...`
- The contract stays generic and does not special-case `oversight`.
- Shared documentation and regression tests describe and prove that root packs are valid for schema-catalog publication.

## In Scope
- `core/control_plane/schemas/artifacts/schema_catalog.schema.json`
- reusable-core tests that enforce or depend on schema-catalog canonical-path validation
- shared pack-authoring or schema-catalog docs that need to reflect the broadened root-pack contract

## Out Of Scope
- Oversight-owned schema IDs, titles, or donor naming residue
- pack registry defaults, pack CLI namespace wiring, or workspace dependency rewrites
- plan-pack deplanification beyond the minimum wording needed to keep the contract donor-neutral

## Acceptance Criteria
- A schema catalog under a first-party root pack such as `oversight/.wt/registries/schema_catalog.json` can publish canonical schema paths under `oversight/.wt/schemas/...` without failing the shared schema-catalog artifact contract.
- Existing nested-pack fixture coverage under `packs/<slug>/.wt` continues to pass unchanged.
- Existing plan root-pack behavior under `plan/.wt` continues to pass unchanged.
- `watchtower-core validate all --skip-acceptance --format json` remains green after the contract update.

## Non-Goals
- Do not introduce donor-specific path allowlists for `oversight`.
- Do not relax the contract to arbitrary repository paths; keep it constrained to supported reusable-core schema roots.
