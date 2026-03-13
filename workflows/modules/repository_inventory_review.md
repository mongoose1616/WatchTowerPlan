# Repository Inventory Review Workflow

## Purpose
Use this workflow to inventory the repository's major surfaces, authority boundaries, execution paths, and review hotspots before deeper repository assessment begins.

## Use When
- A repository review needs a concrete inventory of the current project before quality judgments are made.
- The active review should map the repo's main applications, docs, workflows, packages, services, scripts, and machine-readable artifact families.
- A reviewer needs a clear picture of what exists, what appears missing, and where ownership boundaries are unclear.

## Inputs
- Scoped repository-review brief
- Repository contents
- Top-level docs, manifests, control-plane artifacts, and workflow surfaces
- Known risk areas, review focus themes, or inventory questions

## Workflow
1. Build the repository coverage map.
   - Identify the primary documentation, workflow, implementation, schema, registry, contract, policy, example, command, template, test, and planning surfaces.
   - Record the main entrypoints a reviewer would use to navigate the repository and note any intentionally excluded regions.
2. Classify the major surfaces and boundaries.
   - Record which surfaces are authored versus derived, human-readable versus machine-readable, executable versus reserved, and canonical versus supporting.
   - Note the main ownership, packaging, and reusable-versus-repo-local boundaries.
3. Identify execution, validation, and projection paths.
   - Record the main languages, frameworks, tooling, validators, sync paths, query paths, loaders, and runtime entrypoints present in the repo.
   - Distinguish live executable or enforced surfaces from scaffolds, examples, placeholders, and dormant families.
4. Flag structural risk areas and hotspots.
   - Note dead areas, duplicated systems, unclear source-of-truth boundaries, placeholder-only surfaces, hotspot files, or missing navigation aids that may affect the review.
   - Separate intentional governed explicitness from probable sprawl or accidental duplication.

## Data Structure
- Repository coverage map
- Surface classification and authority boundaries
- Main entrypoints and execution paths
- Validation, sync, query, and loader surfaces
- Structural risk areas and hotspots

## Outputs
- A structured repository inventory and coverage map for the active review
- A short record of hotspots, structural gaps, duplicated areas, or unclear ownership boundaries

## Done When
- The repository's main surfaces, technology boundaries, and authority boundaries are mapped.
- The review has enough inventory context to assess the repo deliberately.
- Structural gaps, hotspots, or dead areas that may affect later judgments are explicit.
