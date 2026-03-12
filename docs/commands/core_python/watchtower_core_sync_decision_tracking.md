# `watchtower-core sync decision-tracking`

## Summary
This command rebuilds the human-readable decision tracker from the governed decision index and the initiative-closeout state stored in traceability.

## Use When
- You changed a decision record or initiative closeout state and need the decision tracker to match.
- You want a readable decision-tracking refresh without hand-editing `decision_tracking.md`.
- You want to inspect the rebuilt tracker in dry-run mode before writing it canonically.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync decision-tracking` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync decision-tracking [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt tracker to the canonical decision-tracking path in `docs/planning/decisions/`.
- `--output <path>`: Optional explicit output path for the rebuilt tracker.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync decision-tracking
```

```sh
cd core/python
uv run watchtower-core sync decision-tracking --write
```

## Behavior and Outputs
- The command is derived from the decision index and the traceability closeout layer rather than hand-maintained tracker text.
- By default the command runs in dry-run mode and does not mutate the canonical tracker.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many decision records it tracked.
- In `json` mode, the command prints one JSON object with the command name, status, decision count, write flag, and output path when one was written.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync decision-index` | Rebuilds the machine-readable decision index that this tracker reads. |
| `watchtower-core sync traceability-index` | Rebuilds the traceability layer that provides initiative closeout state to this tracker. |
| `watchtower-core closeout initiative` | Updates the initiative-closeout state that this tracker mirrors. |
| `watchtower-core query decisions` | Reads the decision index directly when you need machine-readable lookup rather than the human tracker. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/repo_ops/sync/decision_tracking.py`
- `docs/planning/decisions/decision_tracking.md`

## Updated At
- `2026-03-12T22:05:00Z`
