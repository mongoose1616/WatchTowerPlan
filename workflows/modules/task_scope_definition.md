# Task Scope Definition Workflow

## Purpose
Use this workflow to define the task objective, scope boundary, and success conditions clearly enough that downstream workflow modules can execute without guessing.

## Use When
- A routed task needs an explicit objective and boundary before task-specific execution begins.
- A request is broad enough that the next workflow needs the target surfaces and expected outcome stated clearly.
- The active task may be blocked by unresolved scope, assumptions, or ambiguity that should be made visible before deeper work begins.

## Inputs
- User request or triggering task
- Known artifacts, surfaces, or outputs in scope
- Current ambiguity, constraints, or assumptions
- Any acceptance criteria, target outcome, or handoff expectation already provided

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

## Workflow
1. State the task objective.
   - Describe the primary goal in one or two sentences.
   - Name the main artifact, surface, or decision the task is expected to affect.
2. Define the scope boundary.
   - Identify what is in scope for the active task.
   - Identify adjacent concerns that should stay out of scope for this task.
   - Name the repository surfaces most likely to be touched or inspected.
3. Capture success conditions and blockers.
   - Record what must be true for the task to count as complete.
   - Surface missing inputs, assumptions, conflicts, or ambiguity that may still block progress.
   - If the task cannot proceed safely, note that clarification is required before deeper execution continues.

## Data Structure
- Task objective
- Scope boundary
- In-scope surfaces
- Out-of-scope concerns
- Success conditions
- Blocking ambiguity or assumptions

## Outputs
- A scoped task brief that downstream workflow modules can use
- A short record of in-scope surfaces, success conditions, and blockers

## Done When
- The task objective and scope boundary are explicit.
- Downstream workflow modules can proceed without re-deriving the basic task frame.
- Any blocking ambiguity has been surfaced clearly enough to continue or reroute deliberately.
