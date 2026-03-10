# `watchtower-core sync workflow-index`

## Summary
This command rebuilds the governed workflow index from the workflow modules under `workflows/modules/`.

## Use When
- You changed a workflow module and need the machine-readable workflow index to reflect the current workflow corpus.
- You want workflow lookup and routing surfaces to stay aligned with the current workflow modules.
- You want a controlled way to regenerate one workflow-specific index without rebuilding unrelated derived artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync workflow-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync workflow-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical workflow-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync workflow-index
```

```sh
cd core/python
uv run watchtower-core sync workflow-index --write
```

```sh
cd core/python
uv run watchtower-core sync workflow-index --output /tmp/workflow_index.v1.json --format json
```

## Behavior and Outputs
- The command reads workflow modules under `workflows/modules/` and rebuilds the machine-readable workflow index deterministically.
- The rebuild validates workflow structure, section order, optional explained `Additional Files to Load` bullets, and governed local-reference usage.
- Workflow modules that publish `Additional Files to Load` must keep it task-specific, repo-local, and free of generic routing-baseline boilerplate.
- Workflow modules that try to cite raw external URLs instead of governed local reference docs under `docs/references/` are rejected during rebuild.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many workflow entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt workflow-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source workflow modules or rebuilt artifact are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core query workflows` | Reads the workflow index that this command rebuilds. |
| `watchtower-core sync reference-index` | Rebuilds the companion reference index used to derive transitive external authority. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/sync/workflow_index.py`
- `core/control_plane/indexes/workflows/workflow_index.v1.json`

## Updated At
- `2026-03-10T00:55:31Z`
