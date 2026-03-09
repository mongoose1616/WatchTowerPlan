# Repository Assessment Workflow

## Purpose
Use this workflow to assess an inventoried repository for coherence, freshness, maintainability, validation coverage, security posture, operational readiness, and developer experience.

## Use When
- A repository review has already established the current inventory and now needs quality assessment.
- The active review should evaluate the repository across multiple quality dimensions rather than only one narrow concern.
- A reviewer needs a structured assessment before findings are prioritized and summarized.

## Inputs
- Scoped repository-review brief
- Repository inventory
- Current repository docs, code, tooling, configs, and control-plane artifacts
- Internal standards and canonical references applied
- External guidance notes when needed

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

## Workflow
1. Check coherence and consistency.
   - Review whether code structure, naming, layering, module boundaries, docs, and automation describe the same system.
   - Note drift between intended architecture and current implementation.
2. Check accuracy and freshness.
   - Review whether setup docs, README files, workflow names, paths, versions, and operational notes still match reality.
   - Flag stale assumptions, deprecated tools, or outdated guidance.
3. Review maintainability and validation coverage.
   - Assess code quality, coupling, duplication, error handling, test coverage, linting, formatting, typechecking, and build or verification surfaces where they exist.
   - Note where validation expectations are missing, weak, or not enforced.
4. Review security, operational readiness, and developer experience.
   - Check secret handling, auth boundaries, dependency risk, unsafe defaults, rollout or incident-readiness signals, and local setup ergonomics.
   - Record friction that makes common contributor tasks harder than they should be.

## Data Structure
- Coherence and consistency assessment
- Accuracy and freshness assessment
- Maintainability assessment
- Validation coverage assessment
- Security and operational readiness assessment
- Developer experience assessment

## Outputs
- A structured repository assessment across the main review dimensions
- A short record of risks, weak controls, and sustainability concerns found during assessment

## Done When
- The repository has been assessed across the key review dimensions rather than only one slice.
- Risks, drift, and weak controls are visible before findings are prioritized.
- The review is ready for findings synthesis and remediation planning.
