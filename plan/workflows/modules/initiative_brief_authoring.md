# Initiative Brief Authoring Workflow

## Purpose
Use this workflow to turn a scoped planning request into a review-ready `initiative_brief.md` that defines the package before design and execution begin.

## Use When
- A new initiative or scoped change needs authoritative intake before design and execution.
- Scope is still fuzzy and needs structure.
- Stakeholders need a written document to review or approve.

## Inputs
- Scoped initiative-intake request
- Problem statement
- Target users
- Business goal
- Foundation-context brief
- Current-state context summary when the initiative brief depends on an existing repository or product surface
- Internal standards and canonical references applied
- External guidance notes when needed
- Constraints
- Timeline expectations
- Known dependencies
- Open questions

## Additional Files to Load
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md): defines the live initiative package model and keeps new briefs aligned with the current plan roots and downstream phase boundaries.
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md): defines the shared trace IDs and artifact-link expectations that the brief should seed.
- [README.md](/plan/docs/foundations/README.md): routes the author to the mirrored foundations corpus that should shape the brief.

## Workflow
1. Confirm the upstream intake boundary.
   - Resolve the scoped planning request, current-state dependency boundary, and governing constraints the brief must absorb before design begins.
   - If the request does not yet identify a concrete problem, target users, scope boundary, or success condition, merge clarification before drafting instead of guessing.
2. Define scope and success.
   - Record what is in scope, what is out of scope, the primary goal, measurable success signals when they matter, and the assumptions or constraints that downstream planning must preserve.
   - Use the current-state context when the initiative brief extends, replaces, or depends on an existing repository or product surface.
3. Draft the authoritative intake brief.
   - Capture the requirements, scenarios, acceptance criteria, dependencies, and risks that materially reduce ambiguity for downstream design work.
   - Include every materially distinct requirement, constraint, scenario, and boundary that `design_record.md` may assume without reopening intake.
4. Escalate unresolved ambiguity explicitly.
   - If material product, architecture, or governance tradeoffs remain unresolved, merge `decision_capture.md` rather than treating one option as settled brief scope.
   - If open questions remain but do not block design, mark them as downstream inputs to `design_record_planning.md` instead of leaving them implicit.
5. Validate the downstream handoff.
   - Confirm the brief defines the upstream boundary for `design_record.md`, including goals, non-goals, acceptance criteria, constraints, dependencies, and unresolved questions.
   - Remove vague language that would force design work to restate intake assumptions verbally.

## Data Structure
- Problem statement
- Goals and non-goals
- Requirements and acceptance criteria
- Risks and dependencies
- Optional actors, scenarios, metrics, or open questions only when material

## Outputs
- A review-ready `initiative_brief.md` draft
- Explicit downstream handoff inputs for `design_record.md`
- Explicit unresolved questions only when they remain

## Done When
- The problem, goals, scope, and requirements are documented.
- The initiative brief remains aligned with the repository foundations in `core/docs/foundations/`.
- The initiative brief reflects applicable internal standards, canonical references, and existing planning patterns.
- Success metrics and acceptance criteria are defined.
- Risks, dependencies, and open questions are visible.
- The design-record handoff boundary is explicit enough that design work can start without re-scoping the initiative orally.
- The initiative brief does not omit materially distinct planning detail that downstream design or execution work would otherwise have to rediscover verbally.
