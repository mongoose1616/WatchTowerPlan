# `watchtower-core query paths`

## Summary
This command searches the repository path index with simple structured filters and returns matching path entries.

## Use When
- You want to find governed entrypoint paths without scanning the tree manually.
- You want to filter repository surfaces by `surface_kind`, tag, or parent path.
- You need machine-readable lookup output for automation or agent workflows.

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
uv run watchtower-core query paths [options]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed path fields.
- `--surface-kind <kind>`: Exact `surface_kind` filter.
- `--tag <tag>`: Exact tag filter.
- `--parent-path <path>`: Exact parent-path filter.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Defaults to `human`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query paths --query planning
```

```sh
cd core/python
uv run watchtower-core query paths --surface-kind prd --format json
```

## Behavior and Outputs
- In `human` mode, the command prints a compact list of matching paths and summaries.
- In `json` mode, the command prints a single JSON object with `result_count` and `results`.
- If no paths match, the command prints an explicit no-match message and exits with status code `0`.
- The command reads the current repository path index and does not mutate repository state.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent namespace for query subcommands. |
| `watchtower-core query commands` | Searches command-index entries instead of repository paths. |
| `watchtower-core sync repository-paths` | Rebuilds the repository path index consumed by this query. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/repository.py`
- `core/control_plane/indexes/repository_paths/repository_path_index.v1.json`

## Updated At
- `2026-03-09T05:43:10Z`
