# Decision Capture Standard

## Summary
This standard defines how durable repository decisions should be recorded so rationale, tradeoffs, status, and downstream impacts remain clear over time.

## Purpose
- Prevent consequential decisions from remaining implicit, verbal, or scattered across unrelated artifacts.
- Preserve enough context that future contributors can understand what was decided, why it was decided, and what changed because of it.
- Keep a clear boundary between decision history and active repository policy.
- Ensure accepted decisions are propagated into canonical repository artifacts instead of living only in a decision record.

## Scope
- Applies to durable repository decisions such as architecture choices, governance decisions, standards decisions, workflow-policy decisions, and major planning or design tradeoffs.
- Covers decision boundaries, statuses, rationale, options, evidence, consequences, and synchronization with canonical repository artifacts.
- Applies whether the record is expressed as an ADR, a planning decision record, or another durable decision artifact.
- Does not define a single mandatory storage location or file template for all decision records.
- Does not replace PRDs, implementation plans, standards, or references that should hold the active repository guidance after a decision is accepted.

## Use When
- A repository decision needs a durable written record.
- Multiple viable options or tradeoffs were considered and the chosen direction should be preserved.
- A blocker, policy choice, or architecture question must be resolved before downstream work can proceed.
- Future contributors would likely need the rationale or consequences to avoid re-litigating the same decision.

## Related Standards and Sources
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md)
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)
- [decision_capture.md](/home/j/WatchTowerPlan/workflows/modules/decision_capture.md)
- [documentation_generation.md](/home/j/WatchTowerPlan/workflows/modules/documentation_generation.md)
- [documentation_refresh.md](/home/j/WatchTowerPlan/workflows/modules/documentation_refresh.md)
- [adr_guidance_reference.md](/home/j/WatchTowerPlan/docs/references/adr_guidance_reference.md)

## Guidance
- Capture one durable decision per record. Do not blend unrelated decisions into one artifact just because they were discussed together.
- State the decision in one clear sentence near the top of the record.
- Mark the status clearly, such as `proposed`, `accepted`, `deferred`, `rejected`, or `superseded`.
- Record the triggering request, blocker, or question that made decision capture necessary.
- Identify the repository surfaces affected by the decision, including standards, workflows, templates, plans, architecture docs, interfaces, or implementation areas.
- Gather and apply relevant internal standards, workflows, templates, ADR guidance, and canonical repository documents before inferring new local policy.
- Use authoritative external sources only when internal guidance is incomplete or the decision depends on version-sensitive, standards-driven, regulatory, framework, or vendor behavior.
- If external guidance materially shapes the decision, record the specific sources used and keep the source facts separate from local interpretation.
- Capture the viable options, including deferral or no change when those are credible choices.
- Record the rationale in terms of correctness, policy fit, maintainability, delivery risk, operational consequences, and repository coherence rather than only preference language.
- Make assumptions, conditions, and known constraints explicit when the decision depends on them.
- Distinguish clearly between:
  - the decision record as history and rationale
  - canonical repository artifacts that define the active current policy or guidance
- If an accepted decision changes repository policy, standards, workflows, templates, or design expectations, update those canonical artifacts in the same change set when practical.
- If canonical updates are deferred, record the follow-up work explicitly so the decision does not become the only place where the active rule exists.
- Surface unresolved questions, dependencies, and risks explicitly rather than hiding them inside vague rationale text.
- When a later decision replaces an earlier one, mark the supersession clearly so readers can tell which outcome is current.

## Structure or Data Model
- Decision title
- Decision statement
- Decision status
- Trigger or source request
- Current context and constraints
- Affected surfaces or artifacts
- Internal standards and canonical references applied
- External sources consulted when needed
- Options considered
- Recommended or chosen outcome
- Rationale and tradeoffs
- Consequences and follow-up impacts
- Risks, dependencies, and assumptions
- Open questions
- Supersedes or superseded-by links when applicable

## Process or Workflow
1. Confirm that the issue needs durable decision capture rather than only a PRD note, implementation-task comment, or transient discussion.
2. Define the decision boundary so the record covers one clear question.
3. Inspect the current repository context, affected surfaces, constraints, and dependencies.
4. Gather the internal standards, workflows, templates, and canonical references that should govern the choice.
5. Research authoritative external guidance only when repository guidance is incomplete or the decision depends on external authority.
6. Compare viable options and record the material tradeoffs.
7. Record the current recommendation or chosen outcome, plus status, rationale, assumptions, and consequences.
8. Propagate accepted policy into canonical standards, workflows, templates, plans, or design docs so the decision record does not become the sole source of truth.
9. If later work changes the outcome materially, create or update the relevant decision record so supersession is explicit rather than implied.

## Validation
- The record captures one decision cleanly.
- The decision statement and status are immediately understandable.
- The record identifies the repository surfaces affected by the outcome.
- Applicable internal standards and canonical references were used before inventing new local policy.
- External sources are recorded when they materially influenced the decision.
- Viable options, tradeoffs, and rationale are visible rather than implied.
- Consequences, follow-up work, and unresolved questions are explicit.
- Accepted decisions are reflected in canonical repository artifacts or have explicit follow-up to make that happen.
- A future contributor can understand the decision without relying on undocumented verbal context.
- Superseded decisions are marked clearly enough that stale records are not mistaken for active policy.

## Change Control
- Update this standard when the repository changes how durable decisions are recorded, reviewed, or synchronized with canonical artifacts.
- Update the decision-capture workflow and any decision-record templates or automation in the same change set when this standard changes materially.
- If the repository later standardizes a dedicated ADR or decision-record directory, define that file-location rule in the same governance change set.

## References
- [decision_capture.md](/home/j/WatchTowerPlan/workflows/modules/decision_capture.md)
- [adr_guidance_reference.md](/home/j/WatchTowerPlan/docs/references/adr_guidance_reference.md)
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md)

## Notes
- A decision record preserves why a choice was made. The repository's active operating rules should still live in the canonical artifacts that govern current behavior.
- Not every local implementation choice needs durable decision capture. Use it when the rationale, alternatives, or downstream consequences are important enough to matter later.

## Last Synced
- `2026-03-09`
