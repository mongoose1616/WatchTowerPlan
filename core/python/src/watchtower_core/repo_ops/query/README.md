# `watchtower_core.repo_ops.query`

## Summary
Authoritative repository query services for governed indexes, planning joins, and route-preview lookup behavior.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit query services such as `StandardQueryService`, `RouteQueryService`, and planning-record query modules.
- `Non-Goals`: Stable public export surface through `watchtower_core.query`.

## Key Surfaces
- `commands.py`, `coordination.py`, and `planning.py`: Machine-readable repository navigation and planning lookup.
- `routes.py`: Advisory route-preview matching logic.
- `standards.py`, `tasks.py`, `workflows.py`, and related modules: Family-specific index-backed lookup.

## Related Surfaces
- `core/python/src/watchtower_core/query/README.md`
- `docs/commands/core_python/watchtower_core_query.md`
