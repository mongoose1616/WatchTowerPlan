# `watchtower_core.sync`

## Summary
Guardrail namespace root that keeps repo-local sync orchestration out of the export-safe package surface.

## Boundary
- `Classification`: `boundary_layer`
- `Supported Imports`: The namespace root only, for boundary discovery and explicit failure when callers reach for repo-local sync services from the wrong package.
- `Non-Goals`: Supported repo-specific leaf imports under `watchtower_core.sync`.

## Key Surfaces
- `__init__.py`: Guardrail that rejects repo-local sync imports and redirects callers to `watchtower_core.repo_ops.sync`.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/sync/README.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
