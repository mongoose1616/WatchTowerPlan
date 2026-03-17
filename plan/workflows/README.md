# `plan/workflows`

## Description
`This directory is the human workflow entrypoint for the live plan domain. Use it to find the plan-side workflow starting points and migration notes for routed execution while the canonical routing table and workflow modules still live under the repository-root workflows tree.`

## Paths
| Path | Description |
|---|---|
| `plan/workflows/README.md` | Describes the purpose of the plan workflow entrypoint and its current migration boundary. |
| `plan/workflows/AGENTS.md` | Defines local instructions for plan-domain workflow guidance surfaces. |

## Notes
- Start here when the main question is how live plan work should be routed or narrated for humans.
- The canonical routing backend remains [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md) plus the modules under [workflows/modules](/home/j/WatchTowerPlan/workflows/modules) until a later slice completes the workflow-root split.
- This directory is intentionally thin in the current cutover step: it publishes the plan-domain start-here surface without duplicating the underlying workflow engine.
