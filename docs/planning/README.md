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
- Start with `uv run watchtower-core query coordination --format json` when the main question is the machine-readable active current-state view and next action.
- Use `./.venv/bin/watchtower-core query coordination --format json` from `core/python/` when you need the same machine-readable planning view without relying on `uv` on `PATH`.
- Treat coordination as an active-first start-here projection plus compact recent-closeout context, not as the exhaustive historical planning view.
- Filterless `uv run watchtower-core query initiatives --format json` and `uv run watchtower-core query planning --format json` now default to `initiative_status=active`; use explicit `--initiative-status <status>` for terminal history and `--trace-id <trace_id>` when you already know the closed trace you need.
- Use `docs/planning/initiatives/initiative_tracking.md` or `uv run watchtower-core query initiatives --initiative-status <status> --format json` when you need filtered terminal history, broader initiative-family browsing, or explicit non-active status lookup.
- Use `uv run watchtower-core query planning --trace-id <trace_id> --format json` when the main question is the canonical deep planning record for one known trace rather than the filterless active browse.
- Machine-readable planning projections use explicit status fields such as `artifact_status`, `initiative_status`, `record_status`, `decision_status`, and `task_status`; do not collapse them into one generic status concept.
- Use `uv run watchtower-core query authority --domain planning --format json` when the main question is which planning or governance surface is canonical for a recurring lookup question.
- Use `docs/planning/initiatives/initiative_tracking.md` when you need the deeper initiative-family view instead of the compact root tracker.
- Keep upstream product intent in `prds/`, solution design in `design/`, and durable choice history in `decisions/` after current repository scope is clear.
- Keep engineer-sized execution work in `tasks/` rather than overloading PRD or design trackers as task boards.
- Keep standards in `docs/standards/`, references in `docs/references/`, and workflows in `workflows/`.
