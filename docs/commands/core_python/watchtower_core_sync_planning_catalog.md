# `watchtower-core sync planning-catalog`

## Summary
This command rebuilds the canonical planning catalog from traceability, initiative, planning-document, task, acceptance-contract, and validation-evidence sources.

## Use When
- You changed trace-linked planning state and need the canonical deep-planning machine surface refreshed.
- You want to materialize the planning catalog for review without writing the canonical artifact yet.
- You are validating the canonical machine planning join after changes to PRDs, designs, tasks, acceptance contracts, or evidence.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync planning-catalog` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync planning-catalog [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt planning catalog to its canonical repository path.
- `--output <path>`: Write the rebuilt planning catalog to an explicit path instead of the canonical location.
- `--include-document`: Include the rebuilt JSON document in the command output payload.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync planning-catalog
```

```sh
cd core/python
uv run watchtower-core sync planning-catalog --write
```

```sh
cd core/python
uv run watchtower-core sync planning-catalog --output /tmp/planning_catalog.v1.json --format json
```

## Behavior and Outputs
- The command is dry-run by default.
- With `--write`, it updates `core/control_plane/indexes/planning/planning_catalog.v1.json`.
- With `--output`, it writes the rebuilt planning catalog to the requested path.
- In `json` mode, the command prints one JSON object with the command name, status, record count, write outcome, and output path when applicable.
- If `--include-document` is set, the output includes the rebuilt planning-catalog JSON document.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync coordination` | Rebuilds the current execution coordination slice that the planning catalog embeds per trace. |
| `watchtower-core sync initiative-index` | Rebuilds one of the source index families used by the planning catalog. |
| `watchtower-core sync traceability-index` | Rebuilds the trace-linked source join used by the planning catalog. |
| `watchtower-core sync all` | Rebuilds the planning catalog alongside the other deterministic derived surfaces. |
| `watchtower-core query planning` | Reads the canonical planning catalog after it has been rebuilt. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/cli/sync_handlers.py`
- `core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py`
- `core/control_plane/indexes/planning/planning_catalog.v1.json`

## Updated At
- `2026-03-11T02:15:00Z`
