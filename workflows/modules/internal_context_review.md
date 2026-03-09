# Internal Context Review Workflow

## Purpose
Use this workflow to identify the repository-specific standards, templates, workflows, ADRs, and canonical documents that should govern the active task before new local behavior is inferred.

## Use When
- A routed task needs repository-specific standards or canonical references to judge the work correctly.
- The active task could drift into ad hoc local policy if internal guidance is not loaded first.
- A task should produce a short record of the internal documents that materially governed the work.

## Inputs
- Scoped task brief
- Relevant repository surfaces already identified for the task
- Applicable standards, templates, workflows, ADRs, and canonical docs already known or likely relevant

## Workflow
1. Gather the governing internal documents.
   - Identify the repository-specific standards, templates, workflows, ADRs, and canonical docs that apply to the active task.
   - Prefer explicit local conventions and current repository patterns over inferred preferences.
2. Reduce the set to the material context.
   - Keep only the internal documents that materially change how the task should be executed or judged.
   - Avoid broad loading that does not affect the active work.
3. Record the governing internal context.
   - Note which internal documents should shape the task output or decision.
   - Surface any internal guidance gaps that may require clarification, documentation work, or narrower standards later.

## Data Structure
- Internal standards applied
- Templates and workflows applied
- Canonical repository references applied
- Internal guidance gaps or conflicts

## Outputs
- A short record of the internal standards, workflows, templates, and canonical references that govern the task
- A clear internal-context package for downstream task modules

## Done When
- The active task is grounded in the material internal repository guidance.
- Internal references that govern the task are explicit and reviewable.
- Missing or conflicting internal guidance has been surfaced rather than silently ignored.
