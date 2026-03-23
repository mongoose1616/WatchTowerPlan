# `watchtower-core query`

## Summary
This command group provides read-only lookup over shared governed repository indexes and durable records. Use it to route from a discovery or governance question to the smallest useful command or machine-readable surface.

## Use When
- You need to choose the correct lookup path before opening raw JSON or scanning docs manually.
- You want one read-only command group for command discovery, repository paths, standards lookup, foundations, references, workflow lookup, or durable traced records.
- You need structured JSON output for scripts, workflows, or agent use.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query <query_command> [args]
```

## Arguments and Options
- `<query_command>`: Choose a leaf command such as `commands`, `paths`, `standards`, `workflows`, `references`, `acceptance`, `evidence`, or `foundations`.
- `-h`, `--help`: Show the query-group help text.
- Pass filters, limits, and output-mode flags to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core query --help
```

```sh
cd core/python
uv run watchtower-core query commands --query doctor --format json
```

```sh
cd core/python
uv run watchtower-core query foundations --query philosophy
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- Every leaf command is read-only and supports `--format human` or `--format json`.
- Use `commands` or `paths` when the main task is discovery rather than opening docs or indexes manually.
- Use `foundations`, `standards`, `references`, and `workflows` when the main question is governed repository intent, rules, source guidance, or routed workflow behavior.
- Use `acceptance` or `evidence` when the main question is durable traced validation contracts or recorded proof rather than live pack execution state.
- Use `references --repository-status <status>` when you need only active-support, supporting-authority, or candidate-future guidance from the governed reference corpus.
- Live pack-workspace queries now live under the owning pack namespace such as `watchtower-core <pack-namespace> query ...`.
- For exact filters and field behavior, open the leaf command page or CLI help for the selected query command.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core <pack-namespace> query` | Pack-owned live lookup surface for coordination, tasks, readiness, projects, reviews, closeouts, and retained trace-linked records. |
| `watchtower-core query commands` | Machine-readable command discovery without scanning docs manually. |
| `watchtower-core query foundations` | Governing foundation lookup surface for repository scope and intent. |
| `watchtower-core query standards` | Governing repository-standard lookup surface. |
| `watchtower-core query references` | Governed reference-library lookup surface. |
| `watchtower-core` | Root command that dispatches to this group. |

## Source Surface
- `core/python/src/watchtower_host/cli/query_family.py`
- `core/python/src/watchtower_host/cli/query_discovery_family.py`
- `core/python/src/watchtower_host/cli/query_knowledge_family.py`
- `core/python/src/watchtower_host/cli/query_records_family.py`

## Updated At
- `2026-03-22T22:15:00Z`
