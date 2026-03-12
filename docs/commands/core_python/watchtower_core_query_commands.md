# `watchtower-core query commands`

## Summary
This command searches the governed command index so engineers can discover available CLI commands, their command pages, and their implementation surfaces.

## Use When
- You know the task you want to perform but not the exact command name.
- You want to filter commands by kind or tag instead of scanning command docs manually.
- You want machine-readable command lookup results for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query commands` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query commands [--query <text>] [--kind <kind>] [--tag <tag>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed fields such as command name, summary, synopsis, aliases, and output formats.
- `--kind <kind>`: Exact command-kind filter such as `root_command` or `subcommand`.
- `--tag <tag>`: Exact tag filter.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query commands --query doctor
```

```sh
cd core/python
uv run watchtower-core query commands --tag query --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints a short result summary followed by matching command names and summaries.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and result records.
- If no entries match the requested filters, the command exits successfully and reports that no command entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core` | Root command that exposes the CLI family. |
| `docs/commands/core_python/README.md` | Human-readable command-family inventory for the current workspace. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/repo_ops/query/commands.py`
- `core/control_plane/indexes/commands/command_index.v1.json`

## Updated At
- `2026-03-12T22:05:00Z`
