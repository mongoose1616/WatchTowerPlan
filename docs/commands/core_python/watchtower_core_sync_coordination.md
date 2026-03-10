# `watchtower-core sync coordination`

## Summary
This command rebuilds the deterministic coordination slice for task, traceability, initiative, and coordination-index surfaces in one dependency-ordered run.

## Use When
- You changed governed task records and need the task index and task tracker refreshed together.
- You changed trace links or initiative-planning surfaces and want the initiative and coordination views rebuilt in order.
- You want a focused coordination rebuild without running the broader `sync all` surface set.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync coordination` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync coordination [--write] [--output-dir <dir>] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt coordination surfaces to their canonical repository paths.
- `--output-dir <dir>`: Optional explicit directory for materializing the coordination slice while preserving each rebuilt surface's repo-relative path.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync coordination
```

```sh
cd core/python
uv run watchtower-core sync coordination --write
```

```sh
cd core/python
uv run watchtower-core sync coordination --output-dir /tmp/watchtower_coordination --format json
```

## Behavior and Outputs
- The command runs the coordination sync registry group in deterministic order: `task-index`, `traceability-index`, `initiative-index`, `coordination-index`, `task-tracking`, and `initiative-tracking`.
- The command is dry-run by default and only reports what would be rebuilt unless `--write` or `--output-dir` is provided.
- With `--write`, the command updates the canonical task, traceability, initiative, and coordination surfaces in place.
- With `--output-dir`, the command materializes the rebuilt coordination slice into the selected directory while preserving repo-relative paths.
- In `json` mode, the command returns one result object per rebuilt surface with target name, output path, record count, and write status.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync all` | Rebuilds the coordination slice plus the rest of the deterministic local sync surfaces. |
| `watchtower-core sync task-index` | Rebuilds one of the machine-readable coordination surfaces included in this command. |
| `watchtower-core sync traceability-index` | Rebuilds one of the machine-readable coordination surfaces included in this command. |
| `watchtower-core sync initiative-index` | Rebuilds one of the machine-readable coordination surfaces included in this command. |
| `watchtower-core sync task-tracking` | Rebuilds one of the human-readable coordination trackers included in this command. |
| `watchtower-core sync initiative-tracking` | Rebuilds one of the human-readable coordination trackers included in this command. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/repo_ops/sync/coordination.py`
- `core/python/src/watchtower_core/repo_ops/sync/coordination_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/registry.py`

## Updated At
- `2026-03-10T19:06:55Z`
