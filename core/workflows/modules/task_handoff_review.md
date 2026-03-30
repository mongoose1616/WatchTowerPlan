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
- Current tracked-work or coordination state when the task belongs to a governed local follow-up system
- Known related surfaces, unresolved questions, or follow-up concerns
- Commit readiness signal when the task may be ready for closeout

## Workflow
1. Review the output for handoff readiness.
   - Confirm the task output is clear enough for the next contributor, reviewer, or workflow to use without major verbal context filling gaps.
   - Check that the result matches the scoped objective and current repository state.
   - Confirm that the governing standards, references, or design docs that materially shaped the result are explicit enough to survive handoff.
   - If the output is a review or audit, confirm that the scope boundary, evidence basis, and any confirmation-pass result are explicit.
2. Identify related-surface impacts.
   - Note any adjacent standards, workflows, templates, docs, tests, schemas, tracked-work surfaces, or machine-readable artifacts that should be updated in the same change set.
   - Check whether the task-tracking, documentation, or review surfaces should carry explicit links or references to the governing documents used during the work.
   - When the task changed workflow docs, routing tables, validator coverage, or command behavior, explicitly check the companion route index, workflow index, validator registry, route-preview behavior, and relevant command docs instead of assuming those surfaces stayed aligned.
   - When the task belongs to a governed local tracker or coordination surface, check whether the current result changes status, ownership, blockers, next-step projection, or closeout readiness.
   - Distinguish same-change updates from explicit deferred follow-up work.
3. Record follow-up and closeout needs.
   - Surface unresolved questions, risks, blockers, and recommended next steps explicitly.
   - Record any deviation from governing standards or references, plus whether it was resolved, intentionally accepted, or deferred.
   - If the task was a review loop, record whether repeated passes found no new actionable issues or which gaps remain open.
   - If workflow or routing behavior changed, record the exact preview or query checks used to confirm the new route behavior and call out any still-unverified paths.
   - Confirm any repository-local task or closeout outcome is explicit for non-trivial work when the active pack or repository requires it.
   - If the change is ready to be committed, add the commit-closeout workflow rather than improvising commit behavior here.

## Data Structure
- Handoff-ready output summary
- Review scope and confirmation status when applicable
- Governing documents carried through the task
- Related surfaces to update
- Tracked-work or coordination follow-up when the task belongs to a governed local tracker
- Route-index, workflow-index, validator, route-preview, and command-doc parity status when workflow behavior changed
- Deferred follow-up work
- Remaining risks or open questions
- Repository-local task-handling outcome when required
- Commit-closeout recommendation when relevant

## Outputs
- A handoff-ready result or update
- Governing-document references and any deviation follow-up made explicit for downstream work
- Same-change related-surface updates and deferred follow-up, when any
- Explicit parity status for companion workflow, routing, validator, and command surfaces when those surfaces were in scope
- A clear signal about whether commit closeout should be added next

## Done When
- The task output is ready for downstream use or review.
- Governing-document references, gaps, or deviations are explicit rather than implicit.
- Related-surface impacts are explicit rather than implied.
- Companion route, workflow, validator, preview, and command-doc surfaces are either aligned in the same change or deferred explicitly when workflow behavior changed.
- Follow-up work, risks, and closeout needs are clear enough for the next workflow to continue without ambiguity.
