# `watchtower-core query commands`

## Summary
This command searches the command index with simple structured filters and returns matching command entries.

## Use When
- You want to discover the current documented command surface quickly.
- You want to filter commands by kind or tag instead of reading command pages manually.
- You need machine-readable command lookup output for automation or agent workflows.

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
uv run watchtower-core query commands [options]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed command fields.
- `--kind <kind>`: Exact command-kind filter.
- `--tag <tag>`: Exact tag filter.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Defaults to `human`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query commands --query doctor
```

```sh
cd core/python
uv run watchtower-core query commands --tag sync --format json
```

## Behavior and Outputs
- In `human` mode, the command prints a compact list of matching commands and summaries.
- In `json` mode, the command prints a single JSON object with `result_count` and `results`.
- If no commands match, the command prints an explicit no-match message and exits with status code `0`.
- The command reads the current command index and does not mutate repository state.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent namespace for query subcommands. |
| `watchtower-core` | Root command whose documented subcommands are discoverable through this lookup. |
| `watchtower-core query paths` | Searches repository paths instead of command pages. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/commands.py`
- `core/control_plane/indexes/commands/command_index.v1.json`

## Updated At
- `2026-03-09T05:43:10Z`
