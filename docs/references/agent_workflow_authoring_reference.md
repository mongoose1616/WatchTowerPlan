---
id: "ref.agent_workflow_authoring"
title: "Agent Workflow Authoring Reference"
summary: "Working reference for writing workflow modules that are efficient, explicit, and load only the context an LLM or agent actually needs."
type: "reference"
status: "active"
tags:
  - "reference"
  - "workflows"
  - "agents"
  - "prompt_authoring"
owner: "repository_maintainer"
updated_at: "2026-03-12T02:46:38Z"
audience: "shared"
authority: "reference"
applies_to:
  - "docs/standards/documentation/workflow_md_standard.md"
  - "docs/standards/workflows/workflow_design_standard.md"
  - "docs/standards/workflows/routing_and_context_loading_standard.md"
  - "docs/templates/workflow_template.md"
  - "workflows/modules/"
aliases:
  - "llm_workflow_authoring"
  - "agent_context_loading"
  - "workflow_prompting"
---

# Agent Workflow Authoring Reference

## Summary
This document provides a working reference for shaping repository workflow modules so they are efficient for LLM and agent use without losing clarity for human maintainers.

## Purpose
Give maintainers a compact set of practical rules for writing workflow modules that load only the necessary context, make the next files to open explicit, and avoid token-heavy boilerplate.

## Scope
- Covers workflow-module structure, context-loading hints, instruction density, and authority capture for LLM or agent use.
- Focuses on repo-local workflow authoring rather than general chatbot prompt writing.
- Does not replace the repository standards that define the final workflow file shape.

## Canonical Upstream
- `https://cookbook.openai.com/examples/gpt-5-codex_prompting_guide` - verified 2026-03-10; OpenAI cookbook guidance for coding-agent prompts, instruction structure, and patch-oriented execution.
- `https://cookbook.openai.com/examples/prompt_caching101` - verified 2026-03-10; OpenAI cookbook guidance on keeping reusable prompt content stable and separating static versus dynamic context.
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct` - verified 2026-03-10; Anthropic guidance for clear, explicit instructions.
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags` - verified 2026-03-10; Anthropic guidance for strongly separated prompt sections.
- `https://docs.anthropic.com/en/docs/claude-code/sub-agents` - verified 2026-03-10; Anthropic guidance for narrow, specialized agent responsibilities and reduced context sprawl.

## Related Standards and Sources
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md)
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)

## Quick Reference or Distilled Reference
### Core Rules
- Load only the context that changes execution. Repeating repository-wide baseline instructions in every workflow wastes tokens and hides the files that actually matter next.
- Keep reusable static context separate from task-specific context. Stable routing and instruction layers should stay in `AGENTS.md`, `ROUTING_TABLE.md`, and shared workflow modules instead of being recopied into every leaf workflow.
- Use clear section boundaries and explicit done conditions. Agents perform better when purpose, trigger, inputs, ordered steps, outputs, and stop conditions are easy to locate.
- Prefer narrow workflow modules with one primary objective. Small specialized modules compose better than broad workflows that mix planning, validation, reconciliation, and closeout into one prompt surface.
- Turn authority capture into execution hints. A workflow should name only the extra repo-local files the agent should open next and explain why each file matters.
- Prefer local distilled references over raw vendor URLs. If external guidance matters, point the workflow at a governed local reference doc so execution stays repo-native and queryable.
- Treat `Data Structure` and `Outputs` as internal workflow scaffolding. They should stay terse and should not imply extra repository prose when the final artifact already carries the needed information.
- If the requested change itself is the output, say so directly instead of inventing extra records, summaries, or checklists.

### Preferred Workflow-Authoring Decisions
| Question | Preferred Answer | Why |
|---|---|---|
| Where does default context live? | `AGENTS.md`, `ROUTING_TABLE.md`, and `workflows/modules/core.md` | Keeps the baseline stable and avoids repeating it in every workflow module. |
| How should extra context be surfaced? | Optional `Additional Files to Load` bullets | Makes the next files to open explicit without turning every module into a bibliography. |
| What form should each extra-context bullet use? | `source: execution implication` | Tells the reader or agent why the file matters, not just that it exists. |
| What should the extra-context section point to? | Repo-local files, especially standards, templates, command docs, and local references | Keeps execution deterministic and aligned with governed repository surfaces. |
| What should happen when no extra files are needed? | Omit the section entirely | Avoids token-heavy filler and false precision. |
| How should `Data Structure` and `Outputs` be written? | As terse internal workflow scaffolding | Prevents them from turning into prompts for extra low-value artifact prose. |

### Anti-Patterns
- Repeating `AGENTS.md`, `workflows/ROUTING_TABLE.md`, `workflows/modules/core.md`, or the generic workflow standards in every workflow module.
- Listing files without explaining the local execution consequence of each source.
- Using raw external URLs in workflow modules when a local reference doc can carry the same authority.
- Mixing multiple execution concerns into one workflow because the task family is broad.
- Writing long descriptive prose that leaves the actual ordered steps implicit.
- Using `Outputs` to require meta summaries, source logs, or quality-check writeups when the resulting artifact or command outcome already captures that information.

### Reconciliation Boundary Rule
- Pick reconciliation routes by the primary authority conflict, not by the total number of touched files.
- Use documentation-implementation reconciliation for behavior claims.
- Use traceability reconciliation for traced planning links and tracker or index agreement.
- Use governed-artifact reconciliation for schema-backed family coherence.
- Use acceptance-evidence reconciliation for one trace's acceptance coverage and evidence linkage.

### What Good Additional Load Hints Look Like
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): defines the local-versus-remote authority boundary this workflow must preserve.
- [task_lifecycle_management.md](/home/j/WatchTowerPlan/workflows/modules/task_lifecycle_management.md): task sync changes local task metadata and must leave the authoritative local corpus aligned afterward.

### What Poor Additional Load Hints Look Like
- `AGENTS.md`: already part of the routing baseline, so repeating it does not tell the agent what extra file to open.
- `workflow_md_standard.md`: generic structure authority, not a task-specific next file for most modules.
- Bare lists of links with no `: execution implication` explanation.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current workflow standards, workflow modules, semantic workflow validation, and the derived workflow index.

### Current Touchpoints
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md)
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)
- [workflow_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/workflows/workflow_index.v1.json)

### Why It Matters Here
- The repository already has a routed baseline context layer. Workflow modules should only add context that is specific to the module and helpful for immediate execution.
- Workflow modules are read by both humans and agents, so the file needs to stay short enough to scan while still naming the next specific files to load when that matters.
- The derived workflow index and query surfaces are most useful when the workflow body points to a small set of real repo-local files instead of generic boilerplate.

## Process or Workflow
1. Define the workflow's single execution concern first.
2. Assume the routing baseline already provides `AGENTS.md`, `ROUTING_TABLE.md`, and `workflows/modules/core.md`.
3. Add `Additional Files to Load` only when the module truly needs extra repo-local files beyond that baseline.
4. Keep each additional-load bullet short and explicit in `source: execution implication` form.
5. Prefer citing governed local reference docs when external authority materially affects the workflow.

## Examples
- A PRD-generation workflow should point to the PRD standard and template because those files directly shape the output.
- A GitHub-task-sync workflow should point to the GitHub sync standard and sync command doc because they change the authority model and operational behavior.
- A generic code-validation workflow should usually omit `Additional Files to Load` if the routed baseline already gives enough context.

## References
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md)
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)
- `https://cookbook.openai.com/examples/gpt-5-codex_prompting_guide`
- `https://cookbook.openai.com/examples/prompt_caching101`
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct`
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags`
- `https://docs.anthropic.com/en/docs/claude-code/sub-agents`

## Tooling and Automation
- `uv run watchtower-core sync workflow-index`
- `uv run watchtower-core validate document-semantics --path workflows/modules/<module>.md`
- `uv run watchtower-core query workflows --query <topic>`

## Notes
- This reference is intentionally local and practical. It is about making repository workflow modules work well as agent-facing execution docs, not about covering every general prompt-engineering technique.
- The repository standards remain the authority; this document is the distilled working reference that informs them.

## Updated At
- `2026-03-12T02:46:38Z`
