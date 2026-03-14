# `watchtower-core sync traceability-index`

## Summary
This command rebuilds the governed traceability index from the published planning indexes, acceptance contracts, and validation-evidence artifacts.

## Use When
- You changed a PRD, decision, design, acceptance contract, or validation-evidence artifact and need the unified traceability join surface to match.
- You want to inspect the rebuilt traceability index in dry-run mode before writing it to the canonical control-plane path.
- You want a controlled way to regenerate one joined index without rebuilding unrelated artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync traceability-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync traceability-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical traceability-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync traceability-index
```

```sh
cd core/python
uv run watchtower-core sync traceability-index --write
```

```sh
cd core/python
uv run watchtower-core sync traceability-index --output /tmp/traceability_index.v1.json --format json
```

## Behavior and Outputs
- The command reads the governed PRD, decision, and design indexes plus the acceptance-contract and validation-evidence artifacts, then rebuilds the unified traceability index deterministically.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many trace records were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt traceability-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if one of the source artifacts or the rebuilt document is invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync prd-index` | Rebuilds one of the planning-index source surfaces that this command reads. |
| `watchtower-core sync decision-index` | Rebuilds one of the planning-index source surfaces that this command reads. |
| `watchtower-core sync design-document-index` | Rebuilds one of the planning-index source surfaces that this command reads. |
| `watchtower-core query trace` | Reads the traceability index that this command rebuilds. |
| `watchtower-core validate artifact` | Validates the traceability index and related governed JSON artifacts. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/repo_ops/sync/traceability.py`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`

## Updated At
- `2026-03-14T05:37:06Z`
