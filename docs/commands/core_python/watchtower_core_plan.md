# `watchtower-core plan`

## Summary
This command group scaffolds compact governed planning documents and traced bootstrap chains while keeping authored Markdown files authoritative and refreshing derived planning surfaces in write mode.

## Use When
- You want help for the planning scaffold surface without copying templates by hand.
- You need one new PRD, feature design, implementation plan, or decision scaffold.
- You want to bootstrap a traced PRD, design, plan, and bootstrap-task chain for a new initiative.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/plan_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan <plan_command> [args]
```

## Arguments and Options
- `<plan_command>`: Choose `scaffold` or `bootstrap`.
- `-h`, `--help`: Show the command help text.
- Planning scaffolds are dry-run by default. Pass `--write` to the selected leaf command to persist the generated documents and refresh derived planning surfaces.

## Examples
```sh
cd core/python
uv run watchtower-core plan --help
```

```sh
cd core/python
uv run watchtower-core plan scaffold --kind prd --trace-id trace.example --document-id prd.example --title "Example PRD" --summary "Frames the example initiative."
```

```sh
cd core/python
uv run watchtower-core plan bootstrap --trace-id trace.example --title "Example Initiative" --summary "Bootstraps the example initiative." --include-decision --write
```

## Behavior and Outputs
- With no leaf command, the current implementation prints plan-specific help and exits successfully.
- `scaffold` creates one compact PRD, feature design, implementation plan, or decision-record scaffold.
- `bootstrap` creates a traced PRD, design, plan, and bootstrap-task chain, with an optional decision record.
- Optional sections are omitted by default and the rendered documents keep one compact placeholder per required section when richer inputs are not provided.
- In write mode, the command refreshes the deterministic derived planning surfaces after writing the scaffolded files.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan scaffold` | Scaffolds one compact governed planning document. |
| `watchtower-core plan bootstrap` | Scaffolds a compact traced planning chain plus one bootstrap task. |
| `watchtower-core task` | Manages the bootstrap task or follow-up work after the planning chain exists. |
| `watchtower-core sync all` | Rebuilds the same deterministic planning surfaces refreshed in write mode. |
| `watchtower-core query prds` | Reads one planning surface affected by plan writes. |
| `watchtower-core query designs` | Reads one planning surface affected by plan writes. |

## Source Surface
- `core/python/src/watchtower_core/cli/plan_family.py`
- `core/python/src/watchtower_core/cli/plan_handlers.py`
- `core/python/src/watchtower_core/repo_ops/planning_scaffolds.py`

## Updated At
- `2026-03-10T23:01:32Z`
