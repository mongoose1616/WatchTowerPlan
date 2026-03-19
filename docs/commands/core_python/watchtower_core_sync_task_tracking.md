# `watchtower-core sync task-tracking`

## Summary
This command rebuilds the human-readable task tracker from initiative-local live task state under `plan/**/.wt/tasks/**`.

## Use When
- You changed one or more live task records and need the human-readable task board to match current initiative-local task state.
- You want to inspect task counts in dry-run mode before writing the canonical tracker.
- You want a deterministic way to refresh the local task board without hand-editing the tracker.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync task-tracking` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync task-tracking [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt tracker to the canonical task-tracking path under `plan/tracking/`.
- `--output <path>`: Optional explicit output path for the rebuilt tracker.
- `--include-document`: Include the rebuilt tracker content in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync task-tracking
```

```sh
cd core/python
uv run watchtower-core sync task-tracking --write
```

```sh
cd core/python
uv run watchtower-core sync task-tracking --output /tmp/task_tracking.md --format json
```

## Behavior and Outputs
- The command reads initiative-local live task state under `plan/**/.wt/tasks/**` and rebuilds the human-readable task tracker deterministically.
- The tracker renders active and terminal task tables from live task state so humans can browse current work and completed outcomes without opening raw task JSON.
- By default the command runs in dry-run mode and does not mutate the canonical tracker.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many tasks were summarized.
- In `json` mode, the command prints one JSON object with the command name, status, task counts, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt tracker content.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source live task records are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync task-index` | Rebuilds the machine-readable task index from the same live task sources. |
| `watchtower-core query tasks` | Reads the task index that reflects the same live task records. |
| `plan/tracking/task_tracking.md` | Canonical tracker path that this command refreshes in write mode. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/plan_runtime/sync/task_tracking.py`
- `plan/tracking/task_tracking.md`

## Updated At
- `2026-03-15T05:45:00Z`
