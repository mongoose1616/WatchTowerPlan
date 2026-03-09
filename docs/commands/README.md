# `docs/commands`

## Description
`This directory contains repository-native command pages for durable CLI and operator-facing commands. Use it as the human-readable man-page layer for command discovery, usage, and current behavior.`

## Boundaries
`Keep one command or subcommand per page. Keep external command references in docs/references/ and keep machine-readable command lookup data under core/control_plane/indexes/commands/.`

## Paths
| Path | Description |
|---|---|
| `docs/commands/README.md` | Describes the purpose of the command-doc directory and its current command families. |
| `docs/commands/core_python/` | Holds command pages for the core Python workspace and the watchtower-core CLI family. |
