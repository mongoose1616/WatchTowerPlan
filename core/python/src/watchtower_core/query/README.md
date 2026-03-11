# `watchtower_core.query`

## Summary
Compatibility namespace for explicit query wrappers that avoids exporting repo-local query orchestration from the package root.

## Boundary
- `Classification`: `boundary_layer`
- `Supported Imports`: Explicit compatibility wrappers under `watchtower_core.query.<module>` when they exist.
- `Non-Goals`: Direct export of repo-specific query services from `watchtower_core.query` itself.

## Key Surfaces
- `__init__.py`: Guardrail that rejects unsupported repo-local imports from the namespace root.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/query/README.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
