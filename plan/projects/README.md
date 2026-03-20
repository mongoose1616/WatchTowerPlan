# `plan/projects`

## Description
`This directory is the project-container root for project-scoped live plan work. Each project container owns project machine state, rendered project views, repository linkage, and any child initiatives scoped to that project.`

## Notes
- Project containers live at `plan/projects/<project_slug>/`.
- Each project container owns `.wt/project.json`, `.wt/project_repository_map.json`, and the rendered `project.md`, `repositories.md`, and `summary.md` surfaces.
- Each project-scoped initiative lives at `plan/projects/<project_slug>/initiatives/<initiative_slug>/`.
- Project bootstrap must complete before any project-scoped initiative may be created under the container.
