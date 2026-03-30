---
id: "ref.agent_workflow_authoring"
title: "Agent Workflow Authoring Reference"
summary: "Working reference for writing workflow documents that are efficient, explicit, and load only the context an LLM or agent actually needs."
type: "reference"
status: "active"
tags:
  - "reference"
  - "workflows"
  - "agents"
  - "prompt_authoring"
owner: "repository_maintainer"
updated_at: "2026-03-30T04:15:48Z"
audience: "shared"
authority: "reference"
applies_to:
  - "core/docs/standards/documentation/workflow_md_standard.md"
  - "core/docs/standards/workflows/workflow_design_standard.md"
  - "core/docs/standards/workflows/routing_and_context_loading_standard.md"
  - "core/docs/templates/workflow_template.md"
  - "core/workflows/modules/"
  - "core/workflows/roles/"
  - "pack_owned_workflow_modules"
  - "pack_owned_workflow_roles"
aliases:
  - "llm_workflow_authoring"
  - "agent_context_loading"
  - "workflow_prompting"
---

# Agent Workflow Authoring Reference

## Summary
This document provides a working reference for shaping repository workflow documents so they are deterministic for LLM and agent use while preserving every materially distinct execution detail human maintainers need.

## Purpose
Give maintainers a practical set of rules for writing workflow documents that load only the necessary context, make the next files to open explicit, and remove repeated baseline boilerplate only when that boilerplate does not change execution.

## Scope
- Covers workflow-document structure, context-loading hints, instruction density, and authority capture for LLM or agent use.
- Focuses on repo-local workflow authoring rather than general chatbot prompt writing.
- Does not replace the repository standards that define the final workflow file shape.

## Canonical Upstream
- `https://cookbook.openai.com/examples/gpt-5-codex_prompting_guide` - verified 2026-03-10; OpenAI cookbook guidance for coding-agent prompts, instruction structure, and patch-oriented execution.
- `https://cookbook.openai.com/examples/prompt_caching101` - verified 2026-03-10; OpenAI cookbook guidance on keeping reusable prompt content stable and separating static versus dynamic context.
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct` - verified 2026-03-10; Anthropic guidance for clear, explicit instructions.
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags` - verified 2026-03-10; Anthropic guidance for strongly separated prompt sections.
- `https://docs.anthropic.com/en/docs/claude-code/sub-agents` - verified 2026-03-10; Anthropic guidance for narrow, specialized agent responsibilities and reduced context sprawl.

## Related Standards and Sources
- [workflow_md_standard.md](/core/docs/standards/documentation/workflow_md_standard.md)
- [workflow_design_standard.md](/core/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/core/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_template.md](/core/docs/templates/workflow_template.md)

## Quick Reference or Distilled Reference
### Core Rules
- Load only the context that changes execution. Repeating repository-wide baseline instructions in every workflow wastes tokens and hides the files that actually matter next.
- Keep reusable static context separate from task-specific context. Stable routing and instruction layers should stay in `AGENTS.md`, `ROUTING_TABLE.md`, and shared workflow modules instead of being recopied into every leaf workflow document.
- Use clear section boundaries and explicit done conditions. Agents perform better when purpose, trigger, inputs, ordered steps, outputs, and stop conditions are easy to locate.
- Prefer narrow workflow documents with one primary objective. Small specialized modules and roles compose better than broad workflows that mix planning, validation, reconciliation, and closeout into one prompt surface.
- When the file is a workflow role, publish a `Composes Modules` section so the reusable module stack the role directly orchestrates is explicit and queryable.
- Turn authority capture into execution hints. A workflow should name only the extra repo-local files the agent should open next and explain why each file matters.
- Prefer local distilled references over raw vendor URLs. If external guidance matters, point the workflow at a governed local reference doc so execution stays repo-native and queryable.
- Treat `Data Structure` and `Outputs` as internal workflow scaffolding. They should record every materially distinct tracked concept or resulting surface and should not imply extra repository prose when the final artifact already carries the needed information.
- If the requested change itself is the output, say so directly instead of inventing extra records, summaries, or checklists.

### Preferred Workflow-Authoring Decisions
| Question | Preferred Answer | Why |
|---|---|---|
| Where does default context live? | `AGENTS.md`, the authoritative routing tables, and `core/workflows/modules/core.md` | Keeps the baseline stable and avoids repeating it in every workflow document. |
| How should extra context be surfaced? | Optional `Additional Files to Load` bullets | Makes the next files to open explicit without turning every module into a bibliography. |
| What form should each extra-context bullet use? | `source: execution implication` | Tells the reader or agent why the file matters, not just that it exists. |
| What should the extra-context section point to? | Repo-local files, especially standards, templates, command docs, and local references | Keeps execution deterministic and aligned with governed repository surfaces. |
| What link form should those files use? | Repository-native links such as `/core/docs/...`, `/<pack>/docs/...`, `/core/workflows/...`, or `/<pack>/workflows/...` | Keeps the workflow portable across clones, branches, and worktrees instead of binding it to one machine path. |
| What should happen when no extra files are needed? | Omit the section entirely | Avoids filler and false precision while keeping every material extra file explicit when it does exist. |
| How should role docs publish module orchestration? | Required `Composes Modules` section | Makes role-to-module composition explicit and queryable without turning the role into a second routing table. |
| How should `Data Structure` and `Outputs` be written? | As internal workflow scaffolding that is as detailed as needed | Prevents them from turning into prompts for extra low-value artifact prose while still capturing materially distinct workflow state. |

### Anti-Patterns
- Repeating `AGENTS.md`, the authoritative routing tables, `core/workflows/modules/core.md`, or the generic workflow standards in every workflow document.
- Listing files without explaining the local execution consequence of each source.
- Using raw external URLs in workflow documents when a local reference doc can carry the same authority.
- Using filesystem-absolute checkout paths such as `/home/...` in workflow-document links.
- Leaving role-to-module orchestration implicit in workflow-role prose instead of publishing `Composes Modules`.
- Copying the full routed baseline into `Composes Modules` when only a smaller direct role-to-module contract is materially specific to the role.
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
- `pack-owned GitHub task-sync standard`: defines the local-versus-remote authority boundary this workflow must preserve.
- `pack-owned task-lifecycle workflow`: task sync changes local task metadata and must leave the authoritative local corpus aligned afterward.

### What Poor Additional Load Hints Look Like
- `AGENTS.md`: already part of the routing baseline, so repeating it does not tell the agent what extra file to open.
- `workflow_md_standard.md`: generic structure authority, not a task-specific next file for most modules.
- `/home/.../some_checkout/core/docs/...`: machine-local filesystem paths that stop working as soon as the repo is opened from another clone or worktree.
- Bare lists of links with no `: execution implication` explanation.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current workflow standards, workflow documents, semantic workflow validation, and the derived workflow index.

### Current Touchpoints
- [workflow_md_standard.md](/core/docs/standards/documentation/workflow_md_standard.md)
- [workflow_design_standard.md](/core/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/core/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_template.md](/core/docs/templates/workflow_template.md)
- [workflow_index.json](/core/control_plane/indexes/workflows/workflow_index.json)

### Why It Matters Here
- The repository already has a routed baseline context layer. Workflow documents should only add context that is specific to the active module or role and helpful for immediate execution.
- Workflow documents are read by both humans and agents, so the file needs to stay easy to navigate while still naming the next specific files to load and every materially important execution detail.
- The derived workflow index and query surfaces are most useful when the workflow body points to the real repo-local files that materially affect execution instead of generic boilerplate.

## Process or Workflow
1. Define the workflow's single execution concern first.
2. Assume the routing baseline already provides `AGENTS.md`, `core/workflows/ROUTING_TABLE.md`, any active pack-owned `ROUTING_TABLE.md`, and `core/workflows/modules/core.md`.
3. If the file is a workflow role, add `Composes Modules` and list the reusable workflow modules the role directly orchestrates.
4. Add `Additional Files to Load` only when the module or role truly needs extra repo-local files beyond that baseline.
5. Keep each additional-load bullet explicit in `source: execution implication` form and include every extra file that materially changes execution.
6. Prefer citing governed local reference docs when external authority materially affects the workflow.

## Examples
- An initiative-brief-authoring workflow should point to the initiative-package guidance and governing standards because those files directly shape the output.
- A GitHub-task-sync workflow should point to the GitHub sync standard and sync command doc because they change the authority model and operational behavior.
- A generic code-validation workflow should usually omit `Additional Files to Load` if the routed baseline already gives enough context.

## References
- [workflow_md_standard.md](/core/docs/standards/documentation/workflow_md_standard.md)
- [workflow_design_standard.md](/core/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/core/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_template.md](/core/docs/templates/workflow_template.md)
- `https://cookbook.openai.com/examples/gpt-5-codex_prompting_guide`
- `https://cookbook.openai.com/examples/prompt_caching101`
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct`
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags`
- `https://docs.anthropic.com/en/docs/claude-code/sub-agents`

## Tooling and Automation
- `uv run watchtower-core plan sync workflow-index`
- `uv run watchtower-core validate document-semantics --path core/workflows/modules/<module>.md`
- `uv run watchtower-core validate document-semantics --path core/workflows/roles/<role>.md`
- `uv run watchtower-core validate document-semantics --path <pack-root>/workflows/modules/<module>.md`
- `uv run watchtower-core validate document-semantics --path <pack-root>/workflows/roles/<role>.md`
- `uv run watchtower-core query workflows --query <topic>`

## Notes
- This reference is intentionally local and practical. It is about making repository workflow documents work well as agent-facing execution docs, not about covering every general prompt-engineering technique.
- The repository standards remain the authority; this document is the distilled working reference that informs them.

## Updated At
- `2026-03-30T04:15:48Z`
