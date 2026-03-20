# `watchtower-core plan query coordination`

## Summary
This command provides the machine-readable live coordination view for the plan workspace, including active initiatives, actionable tasks, blockers, and recent closeouts.

## Use When
- You want the current live coordination view without reopening initiative, task, and traceability surfaces separately.
- You need machine-readable coordination output for an agent, workflow, or script.
- You want compact active-task summaries plus one recommended next surface to open first.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan query coordination` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/query.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan query coordination [--query <text>] [--trace-id <trace_id>] [--initiative-status <status>] [--current-phase <phase>] [--owner <owner>] [--blocked-only] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over coordination entry fields such as trace ID, title, next action, and active-task summaries.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.plan_live_query_authority_cutover`.
- `--initiative-status <status>`: Exact initiative-status filter such as `active`, `completed`, or `superseded`. Defaults to `active` when omitted.
- `--current-phase <phase>`: Exact current-phase filter such as `capture`, `execution`, `closeout`, or `closed`.
- `--owner <owner>`: Exact active-owner filter such as `repository_maintainer`.
- `--blocked-only`: Return only initiatives with one or more currently blocked active tasks.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Notes
- Use `plan/.wt/indexes/coordination_index.json` as the live plan-workspace machine start-here path.
- This command defaults to active initiatives because it is the start-here path for the live plan workspace.
- The JSON output also carries top-level coordination state, recommended next action, actionable-task summaries, and recent closeout context.
- Explicit non-active `--initiative-status` lookups resolve result rows from initiative-family data while the top-level coordination snapshot remains the current repo state.
- `plan/plan_overview.md` is the compact human companion view built from the same live coordination state, while `plan/tracking/coordination_tracking.md` remains the richer human browse companion.
- Use `watchtower-core plan query trace` after this command when you need the canonical traceability record for one trace.
- Use `watchtower-core plan query authority` when you need to confirm whether coordination is canonical for the question you are asking.
- Use `watchtower-core plan query initiatives` when you want broader initiative-family lookup or exhaustive closed-history browsing.

## Examples
```sh
cd core/python
uv run watchtower-core plan query coordination
```

```sh
cd core/python
uv run watchtower-core plan query coordination --blocked-only --format json
```

```sh
cd core/python
uv run watchtower-core plan query coordination --initiative-status completed --trace-id trace.plan_workflow_root_authority_split
```

```sh
cd core/python
uv run watchtower-core plan query coordination --initiative-status completed --trace-id trace.plan_workflow_root_authority_split --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- With no explicit `--initiative-status`, the command defaults to `active`.
- The default coordination snapshot stays compact by carrying only active initiative entries plus recent closeout context.
- In `human` mode, the command prints the top-level coordination mode, recommended next action, matching initiatives, and recent closeout context when useful.
- In `json` mode, the command prints one JSON object with the command name, coordination mode, recommended next action, result records, actionable tasks, recent closeouts, and the active-only default when it was applied. Embedded initiative entries use `artifact_status` plus `initiative_status`.
- When `--initiative-status` is explicitly set to a non-active value, the command keeps the same top-level coordination snapshot but serves matching result rows from the initiative-family view so historical lookup remains available without bloating the default coordination artifact.
- If no entries match the requested filters, the command still returns the current coordination mode and the default next step.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan query` | Parent command group for all plan-owned index-backed lookup commands. |
| `watchtower-core plan query authority` | Resolves whether coordination, initiative, traceability, or governance surfaces are canonical for a recurring lookup question. |
| `watchtower-core plan query trace` | Descends from the start-here coordination view into the canonical traceability record for one trace. |
| `watchtower-core plan query initiatives` | Broader initiative-family lookup surface, including closed-history inspection. |
| `watchtower-core plan sync all` | Rebuilds the live coordination index and its dependent rendered surfaces. |
| `watchtower-core plan query tasks` | Inspects the full task records behind the compact active-task summaries. |
| `watchtower-core plan query trace` | Resolves the underlying traceability record for one known trace ID. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/query.py`
- `plan/python/src/watchtower_plan/cli/query_rendered_handlers.py`
- `plan/python/src/watchtower_plan/query/coordination.py`
- `plan/.wt/indexes/coordination_index.json`

## Updated At
- `2026-03-17T19:13:00Z`
