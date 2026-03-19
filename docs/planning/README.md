# `docs/planning`

## Description
`This directory holds the traced planning corpus plus the richer human companion trackers derived from the live plan workspace. Use it for PRDs, technical designs, implementation plans, durable decisions, and human-readable tracker pages that complement the authoritative live state under plan/**.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/README.md` | Describes the purpose of the planning directory and its document families. |
| `docs/planning/coordination_tracking.md` | Human-readable companion tracker for retained traced planning context and broader family navigation. |
| `docs/planning/initiatives/` | Holds the initiative-family tracker and retained initiative companion surfaces. |
| `docs/planning/prds/` | Holds product requirements documents and PRD tracking surfaces. |
| `docs/planning/design/` | Holds feature designs, implementation plans, and design tracking surfaces. |
| `docs/planning/decisions/` | Holds durable decision records and decision tracking surfaces. |
| `docs/planning/tasks/` | Holds the derived human task tracker plus retained historical task Markdown. |

## Notes
- Start with `plan/plan_overview.md` when the main question is current live planning state and next action.
- Start with `plan/.wt/indexes/coordination_index.json` when the main question is the machine-readable live current-state view.
- Treat `requirements.md` and `decisions.md` as the authoritative implementation contract for the plan-workspace cutover.
- Treat `docs/planning/**` as the traced planning corpus and human companion layer, not as the live execution authority.
- The live task, initiative, readiness, discrepancy, review, closeout, and evidence indexes now live under `plan/.wt/indexes/`.
- The family trackers in this directory should remain summary-first, but they must retain browseable terminal-history tables where that detail materially helps human review.
- `docs/planning/tasks/**` is no longer the live task authority. New execution work belongs under initiative-local `plan/**/.wt/tasks/**`.
- Use `uv run watchtower-core query coordination --format json`, `query initiatives --format json`, and `query tasks --format json` when you need exact live machine lookup without browsing rendered Markdown.
