# `watchtower_plan.query`

## Summary
Repo-local live plan query services for plan indexes, rendered planning views, and lookup behavior that cannot already live in the reusable-core query package.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit live plan query modules such as `coordination`, `initiatives`, `tasks`, `readiness`, `discrepancies`, `projects`, `reviews`, `closeouts`, `plan_evidence`, and `artifacts`.
- `Non-Goals`: Re-owning generic command, workflow, authority, route-preview, governance-surface, artifact-family, acceptance, evidence, standards, references, foundations, repository-path, or traceability query services that now live under `watchtower_core.query`.
- `Machine-State Boundary`: Query live plan machine state from `plan/.wt/**`; do not turn this package into a second machine-state store.

## Key Surfaces
- `coordination.py`: Active-first coordination lookup over the live plan-workspace indexes and rendered companion surfaces.
- `initiatives.py`, `tasks.py`, `readiness.py`, `discrepancies.py`, `plan_evidence.py`, `closeouts.py`, `reviews.py`, and `projects.py`: Initiative-local and pack-local planning state lookup.
- `artifacts.py`: Repo-local artifact lookup over live plan artifact indexes and package-local orchestration surfaces.
- Reusable command, workflow, authority, route-preview, knowledge, discovery, and record queries resolve directly from `watchtower_core.query`.
- Shared rendered-surface search filters, ranking helpers, and deterministic initiative search-term builders now live in `watchtower_core.query.rendered_search`.

## Shrink Rules
- Keep generic governed-surface query helpers in `watchtower_core.query`.
- Do not mirror reusable-core query structure here just to create plan-flavored duplicates.

## Files
| Path | Description |
|---|---|
| `plan/python/src/watchtower_plan/query/README.md` | Describes the repository query-service boundary and adjacent command docs. |
| `plan/python/src/watchtower_plan/query/initiatives.py` | Compact initiative-family query service over phase, owner, and blocker rendered surfaces. |
| `plan/python/src/watchtower_plan/query/coordination.py` | Active-first coordination query service that layers the coordination snapshot over initiative history lookup. |

## Related Surfaces
- `core/python/src/watchtower_core/query/README.md`
- `core/python/src/watchtower_core/query/rendered_search.py`
- `core/docs/commands/core_python/watchtower_core_query.md`
