# `watchtower-core sync repository-paths`

## Summary
This command rebuilds the repository path index from README inventory tables and can optionally write the result.

## Use When
- You want to regenerate the curated repository path index after README inventory changes.
- You want a dry-run count of the derived path entries before writing the artifact.
- You need machine-readable output for an automated refresh workflow.

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
uv run watchtower-core sync repository-paths [options]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical control-plane path.
- `--output <path>`: Write the rebuilt artifact to an explicit output path.
- `--include-document`: Include the generated document in JSON output.
- `--format <human|json>`: Select human-readable or structured JSON output. Defaults to `human`.
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
uv run watchtower-core sync repository-paths --format json --include-document
```

## Behavior and Outputs
- In `human` mode, the command reports the rebuilt entry count and whether the artifact was written or kept in dry-run mode.
- In `json` mode, the command prints a single JSON object with `entry_count`, `wrote`, and `artifact_path`, and optionally the full generated document.
- By default, the command runs in dry-run mode and does not mutate repository state.
- When `--write` or `--output` is supplied, the command writes the rebuilt artifact to disk.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent namespace for sync subcommands. |
| `watchtower-core query paths` | Reads the repository path index rebuilt by this command. |
| `watchtower-core query trace` | Can depend on path entries that remain discoverable through the rebuilt index. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/sync/repository_paths.py`
- `core/control_plane/indexes/repository_paths/repository_path_index.v1.json`

## Updated At
- `2026-03-09T05:43:10Z`
