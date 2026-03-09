# `watchtower-core query paths`

## Summary
This command searches the repository path index by free text and exact filters so engineers can find high-signal repository surfaces quickly.

## Use When
- You need to locate a directory or file family by purpose rather than exact path.
- You want to browse one surface kind such as `command_doc`, `standard_doc`, or `control_plane_index`.
- You want machine-readable search results for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query paths` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query paths [--query <text>] [--surface-kind <kind>] [--tag <tag>] [--parent-path <path>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed fields such as path, summary, aliases, tags, and related paths.
- `--surface-kind <kind>`: Exact surface-kind filter such as `command_doc`, `standard_doc`, or `control_plane_index`.
- `--tag <tag>`: Exact tag filter.
- `--parent-path <path>`: Exact parent-path filter such as `docs/commands/core_python/`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query paths --query command
```

```sh
cd core/python
uv run watchtower-core query paths --surface-kind command_doc --limit 5 --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints a short result summary followed by matching repository paths and their summaries.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and result records.
- If no entries match the requested filters, the command exits successfully and reports that no repository path entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core query commands` | Searches the command index instead of repository paths. |
| `watchtower-core sync repository-paths` | Rebuilds the repository path index that this command reads. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/repository.py`
- `core/control_plane/indexes/repository_paths/repository_path_index.v1.json`

## Updated At
- `2026-03-09T05:43:47Z`
