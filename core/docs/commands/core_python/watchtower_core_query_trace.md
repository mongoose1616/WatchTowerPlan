# `watchtower-core query trace`

## Summary
This command resolves one governed traceability record by trace ID so engineers can inspect the linked initiative, validation, evidence, task, and closeout surfaces for a single trace.

## Use When
- You already know the trace ID you want to inspect.
- You want one joined record instead of opening initiative, decision, design, implementation, and evidence surfaces separately.
- You want structured traceability lookup output for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query trace` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_coordination_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query trace --trace-id <trace_id> [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Stable trace identifier such as `trace.governed_acceptance_example`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query trace --trace-id trace.governed_acceptance_example
```

```sh
cd core/python
uv run watchtower-core query trace --trace-id trace.governed_acceptance_example --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints the trace ID, title, summary, initiative status, closeout metadata when present, and any linked initiative, decision, design, implementation, task, acceptance-contract, or evidence IDs present in the record.
- In `json` mode, the command prints one JSON object with the command name, status, and the resolved trace record.
- This command stays the durable trace-linked source join for the live initiative model and its surviving governed records.
- If the trace ID is unknown, the command exits with status code `1` and reports the missing ID.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core query authority` | Resolves when traceability is the canonical answer versus when coordination or initiative lookup should answer instead. |
| `watchtower-core query initiatives` | Searches the initiative index when you need broader initiative-family lookup before resolving one trace. |
| `watchtower-core query tasks` | Searches the task index when you want task records rather than a joined trace record. |
| `watchtower-core query acceptance` | Searches the acceptance-contract family for the machine acceptance boundary linked to the trace. |
| `watchtower-core query evidence` | Searches durable validation evidence linked to the trace. |
| `watchtower-core sync traceability-index` | Rebuilds the traceability index that this command reads. |
| `watchtower-core query paths` | Helps find the traceability index artifact path if you need to inspect the source artifact directly. |
| `watchtower-core query commands` | Helps discover other CLI surfaces once you know which workflow you want. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `plan/python/src/watchtower_plan/query/traceability.py`
- `core/control_plane/indexes/traceability/traceability_index.json`

## Updated At
- `2026-03-19T20:15:00Z`
