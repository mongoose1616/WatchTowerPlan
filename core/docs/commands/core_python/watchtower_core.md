# `watchtower-core`

## Summary
This is the root CLI entrypoint for the core Python workspace. It dispatches to the current `watchtower-core` command groups and provides the fastest top-level route into help, routing, hosted-pack inspection, release gating, pack-owned orchestration, query, sync, and validation flows.

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
| Source Surface | `core/python/src/watchtower_host/cli/parser.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core <command> [args]
```

## Arguments and Options
- `<command>`: Dispatch to a command group such as `doctor`, `route`, `pack`, `release`, `<pack-namespace>`, `query`, `sync`, or `validate`.
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
uv run watchtower-core pack list --format json
```

```sh
cd core/python
uv run watchtower-core pack describe --format json
```

```sh
cd core/python
uv run watchtower-core release check --output-root /tmp/customer_plan --include-pack plan --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core sync command-index --write
```

```sh
cd core/python
uv run watchtower-core sync repository-paths --write
```

```sh
cd core/python
uv run watchtower-core validate all --format json
```

## Behavior and Outputs
- With no subcommand, the root command prints help and exits successfully.
- With a valid subcommand, it dispatches to that group's handler and returns the group's exit status.
- Runtime telemetry is default-on and local. Each invocation writes one JSONL file under `<machine_root>/runtime/telemetry/` unless `WATCHTOWER_TELEMETRY=off` disables it or `WATCHTOWER_TELEMETRY_DIR` redirects the sink.
- The CLI keeps human and JSON command payloads on stdout. Telemetry emits only one concise stderr summary line per invocation unless `WATCHTOWER_TELEMETRY_STDERR=off` suppresses it.
- Use the group pages and leaf command pages for exact flags and behavior instead of treating this root page as the exhaustive command catalog.
- Use `watchtower-core query commands --query <term> --format json` when you need machine-readable command discovery instead of browsing docs manually.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core route` | Advisory route preview for turning a request into workflow documents. |
| `watchtower-core pack` | Inspects hosted-pack registry entries, runtime manifests, and pack-contract validation. |
| `watchtower-core release` | Runs the local fail-closed release gate for customer-safe bundle staging. |
| `watchtower-core <pack-namespace>` | Pack-owned namespace for bootstrap, live query, task, closeout, and other pack-local flows. |
| `watchtower-core query` | Shared read-only lookup surface for commands, standards, references, foundations, workflows, and durable records. |
| `watchtower-core sync` | Rebuilds derived governed artifacts and tracking surfaces. |
| `watchtower-core validate` | Runs repo-wide, artifact, document, and acceptance validation flows. |
| `core/docs/commands/core_python/README.md` | Command-family entrypoint for the core Python workspace. |

## Source Surface
- `core/python/src/watchtower_host/cli/parser.py`
- `core/python/src/watchtower_host/cli/registry.py`

## Updated At
- `2026-03-25T02:15:00Z`
