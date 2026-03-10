# `watchtower-core sync`

## Summary
This command group rebuilds derived governed artifacts or hosted-task mirrors from authored repository sources, including command lookup, reference lookup, planning indexes, planning trackers, initiative coordination views, traceability, repository navigation surfaces, and GitHub task sync.

## Use When
- You need help for one of the sync operations without opening the implementation code first.
- You want to rebuild a derived artifact after changing the authored source surfaces it depends on.
- You want to confirm whether a sync command defaults to dry-run or writes to disk.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync <sync_command> [args]
```

## Arguments and Options
- `<sync_command>`: Choose the derived artifact or hosted-task sync you want to run, currently `all`, `coordination`, `command-index`, `foundation-index`, `reference-index`, `standard-index`, `workflow-index`, `prd-index`, `prd-tracking`, `decision-index`, `decision-tracking`, `design-document-index`, `design-tracking`, `initiative-index`, `initiative-tracking`, `task-index`, `task-tracking`, `github-tasks`, `traceability-index`, or `repository-paths`.
- `-h`, `--help`: Show the command help text.
- No group-level write flags exist; pass mutation or output flags to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core sync --help
```

```sh
cd core/python
uv run watchtower-core sync all
```

```sh
cd core/python
uv run watchtower-core sync coordination
```

```sh
cd core/python
uv run watchtower-core sync command-index
```

```sh
cd core/python
uv run watchtower-core sync foundation-index
```

```sh
cd core/python
uv run watchtower-core sync command-index --write
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
uv run watchtower-core sync prd-tracking
```

```sh
cd core/python
uv run watchtower-core sync decision-index
```

```sh
cd core/python
uv run watchtower-core sync decision-tracking
```

```sh
cd core/python
uv run watchtower-core sync design-document-index
```

```sh
cd core/python
uv run watchtower-core sync design-tracking
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
uv run watchtower-core sync repository-paths --write
```

## Behavior and Outputs
- With no leaf command, the current implementation prints sync-specific help and exits successfully.
- The command group explains the available sync surfaces without requiring engineers to inspect the implementation directly.
- The current leaf commands are `all` for one-shot local rebuilds across all deterministic sync surfaces, `coordination` for the focused task-traceability-initiative rebuild slice, `command-index` for command-doc lookup rebuilds, `foundation-index` for the governed foundation intent corpus, `reference-index` for reference-corpus lookup rebuilds, `standard-index` for standards and best-practice lookup rebuilds, `workflow-index` for workflow-module lookup rebuilds, `prd-index` and `prd-tracking` for PRD machine and human tracking refreshes, `decision-index` and `decision-tracking` for decision machine and human tracking refreshes, `design-document-index` and `design-tracking` for design machine and human tracking refreshes, `initiative-index` and `initiative-tracking` for the cross-family initiative coordination view, `task-index` for machine task lookup rebuilds, `task-tracking` for the human-readable task board, `github-tasks` for push-only local task sync to GitHub including bounded managed labels, `traceability-index` for joined planning and evidence rebuilds, and `repository-paths` for README inventory rebuilds.
- Individual leaf commands may be dry-run by default and should document their mutation flags explicitly.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync command-index` | Rebuilds the command index from registry-backed CLI metadata while requiring companion command docs. |
| `watchtower-core sync all` | Rebuilds all local deterministic indexes and trackers in dependency order. |
| `watchtower-core sync coordination` | Rebuilds only the deterministic task, traceability, and initiative coordination slice. |
| `watchtower-core sync foundation-index` | Rebuilds the foundation index from governed foundation docs. |
| `watchtower-core sync reference-index` | Rebuilds the reference index from governed reference docs. |
| `watchtower-core sync standard-index` | Rebuilds the standard index from governed standards docs. |
| `watchtower-core sync workflow-index` | Rebuilds the workflow index from governed workflow modules. |
| `watchtower-core sync prd-index` | Rebuilds the PRD index from governed PRD documents. |
| `watchtower-core sync prd-tracking` | Rebuilds the human-readable PRD tracker from machine indexes and traceability. |
| `watchtower-core sync decision-index` | Rebuilds the decision index from governed decision records. |
| `watchtower-core sync decision-tracking` | Rebuilds the human-readable decision tracker from machine indexes and traceability. |
| `watchtower-core sync design-document-index` | Rebuilds the design-document index from governed design docs. |
| `watchtower-core sync design-tracking` | Rebuilds the human-readable design tracker from machine indexes and traceability. |
| `watchtower-core sync initiative-index` | Rebuilds the cross-family initiative index from traceability plus planning and task indexes. |
| `watchtower-core sync initiative-tracking` | Rebuilds the human-readable initiative tracker from the initiative index. |
| `watchtower-core sync task-index` | Rebuilds the task index from governed task records. |
| `watchtower-core sync task-tracking` | Rebuilds the human-readable task tracker from governed task records. |
| `watchtower-core sync github-tasks` | Pushes local-first task records to GitHub issues and optional project items. |
| `watchtower-core sync traceability-index` | Rebuilds the unified traceability index from governed planning and evidence sources. |
| `watchtower-core sync repository-paths` | Rebuilds the repository path index from README inventories. |
| `watchtower-core query commands` | Reads the command index that one of the current sync commands rebuilds. |
| `watchtower-core query references` | Reads the reference index that one of the current sync commands rebuilds. |
| `watchtower-core query tasks` | Reads the task index that one of the current sync commands rebuilds. |
| `watchtower-core query trace` | Reads the traceability index that one of the current sync commands rebuilds. |
| `watchtower-core query paths` | Reads the repository path index that the current sync command rebuilds. |
| `watchtower-core` | Root command that dispatches to this command group. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/cli/parser.py`
- `core/python/src/watchtower_core/sync/`

## Updated At
- `2026-03-10T06:39:00Z`
