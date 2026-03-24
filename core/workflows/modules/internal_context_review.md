# Internal Context Review Workflow

## Purpose
Use this workflow to identify the repository-specific standards, templates, workflows, ADRs, and canonical documents that should govern the active task before new local behavior is inferred.

## Use When
- A routed task needs repository-specific standards or canonical references to judge the work correctly.
- The active task could drift into ad hoc local policy if internal guidance is not loaded first.
- A task needs the governing internal documents identified without loading broad low-value context.

## Inputs
- Scoped task brief
- Relevant repository surfaces already identified for the task
- Applicable standards, references, templates, workflows, ADRs, and canonical docs already known or likely relevant

## Additional Files to Load
- [README.md](/core/docs/standards/README.md): identifies the governed standards corpus this workflow is expected to scan selectively instead of broad-loading the repository.

## Workflow
1. Gather the governing internal documents.
   - Identify the repository-specific standards, references, templates, workflows, ADRs, and canonical docs that apply to the active task.
   - Build one minimum governing-document set that distinguishes binding local policy from supporting reference material.
   - Prefer explicit local conventions and current repository patterns over inferred preferences.
2. Reduce the set to the material context.
   - Keep only the internal documents that materially change how the task should be executed or judged.
   - For engineering work, include the narrower engineering standards and supporting references that constrain the touched surfaces rather than stopping at generic repository guidance.
   - When standards depend on governed local reference docs, load those specific reference docs instead of broad-scanning the whole reference corpus.
   - Avoid broad loading that does not affect the active work.
3. Record the governing internal context.
   - Note only the internal documents that should shape the task output or decision.
   - Record why each document matters and whether downstream implementation, validation, or handoff should reference it explicitly.
   - Surface any internal guidance gaps that may require clarification, documentation work, or narrower standards later.

## Data Structure
- Governing standards applied
- Supporting references applied
- Templates and workflows applied
- Canonical repository docs applied
- Required downstream links or references
- Internal guidance gaps or conflicts

## Outputs
- Material internal standards, references, templates, workflows, and canonical docs applied to the task
- Governing-document roles and downstream reference expectations made explicit for later workflows
- Internal guidance gaps only when they affect execution

## Done When
- The active task is grounded in the material internal repository guidance.
- The governing standards, references, and canonical docs are explicit, reviewable, and scoped to the task.
- Missing or conflicting internal guidance has been surfaced rather than silently ignored.
