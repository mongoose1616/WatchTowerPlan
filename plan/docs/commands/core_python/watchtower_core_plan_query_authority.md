# `watchtower-core plan query authority`

## Summary
This command searches the authority map for the canonical machine surface, preferred command, and fallback paths for recurring planning and governance questions.

## Use When
- You know the class of question you need to answer but not which machine surface is canonical.
- You want one focused canonical-answer surface instead of scanning coordination, planning, traceability, and command docs manually.
- You need a machine-readable lookup contract for canonical planning or governance navigation.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan query authority` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/query.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan query authority [--query <text>] [--question-id <question_id>] [--domain <planning|governance>] [--artifact-kind <kind>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over authority-map fields such as the question, canonical path, preferred command, aliases, and fallback paths.
- `--question-id <question_id>`: Exact authority question filter such as `authority.planning.current_state`.
- `--domain <planning|governance>`: Exact authority domain filter.
- `--artifact-kind <kind>`: Exact canonical artifact-kind filter such as `coordination_index`, `initiative_index`, or `route_index`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan query authority --domain planning
```

```sh
cd core/python
uv run watchtower-core plan query authority --question-id authority.planning.deep_trace_context --format json
```

```sh
cd core/python
uv run watchtower-core plan query authority --artifact-kind route_index
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching authority questions, canonical artifact paths, preferred commands, optional human companion paths, and any named status fields to trust.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and authority-map entries.
- The command is authority-oriented: it tells you which surface is canonical, not every surface that might contain related data.
- For planning questions, the active-first navigation model still applies after authority resolution: filterless `plan query initiatives` browse calls default to active, while explicit historical lookup remains opt-in through `--initiative-status` or a known `--trace-id`.
- The current planning authority entries now point first to live `plan/.wt/**` indexes and `plan/plan_overview.md`, with retained trace records used only when explicitly requested.
- If no entries match the requested filters, the command exits successfully and reports that no authority-map entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan query coordination` | Canonical machine start-here path for current planning state and next action. |
| `watchtower-core plan query artifacts` | Canonical cross-family artifact lookup when the question spans multiple live plan machine artifact families. |
| `watchtower-core plan query readiness` | Canonical execution-gate lookup when the question is whether an initiative may start or resume work. |
| `watchtower-core plan query discrepancies` | Canonical mismatch and drift lookup when the question is blocking discrepancies. |
| `watchtower-core plan query projects` | Canonical project-container browse surface for pack-level project lookup. |
| `watchtower-core plan query initiatives` | Focused initiative-family lookup surface that the authority map may point to for history or phase browsing. |
| `watchtower-core plan query trace` | Durable trace-linked source join when the question is IDs or closeout state rather than the full planning read model. |
| `watchtower-core route preview` | Preferred command for workflow-routing questions resolved by the authority map. |
| `watchtower-core query standards` | Preferred command for repository rule and standard lookup questions resolved by the authority map. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/query.py`
- `plan/python/src/watchtower_plan/cli/query_lookup_handlers.py`
- `core/python/src/watchtower_core/query/authority.py`
- `core/control_plane/registries/authority_map.json`

## Updated At
- `2026-03-17T20:03:23Z`
