# `watchtower-core pack apply-core`

## Summary
This command applies a staged engineering shared-core extract into the current repository's `core/` tree while preserving recipient-local developer residue such as `.venv` and cache directories.

## Use When
- You already staged a donor-neutral shared-core extract with `watchtower-core pack extract-core`.
- You want a recipient-side helper instead of a raw `rsync` or manual copy command.
- You need to replace governed `core/**` content without deleting the recipient's local `.venv`, caches, or similar machine-local residue.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack apply-core` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/pack_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack apply-core --source-root <path> [--write] [--format <human|json>]
```

## Arguments and Options
- `--source-root <path>`: Required filesystem path to the staged engineering shared-core extract root.
- `--write`: Replace the local `core/` tree from the staged extract. Without this flag, the command reports the planned changes only.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack apply-core --source-root /tmp/shared_core --format json
```

```sh
cd core/python
uv run watchtower-core pack apply-core --source-root /tmp/shared_core --write --format json
```

## Behavior and Outputs
- Validates the staged source root against the engineering shared-core portability contract before mutating the recipient repository.
- Applies only `core/`. It does not rewrite the recipient root shell or any pack-owned roots.
- Replaces governed shared-core files and removes destination-only governed `core/**` paths that are not present in the staged extract.
- Preserves recipient-local developer residue under `core/**`, including `.venv`, cache directories, and similar machine-local scratch families, instead of deleting them during the apply step.
- Reports changed, deleted, and preserved repository-relative paths in the result payload.
- Use `watchtower-core pack bootstrap --pack-settings-path <recipient-pack-settings> --replace-hosted-packs --write --sync-extra dev --format json` immediately after a successful write-mode apply.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack extract-core` | Stages the engineering shared-core extract that this command applies. |
| `watchtower-core pack bootstrap` | Reconciles the recipient pack into the newly applied shared core. |
| `watchtower-core validate portability` | Validates a staged engineering extract directly when you need a read-only readiness check. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_family.py`
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/python/src/watchtower_core/pack_integration/export.py`

## Updated At
- `2026-03-29T02:35:00Z`
