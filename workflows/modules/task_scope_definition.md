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
- Existing `trace_id`, current initiative phase, or current initiative owner when the work belongs to an already-tracked initiative

## Workflow
1. State the task objective.
   - Describe the primary goal in one or two sentences.
   - Name the main artifact, surface, or decision the task is expected to affect.
2. Define the scope boundary.
   - Identify what is in scope for the active task.
   - Identify adjacent concerns that should stay out of scope for this task.
   - Name the repository surfaces most likely to be touched or inspected.
   - When the task belongs to an existing initiative, record the `trace_id` and current initiative phase explicitly so downstream workflows do not have to re-derive them.
   - Decide whether the task-handling threshold implies a durable task record or an explicit no-task outcome before deeper work begins.
3. Capture success conditions and blockers.
   - Record what must be true for the task to count as complete.
   - Surface missing inputs, assumptions, conflicts, or ambiguity that may still block progress.
   - If the task cannot proceed safely, note that clarification is required before deeper execution continues.

## Data Structure
- Task objective
- Scope boundary
- In-scope surfaces
- Existing initiative context when present
- Task-handling outcome when the work is non-trivial
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
