# `watchtower_core.repo_ops.query`

## Summary
Authoritative repository query services for live planning indexes, planning joins, and other repo-local lookup behavior that is not export-safe enough for the reusable-core query package.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit query services such as `StandardQueryService`, `RouteQueryService`, and planning-record query modules.
- `Non-Goals`: Re-owning the generic command, workflow, authority, route-preview, governance-surface, or artifact-family query services that now live under `watchtower_core.query`.

## Key Surfaces
- `coordination.py` and `planning.py`: Live planning and deep-trace lookup over plan-workspace indexes and joins.
- `initiatives.py`, `tasks.py`, `readiness.py`, `projects.py`, and `discrepancies.py`: Initiative-local and pack-local planning state lookup.
- `standards.py`, `references.py`, `foundations.py`, and related modules: Repo-local docs-backed knowledge lookup that still depends on this repository's current corpus.
- `commands.py`, `workflows.py`, `authority.py`, and `routes.py`: Compatibility import locations for reusable-core generic query services.

## Files
| Path | Description |
|---|---|
| `core/python/src/watchtower_core/repo_ops/query/README.md` | Describes the repository query-service boundary and adjacent command docs. |
| `core/python/src/watchtower_core/repo_ops/query/common.py` | Shared rendered-surface search helpers and deterministic query-term builders for trace-linked planning views. |
| `core/python/src/watchtower_core/repo_ops/query/planning.py` | Deep planning-catalog query service over the canonical planning join. |
| `core/python/src/watchtower_core/repo_ops/query/initiatives.py` | Compact initiative-family query service over phase, owner, and blocker rendered surfaces. |
| `core/python/src/watchtower_core/repo_ops/query/coordination.py` | Active-first coordination query service that layers the coordination snapshot over initiative history lookup. |

## Related Surfaces
- `core/python/src/watchtower_core/query/README.md`
- `docs/commands/core_python/watchtower_core_query.md`
