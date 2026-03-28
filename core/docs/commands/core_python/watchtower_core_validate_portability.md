# `watchtower-core validate portability`

## Summary
This command validates a repository bundle, engineering shared-core extract, or pack-only bundle against the current portability contract.

## Use When
- You want a deterministic report of what still needs to be scrubbed before customer release.
- You need to validate a staged export for core-only bootstrap or core-plus-selected-pack bootstrap.
- You need to validate a donor-neutral shared-core extract intended for engineering repo-to-repo refresh.
- You need to validate a pack-only bundle that intentionally omits shared core.
- You want to detect retained records, non-portable acceptance lineage, tests, pack runtime residue, omitted hosted packs, donor-only assessment references, or absolute donor paths before handoff.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate portability` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/validate_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate portability [--root <path>] [--include-pack <pack_slug>]... [--pack-only] [--engineering-core] [--format <human|json>]
```

## Arguments and Options
- `--root <path>`: Repository root or staged export root to validate. Defaults to the current directory.
- `--include-pack <pack_slug>`: Hosted pack slug allowed in the target root. Repeat to validate a core-plus-selected-pack export. Omit for core-only bootstrap validation. Required with `--pack-only`.
- `--pack-only`: Validate the target root as a pack-only bundle that intentionally omits shared `core/`.
- `--engineering-core`: Validate the target root as a donor-neutral engineering shared-core extract that retains reusable-core tests but excludes donor hosted-pack wiring and donor-only retained artifacts.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core validate portability
```

```sh
cd core/python
uv run watchtower-core validate portability --include-pack plan --format json
```

```sh
cd core/python
uv run watchtower-core validate portability --root /tmp/shared_core --engineering-core --format json
```

```sh
cd core/python
uv run watchtower-core validate portability --root /tmp/customer_plan_pack --include-pack plan --pack-only --format json
```

```sh
cd core/python
uv run watchtower-core validate portability --root /tmp/customer_export --include-pack plan --format json
```

## Behavior and Outputs
- The command scans the target root for retained control-plane history, shared acceptance-contract artifacts, acceptance-linked traceability lineage that depends on scrubbed retained evidence, developer-machine residue, pack-local runtime outputs, shared and pack-owned test trees, pack-owned `watchtower_<pack>.testing` helpers, donor project repository maps, donor-only assessment or comparison closeout references, shared workspace references to omitted packs, and filesystem-absolute donor paths.
- With no `--include-pack` flags, the command validates a core-only bootstrap target and treats every hosted pack as omitted.
- When one or more `--include-pack` flags are provided, the command expects the shared pack registry and shared `core/python` workspace metadata to match exactly that selected pack set.
- With `--pack-only`, the command validates the target as an additive pack bundle. It requires at least one selected pack slug, rejects bundled shared `core/`, and checks the discovered pack manifests against the selected pack set without expecting shared registry or workspace metadata.
- With `--engineering-core`, the command validates the target as a donor-neutral shared-core engineering extract. Shared `core/python/tests/**` and the minimal portable root shell are allowed there, but donor pack roots, donor-only retained history, donor pack wiring, and donor-specific acceptance lineage still fail closed.
- `--engineering-core` cannot be combined with `--pack-only` or `--include-pack`.
- The command is read-only. It does not mutate the target root.
- A working repository that has been used after bootstrap can legitimately fail portability because runtime telemetry, caches, or other developer residue were generated after the last scrub. Use `watchtower-core pack export` to produce the final customer/bootstrap artifact or `watchtower-core pack extract-core` to produce the engineering shared-core extract.
- Use `watchtower-core release check` when you want portability validation coupled to dirty-worktree protection, the broad validation baseline, and final staged export creation.
- Follow [customer_release_and_bootstrap_standard.md](/core/docs/standards/operations/customer_release_and_bootstrap_standard.md) when portability validation is part of the full release sequence rather than a one-off diagnostic check.
- The command exits non-zero when portability issues are found.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate` | Parent command group for governed validation behavior. |
| `watchtower-core pack extract-core` | Stages a donor-neutral shared-core extract and runs this validator in engineering-core mode. |
| `watchtower-core pack export` | Builds a curated staged export and then runs this portability validator against the staged output. |
| `watchtower-core release check` | Preferred one-shot local release gate when portability should be proven on the final staged export in the same run. |
| `watchtower-core pack bootstrap` | Reconciles shared registry and workspace metadata to a selected hosted-pack set before portability validation. |
| `watchtower-core validate all` | Runs the current repository validation baseline, which is separate from customer-release scrub checks. |

## Source Surface
- `core/python/src/watchtower_host/cli/validate_family.py`
- `core/python/src/watchtower_host/cli/validation_handlers.py`
- `core/python/src/watchtower_core/validation/portability.py`

## Updated At
- `2026-03-28T04:20:00Z`
