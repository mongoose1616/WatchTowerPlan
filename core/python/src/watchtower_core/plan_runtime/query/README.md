# `watchtower_core.plan_runtime.query`

## Summary
Authoritative repository query services for live plan indexes, promoted guidance, and other repo-local lookup behavior that is not export-safe enough for the reusable-core query package.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit plan-runtime query modules such as `coordination`, `initiatives`, `tasks`, `readiness`, `discrepancies`, `projects`, `standards`, `references`, `foundations`, `acceptance`, `evidence`, and `traceability`.
- `Non-Goals`: Re-owning the generic command, workflow, authority, route-preview, governance-surface, or artifact-family query services that now live under `watchtower_core.query`.

## Key Surfaces
- `coordination.py`: Active-first coordination lookup over the live plan-workspace indexes and rendered companion surfaces.
- `initiatives.py`, `tasks.py`, `readiness.py`, `discrepancies.py`, `plan_evidence.py`, `closeouts.py`, `reviews.py`, and `projects.py`: Initiative-local and pack-local planning state lookup.
- `standards.py`, `references.py`, `foundations.py`, `acceptance.py`, `evidence.py`, `artifacts.py`, and `traceability.py`: Repo-local durable-guidance and trace-linked lookup layered over the current promoted plan/docs and control-plane surfaces.
- Reusable command, workflow, authority, and route-preview queries now resolve directly from `watchtower_core.query` even when imported through `watchtower_core.plan_runtime.query`.

## Files
| Path | Description |
|---|---|
| `core/python/src/watchtower_core/plan_runtime/query/README.md` | Describes the repository query-service boundary and adjacent command docs. |
| `core/python/src/watchtower_core/plan_runtime/query/common.py` | Shared rendered-surface search helpers and deterministic query-term builders for trace-linked planning views. |
| `core/python/src/watchtower_core/plan_runtime/query/initiatives.py` | Compact initiative-family query service over phase, owner, and blocker rendered surfaces. |
| `core/python/src/watchtower_core/plan_runtime/query/coordination.py` | Active-first coordination query service that layers the coordination snapshot over initiative history lookup. |

## Related Surfaces
- `core/python/src/watchtower_core/query/README.md`
- `core/docs/commands/core_python/watchtower_core_query.md`
