# Core Workflow

## Purpose
Use this workflow to load the minimum shared standards and instructions that apply across all routed workflow modules.

## Use When
- Any task has been routed through `workflows/ROUTING_TABLE.md`.
- A task needs the shared repository-level or path-level instructions that apply before task-specific module behavior.

## Inputs
- User request
- Root and local `AGENTS.md` instructions
- Routed workflow modules
- Relevant shared repository standards, templates, or canonical docs when they apply across the routed modules

## Workflow
1. Load repository instructions.
   - Apply the repository `AGENTS.md` and any more-local instruction overlays that govern the target paths.
2. Confirm the routed module set.
   - Use only the minimum workflow modules selected by the routing surface.
   - Treat `core.md` as shared context, not as a replacement for task-specific modules.
3. Load shared standards and canonical instructions.
   - Gather only the standards, templates, or canonical docs that apply across the routed modules or are explicitly required by the request.
   - Prefer explicit repository rules over inferred conventions.
   - When the target surface includes `core/python/**`, include the Python workspace standard and the Python workspace README in the shared context set.
4. Stop at shared context.
   - Do not add task-specific execution, review, validation, or research behavior here.
   - Defer task-specific steps to the additional routed modules.

## Data Structure
- Applicable instruction layers
- Confirmed routed module set
- Shared standards, templates, and canonical docs loaded
- Path-local instruction overlays
- Open routing or instruction conflicts

## Outputs
- Shared context loaded for the routed task
- Confirmed routed module set for downstream execution
- Any instruction conflict that materially affects execution, if present

## Done When
- The minimum shared instructions for the routed task have been loaded.
- Shared repository standards or canonical docs that apply across the routed modules have been identified.
- Task-specific behavior has been left to the additional routed modules.
