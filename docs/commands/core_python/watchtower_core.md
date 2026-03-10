# `watchtower-core`

## Summary
This command is the root CLI entrypoint for the core Python workspace and dispatches to the available `watchtower-core` command groups and subcommands.

## Use When
- You want to discover the current core helper and harness commands.
- You need a stable CLI entrypoint for workspace checks, governed validation, index queries, derived-artifact sync tasks, or initiative closeout.
- You want the built-in help output for the current command surface.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core` |
| Kind | `root_command` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core <command> [args]
```

## Arguments and Options
- `<command>`: Dispatch to an available subcommand such as `doctor`, `query`, `sync`, `closeout`, or `validate`.
- `-h`, `--help`: Show the command help text.
- No root-command-specific options exist yet beyond help and subcommand selection.

## Examples
```sh
cd core/python
uv run watchtower-core --help
```

```sh
cd core/python
uv run watchtower-core doctor
```

```sh
cd core/python
uv run watchtower-core query commands --query doctor --format json
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
uv run watchtower-core query standards --category governance --format json
```

```sh
cd core/python
uv run watchtower-core query prds --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core query acceptance --trace-id trace.core_python_foundation
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
uv run watchtower-core sync command-index
```

```sh
cd core/python
uv run watchtower-core sync all
```

```sh
cd core/python
uv run watchtower-core sync foundation-index
```

```sh
cd core/python
uv run watchtower-core sync reference-index
```

```sh
cd core/python
uv run watchtower-core sync standard-index
```

```sh
cd core/python
uv run watchtower-core sync workflow-index
```

```sh
cd core/python
uv run watchtower-core sync prd-index
```

```sh
cd core/python
uv run watchtower-core sync initiative-index
```

```sh
cd core/python
uv run watchtower-core sync initiative-tracking
```

```sh
cd core/python
uv run watchtower-core sync task-index
```

```sh
cd core/python
uv run watchtower-core sync task-tracking
```

```sh
cd core/python
uv run watchtower-core sync github-tasks --repo owner/repo
```

```sh
cd core/python
uv run watchtower-core sync github-tasks --repo owner/repo --no-label-sync
```

```sh
cd core/python
uv run watchtower-core sync traceability-index
```

```sh
cd core/python
uv run watchtower-core sync repository-paths
```

```sh
cd core/python
uv run watchtower-core closeout initiative --trace-id trace.example --initiative-status completed --closure-reason "Delivered and validated"
```

```sh
cd core/python
uv run watchtower-core validate all --skip-acceptance
```

```sh
cd core/python
uv run watchtower-core validate document-semantics --path workflows/modules/code_validation.md
```

```sh
cd core/python
uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation --format json
```

```sh
cd core/python
uv run watchtower-core validate artifact --path core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json --format json
```

## Behavior and Outputs
- With no subcommand, the current implementation prints the root CLI help text, including onboarding-friendly examples, and exits successfully.
- With a valid subcommand, the root command dispatches to that subcommand handler.
- The current top-level command families are `doctor`, `query`, `sync`, `closeout`, and `validate`.
- `query` now covers repository navigation, command discovery, governed foundations lookup, workflow-module lookup, curated reference lookup, standards and best-practice lookup, planning lookup, initiative coordination lookup, acceptance contracts, validation evidence, task lookup, and trace lookup.
- The `sync` family now covers one-shot local rebuilds through `sync all`, plus command lookup, foundation lookup, reference lookup, standard lookup, workflow lookup, PRD tracking, decision tracking, design tracking, initiative tracking, task tracking, GitHub task sync with managed labels, traceability, and repository-path rebuilds.
- `validate` now covers aggregate repo validation, document front matter, governed document semantics, schema-backed governed artifacts, and semantic acceptance reconciliation.
- Unknown subcommands are rejected by the underlying CLI parser.
- The current command surface is intentionally small and acts as the operator entrypoint for the growing core workspace.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core doctor` | Lightweight workspace health snapshot exposed through the root CLI. |
| `watchtower-core query` | Namespace command for governed index lookups over paths, commands, planning docs, acceptance contracts, evidence, tasks, and traces. |
| `watchtower-core sync` | Namespace command for rebuilding derived governed artifacts and hosted task mirrors. |
| `watchtower-core closeout` | Namespace command for initiative-level closeout operations over traced planning surfaces. |
| `watchtower-core validate` | Namespace command for governed validation operations such as document, artifact, and acceptance checks. |
| `docs/commands/core_python/README.md` | Local command-family inventory for the core Python workspace. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/README.md`

## Updated At
- `2026-03-10T05:20:00Z`
