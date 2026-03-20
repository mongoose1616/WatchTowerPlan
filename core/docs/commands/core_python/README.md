# `core/docs/commands/core_python`

## Description
`This directory contains shared and reusable-core command pages for the core Python workspace and the watchtower-core CLI family. Use it to find the root command, shared command groups, and the highest-signal shared leaf pages before falling back to machine-readable command lookup.`

## Notes
- Start with `watchtower_core.md` for the root command and shared options.
- Use `watchtower_core_route.md` when the main question is how a request maps to workflow modules.
- Use `watchtower_core_query.md` when the main question is which shared read-only lookup surface to use.
- Use `watchtower_core_sync.md` when the main question is which shared derived artifact to rebuild.
- For plan-owned command groups and leaf pages, start in `plan/docs/commands/core_python/`.
- Use the command-group pages before opening individual subcommand pages.
- Use `watchtower_core_validate_suite.md` when the main question is how to run one pack-declared validation suite with optional `pack_settings` selection.
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you want the governed machine lookup surface instead of browsing this directory.

## Files
| Path | Description |
|---|---|
| `core/docs/commands/core_python/README.md` | Describes the purpose of the core Python command-doc directory and the fastest ways to find command details. |
| `core/docs/commands/core_python/watchtower_core.md` | Human-readable page for the root `watchtower-core` command and shared CLI behavior. |
| `core/docs/commands/core_python/watchtower_core_route.md` | Entry page for advisory route preview commands. |
| `core/docs/commands/core_python/watchtower_core_query.md` | Entry page for shared governed query commands such as command discovery, repository paths, standards, references, foundations, workflows, acceptance, and evidence. |
| `core/docs/commands/core_python/watchtower_core_query_foundations.md` | Query foundations by topic, related surface, authority, or downstream citation or application use. |
| `core/docs/commands/core_python/watchtower_core_query_commands.md` | Machine-readable lookup page for finding any other current command page without scanning the directory manually. |
| `core/docs/commands/core_python/watchtower_core_sync.md` | Entry page for reusable-core sync commands such as command, route, and repository-path rebuilds. |
| `core/docs/commands/core_python/watchtower_core_validate.md` | Entry page for validation commands across artifacts, semantics, and repo-wide checks. |
| `core/docs/commands/core_python/watchtower_core_validate_suite.md` | Runs one pack-declared validation suite through the reusable-core suite runtime. |
| `core/docs/commands/core_python/watchtower_core_doctor.md` | Fastest non-mutating health snapshot for the Python workspace and governed repository surfaces. |
