# `watchtower-core sync initiative-index`

## Summary
This command rebuilds the governed initiative index from traceability plus the current planning and task indexes.

## Use When
- You changed traced planning, task, evidence, or closeout state and need the cross-family initiative view to match.
- You want to inspect the rebuilt initiative index in dry-run mode before writing it to the canonical control-plane path.
- You want a deterministic way to regenerate initiative coordination data without rebuilding unrelated derived artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync initiative-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync initiative-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical initiative-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync initiative-index
```

```sh
cd core/python
uv run watchtower-core sync initiative-index --write
```

```sh
cd core/python
uv run watchtower-core sync initiative-index --output /tmp/initiative_index.v1.json --format json
```

## Behavior and Outputs
- The command reads the governed traceability, PRD, decision, design, and task indexes and rebuilds the machine-readable initiative index deterministically.
- The rebuild projects current phase, active ownership, blockers, the key surface to open first, and the next expected action for each trace.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many initiative entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt initiative-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source surfaces or rebuilt artifact are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync traceability-index` | Rebuilds the joined traceability layer this command projects from. |
| `watchtower-core sync initiative-tracking` | Rebuilds the human-readable tracker from the initiative index this command writes. |
| `watchtower-core query initiatives` | Reads the initiative index that this command rebuilds. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`
- `core/control_plane/indexes/initiatives/initiative_index.v1.json`

## Updated At
- `2026-03-14T05:37:06Z`
