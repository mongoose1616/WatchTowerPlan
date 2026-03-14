# `watchtower-core sync standard-index`

## Summary
This command rebuilds the governed standard index from the governed standards and best-practice documents under `docs/standards/`.

## Use When
- You changed a standard or best-practice doc and need the machine-readable standard index to reflect the current standards corpus.
- You want to audit reference capture across standards without reparsing Markdown manually.
- You want a controlled way to regenerate one governance index without rebuilding unrelated derived artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync standard-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync standard-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical standard-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync standard-index
```

```sh
cd core/python
uv run watchtower-core sync standard-index --write
```

```sh
cd core/python
uv run watchtower-core sync standard-index --output /tmp/standard_index.v1.json --format json
```

## Behavior and Outputs
- The command reads the governed standards under `docs/standards/` and rebuilds the machine-readable standard index deterministically.
- The rebuild validates standard front matter, enforces the required source sections, and captures whether each standard uses internal references, local governed reference docs, transitive external authority, and authored operationalization metadata.
- Standards that cite raw external URLs without also citing a governed local reference doc under `docs/references/` are rejected during rebuild.
- Standards that omit the required `Operationalization` metadata bullets or point them at invalid repository paths are rejected during rebuild.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many standard entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt standard-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source documents or rebuilt artifact are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core query standards` | Reads the standard index that this command rebuilds. |
| `watchtower-core sync reference-index` | Rebuilds the companion reference index used to derive transitive external authority. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/repo_ops/sync/standard_index.py`
- `core/control_plane/indexes/standards/standard_index.v1.json`

## Updated At
- `2026-03-14T05:37:06Z`
