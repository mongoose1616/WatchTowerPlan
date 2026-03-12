# `watchtower-core sync design-document-index`

## Summary
This command rebuilds the governed design-document index from the governed feature designs and implementation plans under `docs/planning/design/`.

## Use When
- You changed a feature design or implementation plan and need the machine-readable design-document index to match the current planning docs.
- You want to inspect the rebuilt design-document index in dry-run mode before writing it to the canonical control-plane path.
- You want a controlled way to regenerate one planning index without rebuilding unrelated derived artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync design-document-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync design-document-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical design-document-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync design-document-index
```

```sh
cd core/python
uv run watchtower-core sync design-document-index --write
```

```sh
cd core/python
uv run watchtower-core sync design-document-index --output /tmp/design_document_index.v1.json --format json
```

## Behavior and Outputs
- The command reads the governed design documents under `docs/planning/design/` and rebuilds the machine-readable design-document index deterministically.
- The rebuild uses governed feature-design and implementation-plan front matter as the primary source for stable identity, traceability, lifecycle, and update timestamps.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many design-document entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt design-document-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source documents or rebuilt artifact are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync traceability-index` | Reads the design-document index as one of its governed source surfaces. |
| `watchtower-core validate front-matter` | Validates the governed design-document front matter that this command depends on. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/repo_ops/sync/design_document_index.py`
- `core/control_plane/indexes/design_documents/design_document_index.v1.json`

## Updated At
- `2026-03-12T22:05:00Z`
