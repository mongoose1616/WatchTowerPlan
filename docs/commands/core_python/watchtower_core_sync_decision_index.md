# `watchtower-core sync decision-index`

## Summary
This command rebuilds the governed decision index from the governed decision records under `docs/planning/decisions/`.

## Use When
- You changed a durable decision record and need the machine-readable decision index to match the current planning document.
- You want to inspect the rebuilt decision index in dry-run mode before writing it to the canonical control-plane path.
- You want a controlled way to regenerate one planning index without rebuilding unrelated derived artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync decision-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync decision-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical decision-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync decision-index
```

```sh
cd core/python
uv run watchtower-core sync decision-index --write
```

```sh
cd core/python
uv run watchtower-core sync decision-index --output /tmp/decision_index.v1.json --format json
```

## Behavior and Outputs
- The command reads the governed decision records under `docs/planning/decisions/` and rebuilds the machine-readable decision index deterministically.
- The rebuild uses governed decision-record front matter as the primary source for stable identity, traceability, lifecycle, and update timestamps.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many decision entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt decision-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source documents or rebuilt artifact are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync traceability-index` | Reads the decision index as one of its governed source surfaces. |
| `watchtower-core validate front-matter` | Validates the governed decision-record front matter that this command depends on. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/repo_ops/sync/decision_index.py`
- `core/control_plane/indexes/decisions/decision_index.v1.json`

## Updated At
- `2026-03-14T05:37:06Z`
