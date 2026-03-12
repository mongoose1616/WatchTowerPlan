# `docs/commands/core_python`

## Description
`This directory contains command pages for the core Python workspace and the watchtower-core CLI family. Use it to find the root command, the main command groups, and the highest-signal leaf pages to open before falling back to machine-readable command lookup.`

## Notes
- Start with `watchtower_core.md` for the root command and shared options.
- Use `watchtower_core_route.md` when the main question is how a request maps to workflow modules.
- Use `watchtower_core_plan.md` when the main question is how to scaffold planning artifacts or bootstrap a traced planning chain.
- Use `watchtower_core_query.md` when the main question is which read-only lookup surface to use, then open `watchtower_core_query_foundations.md` when the question is which foundation document governs a surface or which docs cite or apply it.
- Use `watchtower_core_task.md` when the main question is how to create, update, or transition governed local task records.
- Use `watchtower_core_sync.md` when the main question is which derived artifact to rebuild, then open `watchtower_core_sync_foundation_index.md` when a foundations change needs the machine-readable intent index refreshed.
- Use the command-group pages before opening individual subcommand pages.
- Use `watchtower_core_query_coordination.md` when the main question is current planning state, next action, and active work context.
- Use `watchtower_core_query_planning.md` when the main question is the canonical deep planning record for one trace after coordination routing.
- Use `watchtower_core_query_authority.md` when the main question is which machine surface is canonical for a planning or governance lookup.
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you want the governed machine lookup surface instead of browsing this directory.

## Files
| Path | Description |
|---|---|
| `docs/commands/core_python/README.md` | Describes the purpose of the core Python command-doc directory and the fastest ways to find command details. |
| `docs/commands/core_python/watchtower_core.md` | Human-readable page for the root `watchtower-core` command and shared CLI behavior. |
| `docs/commands/core_python/watchtower_core_route.md` | Entry page for advisory route preview commands. |
| `docs/commands/core_python/watchtower_core_plan.md` | Entry page for planning scaffold and bootstrap commands. |
| `docs/commands/core_python/watchtower_core_query.md` | Entry page for all governed query commands, including planning, standards, references, and trace surfaces. |
| `docs/commands/core_python/watchtower_core_query_foundations.md` | Query foundations by topic, related surface, authority, or downstream citation or application use. |
| `docs/commands/core_python/watchtower_core_query_coordination.md` | Machine start-here command page for active traced initiative coordination and next-step lookup. |
| `docs/commands/core_python/watchtower_core_query_planning.md` | Canonical deep-planning query page for one trace-linked planning record with explicit status semantics. |
| `docs/commands/core_python/watchtower_core_query_authority.md` | Canonical surface-discovery query page for planning and governance questions. |
| `docs/commands/core_python/watchtower_core_query_commands.md` | Machine-readable lookup page for finding any other current command page without scanning the directory manually. |
| `docs/commands/core_python/watchtower_core_task.md` | Entry page for task lifecycle commands that mutate governed local task records in dry-run or write mode. |
| `docs/commands/core_python/watchtower_core_sync.md` | Entry page for all sync commands, including full repo rebuilds and narrower index/tracking refreshes. |
| `docs/commands/core_python/watchtower_core_sync_foundation_index.md` | Rebuild surface for the machine-readable foundation index derived from governed foundation docs. |
| `docs/commands/core_python/watchtower_core_sync_planning_catalog.md` | Rebuild surface for the canonical planning catalog derived from trace-linked planning sources. |
| `docs/commands/core_python/watchtower_core_validate.md` | Entry page for validation commands across artifacts, semantics, and repo-wide checks. |
| `docs/commands/core_python/watchtower_core_closeout.md` | Entry page for closeout commands used to terminally update traced initiative state. |
| `docs/commands/core_python/watchtower_core_doctor.md` | Fastest non-mutating health snapshot for the Python workspace and governed repository surfaces. |
