# `watchtower_core.sync`

## Summary
Sync namespace for the reusable generic harness plus repo-shared governed-index rebuild services that are not specific to pack-owned business logic.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.sync.SyncHarness`, `SyncTargetSpec`, `SyncRecord`, and `SyncResult` from the package root, plus explicit repo-shared leaf modules such as `watchtower_core.sync.reference_index`, `watchtower_core.sync.foundation_index`, `watchtower_core.sync.standard_index`, `watchtower_core.sync.workflow_index`, `watchtower_core.sync.route_index`, and `watchtower_core.sync.repository_paths`.
- `Non-Goals`: Pack-owned coordination, initiative, task, tracker, and external-system sync orchestration that belongs under the owning `watchtower_<pack>.sync` package, plus pack-flavored copies of the generic sync harness or rebuild helpers.

## Key Surfaces
- `__init__.py`: Export-safe root for the generic sync harness and fail-closed guidance for repo-specific sync services.
- `harness.py`: Shared sync target contracts, result models, overlay-aware runtime loader, and dependency-ordered orchestration helpers.
- `reference_index.py`, `foundation_index.py`, `standard_index.py`, and `workflow_index.py`: Repo-shared governed-doc and workflow index rebuild services consumed by hosted packs.
- `reference_resolution.py`: Shared reference-resolution helpers for governed-doc rebuild reuse.
- `path_support.py`: Shared repo-path existence helpers used by sync and traceability services.
- `route_index.py`: Repo-shared route-index rebuild service.
- `repository_paths.py`: Repo-shared repository-path index rebuild service.
- `rendered_tracking.py`: Shared rendered-tracker bootstrap, write helpers, and initiative-status summary shaping used by hosted packs.

## Related Surfaces
- `core/control_plane/indexes/references/reference_index.json`
- `core/control_plane/indexes/workflows/workflow_index.json`

## Notes
- Keep reusable harness behavior, dependency ordering, shared reference-resolution helpers, and repo-shared rebuild targets here.
- Keep host-composed command-index rebuilding under `watchtower_host.cli.command_index`, because it depends on the host parser tree rather than reusable-core runtime alone.
- Keep pack-owned sync packages such as `watchtower_<pack>.sync` narrow and limited to pack-local write targets, joins, and orchestration that depend on the current pack layout.
- Do not create pack-flavored copies of the generic sync harness, shared rebuild targets, or reusable sync result models.
