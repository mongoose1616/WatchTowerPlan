# `watchtower-core plan closeout purge-trace`

## Summary
This command deletes one eligible closed trace-local planning package, writes the minimal
surviving purge record, and refreshes derived repository surfaces after the retention
guards pass.

## Use When
- A traced initiative is already terminal and its trace-local planning package is ready to leave the repository.
- You need a governed purge path instead of ad hoc deletion of closed initiative-package artifacts, tasks, contracts, and evidence.
- You want a dry-run check that surviving canonical surfaces no longer depend on the trace before removing it.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan closeout purge-trace` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/closeout.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan closeout purge-trace --trace-id <trace_id> [--retained-authority-path <path>]... [--purged-at <timestamp>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Stable trace identifier such as `trace.governed_acceptance_example`.
- `--retained-authority-path <path>`: Repository-relative canonical path that remains authoritative after purge. Repeat the option to record more than one surviving path.
- `--purged-at <timestamp>`: Explicit RFC 3339 UTC purge timestamp. Defaults to the current UTC time.
- `--write`: Delete the trace package, write the purge record, and refresh derived surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan closeout purge-trace --trace-id trace.example --retained-authority-path plan/docs/standards/governance/planning_retention_and_purge_standard.md
```

```sh
cd core/python
uv run watchtower-core plan closeout purge-trace --trace-id trace.example --retained-authority-path plan/python/src/watchtower_plan/example.py --write --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate the repository.
- The command refuses purge attempts when the target trace is not terminal, still has open tasks, still has acceptance-reconciliation drift, already has a purge record, or is still referenced by surviving canonical surfaces.
- The purge boundary is trace-scoped: the command removes trace-local initiative-package artifacts, decision notes, design records, implementation slices, tasks, acceptance contracts, and validation evidence together rather than allowing partial family cleanup.
- If `--retained-authority-path` is omitted, the implementation falls back to surviving non-package `related_paths` already published by the trace and records those in the purge record when they remain valid.
- In write mode, the command deletes the trace package, writes one purge record under `core/control_plane/ledgers/purges/`, and then runs the full derived-surface refresh path.
- In `human` mode, the command prints the purge timestamp, removed-path count, purge-record path, retained-authority paths, and whether it wrote the change.
- In `json` mode, the command prints one JSON object with the removed paths, retained-authority paths, purge-record path, refreshed sync targets, and write status.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan closeout` | Parent command group for live plan closeout and purge operations. |
| `watchtower-core closeout initiative` | Use this first when the trace still needs retained terminal closeout before purge. |
| `watchtower-core validate acceptance` | Confirms trace-level acceptance and evidence coherence before purge. |
| `watchtower-core sync all` | Rebuilds the derived surfaces that this command refreshes automatically in write mode. |
| `watchtower-core query trace` | Confirms the purged trace no longer appears in the retained traceability surface. |
| `watchtower-core query coordination` | Confirms the retained coordination surface no longer carries the purged trace as active or recent retained work. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/closeout.py`
- `plan/python/src/watchtower_plan/closeout/purge_trace.py`

## Updated At
- `2026-03-16T03:35:00Z`
