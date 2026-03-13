# `watchtower-core query authority`

## Summary
This command searches the authority map for the canonical machine surface, preferred command, and fallback paths for recurring planning and governance questions.

## Use When
- You know the class of question you need to answer but not which machine surface is canonical.
- You want one compact policy answer instead of scanning coordination, planning, traceability, and command docs manually.
- You need a machine-readable lookup contract for canonical planning or governance navigation.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query authority` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_coordination_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query authority [--query <text>] [--question-id <question_id>] [--domain <planning|governance>] [--artifact-kind <kind>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over authority-map fields such as the question, canonical path, preferred command, aliases, and fallback paths.
- `--question-id <question_id>`: Exact authority question filter such as `authority.planning.current_state`.
- `--domain <planning|governance>`: Exact authority domain filter.
- `--artifact-kind <kind>`: Exact canonical artifact-kind filter such as `planning_catalog`, `coordination_index`, or `route_index`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query authority --domain planning
```

```sh
cd core/python
uv run watchtower-core query authority --question-id authority.planning.deep_trace_context --format json
```

```sh
cd core/python
uv run watchtower-core query authority --artifact-kind route_index
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching authority questions, canonical artifact paths, preferred commands, optional human companion paths, and any named status fields to trust.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and authority-map entries.
- The command is policy-oriented: it tells you which surface is canonical, not every surface that might contain related data.
- For planning questions, the active-first navigation model still applies after authority resolution: filterless `query planning` and `query initiatives` browse calls default to active, while explicit historical lookup remains opt-in through `--initiative-status` or a known `--trace-id`.
- If no entries match the requested filters, the command exits successfully and reports that no authority-map entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query coordination` | Canonical machine start-here path for current planning state and next action. |
| `watchtower-core query planning` | Canonical deep-planning read path for one trace after coordination identifies it. |
| `watchtower-core query initiatives` | Focused initiative-family lookup surface that the authority map may point to for history or compact phase browsing. |
| `watchtower-core query trace` | Durable trace-linked source join when the question is IDs or closeout state rather than the full planning read model. |
| `watchtower-core route preview` | Preferred command for workflow-routing questions resolved by the authority map. |
| `watchtower-core query standards` | Preferred command for repository policy and standard lookup questions resolved by the authority map. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/authority.py`
- `core/control_plane/registries/authority_map/authority_map.v1.json`

## Updated At
- `2026-03-13T23:21:33Z`
