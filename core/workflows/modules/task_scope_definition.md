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
- Known governing standards, references, design docs, or implementation guidance already linked to the request
- Current ambiguity, constraints, or assumptions
- Any acceptance criteria, target outcome, or handoff expectation already provided
- Existing tracked-work context, pack-owned coordination state, or repository closeout expectations when the work already belongs to a governed local follow-up system

## Workflow
1. State the task objective.
   - Describe the primary goal in one or two sentences.
   - Name the main artifact, surface, or decision the task is expected to affect.
2. Define the scope boundary.
   - Identify what is in scope for the active task.
   - Identify adjacent concerns that should stay out of scope for this task.
   - Name the repository surfaces most likely to be touched or inspected.
   - Name the governing standards, references, or design docs that must be reviewed before implementation or validation begins.
   - When the task already belongs to a governed local tracker, coordination surface, or review loop, record only the local context that downstream workflows would otherwise need to rediscover.
   - Note whether the scoped task, companion artifact, or final handoff should carry explicit links or references to those governing documents.
   - Decide whether repository-local task or closeout rules require a durable task record or an explicit no-task outcome before deeper work begins.
3. Capture success conditions and blockers.
   - Record what must be true for the task to count as complete.
   - Treat missing governing guidance or unresolved conflicts between governing documents as blockers when they materially affect correctness, maintainability, or reviewability.
   - Surface missing inputs, assumptions, conflicts, or ambiguity that may still block progress.
   - If the task cannot proceed safely, note that clarification is required before deeper execution continues.

## Data Structure
- Task objective
- Scope boundary
- In-scope surfaces
- Governing standards, references, or design docs to review
- Existing tracked-work context when present
- Expected task or handoff links to governing documents when applicable
- Repository-local task-handling outcome when required
- Out-of-scope concerns
- Success conditions
- Blocking ambiguity or assumptions

## Outputs
- A scoped task brief that downstream workflow modules can use
- Governing-document expectations that downstream implementation, validation, and handoff work must preserve
- Blocking ambiguity called out only when it materially affects execution

## Done When
- The task objective and scope boundary are explicit.
- Governing-document expectations are explicit enough that downstream workflows do not need to rediscover them from scratch.
- Downstream workflow modules can proceed without re-deriving the basic task frame.
- Any blocking ambiguity has been surfaced clearly enough to continue or reroute deliberately.
