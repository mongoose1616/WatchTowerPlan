# `watchtower-core pack extract-core`

## Summary
This command stages a donor-neutral shared-core extract for engineering repo-to-repo reuse.

## Use When
- You need to refresh `core/` from one WatchTower-style repository into another repository.
- You want shared reusable-core tests, docs, and governed source material retained for engineering work after copy.
- You need donor hosted-pack wiring, donor-only retained artifacts, and donor-only trace lineage removed before the recipient bootstraps its own pack.
- You want a fail-closed readiness check on the staged `core/` bundle before copying it into a recipient repository.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack extract-core` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/pack_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack extract-core --output-root <path> [--overwrite] [--format <human|json>]
```

## Arguments and Options
- `--output-root <path>`: Required filesystem path where the staged engineering extract should be written.
- `--overwrite`: Replace an existing staged extract directory.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack extract-core --output-root /tmp/shared_core --overwrite --format json
```

## Behavior and Outputs
- Stages shared `core/` plus the minimal portable root shell needed to keep governed lookup surfaces coherent. It does not copy donor pack roots or unrelated donor repository material.
- Scrubs donor hosted-pack registry entries and shared `core/python/pyproject.toml` pack wiring from the staged extract so the recipient can bootstrap its own hosted-pack contract cleanly.
- Removes `core/python/uv.lock` when shared workspace wiring changes so the recipient does not inherit a stale donor lockfile.
- Preserves reusable shared-core tests and other shared engineering surfaces that customer-safe bundle export intentionally removes.
- Preserves only shared acceptance, validation-evidence, and traceability lineage that remains fully `core/**`-scoped and reusable-core portable. Donor-specific retained history and donor-specific acceptance lineage are removed.
- Rebuilds the shared discovery indexes when hosted-pack wiring changes during the scrub so the staged `core/` remains internally coherent.
- Validates the staged output against the engineering-core portability contract before returning success.
- Use `watchtower-core pack bootstrap --pack-settings-path <recipient-pack-settings> --replace-hosted-packs --write --sync-extra dev --format json` in the recipient repository after copying the staged `core/`; that bootstrap pass now materializes the recipient pack's declared `sync all` slice when the workspace is ready.
- Exits non-zero when staging or readiness validation fails. The staged output is left on disk for inspection.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection, bootstrap, extract, export, scaffold, and validation flows. |
| `watchtower-core pack bootstrap` | Reconciles the recipient repository's hosted-pack wiring after this staged `core/` is copied in. |
| `watchtower-core pack export` | Builds the stricter customer-safe handoff bundle rather than the engineering repo-to-repo shared-core extract. |
| `watchtower-core validate portability` | Validates an already-staged extract with `--engineering-core` when you need a standalone readiness check. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_family.py`
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/python/src/watchtower_core/pack_integration/export.py`
- `core/python/src/watchtower_core/validation/portability.py`

## Updated At
- `2026-03-28T04:20:00Z`
