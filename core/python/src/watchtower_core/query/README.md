# `watchtower_core.query`

## Summary
Export-safe generic query services over governed pack surfaces, command and workflow indexes, authority maps, route metadata, and artifact-family rules.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: The package root plus explicit generic query submodules such as `commands`, `workflows`, `routes`, `authority`, `governance_surfaces`, and `artifact_families`.
- `Non-Goals`: Live planning, initiative, task, discrepancy, and docs-backed knowledge query services that still depend on `watchtower_core.repo_ops.query`.

## Key Surfaces
- `__init__.py`: Curated root export surface for reusable generic query services while still fail-closing repo-local planning queries.
- `commands.py`, `workflows.py`, and `authority.py`: Index and registry query services for generic governed lookups.
- `routes.py`: Export-safe advisory route-preview service over the governed route and workflow indexes.
- `governance_surfaces.py`: Pack-surface lookup over `pack_settings` and `governance_surface_map`.
- `artifact_families.py`: Artifact-family registry query and path-resolution helpers.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/query/README.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
