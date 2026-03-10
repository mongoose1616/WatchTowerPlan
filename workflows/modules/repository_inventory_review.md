# Repository Inventory Review Workflow

## Purpose
Use this workflow to inventory the repository's major surfaces, implementation areas, tooling, and ownership boundaries before deeper repository assessment begins.

## Use When
- A repository review needs a concrete inventory of the current project before quality judgments are made.
- The active review should map the repo's main applications, docs, workflows, packages, services, scripts, and machine-readable artifact families.
- A reviewer needs a clear picture of what exists, what appears missing, and where ownership boundaries are unclear.

## Inputs
- Scoped repository-review brief
- Repository contents
- Top-level docs, manifests, control-plane artifacts, and workflow surfaces
- Known risk areas or inventory questions

## Workflow
1. Map the main repository surfaces.
   - Identify the primary documentation, workflow, implementation, schema, registry, contract, policy, and example surfaces.
   - Note the main entrypoints a reviewer would use to navigate the repository.
2. Identify technologies and execution surfaces.
   - Record the main languages, frameworks, tooling, validation surfaces, and packaging or runtime boundaries present in the repo.
   - Distinguish scaffolded implementation surfaces from live executable surfaces.
3. Flag structural risk areas.
   - Note dead areas, duplicated systems, missing inventories, placeholder-only surfaces, or unclear ownership boundaries that may affect the review.

## Data Structure
- Repository inventory
- Main entrypoints
- Technologies and tooling present
- Executable versus placeholder surfaces
- Structural risk areas

## Outputs
- A structured repository inventory for the active review
- A short record of structural gaps, duplicated areas, or unclear ownership boundaries

## Done When
- The repository's main surfaces and technology boundaries are mapped.
- The review has enough inventory context to assess the repo deliberately.
- Structural gaps or dead areas that may affect later judgments are explicit.
