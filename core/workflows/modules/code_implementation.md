# Code Implementation Workflow

## Purpose
Use this workflow to define the implementation approach and apply the requested code change while keeping the affected repository surfaces coherent.

## Use When
- A feature, fix, refactor, or behavior change needs to be implemented.
- Existing code must be changed to satisfy a design brief, implementation slice, issue, or bug report.
- A task requires code changes plus the adjacent tests, docs, or configuration updates needed to keep the repository coherent.

## Inputs
- Scoped implementation brief
- Relevant design brief, implementation slice, issue, or acceptance criteria
- Current-state context summary
- Governing standards, references, and design docs applied
- External guidance notes when needed
- Required task-tracking, review, or handoff reference expectations when already identified
- Technical constraints and non-functional requirements
- Open questions

## Workflow
1. Define the implementation approach.
   - Decide how the change will be introduced before editing.
   - Confirm which governing standards, references, or design docs materially constrain the implementation and return to internal-context review if they are still unclear.
   - Keep the scope aligned with the request and avoid unrelated cleanup.
   - Call out tradeoffs or risks when they affect correctness or maintainability.
2. Implement the change.
   - Modify the relevant code, tests, docs, configs, or schemas needed for a coherent result.
   - Apply the governing-document set deliberately instead of relying only on nearby repository patterns or memory.
   - Keep related surfaces synchronized when the change affects a governed source of truth.
   - Update task-tracking, documentation, or handoff surfaces when the governing standards or references need explicit links or traceable mention for later review and validation.
   - Follow existing repository patterns unless there is a clear reason to change them.
   - If the implementation intentionally deviates from a governing document, make that deviation explicit and either update the governing document or record focused follow-up work.

## Data Structure
- Change summary
- Implementation approach
- Governing documents applied
- Affected surfaces
- Open questions or implementation risks

## Outputs
- A code change aligned with the request, repository standards, and governing design guidance
- Updated adjacent surfaces when needed to keep the change coherent
- An explicit record of the implementation approach, governing-document set, affected surfaces, and any materially distinct tradeoff or deviation boundary

## Done When
- The requested code change has been implemented.
- The implementation reflects applicable internal standards, canonical references, and existing repository patterns.
- The governing documents that shaped the change are explicit enough for downstream validation and review.
- Related tests, docs, configs, or other affected surfaces have been updated when needed.
