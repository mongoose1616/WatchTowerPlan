# `watchtower_core.repo_ops.query`

## Summary
Authoritative repository query services for live planning indexes, planning joins, and other repo-local lookup behavior that is not export-safe enough for the reusable-core query package.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit planning and retained-corpus query modules such as `coordination`, `planning`, `initiatives`, `tasks`, `readiness`, `discrepancies`, `projects`, `standards`, and `references`.
- `Non-Goals`: Re-owning the generic command, workflow, authority, route-preview, governance-surface, or artifact-family query services that now live under `watchtower_core.query`.

## Key Surfaces
- `coordination.py` and `planning.py`: Live planning and deep-trace lookup over plan-workspace indexes and joins.
- `initiatives.py`, `tasks.py`, `readiness.py`, `discrepancies.py`, `plan_evidence.py`, `closeouts.py`, `reviews.py`, and `projects.py`: Initiative-local and pack-local planning state lookup.
- `standards.py`, `references.py`, `foundations.py`, `acceptance.py`, `evidence.py`, `artifacts.py`, and `traceability.py`: Repo-local retained-corpus and trace-linked lookup that still depends on this repository's current docs corpus.
- Reusable command, workflow, authority, and route-preview queries now resolve directly from `watchtower_core.query` even when imported through `watchtower_core.repo_ops.query`.

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
