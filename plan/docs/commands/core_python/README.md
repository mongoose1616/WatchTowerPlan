# `plan/docs/commands/core_python`

## Description
`This directory contains plan-owned command pages for the watchtower-core plan namespace. Use it for pack-native bootstrap, query, sync, task, and closeout behavior that no longer belongs in shared core docs.`

## Notes
- Start with `watchtower_core_plan.md` for the plan namespace entrypoint.
- Use `watchtower_core_plan_query.md` for live plan lookup and `watchtower_core_plan_sync.md` for plan-owned derived-surface rebuilds.
- Use `watchtower_core_plan_task.md` for initiative-local task lifecycle mutation and `watchtower_core_plan_closeout.md` for terminal plan closeout flows.
- Keep shared and reusable-core command docs under `core/docs/commands/core_python/`.
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you need machine lookup instead of browsing command pages manually.

## Paths
| Path | Description |
|---|---|
| `plan/docs/commands/core_python/README.md` | Describes the purpose of the plan-owned core Python command-doc directory. |
| `plan/docs/commands/core_python/watchtower_core_plan.md` | Entry page for the pack-owned `watchtower-core plan` namespace. |
| `plan/docs/commands/core_python/watchtower_core_plan_query.md` | Entry page for plan-owned live query commands. |
| `plan/docs/commands/core_python/watchtower_core_plan_sync.md` | Entry page for plan-owned sync commands. |
| `plan/docs/commands/core_python/watchtower_core_plan_task.md` | Entry page for plan-owned task lifecycle commands. |
| `plan/docs/commands/core_python/watchtower_core_plan_closeout.md` | Entry page for plan-owned closeout commands. |
