# External Guidance Research Workflow

## Purpose
Use this workflow to consult authoritative external guidance only when internal repository guidance is incomplete or the active task depends on version-sensitive, domain-specific, regulatory, standards-driven, or vendor-controlled behavior.

## Use When
- Internal repository guidance is incomplete for the active task.
- The task depends on external authority such as official language, framework, protocol, standards-body, security, regulatory, or vendor documentation.
- The work needs a short record of which external sources materially shaped the result.

## Inputs
- Scoped task brief
- Current internal-context package
- Specific open questions, uncertainties, or version-sensitive concerns
- Candidate authoritative sources when already known

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md): constrains how material external guidance should be normalized into repo-local references.

## Workflow
1. Decide whether external research is necessary.
   - Confirm that the active task cannot be resolved reliably from internal repository guidance alone.
   - Keep the research boundary tied to the specific missing guidance.
2. Choose authoritative sources.
   - Prefer official standards bodies, platform documentation, language or framework maintainers, security guidance, regulatory materials, and vendor documentation.
   - Avoid secondhand summaries when primary sources are available.
3. Extract only the material guidance.
   - Record the external guidance that materially affects the task.
   - Capture relevant version, date, or baseline details when the source is time-sensitive.
   - Distinguish direct source guidance from local interpretation or still-open uncertainty.

## Data Structure
- Research trigger or gap
- Authoritative sources consulted
- Version or date context when relevant
- Material guidance extracted
- Remaining uncertainty

## Outputs
- A short record of the authoritative external guidance that materially affects the task
- Explicit confirmation when no external research was needed

## Done When
- The active task has the minimum external guidance it needs, if any.
- Material source details and relevant version or date context are recorded.
- External authority has been used to close a real gap rather than as routine background browsing.
