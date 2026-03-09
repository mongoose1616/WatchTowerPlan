# `workflows`

## Description
`This directory contains the repository routing surface and the workflow modules used to execute planning tasks. Use ROUTING_TABLE.md to select the minimum required modules, then load the specific workflow documents from workflows/modules/. Routes may combine shared phase modules with narrower task-family modules so execution stays modular.`

## Paths
| Path | Description |
|---|---|
| `workflows/README.md` | Describes the purpose of the workflows directory and the main workflow entrypoints stored here. |
| `workflows/ROUTING_TABLE.md` | Defines task classification and the minimum workflow modules to load for each task type. |
| `workflows/modules/` | Holds the task-specific workflow modules used after routing. |
