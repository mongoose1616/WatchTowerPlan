# `watchtower-core query authority`

## Summary
This command searches the shared authority map so engineers and agents can resolve which governed surface is canonical before opening docs, registries, or raw repo search results directly.

## Use When
- You know the class of question you need to answer but not which machine or human surface is authoritative.
- You need one compact canonical-answer surface for governance questions such as lookup order, command discovery, template selection, or standards lookup.
- You want machine-readable authority resolution for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query authority` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/query_knowledge_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query authority [--query <text>] [--question-id <question_id>] [--domain <domain>] [--artifact-kind <kind>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over authority-map fields such as the question, canonical path, preferred command, aliases, and fallback paths.
- `--question-id <question_id>`: Exact authority question filter such as `authority.governance.template_selection`.
- `--domain <domain>`: Exact authority domain filter such as `governance`.
- `--artifact-kind <kind>`: Exact canonical artifact-kind filter such as `command_index`, `template_catalog`, or `authority_map`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query authority --query canonical --format json
```

```sh
cd core/python
uv run watchtower-core query authority --question-id authority.governance.template_selection
```

```sh
cd core/python
uv run watchtower-core query authority --artifact-kind template_catalog
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching authority questions, canonical artifact paths, preferred commands, optional human companion paths, and any named status fields to trust.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and authority-map entries.
- The command is authority-oriented: it tells you which surface to trust first, not every surface that might contain related information.
- If no entries match the requested filters, the command exits successfully and reports that no authority-map entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for shared governed lookup commands. |
| `watchtower-core query commands` | Use after authority resolution when the next question is which CLI command matches the task. |
| `watchtower-core query templates` | Use after authority resolution when the next question is which governed template defines document shape. |
| `watchtower-core query standards` | Use after authority resolution when the next question is which repository rule governs the surface. |
| `watchtower-core route preview` | Preferred command for workflow-routing questions resolved by the authority map. |

## Source Surface
- `core/python/src/watchtower_host/cli/query_knowledge_family.py`
- `core/python/src/watchtower_host/cli/query_knowledge_handlers.py`
- `core/python/src/watchtower_core/query/authority.py`
- `core/control_plane/registries/authority_map.json`

## Updated At
- `2026-03-27T15:00:00Z`
