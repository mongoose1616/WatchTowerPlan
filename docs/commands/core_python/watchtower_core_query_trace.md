# `watchtower-core query trace`

## Summary
This command resolves one governed traceability record by trace ID so engineers can inspect the linked planning, validation, evidence, task, and closeout surfaces for a single initiative.

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
| Source Surface | `core/python/src/watchtower_core/cli/query_coordination_family.py` |

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
- In `human` mode, the command prints the trace ID, title, summary, initiative status, closeout metadata when present, and any linked PRD, decision, design, plan, task, acceptance-contract, or evidence IDs present in the record.
- In `json` mode, the command prints one JSON object with the command name, status, and the resolved trace record.
- This command stays the durable trace-linked source join, not the richer deep-planning read model that the planning catalog now provides.
- If the trace ID is unknown, the command exits with status code `1` and reports the missing ID.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core query authority` | Resolves when traceability is the canonical answer versus when coordination or the planning catalog should answer instead. |
| `watchtower-core query planning` | Returns the richer planning read model when the question needs joined planning, task, acceptance, and evidence context. |
| `watchtower-core query prds` | Searches the PRD index when you do not already know the exact trace ID. |
| `watchtower-core query decisions` | Searches the decision index when you want decision records rather than a joined trace record. |
| `watchtower-core query designs` | Searches the design-document index when you want design docs rather than a joined trace record. |
| `watchtower-core query tasks` | Searches the task index when you want task records rather than a joined trace record. |
| `watchtower-core sync traceability-index` | Rebuilds the traceability index that this command reads. |
| `watchtower-core query paths` | Helps find the traceability index artifact path if you need to inspect the source artifact directly. |
| `watchtower-core query commands` | Helps discover other CLI surfaces once you know which workflow you want. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/traceability.py`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`

## Updated At
- `2026-03-13T23:21:33Z`
