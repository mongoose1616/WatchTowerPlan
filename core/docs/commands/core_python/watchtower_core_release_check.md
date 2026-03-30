# `watchtower-core release check`

## Summary
This command runs the local fail-closed release gate and stages one final export for customer handoff or downstream bootstrap.

## Use When
- You want one command that enforces the current local release contract instead of running each step separately.
- You need the donor worktree checked for cleanliness before a release claim is accepted.
- You want the broad repository validation baseline, changed-schema validation, and final export staging tied together in one result payload.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core release check` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/release_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core release check --output-root <path> [--include-pack <pack_slug>]... [--pack-only] [--schema-path <path>]... [--pack-settings-path <path>] [--allow-dirty] [--overwrite] [--format <human|json>]
```

## Arguments and Options
- `--output-root <path>`: Required filesystem path where the staged export should be written.
- `--include-pack <pack_slug>`: Hosted pack slug to include in the staged export. Repeat for multiple packs. Omit for core-only release bundles. Required with `--pack-only`.
- `--pack-only`: Stage only the selected hosted-pack roots without shared core. Use this for additive pack bundles that will be copied into a compatible core repository.
- `--schema-path <path>`: Explicit schema-definition path to validate as part of the release gate. Repeat for multiple files.
- `--pack-settings-path <path>`: Optional repository-relative path to the pack settings surface whose default validation suite should supply the broad validation baseline.
- `--allow-dirty`: Continue even when git metadata reports a dirty worktree. Use only for local rehearsal, not final customer handoff.
- `--overwrite`: Replace an existing staged export directory.
- `--format <human|json>`: Select human-readable or structured JSON output. Agents should prefer `json`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core release check --output-root /tmp/customer_core --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core release check --output-root /tmp/customer_pack_repo --include-pack <pack-slug> --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core release check --output-root /tmp/customer_pack_bundle --include-pack <pack-slug> --pack-only --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core release check --output-root /tmp/customer_release --include-pack <pack-slug> --schema-path core/control_plane/schemas/interfaces/packs/pack_settings.schema.json --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core release check --output-root /tmp/rehearsal --include-pack <pack-slug> --allow-dirty --overwrite --format json
```

## Behavior and Outputs
- When git metadata is available, the command inspects the donor worktree before running validation or export. A dirty worktree fails closed unless `--allow-dirty` is supplied.
- The command runs `watchtower-core validate all` semantics through the reusable-core validation service before export staging.
- The command runs explicit Draft 2020-12 schema-definition validation for every `--schema-path` target and for any locally changed `*.schema.json` files discovered from git worktree status.
- The command then stages the final export through the same pack-export runtime used by `watchtower-core pack export`, including pack-contract validation and portability validation on the staged output.
- With `--pack-only`, the staged output is an additive pack bundle rather than a standalone repository. The portability scope switches to `pack_bundle`.
- If git metadata is unavailable, the command does not fail solely for that reason. It records that the dirty-worktree check was unavailable and continues with validation plus export.
- In `json` mode, the payload includes the worktree summary, selected schema-definition validations, broad validation summary, and nested export plus portability details.
- In `human` mode, the command prints a focused release summary. Non-zero exit means either the dirty-worktree guard tripped, validation failed, or the staged export failed validation.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core release` | Parent command group for local release-gate behavior. |
| `watchtower-core validate all` | Manual baseline validation path when you want the broad validation result independently. |
| `watchtower-core validate schema` | Manual schema-definition validation path when you want separate per-schema output or evidence. |
| `watchtower-core pack export` | Manual export path when you want to stage a curated bundle without the combined local gate. |
| `watchtower-core pack bootstrap` | Required after copying a pack-only bundle into compatible shared core. |

## Source Surface
- `core/python/src/watchtower_host/cli/release_handlers.py`
- `core/python/src/watchtower_host/cli/release_family.py`
- `core/python/src/watchtower_core/pack_integration/release_check.py`

## Updated At
- `2026-03-25T02:15:00Z`
