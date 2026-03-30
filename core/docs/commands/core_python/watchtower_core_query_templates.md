# `watchtower-core query templates`

## Summary
This command searches the governed template catalog so engineers and agents can find the correct document scaffold, required sections, allowed roots, and authoring guidance before drafting or refreshing governed docs.

## Use When
- You need to know which governed template applies to a new or refreshed document.
- You want the required sections, section order, allowed roots, or LLM/operator guidance without browsing multiple template files manually.
- You want machine-readable template lookup for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query templates` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/query_knowledge_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query templates [--query <text>] [--template-id <template_id>] [--family-id <family_id>] [--surface-id <surface_id>] [--authorship-mode <authored|rendered>] [--llm-guidance-mode <required|advisory|none>] [--allowed-root <path>] [--required-section-id <section_id>] [--required-rendered-surface-id <surface_id>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over template IDs, template paths, section IDs, allowed roots, authoring goals, operator notes, and guidance text.
- `--template-id <template_id>`: Exact template identifier such as `template.core.documentation.standard`.
- `--family-id <family_id>`: Exact documentation-family filter such as `workflow`.
- `--surface-id <surface_id>`: Exact surface filter such as `surface.documentation.command_reference`.
- `--authorship-mode <authored|rendered>`: Exact authorship-mode filter.
- `--llm-guidance-mode <required|advisory|none>`: Exact LLM-guidance-mode filter.
- `--allowed-root <path>`: Exact allowed-root filter such as `core/docs/standards` or `<pack>/docs/commands`.
- `--required-section-id <section_id>`: Exact required-section filter such as `operationalization` or `command`.
- `--required-rendered-surface-id <surface_id>`: Exact required rendered-surface filter when the template binds to rendered companions.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query templates --query standard --format json
```

```sh
cd core/python
uv run watchtower-core query templates --allowed-root core/docs/commands
```

```sh
cd core/python
uv run watchtower-core query templates --family-id workflow --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching template IDs, paths, target families or surfaces, allowed roots, required sections, and any available authoring-goal or operator notes.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and template-catalog records including section order, allowed roots, and structured LLM guidance.
- The command helps stop document-shape guesswork: use it before drafting or materially restructuring governed docs whose family already has a published scaffold.
- If no entries match the requested filters, the command exits successfully and reports that no template-catalog entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for shared governed lookup commands. |
| `watchtower-core query authority` | Resolves whether template-catalog lookup is the right authoritative discovery surface before deeper browsing. |
| `watchtower-core query standards` | Use after template lookup when the next question is which standard governs the document family. |
| `watchtower-core query workflows` | Use after template lookup when the next question is which workflow governs how the document should be produced or refreshed. |
| `watchtower-core query commands` | Use when the next question is which command doc or CLI surface operationalizes the resulting workflow. |

## Source Surface
- `core/python/src/watchtower_host/cli/query_knowledge_family.py`
- `core/python/src/watchtower_host/cli/query_knowledge_handlers.py`
- `core/python/src/watchtower_core/query/templates.py`
- `core/control_plane/registries/template_catalog.json`

## Updated At
- `2026-03-27T15:00:00Z`
