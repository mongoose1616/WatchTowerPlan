# `watchtower-core query`

## Summary
This command group searches the governed lookup indexes for repository paths, documented commands, foundation docs, workflow modules, curated references, governed standards, planning artifacts, coordination views, canonical planning records, and traceability records.

## Use When
- You need to discover a path, command, or trace record without opening raw control-plane JSON files directly.
- You want command-family help that explains the difference between the available query modes.
- You are onboarding to the workspace and need a safe, read-only way to inspect governed data.

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
- `<query_command>`: Choose `paths`, `commands`, `coordination`, `planning`, `foundations`, `workflows`, `references`, `standards`, `prds`, `decisions`, `designs`, `acceptance`, `evidence`, `tasks`, `initiatives`, or `trace`.
- `-h`, `--help`: Show the command help text.
- No group-level filters exist; pass filtering arguments to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core query --help
```

```sh
cd core/python
uv run watchtower-core query commands --query doctor
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
uv run watchtower-core query foundations --query philosophy
```

```sh
cd core/python
uv run watchtower-core query workflows --query validation
```

```sh
cd core/python
uv run watchtower-core query references --query uv
```

```sh
cd core/python
uv run watchtower-core query standards --reference-path docs/references/github_collaboration_reference.md
```

```sh
cd core/python
uv run watchtower-core query prds --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core query decisions --decision-status accepted
```

```sh
cd core/python
uv run watchtower-core query designs --family implementation_plan
```

```sh
cd core/python
uv run watchtower-core query acceptance --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core query evidence --trace-id trace.core_python_foundation --format json
```

```sh
cd core/python
uv run watchtower-core query tasks --task-status backlog
```

```sh
cd core/python
uv run watchtower-core query initiatives --current-phase execution
```

```sh
cd core/python
uv run watchtower-core query trace --trace-id trace.core_python_foundation --format json
```

## Behavior and Outputs
- With no leaf command, the current implementation prints query-specific help and exits successfully.
- The command group is read-only and does not mutate repository state.
- Each leaf command supports `--format human` and `--format json`.
- Use `coordination` as the machine start-here path for current planning state and next-step lookup.
- Use `planning` as the canonical deep machine planning join after you know the trace or need one full trace-linked planning record.
- Use `paths` for repository navigation, `commands` for CLI discovery, `foundations` for the governed intent layer, `workflows` for workflow-module lookup, `references` for the reference corpus, `standards` for standards and best-practice lookup, `prds`, `decisions`, and `designs` for planning-family lookup, `acceptance` and `evidence` for governed acceptance coverage lookup, `tasks` for local execution work lookup, `initiatives` for broader initiative-family lookup including closed history, and `trace` when you already know the trace ID but only need the traceability join.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query paths` | Searches the repository path index. |
| `watchtower-core query commands` | Searches the command index. |
| `watchtower-core query coordination` | Starts with the current coordination view and recommended next action. |
| `watchtower-core query planning` | Returns the canonical deep planning record for one trace with explicit status semantics and linked sections. |
| `watchtower-core query foundations` | Searches the foundation index. |
| `watchtower-core query workflows` | Searches the workflow index. |
| `watchtower-core query references` | Searches the reference index. |
| `watchtower-core query standards` | Searches the standard index. |
| `watchtower-core query prds` | Searches the PRD index. |
| `watchtower-core query decisions` | Searches the decision index. |
| `watchtower-core query designs` | Searches the design-document index. |
| `watchtower-core query acceptance` | Searches governed acceptance contracts. |
| `watchtower-core query evidence` | Searches durable validation-evidence artifacts. |
| `watchtower-core query tasks` | Searches the task index. |
| `watchtower-core query initiatives` | Searches the initiative index. |
| `watchtower-core query trace` | Resolves one traceability record by trace ID. |
| `watchtower-core` | Root command that dispatches to this command group. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/repo_ops/query/`

## Updated At
- `2026-03-11T02:15:00Z`
