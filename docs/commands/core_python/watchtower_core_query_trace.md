# `watchtower-core query trace`

## Summary
This command resolves one joined traceability record by `trace_id`.

## Use When
- You want to inspect the current PRD, design, plan, acceptance, and evidence links for one initiative.
- You need a structured trace lookup result for automation or agent workflows.
- You want a compact view over a traced change without reading multiple tracking surfaces separately.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query trace` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query trace --trace-id <trace_id>
```

## Arguments and Options
- `--trace-id <trace_id>`: Required trace identifier to resolve.
- `--format <human|json>`: Select human-readable or structured JSON output. Defaults to `human`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query trace --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core query trace --trace-id trace.core_python_foundation --format json
```

## Behavior and Outputs
- In `human` mode, the command prints the resolved trace title, summary, and the main linked artifact IDs that are present.
- In `json` mode, the command prints a single JSON object with the resolved trace record.
- If the requested trace is unknown, the command exits with status code `1` and prints an error in the selected output format.
- The command reads the current traceability index and does not mutate repository state.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent namespace for query subcommands. |
| `watchtower-core query paths` | Finds related repository paths without resolving a joined trace record. |
| `watchtower-core sync repository-paths` | Rebuilds one of the derived artifacts that trace records can reference. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/traceability.py`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`

## Updated At
- `2026-03-09T05:43:10Z`
