# `watchtower-core query trace`

## Summary
This command resolves one governed traceability record by trace ID so engineers can inspect the linked planning, validation, and evidence surfaces for a single initiative.

## Use When
- You already know the trace ID you want to inspect.
- You want one joined record instead of opening PRD, decision, design, and evidence surfaces separately.
- You want structured traceability lookup output for a workflow, script, or agent.

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
uv run watchtower-core query trace --trace-id <trace_id> [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Stable trace identifier such as `trace.core_python_foundation`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
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
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints the trace ID, title, summary, and any linked PRD, decision, design, plan, acceptance-contract, or evidence IDs present in the record.
- In `json` mode, the command prints one JSON object with the command name, status, and the resolved trace record.
- If the trace ID is unknown, the command exits with status code `1` and reports the missing ID.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core query paths` | Helps find the traceability index artifact path if you need to inspect the source artifact directly. |
| `watchtower-core query commands` | Helps discover other CLI surfaces once you know which workflow you want. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/traceability.py`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`

## Updated At
- `2026-03-09T05:43:47Z`
