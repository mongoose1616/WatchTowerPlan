# `watchtower_core.query`

## Summary
Export-safe generic query services over governed pack surfaces, command and workflow indexes, authority maps, route metadata, artifact-family rules, and governed knowledge or record indexes such as standards, references, foundations, acceptance contracts, evidence, repository paths, and traceability.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: The package root plus explicit generic query submodules such as `commands`, `workflows`, `routes`, `authority`, `governance_surfaces`, `artifact_families`, `acceptance`, `evidence`, `foundations`, `references`, `repository`, `standards`, and `traceability`.
- `Non-Goals`: Pack-owned initiative, task, review, closeout, discrepancy, readiness, evidence, and other pack-local query services that belong under the owning pack package such as `watchtower_plan.query`, plus pack-flavored duplicates of reusable query helpers.

## Key Surfaces
- `__init__.py`: Curated root export surface for reusable generic query services while still fail-closing pack-owned query surfaces that do not belong in reusable core.
- `common.py`: Shared text normalization, scoring, and query-adapter helpers used by both reusable-core and pack-owned query services.
- `rendered_search.py`: Shared rendered-surface search filters, ranking helpers, and deterministic initiative search-term builders used by hosted packs.
- `commands.py`, `workflows.py`, and `authority.py`: Index and registry query services for generic governed lookups.
- `routes.py`: Export-safe advisory route-preview service over the governed route and workflow indexes.
- `governance_surfaces.py`: Pack-surface lookup over `pack_settings` and `governance_surface_map`.
- `artifact_families.py`: Artifact-family registry query and path-resolution helpers.
- `acceptance.py`, `evidence.py`, and `traceability.py`: Governed record lookup over acceptance contracts, validation evidence, and traceability indexes.
- `foundations.py`, `references.py`, `standards.py`, and `repository.py`: Structured query services over governed knowledge and repository-discovery indexes.

## Related Surfaces
- `plan/python/src/watchtower_plan/query/README.md`
- `requirements.md`
- `decisions.md`

## Notes
- Keep generic governed-surface query helpers here.
- Keep pack-owned query packages such as `watchtower_plan.query` narrow and limited to pack-local lookup behavior that cannot already live under reusable core.
- Do not reintroduce plan-flavored duplicates of query helpers that already fit the reusable-core boundary.
