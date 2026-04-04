# `watchtower-core telemetry delete`

## Summary
This command previews or deletes retained runtime telemetry JSONL files under one resolved telemetry root. It defaults to dry-run output and applies deletion only when `--write` is present.

## Use When
- You need to prune old telemetry JSONL files under the active pack machine root.
- You want to target another pack telemetry root through `--pack-settings-path`.
- You need a governed cleanup path that excludes the active invocation's own telemetry file automatically.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core telemetry delete` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/telemetry_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core telemetry delete (--older-than-days <days> | --before <utc_cutoff> | --all) [--pack-settings-path <path> | --telemetry-root <path>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--older-than-days <days>`: Match telemetry files older than this many days.
- `--before <utc_cutoff>`: Match telemetry files older than this UTC cutoff. Accepts an ISO timestamp or `YYYY-MM-DD`.
- `--all`: Match every retained telemetry JSONL file under the resolved telemetry root.
- `--pack-settings-path <path>`: Resolve the telemetry root from one hosted pack instead of the active default pack.
- `--telemetry-root <path>`: Optional explicit telemetry root override. The directory name must be `telemetry`.
- `--write`: Apply deletion. Without this flag the command reports a dry-run preview only.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core telemetry delete --older-than-days 7 --format json
```

```sh
cd core/python
uv run watchtower-core telemetry delete --before 2026-03-01 --format json
```

```sh
cd core/python
# Illustrative: substitute a real hosted-pack settings path from this repo.
uv run watchtower-core telemetry delete --all --pack-settings-path <pack-root>/.wt/manifests/pack_settings.json --write --format json
```

## Behavior and Outputs
- The command requires exactly one selector: `--older-than-days`, `--before`, or `--all`.
- The command accepts either `--pack-settings-path` or `--telemetry-root`, not both.
- The active invocation's own telemetry JSONL file is always excluded from matching and deletion.
- Only telemetry `*.jsonl` files under the resolved telemetry root are matched.
- When matched file deletion would leave dated directories empty, the command also removes those empty directories.
- In `human` mode, the command prints the resolved root, matched counts, optional cutoff, and the file and directory paths involved.
- In `json` mode, the command prints one structured result object with counts, bytes, and matched paths.
- The command exits with status code `0` when the preview or deletion succeeds and `1` when input validation or filesystem operations fail.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core telemetry` | Parent command group for local telemetry cleanup commands. |
| `watchtower-core benchmark` | Deliberate retained performance measurement rather than runtime telemetry cleanup. |
| `watchtower-core query benchmarks` | Reads retained benchmark evidence when the real question is performance history rather than telemetry sink hygiene. |

## Source Surface
- `core/python/src/watchtower_host/cli/telemetry_handlers.py`
- `core/python/src/watchtower_host/cli/telemetry_family.py`
- `core/python/src/watchtower_core/telemetry/cleanup.py`

## Updated At
- `2026-04-04T17:00:00Z`
