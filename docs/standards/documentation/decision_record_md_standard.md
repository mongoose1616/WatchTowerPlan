---
id: "std.documentation.decision_record_md"
title: "Decision Record Document Standard"
summary: "This standard defines the structure, placement, and document-shape rules for durable decision records stored under `docs/planning/decisions/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "decision_record_md"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:23:35Z"
audience: "shared"
authority: "authoritative"
---

# Decision Record Document Standard

## Summary
This standard defines the structure, placement, and document-shape rules for durable decision records stored under `docs/planning/decisions/`.

## Purpose
Keep decision records consistent enough that rationale, status, affected surfaces, and downstream planning links remain easy to review and easy to index.

## Scope
- Applies to durable decision-record documents stored under `docs/planning/decisions/`.
- Covers placement, required sections, and the relationship between decision records, their tracker, and the machine-readable decision index.
- Does not replace the governance rules in [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md).

## Use When
- Creating a new durable decision record.
- Refreshing a decision record after its outcome, scope, or downstream impacts change.
- Reviewing whether a decision record is structured clearly enough to support traceability and later lookup.

## Related Standards and Sources
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [decision_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/decision_index_standard.md)
- [decision_record_template.md](/home/j/WatchTowerPlan/docs/templates/decision_record_template.md)
- [README.md](/home/j/WatchTowerPlan/docs/planning/decisions/README.md)

## Guidance
- Store durable decision records under `docs/planning/decisions/`.
- Keep one primary decision per document.
- Include explicit record metadata near the top of the document so decision ID, record status, and decision status are easy to find.
- Include a shared `Trace ID` in the record metadata so the decision can join to its PRD, design, and implementation-plan context.
- Distinguish clearly between:
  - `Record Status`, which follows the governed lifecycle vocabulary
  - `Decision Status`, which captures the outcome state such as `proposed` or `accepted`
- Link the decision to affected PRDs, designs, plans, or paths when they exist.
- Keep the decision record focused on the decision boundary and its tradeoffs rather than restating broad repository background.
- Update the decision tracker and machine-readable decision index in the same change set when a decision record changes materially.

## Structure or Data Model
### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| Decision record | `docs/planning/decisions/<decision_name>.md` | Use stable snake_case filenames derived from the decision topic. |
| Decision tracker | `docs/planning/decisions/decision_tracking.md` | Human-readable tracker for the current decision corpus. |
| Decision directory README | `docs/planning/decisions/README.md` | Directory orientation and inventory only. |

### Required sections for decision records
| Section | Requirement | Notes |
|---|---|---|
| `Record Metadata` | Required | Include `Decision ID`, `Record Status`, `Decision Status`, and `Updated At` in RFC 3339 UTC form `YYYY-MM-DDTHH:MM:SSZ` at minimum. |
| `Summary` | Required | One short explanation of the decision boundary. |
| `Decision Statement` | Required | State the decision in one clear sentence. |
| `Trigger or Source Request` | Required | Record what prompted the decision. |
| `Current Context and Constraints` | Required | Summarize the current state that shaped the decision. |
| `Affected Surfaces` | Required | Identify the PRDs, designs, plans, or paths affected. |
| `Options Considered` | Required | Record the viable options and tradeoffs. |
| `Chosen Outcome` | Required | Record the recommended or accepted outcome. |
| `Rationale and Tradeoffs` | Required | Explain why the chosen outcome won. |
| `Consequences and Follow-Up Impacts` | Required | Record what changes next. |
| `Risks, Dependencies, and Assumptions` | Required | Make material constraints explicit. |
| `References` | Required | Link the relevant internal companion docs and any material external sources. |

### Optional sections for decision records
| Section | Use When |
|---|---|
| `Open Questions` | A real unresolved question remains. |
| `Supersession` | The decision supersedes or is superseded by another decision. |

## Process or Workflow
1. Place the decision record under `docs/planning/decisions/` with a stable snake_case filename.
2. Draft the document from the decision-record template and keep the required sections in order.
3. Update the decision tracker and the machine-readable decision index in the same change set.
4. Propagate accepted decisions into canonical repository artifacts so the decision record does not become the only active policy surface.

## Validation
- Decision records should contain the required sections in the documented order.
- The decision boundary and current status should be easy to identify without reading the full document.
- Affected upstream and downstream planning artifacts should be linked when they exist.
- Reviewers should reject decision records that capture multiple unrelated decisions or omit the outcome state.

## Change Control
- Update this standard and the decision-record template in the same change set when the decision-record document shape changes.
- Update the decision tracker and machine-readable decision index in the same change set when decision records are added, renamed, removed, or materially retargeted.

## References
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [decision_record_template.md](/home/j/WatchTowerPlan/docs/templates/decision_record_template.md)

## Updated At
- `2026-03-09T05:23:35Z`
