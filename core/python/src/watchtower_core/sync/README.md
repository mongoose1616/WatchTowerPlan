# `watchtower_core.sync`

## Summary
Sync namespace for the reusable generic harness plus repo-shared governed-index rebuild services that are not specific to plan-domain business logic.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.sync.SyncHarness`, `SyncTargetSpec`, `SyncRecord`, and `SyncResult` from the package root, plus explicit repo-shared leaf modules such as `watchtower_core.sync.reference_index`, `watchtower_core.sync.foundation_index`, `watchtower_core.sync.standard_index`, `watchtower_core.sync.workflow_index`, `watchtower_core.sync.route_index`, and `watchtower_core.sync.repository_paths`.
- `Non-Goals`: Plan-domain coordination, initiative, task, tracker, and GitHub sync orchestration that still belongs under `watchtower_plan.sync`, and plan-flavored copies of the generic sync harness or rebuild helpers.

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
- `plan/python/src/watchtower_plan/sync/README.md`
- `requirements.md`
- `decisions.md`

## Notes
- Keep reusable harness behavior, dependency ordering, shared reference-resolution helpers, and repo-shared rebuild targets here.
- Keep host-composed command-index rebuilding under `watchtower_host.cli.command_index`, because it depends on the host parser tree rather than reusable-core runtime alone.
- Keep `watchtower_plan.sync` narrow and limited to live plan write targets, joins, and orchestration that depend on the current WatchTowerPlan layout.
