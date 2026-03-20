# `watchtower-core pack validate`

## Summary
This command validates one hosted pack contract against the shared registry, runtime manifest, and typed integration descriptor.

## Use When
- You want a focused pack-interface validation pass for one hosted pack.
- You are changing pack manifests, integration hooks, or host wiring and want a narrower proof than `validate all`.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack validate` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/pack_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack validate [--pack <pack_slug>] [--pack-settings-path <path>] [--format <human|json>]
```

## Arguments and Options
- `--pack <pack_slug>`: Hosted pack slug such as `plan`. Defaults to the default repository pack.
- `--pack-settings-path <path>`: Optional pack settings path override for a non-default hosted pack.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack validate --pack plan
```

```sh
cd core/python
uv run watchtower-core pack validate --pack plan --format json
```

```sh
cd core/python
uv run watchtower-core pack validate --pack-settings-path packs/oversight/.wt/manifests/pack_settings.json --format json
```

## Behavior and Outputs
- Resolves the selected hosted pack from the shared pack registry unless `--pack-settings-path` overrides it.
- Runs the same pack-contract validator that `validate all` includes in the full repository pass.
- Reports pass or fail plus any contract drift issues around registry parity, runtime manifest fields, importable integration modules, typed capability runtimes, owned roots, pack-owned command docs, or validation-suite declarations.
- Query and sync runtimes fail closed when they publish empty command or target sets, even if they return the right runtime type.
- Fails closed when the pack-owned namespace command page is missing from the pack docs root or when a declared owned root is missing from the repository tree.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection and validation. |
| `watchtower-core pack describe` | Shows the hosted pack contract being validated. |
| `watchtower-core validate all` | Includes pack-contract validation in the broader repository validation pass. |
| `watchtower-core validate suite` | Runs one pack-declared validation suite after the pack contract itself is valid. |

## Source Surface
- `core/python/src/watchtower_core/cli/pack_handlers.py`
- `core/python/src/watchtower_core/validation/pack_contract.py`

## Updated At
- `2026-03-21T02:20:00Z`
