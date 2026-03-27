# Source-Of-Truth Contract Map

## Current Contract Docs

Use these as primary authority for the live platform:

- `core/docs/standards/engineering/domain_pack_authoring_standard.md`
- `core/docs/standards/engineering/hosted_pack_integration_standard.md`
- `core/docs/standards/engineering/core_host_pack_python_boundary_standard.md`
- `core/docs/standards/data_contracts/pack_interface_contract_standard.md`
- `core/docs/standards/operations/customer_release_and_bootstrap_standard.md`
- `core/docs/commands/core_python/watchtower_core_pack_scaffold.md`
- `core/docs/commands/core_python/watchtower_core_pack_bootstrap.md`
- `core/docs/commands/core_python/watchtower_core_pack_validate.md`
- `core/docs/commands/core_python/watchtower_core_pack_export.md`
- `core/docs/commands/core_python/watchtower_core_validate_document_semantics.md`

## Reusable-Core Implementation References

Use these to resolve concrete runtime shape:

- `core/python/src/watchtower_core/pack_integration/`
- `core/python/src/watchtower_core/query/`
- `core/python/src/watchtower_core/sync/`
- `core/python/src/watchtower_core/rebuild/`
- `core/python/src/watchtower_core/control_plane/pack_context.py`
- `core/python/src/watchtower_core/control_plane/governance_surfaces.py`
- `core/control_plane/registries/*.json`
- `core/control_plane/schemas/interfaces/packs/*.schema.json`

## Working Hosted-Pack References

Use working packs as implementation-pattern references, not higher authority:

- `/home/j/WatchTowerPlan/plan`
- `/home/j/WatchTowerOversight/oversight`

Reference patterns to lift:

- pack root layout;
- pack settings and runtime manifest shape;
- workflow metadata registry shape;
- integration descriptor shape;
- pack-owned document semantics wiring;
- docs and workflow layout.

## Target-Repository Integration Steps

The final implementation target is `/home/j/WatchTower`. The planning package must keep this sequence explicit:

1. export shared core from `/home/j/WatchTowerPlan/core`;
2. copy exported core into `/home/j/WatchTower`;
3. scaffold or author the offensive-security pack against that copied core;
4. run `pack bootstrap` to reconcile shared registry/workspace state inside `/home/j/WatchTower`;
5. run `pack validate` and `validate all`;
6. run export or release proof for the intended handoff mode.
