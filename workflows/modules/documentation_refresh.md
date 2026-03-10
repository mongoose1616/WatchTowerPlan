# Documentation Refresh Workflow

## Purpose
Use this workflow to review, update, and reconcile existing repository documentation so it stays accurate, current, structurally consistent, and correctly classified.

## Use When
- Documentation has drifted from the current repository structure or behavior.
- A major change has landed in workflows, standards, templates, or project direction and the docs need to be updated to match.
- A repo review has identified stale, inconsistent, incomplete, or duplicated docs.
- A directory or document set needs a maintenance pass before handoff, onboarding, or broader use.

## Inputs
- Scoped documentation-refresh brief
- Current repository contents
- Existing documentation files
- Internal standards and canonical references applied
- External guidance notes when needed
- Current product, design, and reference docs
- Known documentation gaps, issues, or open questions

## Workflow
1. Inventory the current documentation set.
   - List the files in scope.
   - Identify missing README files, stale files, duplicate coverage, and unclear ownership.
   - Flag documents that appear to overlap or compete for the same purpose.
2. Compare docs to current reality.
   - Check that file paths, workflow names, templates, standards, commands, and described behavior still match the repository.
   - Verify that examples, references, and local mappings still point to real and relevant surfaces.
   - Flag outdated assumptions, placeholder content, and broken structure.
3. Check document shape and classification.
   - Confirm that each document uses the right document mode, such as reference, how-to, explanation, standard, or template.
   - Reclassify documents that are mixing incompatible purposes or using the wrong template.
   - Split or simplify documents that are trying to do too much in one file.
4. Refresh the content.
   - Update summaries, purpose statements, paths, tables, examples, and guidance to match the current repository state.
   - Remove stale claims and replace them with current facts.
   - Tighten structure so the document is easier to route to and easier to maintain.
5. Reconcile related surfaces and review maintainability.
   - Update affected templates, standards, README files, references, or companion docs in the same change set when needed.
   - Keep document relationships coherent so refreshed docs do not contradict each other.
   - Remove checklist-style or authoring-only content that belongs in workflows or standards rather than in the document body.

## Data Structure
- Refresh scope
- Documents reviewed
- Current-state findings
- Outdated or inconsistent items
- Updated documents
- Related documents affected
- Quality and structure issues removed
- Open questions

## Outputs
- A refreshed documentation set for the selected scope
- A list of corrected inconsistencies or stale items
- A short record of related docs that were updated together to keep the refreshed scope coherent
- A short record of remaining gaps that still need follow-up work

## Done When
- The documents in scope match the current repository structure and behavior.
- Stale, conflicting, or placeholder content has been removed or corrected.
- The refresh reflects applicable internal standards, canonical references, and existing repository patterns.
- Related docs are no longer contradicting each other within the refreshed scope.
- The refreshed documents are easier to navigate, classify, and maintain.
