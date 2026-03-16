# `watchtower_core.query`

## Summary
Guardrail namespace root that keeps repo-local query orchestration out of the export-safe package surface.

## Boundary
- `Classification`: `boundary_layer`
- `Supported Imports`: The namespace root only, for boundary discovery and explicit failure when callers reach for repo-local query services from the wrong package.
- `Non-Goals`: Supported repo-specific leaf imports under `watchtower_core.query`.

## Key Surfaces
- `__init__.py`: Guardrail that rejects repo-local query imports and redirects callers to `watchtower_core.repo_ops.query`.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/query/README.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
