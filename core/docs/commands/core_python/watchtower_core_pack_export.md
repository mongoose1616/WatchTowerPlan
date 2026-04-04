# `watchtower-core pack export`

## Summary
This command stages either a portability-clean repository bundle or a portability-clean pack-only bundle for customer handoff.

## Use When
- You want a curated customer-safe export instead of handing off a raw donor repository snapshot.
- You need a core-only bootstrap bundle with hosted-pack wiring scrubbed out of shared registry and workspace metadata.
- You need a core-plus-selected-pack bundle with omitted pack roots, retained history, tests, runtime residue, and donor-only assessment references removed.
- You need a scrubbed pack-only bundle that can be copied into a compatible core repository and bootstrapped there.
- You do not want to retain shared reusable-core tests or other engineering-only source surfaces in the staged handoff.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack export` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/pack_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack export --output-root <path> [--include-pack <pack_slug>]... [--pack-only] [--overwrite] [--format <human|json>]
```

## Arguments and Options
- `--output-root <path>`: Required filesystem path where the staged export should be written.
- `--include-pack <pack_slug>`: Hosted pack slug to include in the staged export. Repeat for multiple packs. Omit for core-only bootstrap export. Required with `--pack-only`.
- `--pack-only`: Stage only the selected hosted-pack roots without shared `core/`. Use this for additive pack bundles that will be copied into a compatible core repository.
- `--overwrite`: Replace an existing staged export directory.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack export --output-root /tmp/customer_core --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core pack export --output-root /tmp/customer_pack_repo --include-pack <pack-slug> --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core pack export --output-root /tmp/customer_pack_bundle --include-pack <pack-slug> --pack-only --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core pack export --output-root /tmp/customer_bundle --include-pack <pack-slug> --include-pack <second-pack-slug> --overwrite --format json
```

## Behavior and Outputs
- By default, copies only the allowlisted root files plus shared `core/` and the selected hosted-pack roots. It does not copy unrelated root notes, donor caches, or omitted hosted-pack roots into the staged export.
- With `--pack-only`, copies only the selected hosted-pack roots. Shared `core/`, root routing material, and shared workspace files are intentionally omitted.
- This is the customer-safe handoff builder, not the engineering repo-to-repo shared-core refresh path. Use `watchtower-core pack extract-core` when the recipient needs reusable-core tests and other engineering surfaces retained.
- Scrubs retained governed history under `core/control_plane/records/**`, shared acceptance-contract examples, traceability entries that depend on scrubbed retained evidence or still point outside shared `core/` and the selected hosted-pack roots, shared and pack-owned test trees, pack-owned `watchtower_<pack>.testing` helpers, pack `.wt/runtime/**`, donor project repository maps, developer-machine residue, and internal assessment or comparison closeout references.
- When a selected hosted pack declares the optional `export_cleanup` capability, the export runtime also runs that pack-owned cleanup hook against the staged bundle. Repository-bundle exports may use it to remove pack-local live history, replace scrubbed-but-still-governed files with empty schema-valid placeholders when needed, and then rebuild clean derived pack surfaces before portability validation. Pack-only exports may use it to scrub pack-local history even when shared-core rebuild surfaces are intentionally unavailable.
- Treat the staged export as the final handoff surface. An actively used working repository can accumulate fresh telemetry, caches, or runtime residue after validation, so rerun `pack export` immediately before release or customer bootstrap.
- Use `watchtower-core release check` when you want the fail-closed local gate to wrap dirty-worktree protection, the broad validation baseline, and the final staged export in one command instead of running this export step directly.
- Follow [customer_release_and_bootstrap_standard.md](/core/docs/standards/operations/customer_release_and_bootstrap_standard.md) when sequencing the broad repo gate, explicit schema checks, export, and recipient bootstrap guidance.
- Repository-bundle mode reconciles the staged shared hosted-pack registry and staged `core/python/pyproject.toml` to exactly the selected pack set.
- Repository-bundle mode treats the first `--include-pack` slug as the default hosted pack in the staged export. With no selected packs, the staged shared pack registry is emptied for core-only bootstrap.
- Core-only repository-bundle mode also rewrites the staged root `README.md` and `AGENTS.md` so they no longer route operators toward omitted pack roots.
- Repository-bundle mode rebuilds the shared command, repository-path, reference, foundation, standard, workflow, and route discovery indexes inside the staged export after the scrub and pack-selection reconciliation steps.
- Repository-bundle mode may legitimately leave `core/control_plane/indexes/traceability/traceability_index.json` with `entries: []` when the export contains no portable trace lineage after the acceptance/evidence scrub and export-root filtering pass.
- Repository-bundle mode removes `core/python/uv.lock` from the staged export so the recipient does not inherit donor lock state.
- Core-only repository-bundle mode strips hosted-pack coverage source paths from `core/python/pyproject.toml`.
- Repository-bundle mode validates each included hosted pack contract in the staged export before running the portability scan.
- Pack-only mode skips full hosted-pack contract validation because shared core surfaces are intentionally absent. Use `watchtower-core pack bootstrap` and `watchtower-core pack validate` after copying the bundle into a compatible core repository.
- Exits non-zero when hosted-pack validation or portability validation fails. The staged export is left on disk for inspection.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection, export, scaffold, bootstrap, and validation flows. |
| `watchtower-core pack extract-core` | Builds the looser engineering shared-core extract when the goal is repo-to-repo reuse rather than customer-safe handoff. |
| `watchtower-core release check` | Preferred one-shot local release gate when you want validation and dirty-worktree protection around this export step. |
| `watchtower-core pack bootstrap` | Reconciles shared hosted-pack wiring in-place without building a curated staged export. |
| `watchtower-core validate portability` | Validates an already-staged export or donor root without mutating it. |
| `watchtower-core validate all` | Runs the repository validation baseline, which is separate from customer-release scrub validation. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_family.py`
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/python/src/watchtower_core/pack_integration/export.py`
- `core/python/src/watchtower_core/pack_integration/bootstrap.py`

## Updated At
- `2026-04-03T21:00:00Z`
