# `watchtower-core sync task-index`

## Summary
This command rebuilds the live plan task index from initiative-local task state under `plan/**/.wt/tasks/**`.

## Use When
- You changed one or more live task records and need the machine-readable task index to match current initiative-local task state.
- You want to inspect the rebuilt task index in dry-run mode before writing it to the canonical live plan path.
- You want a controlled way to regenerate task lookup data without rebuilding unrelated derived artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync task-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync task-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical task-index path in `plan/.wt/indexes/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync task-index
```

```sh
cd core/python
uv run watchtower-core sync task-index --write
```

```sh
cd core/python
uv run watchtower-core sync task-index --output /tmp/task_index.json --format json
```

## Behavior and Outputs
- The command reads initiative-local task state under `plan/**/.wt/tasks/**` and rebuilds the machine-readable task index deterministically.
- The rebuild uses live task JSON as the primary source for stable identity, task execution state, ownership, trace links, initiative context, and update timestamps.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many task entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt task-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source documents or rebuilt artifact are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync task-tracking` | Rebuilds the human-readable task tracker from the same live task sources. |
| `watchtower-core plan query tasks` | Reads the task index that this command rebuilds. |
| `watchtower-core sync traceability-index` | Reads the task index as one of its governed source surfaces. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `plan/python/src/watchtower_plan/sync/task_index.py`
- `plan/.wt/indexes/task_index.json`

## Updated At
- `2026-03-14T05:37:06Z`
