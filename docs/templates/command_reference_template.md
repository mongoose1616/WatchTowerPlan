# `<command>`

> Use this template for repository-native command pages under `docs/commands/`.
> Keep one primary command or subcommand per document.
> Treat the page as the human-readable man page for that command.

## Summary
<One short explanation of what the command does.>

## Use When
- <When an engineer or operator should use this command.>
- <What need or task it solves.>

## Command
| Field | Value |
|---|---|
| Invocation | `<command>` |
| Kind | `<root_command_or_subcommand>` |
| Workspace | `<workspace_label>` |
| Source Surface | `<repo-relative implementation path>` |

## Synopsis
```sh
<command> [args]
```

## Arguments and Options
- `<argument_or_option>`: <what it does.>
- `-h`, `--help`: Show the command help text.

## Examples
```sh
<real repository example>
```

## Behavior and Outputs
- <What the command does when it succeeds.>
- <What output or side effects it currently produces.>
- <What exit behavior matters.>

## Related Commands
| Command | Relationship |
|---|---|
| `<related command>` | <How it relates.> |

## Source Surface
- `<repo-relative implementation path>`
- `<related doc or workspace path>`

## Last Synced
- `YYYY-MM-DD`
