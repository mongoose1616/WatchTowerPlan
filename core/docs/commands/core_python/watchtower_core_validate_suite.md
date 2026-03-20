# `watchtower-core validate suite`

## Summary
This command runs one validation suite declared in the active validation-suite registry and returns one aggregate suite result.

## Use When
- You want reusable-core orchestration over a pack-declared validation baseline instead of invoking each validation family manually.
- You need to validate an external domain pack by pointing at its `pack_settings` surface.
- You want structured JSON output for workflows, agents, or higher-level automation.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate suite` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/validate_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate suite --suite-id <suite_id> [--pack-settings-path <path>] [--format <human|json>]
```

## Arguments and Options
- `--suite-id <suite_id>`: Stable validation suite identifier such as `suite.example.validation_baseline` or another pack-declared suite ID.
- `--pack-settings-path <path>`: Optional repository-relative path to the pack settings surface that declares the active schema, validator, and validation-suite registries.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core validate suite --suite-id suite.example.validation_baseline --pack-settings-path /tmp/example_pack/.wt/manifests/pack_settings.json
```

```sh
cd core/python
uv run watchtower-core validate suite --suite-id suite.example.validation_baseline --pack-settings-path /tmp/example_pack/.wt/manifests/pack_settings.json --format json
```

```sh
cd core/python
uv run watchtower-core validate suite --suite-id suite.example.validation_baseline --pack-settings-path /tmp/example_pack/.wt/manifests/pack_settings.json --format json
```

## Behavior and Outputs
- The command loads pack settings first, then resolves the active schema catalog, validator registry, and validation-suite registry from the declared surfaces.
- When `--pack-settings-path` is omitted, the runtime uses the active pack if one was selected explicitly; otherwise it discovers the repository-default pack settings surface and falls back to the shared-core pack only when no repo-local pack exists.
- Suite steps can currently run `pack_contract`, `artifact`, `front_matter`, and `document_semantics` validations.
- The current repository baseline suite uses repo-local target enumeration so the suite runtime can stay generic while the repo keeps its bounded validation target set.
- In `json` mode, the command returns one JSON object with the suite ID, pack-settings path, per-step summaries, and one structured result per executed target.
- The command exits with status code `0` when every executed target passes and `1` when any step fails or suite selection cannot be completed.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate` | Parent command group for governed validation operations. |
| `watchtower-core validate all` | Runs the current repo baseline suite plus acceptance reconciliation. |
| `watchtower-core validate artifact` | Validates one governed JSON artifact directly instead of through a declared suite. |
| `watchtower-core plan query authority` | Helpful when you need to confirm which pack-owned surfaces are authoritative. |

## Source Surface
- `core/python/src/watchtower_core/cli/validate_family.py`
- `core/python/src/watchtower_core/cli/validation_handlers.py`
- `core/python/src/watchtower_core/validation/suite.py`
- `core/python/src/watchtower_core/validation/pack_contract.py`
- `core/control_plane/registries/validation_suite_registry.json`

## Updated At
- `2026-03-19T22:48:00Z`
