# `watchtower_core.routing`

## Summary
Reusable route-selection runtime over the governed route and workflow indexes.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.routing`
- `Non-Goals`: CLI formatting, repo-local route handlers, workflow execution orchestration, or plan-flavored routing wrappers.

## Key Surfaces
- `engine.py`: Stable routing engine that selects governed routes by request text or explicit task type.

## Related Surfaces
- `core/python/src/watchtower_core/query/routes.py`
- `core/control_plane/indexes/routes/route_index.json`

## Notes
- Keep governed route selection here.
- Keep repo-local route narration and command handlers outside this namespace.
