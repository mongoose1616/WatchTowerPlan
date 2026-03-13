# `watchtower-core`

## Summary
This is the root CLI entrypoint for the core Python workspace. It dispatches to the current `watchtower-core` command groups and provides the fastest top-level route into help, routing, planning, query, sync, validation, and closeout flows.

## Use When
- You need the top-level command map before choosing a narrower command group.
- You want stable root help for the current CLI surface.
- You need one consistent entrypoint for workspace-local automation or operator use.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core` |
| Kind | `root_command` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/parser.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core <command> [args]
```

## Arguments and Options
- `<command>`: Dispatch to a command group such as `doctor`, `route`, `plan`, `query`, `task`, `sync`, `closeout`, or `validate`.
- `-h`, `--help`: Show the root command help text.
- No root-only flags exist beyond help and subcommand selection.

## Examples
```sh
cd core/python
uv run watchtower-core --help
```

```sh
cd core/python
uv run watchtower-core route preview --request "do a documentation review of the command docs" --format json
```

```sh
cd core/python
uv run watchtower-core query coordination --format json
```

```sh
cd core/python
uv run watchtower-core sync all --format json
```

```sh
cd core/python
uv run watchtower-core validate all --format json
```

## Behavior and Outputs
- With no subcommand, the root command prints help and exits successfully.
- With a valid subcommand, it dispatches to that group's handler and returns the group's exit status.
- Use the group pages and leaf command pages for exact flags and behavior instead of treating this root page as the exhaustive command catalog.
- Use `watchtower-core query commands --query <term> --format json` when you need machine-readable command discovery instead of browsing docs manually.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core route` | Advisory route preview for turning a request into workflow modules. |
| `watchtower-core query` | Read-only lookup surface for commands, planning, coordination, standards, and other governed indexes. |
| `watchtower-core sync` | Rebuilds derived governed artifacts and tracking surfaces. |
| `watchtower-core validate` | Runs repo-wide, artifact, document, and acceptance validation flows. |
| `docs/commands/core_python/README.md` | Command-family entrypoint for the core Python workspace. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/cli/parser.py`
- `core/python/src/watchtower_core/cli/registry.py`

## Updated At
- `2026-03-13T15:05:00Z`
