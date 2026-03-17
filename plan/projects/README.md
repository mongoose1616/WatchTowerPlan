# `plan/projects`

## Description
`This directory is the project-container root for project-scoped live plan work. Each project container will own project machine state, rendered project views, repository linkage, and any child initiatives scoped to that project.`

## Notes
- Project containers live at `plan/projects/<project_slug>/`.
- Each project-scoped initiative will later live at `plan/projects/<project_slug>/initiatives/<initiative_slug>/`.
- Project bootstrap remains a later task; this slice seeds only the canonical root so project-scoped flows can land without inventing a parallel path.
