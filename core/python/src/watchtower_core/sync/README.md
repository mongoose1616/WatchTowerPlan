# `watchtower_core.sync`

## Summary
Export-safe sync namespace that publishes the reusable generic sync harness while keeping repo-specific sync targets out of the stable core surface.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.sync.SyncHarness`, `SyncTargetSpec`, `SyncRecord`, and `SyncResult` for export-safe multi-target sync orchestration.
- `Non-Goals`: Supported repo-specific leaf imports under `watchtower_core.sync`.

## Key Surfaces
- `__init__.py`: Export-safe root for the generic sync harness and fail-closed guidance for repo-specific sync services.
- `harness.py`: Shared sync target contracts, result models, overlay-aware runtime loader, and dependency-ordered orchestration helpers.

## Related Surfaces
- `core/python/src/watchtower_core/plan_runtime/sync/README.md`
- `requirements.md`
- `decisions.md`
