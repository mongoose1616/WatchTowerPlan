# `watchtower-core sync route-index`

## Summary
This command rebuilds the governed route index from the canonical routing table under `workflows/ROUTING_TABLE.md`.

## Use When
- You changed `AGENTS.md` routing guidance or `workflows/ROUTING_TABLE.md` and need the machine-readable route surface to match.
- You added or removed a routed task type.
- You want to inspect the rebuilt route index in dry-run mode before writing it to the canonical control-plane path.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync route-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync route-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical route-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync route-index
```

```sh
cd core/python
uv run watchtower-core sync route-index --write
```

```sh
cd core/python
uv run watchtower-core sync route-index --output /tmp/route_index.v1.json --format json
```

## Behavior and Outputs
- The command reads `workflows/ROUTING_TABLE.md` and rebuilds the machine-readable route index deterministically.
- The command fails closed when a route row points to a missing workflow module or omits required routing data.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many route entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt route-index document.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core route preview` | Reads the route index that this command rebuilds. |
| `watchtower-core sync workflow-index` | Rebuilds the companion workflow lookup surface referenced by route entries. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/cli/sync_handlers.py`
- `core/python/src/watchtower_core/repo_ops/sync/route_index.py`
- `core/control_plane/indexes/routes/route_index.v1.json`

## Updated At
- `2026-03-10T22:45:00Z`
