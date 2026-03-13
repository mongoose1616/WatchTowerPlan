# `watchtower-core query`

## Summary
This command group provides read-only lookup over governed repository indexes. Use it to route from a current-state question to the smallest useful command or machine-readable surface.

## Use When
- You need to choose the correct lookup path before opening raw JSON or scanning docs manually.
- You want one read-only command group for current planning state, deep planning joins, command discovery, standards lookup, or trace-linked records.
- You need structured JSON output for scripts, workflows, or agent use.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query <query_command> [args]
```

## Arguments and Options
- `<query_command>`: Choose a leaf command such as `coordination`, `planning`, `authority`, `initiatives`, `tasks`, `commands`, `paths`, `standards`, `workflows`, `references`, `prds`, `decisions`, `designs`, `acceptance`, `evidence`, `foundations`, or `trace`.
- `-h`, `--help`: Show the query-group help text.
- Pass filters, limits, and output-mode flags to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core query --help
```

```sh
cd core/python
uv run watchtower-core query coordination --format json
```

```sh
cd core/python
uv run watchtower-core query planning --trace-id trace.core_python_foundation --format json
```

```sh
cd core/python
uv run watchtower-core query initiatives --initiative-status completed --format json
```

```sh
cd core/python
uv run watchtower-core query authority --domain planning --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- Every leaf command is read-only and supports `--format human` or `--format json`.
- Use `coordination` as the active-first machine start-here path for current planning state and next action.
- Use `planning` after coordination when you need the canonical deep machine-readable record for one trace.
- Use `initiatives` when you need broader initiative-family browsing, filtered terminal history, or explicit non-active status lookup.
- Use `authority` when the main question is which planning or governance surface is canonical.
- Use `commands` or `paths` when the main task is discovery rather than planning-state inspection.
- Use `references --repository-status <status>` when you need only active-support, supporting-authority, or candidate-future guidance from the governed reference corpus.
- For exact filters and field behavior, open the leaf command page or CLI help for the selected query command.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query coordination` | Active-first current-state planning entrypoint. |
| `watchtower-core query planning` | Canonical deep planning join for one trace. |
| `watchtower-core query initiatives` | Broader initiative-family and historical-status lookup. |
| `watchtower-core query authority` | Canonical-surface resolver for planning and governance questions. |
| `watchtower-core` | Root command that dispatches to this group. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/`

## Updated At
- `2026-03-13T18:13:00Z`
