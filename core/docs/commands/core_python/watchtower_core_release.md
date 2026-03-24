# `watchtower-core release`

## Summary
This command group runs the local release gate for customer-safe repository bundles and pack bundles.

## Use When
- You want one operator-facing entrypoint for local release and bootstrap handoff checks.
- You need fail-closed dirty-worktree protection before staging a customer bundle.
- You want command-family help for the local release-gate flow instead of assembling the sequence from several command pages.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core release` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/release_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core release <release_command> [args]
```

## Arguments and Options
- `<release_command>`: Choose the release-gate leaf command, currently `check`.
- `-h`, `--help`: Show the command help text.
- No group-level release flags exist; pass release-gate options to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core release --help
```

```sh
cd core/python
uv run watchtower-core release check --output-root /tmp/customer_core --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core release check --output-root /tmp/customer_plan --include-pack plan --overwrite --format json
```

## Behavior and Outputs
- With no leaf command, the group prints release-specific help and exits successfully.
- `check` is the current local fail-closed release gate. It combines dirty-worktree inspection, the broad repository validation baseline, explicit schema-definition checks, and final staged export creation.
- The release family is local orchestration only. It does not replace the lower-level `validate` or `pack export` commands when you need to inspect or rerun one step independently.
- Humans and agents use the same release flow. Agents should prefer `--format json`; humans may use either `human` or `json`.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core release check` | Runs the current local release gate and stages one final export. |
| `watchtower-core pack export` | Manual export step when you need to stage a bundle without the combined local gate. |
| `watchtower-core validate all` | Manual baseline validation step when you need the validation family summary independently. |
| `watchtower-core validate schema` | Manual schema-definition validation step when you need separate evidence per changed schema file. |
| `watchtower-core` | Root command that dispatches to this command group. |

## Source Surface
- `core/python/src/watchtower_host/cli/release_family.py`
- `core/python/src/watchtower_host/cli/release_handlers.py`
- `core/python/src/watchtower_core/pack_integration/release_check.py`

## Updated At
- `2026-03-25T02:15:00Z`
