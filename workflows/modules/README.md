# `workflows/modules`

## Description
`This directory contains the individual workflow modules that define routed task behavior for the planning repository. Some modules are shared execution phases, while others are narrower task-family modules. Each module should stay focused on one workflow concern and be loaded through the routing table rather than treated as an ad hoc document set.`

## Files
| Path | Description |
|---|---|
| `workflows/modules/README.md` | Describes the purpose of the workflow modules directory and the modules stored here. |
| `workflows/modules/code_implementation.md` | Workflow module for implementing code changes. |
| `workflows/modules/code_review.md` | Workflow module for reviewing code changes. |
| `workflows/modules/code_validation.md` | Workflow module for validating code changes. |
| `workflows/modules/clarification.md` | Workflow module for resolving ambiguity that blocks routing or downstream work. |
| `workflows/modules/commit_closeout.md` | Workflow module for preparing and creating repository-compliant Git commits. |
| `workflows/modules/core.md` | Core workflow module that applies across routed tasks. |
| `workflows/modules/current_state_inspection.md` | Shared workflow module for inspecting the relevant current repository state before deeper task execution. |
| `workflows/modules/decision_capture.md` | Workflow module for recording durable decisions and their rationale. |
| `workflows/modules/documentation_implementation_reconciliation.md` | Shared workflow module for reconciling companion documentation and machine-readable lookup surfaces with the actual implementation. |
| `workflows/modules/documentation_generation.md` | Workflow module for generating new documentation. |
| `workflows/modules/documentation_refresh.md` | Workflow module for refreshing and updating existing documentation. |
| `workflows/modules/external_guidance_research.md` | Shared workflow module for consulting authoritative external guidance only when needed. |
| `workflows/modules/feature_design_planning.md` | Workflow module for turning a feature request or PRD into a review-ready technical design for implementation planning. |
| `workflows/modules/foundations_context_review.md` | Shared workflow module for loading repository foundation documents during planning and design work. |
| `workflows/modules/implementation_planning.md` | Workflow module for turning a PRD into an implementation plan. |
| `workflows/modules/internal_context_review.md` | Shared workflow module for identifying the internal standards, templates, workflows, and canonical docs that govern a task. |
| `workflows/modules/prd_generation.md` | Workflow module for planning and generating a PRD. |
| `workflows/modules/reference_distillation.md` | Workflow module for distilling external source material into stable local guidance. |
| `workflows/modules/repository_assessment.md` | Workflow module for assessing repository quality dimensions after inventory work is complete. |
| `workflows/modules/repository_inventory_review.md` | Workflow module for inventorying repository surfaces before deeper repository assessment. |
| `workflows/modules/repository_review.md` | Workflow module for synthesizing repository review findings and remediation guidance. |
| `workflows/modules/task_handoff_review.md` | Shared workflow module for handoff readiness, related-surface impacts, and follow-up recording. |
| `workflows/modules/task_scope_definition.md` | Shared workflow module for defining the objective, boundary, and success conditions of a routed task. |
