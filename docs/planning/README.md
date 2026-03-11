# `docs/planning`

## Description
`This directory groups the repository's planning and decision-making surfaces. Use it for PRDs, technical designs, implementation plans, and durable decision records that should stay linked as one planning corpus.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/README.md` | Describes the purpose of the planning directory and its document families. |
| `docs/planning/coordination_tracking.md` | Generated human-readable current-state tracker for planning coordination, next action, and compact active work context. |
| `docs/planning/initiatives/` | Holds the initiative-family tracking view that projects phase, owner, and next-step status across traced planning work. |
| `docs/planning/prds/` | Holds product requirements documents and PRD tracking surfaces. |
| `docs/planning/design/` | Holds feature designs, implementation plans, and design tracking surfaces. |
| `docs/planning/decisions/` | Holds durable decision records and decision tracking surfaces. |
| `docs/planning/tasks/` | Holds local-first task records plus the human task tracker for active and closed work. |

## Notes
- Start with `docs/foundations/repository_scope.md` when the main question is whether work belongs in this repository or in future product implementation.
- Start with `docs/planning/coordination_tracking.md` when the main question is the current human-readable planning state and next action.
- Start with `uv run watchtower-core query coordination --format json` when the main question is the machine-readable current planning view and next action.
- Use `./.venv/bin/watchtower-core query coordination --format json` from `core/python/` when you need the same machine-readable planning view without relying on `uv` on `PATH`.
- Use `docs/planning/initiatives/initiative_tracking.md` when you need the deeper initiative-family view instead of the compact root tracker.
- Keep upstream product intent in `prds/`, solution design in `design/`, and durable choice history in `decisions/` after current repository scope is clear.
- Keep engineer-sized execution work in `tasks/` rather than overloading PRD or design trackers as task boards.
- Keep standards in `docs/standards/`, references in `docs/references/`, and workflows in `workflows/`.
