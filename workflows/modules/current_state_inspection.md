# Current-State Inspection Workflow

## Purpose
Use this workflow to inspect the current repository, codebase, document set, or architecture surfaces relevant to the active task before recommendations, edits, or judgments are made.

## Use When
- A task depends on understanding the current local state before execution can proceed correctly.
- The active work needs current implementation, document, or artifact context rather than only the request text.
- A task should identify affected surfaces, constraints, dependencies, or existing patterns before acting.

## Inputs
- Scoped task brief
- Relevant repository files, code paths, docs, or machine-readable artifacts
- Known affected surfaces or likely entrypoints
- Current constraints, dependencies, or risk signals already identified

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

## Workflow
1. Identify the current surfaces in scope.
   - Select the files, directories, artifacts, interfaces, or documents that materially affect the task.
   - Focus on the minimum local context needed for correct execution.
2. Inspect the current state directly.
   - Read the relevant local files, neighboring surfaces, and existing patterns.
   - Capture the current behavior, structure, or artifact shape that the task must respect.
3. Record constraints and affected surfaces.
   - Note dependencies, coupling, adjacent surfaces, and known risks.
   - Distinguish confirmed current-state facts from assumptions or still-open questions.

## Data Structure
- Current surfaces inspected
- Current-state facts
- Existing patterns or boundaries
- Constraints and dependencies
- Affected surfaces
- Open questions

## Outputs
- A current-state context summary for the active task
- A short record of affected surfaces, constraints, and existing local patterns

## Done When
- The task has a concrete current-state picture rather than only a requested target state.
- Relevant constraints, dependencies, and affected surfaces are visible.
- Downstream workflow modules can act without needing another broad local scan for the same context.
