# `watchtower_core.sync`

## Summary
Compatibility namespace for explicit sync wrappers while keeping repo-local sync orchestration under `repo_ops.sync`.

## Boundary
- `Classification`: `boundary_layer`
- `Supported Imports`: Explicit compatibility wrappers under `watchtower_core.sync.<module>` when they exist.
- `Non-Goals`: Direct export of repo-specific aggregate sync services from `watchtower_core.sync` itself.

## Key Surfaces
- `__init__.py`: Guardrail that rejects unsupported repo-local sync imports from the namespace root.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/sync/README.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
