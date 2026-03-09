# Task Handoff Review Workflow

## Purpose
Use this workflow to confirm that the active task output is coherent, handoff-ready, and accompanied by any needed related-surface updates, follow-up notes, or commit-closeout escalation.

## Use When
- A routed task has produced a draft result, recommendation, change, or review output that needs a final handoff check.
- The active work may affect related docs, standards, workflows, templates, or validation surfaces.
- The task should end with explicit follow-up work rather than leaving next steps implicit.

## Inputs
- Active task outputs or draft deliverables
- Current task context and applied internal or external guidance records
- Known related surfaces, unresolved questions, or follow-up concerns
- Commit readiness signal when the task may be ready for closeout

## Workflow
1. Review the output for handoff readiness.
   - Confirm the task output is clear enough for the next contributor, reviewer, or workflow to use without major verbal context filling gaps.
   - Check that the result matches the scoped objective and current repository state.
2. Identify related-surface impacts.
   - Note any adjacent standards, workflows, templates, docs, tests, schemas, or machine-readable artifacts that should be updated in the same change set.
   - Distinguish same-change updates from explicit deferred follow-up work.
3. Record follow-up and closeout needs.
   - Surface unresolved questions, risks, blockers, and recommended next steps explicitly.
   - If the change is ready to be committed, add the commit-closeout workflow rather than improvising commit behavior here.

## Data Structure
- Handoff-ready output summary
- Related surfaces to update
- Deferred follow-up work
- Remaining risks or open questions
- Commit-closeout recommendation when relevant

## Outputs
- A handoff-ready result summary
- A short record of related-surface updates, deferred follow-up work, and open questions
- A clear signal about whether commit closeout should be added next

## Done When
- The task output is ready for downstream use or review.
- Related-surface impacts are explicit rather than implied.
- Follow-up work, risks, and closeout needs are clear enough for the next workflow to continue without ambiguity.
