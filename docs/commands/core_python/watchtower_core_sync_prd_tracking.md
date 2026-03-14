# `watchtower-core sync prd-tracking`

## Summary
This command rebuilds the human-readable PRD tracker from the governed PRD index and the initiative-closeout state stored in traceability.

## Use When
- You changed a PRD or initiative closeout state and need the PRD tracker to match.
- You want a readable PRD tracker refresh without hand-editing `prd_tracking.md`.
- You want to inspect the rebuilt tracker in dry-run mode before writing it canonically.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync prd-tracking` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync prd-tracking [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt tracker to the canonical PRD-tracking path in `docs/planning/prds/`.
- `--output <path>`: Optional explicit output path for the rebuilt tracker.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync prd-tracking
```

```sh
cd core/python
uv run watchtower-core sync prd-tracking --write
```

## Behavior and Outputs
- The command is derived from the PRD index and the traceability closeout layer rather than hand-maintained tracker text.
- By default the command runs in dry-run mode and does not mutate the canonical tracker.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many PRDs it tracked.
- In `json` mode, the command prints one JSON object with the command name, status, PRD count, write flag, and output path when one was written.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync prd-index` | Rebuilds the machine-readable PRD index that this tracker reads. |
| `watchtower-core sync traceability-index` | Rebuilds the traceability layer that provides initiative closeout state to this tracker. |
| `watchtower-core closeout initiative` | Updates the initiative-closeout state that this tracker mirrors. |
| `watchtower-core query prds` | Reads the PRD index directly when you need machine-readable lookup rather than the human tracker. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/repo_ops/sync/prd_tracking.py`
- `docs/planning/prds/prd_tracking.md`

## Updated At
- `2026-03-14T05:37:06Z`
