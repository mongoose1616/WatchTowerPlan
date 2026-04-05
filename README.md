# `.`

## Description
`This repository is the first internal plan-domain workspace plus a synchronized local copy of the shared WatchTower core from WatchTowerCore/. Use the root only for repository scope, routing, current-state orientation, and top-level review. Keep the root scoped to those concerns while documenting every materially distinct repository boundary or navigation rule needed to avoid ambiguity: live plan state belongs under plan/, the synchronized shared implementation copy lives under core/, the local shared foundations copy lives under core/docs/foundations/, and the mirrored plan-facing foundations view lives under plan/docs/foundations/.`

## Paths
| Path | Description |
|---|---|
| `README.md` | Describes the purpose of the repository root and the main entrypoints stored here. |
| `AGENTS.md` | Defines the repository-wide wrapper instructions and routes work into `core/workflows/` and `plan/workflows/`. |
| `.github/` | Holds GitHub-hosted collaboration scaffolding such as issue forms and the pull request template. |
| `plan/` | Holds the live plan-domain workspace, machine authority root, and scoped initiative or project containers. |
| `core/docs/` | Holds shared command docs, references, templates, shared standards, and the local synchronized shared foundations copy. |
| `plan/docs/` | Holds durable plan-domain guidance plus the mirrored foundations family. |
| `core/` | Holds the local synchronized shared implementation assets and control-plane tree sourced from `WatchTowerCore/`. |

## Notes
- Current repository contract: `core/docs/foundations/repository_scope.md`, `core/docs/foundations/repository_standards_posture.md`, shared standards under `core/docs/standards/`, plan-domain standards under `plan/docs/standards/`, and the local synchronized shared machine authority under `core/control_plane/` plus `plan/.wt/`.
- Treat supporting references and helper docs as secondary guidance that must stay consistent with those current authority surfaces.
- Human current-state start-here: `plan/README.md`, then `plan/plan_overview.md`
- Shared workflow start-here: `core/workflows/README.md`
- Human plan workflow start-here: `plan/workflows/README.md`
- Local shared foundations start-here: `core/docs/foundations/README.md`
- Mirrored plan foundations start-here: `plan/docs/foundations/README.md`
- Local shared machine authority start-here: `core/control_plane/README.md`
- Machine current-state start-here: `plan/.wt/indexes/coordination_index.json`
- Machine project lookup start-here: `plan/.wt/indexes/project_index.json`
- Shared Python workspace start-here: `core/python/README.md`
- Plan-owned Python boundary start-here: `plan/python/README.md`
- Shared-core upstream authoring home: `WatchTowerCore/core/`
- Machine canonical-surface lookup: `cd core/python && ./.venv/bin/watchtower-core plan query authority --domain planning --format json`
- Legacy docs-backed planning has been purged. Use `plan/initiatives/**`, `plan/projects/**`, and `plan/tracking/**` as the retained working surfaces instead.
- Portable customer bootstrap is an allowlisted export of shared `core/` plus intentionally selected pack roots. Raw repo snapshots, retained records, live plan state, tests, and local runtime outputs are internal repository material by default.
