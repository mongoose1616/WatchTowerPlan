# `watchtower-core sync initiative-tracking`

## Summary
This command rebuilds the human-readable initiative tracker from the governed initiative index.

## Use When
- You changed the initiative index and need the start-here initiative board to match the current traced planning state.
- You want to inspect initiative counts in dry-run mode before writing the canonical tracker.
- You want a deterministic way to refresh the human-readable initiative board without hand-editing it.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync initiative-tracking` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync initiative-tracking [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt tracker to the canonical initiative-tracking path under `docs/planning/initiatives/`.
- `--output <path>`: Optional explicit output path for the rebuilt tracker.
- `--include-document`: Include the rebuilt tracker content in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync initiative-tracking
```

```sh
cd core/python
uv run watchtower-core sync initiative-tracking --write
```

```sh
cd core/python
uv run watchtower-core sync initiative-tracking --output /tmp/initiative_tracking.md --format json
```

## Behavior and Outputs
- The command reads the governed initiative index and rebuilds the human-readable initiative tracker deterministically.
- The tracker summarizes active and closed initiatives with current phase, ownership, key surfaces, next surfaces, and next-action guidance.
- By default the command runs in dry-run mode and does not mutate the canonical tracker.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many initiatives were summarized.
- In `json` mode, the command prints one JSON object with the command name, status, initiative counts, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt tracker content.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source initiative index is invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync initiative-index` | Rebuilds the machine-readable initiative index from the authoritative source surfaces. |
| `watchtower-core query initiatives` | Reads the initiative index that aligns with the same tracker content. |
| `docs/planning/initiatives/initiative_tracking.md` | Canonical tracker path that this command refreshes in write mode. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_tracking.py`
- `docs/planning/initiatives/initiative_tracking.md`

## Updated At
- `2026-03-14T05:37:06Z`
