# `watchtower-core query coordination`

## Summary
This command is the explicit machine start-here path for current planning coordination, including repo state, active initiatives, actionable tasks, blockers, recent closeouts, and bootstrap-ready guidance.

## Use When
- You want the current planning-state view without reopening initiative, task, and traceability surfaces separately.
- You need machine-readable coordination output for an agent, workflow, or script.
- You want compact active-task summaries plus one recommended next surface to open first.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query coordination` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query coordination [--query <text>] [--trace-id <trace_id>] [--initiative-status <status>] [--current-phase <phase>] [--owner <owner>] [--blocked-only] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over coordination entry fields such as trace ID, title, next action, and active-task summaries.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.core_python_foundation`.
- `--initiative-status <status>`: Exact initiative-status filter such as `active`, `completed`, or `superseded`. Defaults to `active` when omitted.
- `--current-phase <phase>`: Exact current-phase filter such as `prd`, `execution`, `validation`, or `closed`.
- `--owner <owner>`: Exact active-owner filter such as `repository_maintainer`.
- `--blocked-only`: Return only initiatives with one or more currently blocked active tasks.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Notes
- This command defaults to active initiatives because it is the coordination start-here path.
- The JSON output also carries top-level coordination state, recommended next action, actionable-task summaries, and recent closeout context.
- `docs/planning/coordination_tracking.md` is the compact human companion view built from the same coordination state.
- Use `watchtower-core query planning` after this command when you need the canonical deep planning record for one trace.
- Use `watchtower-core query authority` when you need to confirm whether coordination is canonical for the question you are asking.
- Use `watchtower-core query initiatives` when you want broader initiative-family lookup or exhaustive closed-history browsing.

## Examples
```sh
cd core/python
uv run watchtower-core query coordination
```

```sh
cd core/python
uv run watchtower-core query coordination --blocked-only --format json
```

```sh
cd core/python
uv run watchtower-core query coordination --initiative-status completed --trace-id trace.core_python_foundation
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- With no explicit `--initiative-status`, the command defaults to `active`.
- In `human` mode, the command prints the top-level coordination mode, recommended next action, matching initiatives, and recent closeout context when useful.
- In `json` mode, the command prints one JSON object with the command name, coordination mode, recommended next action, result records, actionable tasks, recent closeouts, and the active-only default when it was applied. Embedded initiative entries use `artifact_status` plus `initiative_status`.
- If no entries match the requested filters, the command still returns the current coordination mode and the default next step.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core query authority` | Resolves whether coordination, planning, initiative, or governance surfaces are canonical for a recurring lookup question. |
| `watchtower-core query planning` | Descends from the start-here coordination view into the canonical deep planning join for one trace. |
| `watchtower-core query initiatives` | Broader initiative-family lookup surface, including closed-history inspection. |
| `watchtower-core sync coordination` | Rebuilds the coordination index and its dependent machine and human coordination surfaces. |
| `watchtower-core sync initiative-index` | Rebuilds one of the upstream initiative-family surfaces projected into coordination. |
| `watchtower-core query tasks` | Inspects the full task records behind the compact active-task summaries. |
| `watchtower-core query trace` | Resolves the underlying traceability record for one known trace ID. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/repo_ops/query/coordination.py`
- `core/control_plane/indexes/coordination/coordination_index.v1.json`

## Updated At
- `2026-03-11T03:10:00Z`
