# `watchtower-core plan query`

## Summary
This command group provides read-only lookup over live plan state, plan-owned indexes, and retained planning records. Use it when the question is about current planning work, execution state, project context, or retained trace-linked plan records.

## Use When
- You need the live plan workspace start-here lookup surface before opening raw JSON or rendered companions manually.
- You want one read-only command group for coordination, tasks, readiness, discrepancies, projects, closeouts, reviews, or retained trace-linked planning records.
- You need structured JSON output for scripts, workflows, or agent use.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan query` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/query.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan query <plan_query_command> [args]
```

## Arguments and Options
- `<plan_query_command>`: Choose a leaf command such as `coordination`, `initiatives`, `tasks`, `artifacts`, `readiness`, `discrepancies`, `plan-evidence`, `closeouts`, `reviews`, `projects`, `project-context`, `authority`, or `trace`.
- `-h`, `--help`: Show the query-group help text.
- Pass filters, limits, and output-mode flags to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core plan query --help
```

```sh
cd core/python
uv run watchtower-core plan query coordination --format json
```

```sh
cd core/python
uv run watchtower-core plan query artifacts --artifact-family initiative_state --format json
```

```sh
cd core/python
uv run watchtower-core plan query readiness --ready-for-execution true --format json
```

```sh
cd core/python
uv run watchtower-core plan query tasks --task-status planned --format json
```

```sh
cd core/python
uv run watchtower-core plan query authority --domain planning --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- Every leaf command is read-only and supports `--format human` or `--format json`.
- Use `coordination` when you need the live machine start-here planning payload.
- Use `initiatives` when you need broader initiative-family browsing, filtered terminal history, or explicit non-active status lookup.
- Use `tasks` when you need initiative-local task execution state.
- Use `artifacts` when you need cross-family live plan artifact lookup without opening raw JSON manually.
- Use `readiness` when the question is whether an initiative package may start or resume execution.
- Use `discrepancies` when you need mismatch, drift, or stale-surface records without opening one initiative directly.
- Use `projects` when you need project lookup without loading the full project context payload, and `project-context` when you need the validated runtime context for one project container.
- Use `authority` when the main question is which planning or governance surface is canonical.
- Use `plan-evidence`, `reviews`, and `closeouts` when you need the live initiative-local execution, review, and terminal-state support surfaces.
- Use `trace` when you need the retained traceability record for one exact trace ID.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan` | Parent command group for live plan bootstrap, lookup, task, and closeout operations. |
| `watchtower-core query` | Shared governed lookup surface for commands, paths, standards, foundations, references, acceptance, and evidence. |
| `watchtower-core sync all` | Rebuilds the same derived plan indexes and rendered companions that these queries read. |
| `watchtower-core validate all` | Verifies the governed artifacts and live plan indexes that back these lookup surfaces. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/query.py`
- `plan/python/src/watchtower_plan/cli/query_lookup_handlers.py`
- `plan/python/src/watchtower_plan/cli/query_rendered_handlers.py`
- `plan/python/src/watchtower_plan/query/`
- `plan/.wt/indexes/`

## Updated At
- `2026-03-20T21:20:00Z`
