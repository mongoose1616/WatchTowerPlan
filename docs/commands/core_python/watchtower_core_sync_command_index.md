# `watchtower-core sync command-index`

## Summary
This command rebuilds the governed command index from the registry-backed CLI parser metadata while requiring companion command pages under `docs/commands/`.

## Use When
- You changed a command page or the registry-backed CLI parser surface and need to refresh the machine-readable command lookup surface.
- You added or removed a durable CLI command page and want the governed command index to match.
- You want to inspect the rebuilt command index in dry-run mode before writing it to the canonical control-plane path.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync command-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync command-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical command-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync command-index
```

```sh
cd core/python
uv run watchtower-core sync command-index --write
```

```sh
cd core/python
uv run watchtower-core sync command-index --output /tmp/command_index.v1.json --format json
```

## Behavior and Outputs
- The command reads the registry-backed CLI parser metadata and rebuilds the machine-readable command index deterministically.
- The command fails closed when a registry-backed command is missing its companion command page under `docs/commands/`.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many command entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt command-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the parser metadata, companion command docs, or derived document are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core query commands` | Reads the command index that this command rebuilds. |
| `watchtower-core sync repository-paths` | Rebuilds the broader repository path index from README inventories. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/cli/parser.py`
- `core/python/src/watchtower_core/cli/introspection.py`
- `core/python/src/watchtower_core/sync/command_index.py`
- `core/control_plane/indexes/commands/command_index.v1.json`

## Updated At
- `2026-03-10T05:14:33Z`
