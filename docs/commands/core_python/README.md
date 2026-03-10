# `docs/commands/core_python`

## Description
`This directory contains command pages for the core Python workspace and the watchtower-core CLI family. Use it to find the root command, the route, query, task, sync, closeout, and validate command groups, and the current behavior of each durable subcommand.`

## Notes
- Start with `watchtower_core.md` for the root command and shared options.
- Use `watchtower_core_route.md` when the main question is how a request maps to workflow modules.
- Use `watchtower_core_task.md` when the main question is how to create, update, or transition governed local task records.
- Use the command-group pages before opening individual subcommand pages.
- Use `watchtower_core_query_coordination.md` when the main question is current planning state, next action, and active work context.
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you want the governed machine lookup surface instead of browsing this directory.

## Files
| Path | Description |
|---|---|
| `docs/commands/core_python/README.md` | Describes the purpose of the core Python command-doc directory and the fastest ways to find command details. |
| `docs/commands/core_python/watchtower_core.md` | Human-readable page for the root `watchtower-core` command and shared CLI behavior. |
| `docs/commands/core_python/watchtower_core_route.md` | Entry page for advisory route preview commands. |
| `docs/commands/core_python/watchtower_core_route_preview.md` | Preview surface for routed workflow modules by request text or explicit task type. |
| `docs/commands/core_python/watchtower_core_query.md` | Entry page for all governed query commands, including planning, standards, references, and trace surfaces. |
| `docs/commands/core_python/watchtower_core_query_coordination.md` | Machine start-here command page for active traced initiative coordination and next-step lookup. |
| `docs/commands/core_python/watchtower_core_task.md` | Entry page for task lifecycle commands that mutate governed local task records in dry-run or write mode. |
| `docs/commands/core_python/watchtower_core_task_create.md` | Create one governed task document from compact structured inputs. |
| `docs/commands/core_python/watchtower_core_task_update.md` | Apply structured field and body updates to one governed task record. |
| `docs/commands/core_python/watchtower_core_task_transition.md` | Apply a bounded handoff-style status or ownership transition to one task. |
| `docs/commands/core_python/watchtower_core_sync.md` | Entry page for all sync commands, including full repo rebuilds and narrower index/tracking refreshes. |
| `docs/commands/core_python/watchtower_core_sync_route_index.md` | Rebuild surface for the machine-readable route index derived from the routing table. |
| `docs/commands/core_python/watchtower_core_validate.md` | Entry page for validation commands across artifacts, semantics, and repo-wide checks. |
| `docs/commands/core_python/watchtower_core_closeout.md` | Entry page for closeout commands used to terminally update traced initiative state. |
| `docs/commands/core_python/watchtower_core_doctor.md` | Fastest non-mutating health snapshot for the Python workspace and governed repository surfaces. |
| `docs/commands/core_python/watchtower_core_query_commands.md` | Query surface for locating command metadata and exact subcommand pages without scanning this directory manually. |
