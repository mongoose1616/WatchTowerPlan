# `<command>`

> Use this template for repository-native command pages under `docs/commands/`.
> Keep one primary command or subcommand per document.
> Treat the page as the human-readable man page for that command.
> Keep command pages as plain Markdown by default; command-family lookup metadata lives in the machine-readable command index rather than front matter.
> Keep examples runnable from the documented workspace.
> When a command supports structured output, include at least one `--format json` example.

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
- `--format <human|json>`: <include when the command supports both human-readable and structured machine output.>
- `-h`, `--help`: Show the command help text.

## Examples
```sh
<real repository example>
```

## Behavior and Outputs
- <What the command does when it succeeds.>
- <What output or side effects it currently produces.>
- <Describe human-readable and structured output modes separately when both exist.>
- <What exit behavior matters.>

## Related Commands
| Command | Relationship |
|---|---|
| `<related command>` | <How it relates.> |

## Source Surface
- `<repo-relative implementation path>`
- `<related doc or workspace path>`

## Updated At
- `YYYY-MM-DDTHH:MM:SSZ`
