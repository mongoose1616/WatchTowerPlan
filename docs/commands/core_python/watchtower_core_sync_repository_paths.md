# `watchtower-core sync repository-paths`

## Summary
This command rebuilds the repository path index from README inventory tables and can either report the rebuilt result or write it back to disk.

## Use When
- You changed README inventory tables and need the governed repository path index to match.
- You want to inspect the rebuilt path-index document before writing it to the canonical control-plane location.
- You want a controlled way to regenerate one index without rebuilding unrelated artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync repository-paths` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync repository-paths [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical control-plane path.
- `--output <path>`: Write the rebuilt artifact to an explicit alternate path.
- `--include-document`: Include the full generated document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync repository-paths
```

```sh
cd core/python
uv run watchtower-core sync repository-paths --write
```

```sh
cd core/python
uv run watchtower-core sync repository-paths --output /tmp/repository_path_index.v1.json --format json
```

## Behavior and Outputs
- The command rebuilds the repository path index from README inventory rows.
- By default, the command runs in dry-run mode and does not mutate repository state.
- If `--write` is provided, the command writes the rebuilt artifact to the canonical control-plane path.
- If `--output` is provided, the command writes the rebuilt artifact to the requested destination.
- In `human` mode, the command prints whether it ran as a dry run or wrote the rebuilt artifact.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, whether a file was written, and the artifact path when applicable.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for rebuild operations. |
| `watchtower-core query paths` | Reads the repository path index that this command rebuilds. |
| `core/control_plane/indexes/repository_paths/repository_path_index.v1.json` | Canonical governed artifact written by this command when `--write` is used. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/sync/repository_paths.py`
- `core/control_plane/indexes/repository_paths/repository_path_index.v1.json`

## Updated At
- `2026-03-09T05:43:47Z`
