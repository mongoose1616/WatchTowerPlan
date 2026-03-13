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

## Files
| Path | Description |
|---|---|
| `core/python/src/watchtower_core/repo_ops/query/README.md` | Describes the repository query-service boundary and adjacent command docs. |
| `core/python/src/watchtower_core/repo_ops/query/common.py` | Shared projection-search helpers and deterministic query-term builders for trace-linked planning views. |
| `core/python/src/watchtower_core/repo_ops/query/planning.py` | Deep planning-catalog query service over the canonical planning join. |
| `core/python/src/watchtower_core/repo_ops/query/initiatives.py` | Compact initiative-family query service over phase, owner, and blocker projections. |
| `core/python/src/watchtower_core/repo_ops/query/coordination.py` | Active-first coordination query service that layers the coordination snapshot over initiative history lookup. |

## Related Surfaces
- `core/python/src/watchtower_core/query/README.md`
- `docs/commands/core_python/watchtower_core_query.md`
