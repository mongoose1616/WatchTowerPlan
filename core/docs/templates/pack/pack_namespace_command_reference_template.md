# `watchtower-core <command_namespace>`

> Use this template for the pack-owned namespace entry page at `<pack>/docs/commands/core_python/watchtower_core_<command_namespace>.md`.
> Keep the command page under the owning pack docs root, not under shared core docs.
> Treat the page as the human-readable entrypoint for the pack command family and keep examples runnable from the pack-aware workspace.

## Summary
<Explain what the pack namespace does and any materially distinct scope, mode, or workspace boundary the summary needs to signal.>

## Use When
- <When an engineer or operator should enter this pack namespace.>
- <What domain-owned tasks or workflows it exposes.>

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core <command_namespace>` |
| Kind | `pack_namespace` |
| Workspace | `<pack_root>/python` |
| Source Surface | `<pack_root>/python/src/watchtower_<pack_slug>/integration.py` |

## Synopsis
```sh
watchtower-core <command_namespace> <subcommand> [args]
```

## Arguments and Options
- `<subcommand>`: <Describe the primary pack-owned command groups.>
- `--format <human|json>`: Include when the namespace or child commands support structured output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
uv run watchtower-core <command_namespace> --help
```

## Behavior and Outputs
- <Describe how the namespace command family is registered and discovered by the host runtime.>
- <Describe where pack-specific command docs live and how they relate to pack validation.>

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack describe --pack <pack_slug>` | Inspect the hosted-pack registry and runtime contract for this namespace. |
| `watchtower-core pack validate --pack <pack_slug> --format json` | Validate the pack contract, owned roots, and namespace docs for this pack. |

## Source Surface
- `<pack_root>/python/src/watchtower_<pack_slug>/integration.py`
- `<pack_root>/.wt/manifests/pack_runtime_manifest.json`
- `<pack_root>/.wt/manifests/pack_settings.json`

## Updated At
- `YYYY-MM-DDTHH:MM:SSZ`
