# `docs/planning`

## Description
`This directory groups the repository's planning and decision-making surfaces. Use it for PRDs, technical designs, implementation plans, and durable decision records that should stay linked as one planning corpus.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/README.md` | Describes the purpose of the planning directory and its document families. |
| `docs/planning/initiatives/` | Holds the start-here initiative view that projects phase, owner, and next-step status across the planning corpus. |
| `docs/planning/prds/` | Holds product requirements documents and PRD tracking surfaces. |
| `docs/planning/design/` | Holds feature designs, implementation plans, and design tracking surfaces. |
| `docs/planning/decisions/` | Holds durable decision records and decision tracking surfaces. |
| `docs/planning/tasks/` | Holds local-first task records plus the human task tracker for active and closed work. |

## Notes
- Start with `docs/planning/initiatives/` when the main question is "what is happening with this initiative right now?"
- Start with `uv run watchtower-core query coordination --format json` when the main question is the machine-readable current planning view and next action.
- Keep upstream product intent in `prds/`, solution design in `design/`, and durable choice history in `decisions/`.
- Keep engineer-sized execution work in `tasks/` rather than overloading PRD or design trackers as task boards.
- Keep standards in `docs/standards/`, references in `docs/references/`, and workflows in `workflows/`.
