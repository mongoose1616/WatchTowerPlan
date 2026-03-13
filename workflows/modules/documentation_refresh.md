# Documentation Refresh Workflow

## Purpose
Use this workflow to refresh and reconcile existing repository documentation or standards after the active scope and drift findings are known.

## Use When
- Documentation has drifted from the current repository structure or behavior.
- A documentation review or another workflow has already identified docs or standards that need same-change updates.
- A major change has landed in workflows, standards, templates, or project direction and the docs need to be updated to match.
- A repo review has identified stale, inconsistent, incomplete, or duplicated docs.
- A directory or document set needs a maintenance pass before handoff, onboarding, or broader use.

## Inputs
- Scoped documentation-refresh brief or documentation-review findings
- Current repository contents and behavior
- Existing documentation or standards files in scope
- Internal standards and canonical references applied
- External guidance notes when needed
- Current product, design, reference, command, template, and lookup surfaces when they affect the scope
- Known documentation gaps, issues, or open questions

## Workflow
1. Build the documentation coverage map.
   - List the files in scope and the companion templates, examples, command pages, references, indexes, validators, or query and sync surfaces that operationalize them.
   - Keep the inventory proportional to the change instead of narrating every unaffected file, and note any intentionally excluded surfaces.
2. Compare docs or standards to current reality and governing family rules.
   - Check that file paths, workflow names, templates, standards, commands, examples, and described behavior still match the repository.
   - Confirm that each document uses the right document mode, required sections, and family template or standard, and flag stale assumptions, placeholder content, or broken structure.
3. Review operationalization and companion surfaces.
   - For standards, check the templates, examples, validators, loaders, indexes, registries, and query or sync surfaces that are supposed to enforce or expose the standard.
   - For general docs, check related READMEs, command pages, references, and machine-readable lookup surfaces for discoverability and drift.
   - If the main issue is implementation-versus-documentation drift or governed-artifact drift, add the dedicated reconciliation workflow instead of handling it only implicitly here.
4. Refresh and reconcile the content.
   - Update summaries, purpose statements, paths, tables, examples, and guidance to match the current repository state.
   - Remove stale claims, split mixed-purpose docs when needed, and keep same-change companion surfaces aligned when the authoritative document changes materially.
   - Remove checklist-style or authoring-only content that belongs in workflows or standards rather than in the document body.
5. Run a post-refresh review pass.
   - Re-check the touched documents and their direct companion surfaces from a fresh angle for stale examples, broken structure, lookup mismatches, or still-missing operationalization.
   - If the active task is a same-scope review loop and a new actionable issue appears, record it and repeat the refresh.

## Data Structure
- Refresh scope and coverage map
- Documents or standards reviewed
- Current-state and governance findings
- Operationalization and companion-surface gaps
- Updated documents and related surfaces affected
- Remaining follow-up only when unresolved

## Outputs
- A refreshed documentation or standards set for the selected scope
- Related doc, template, command, or lookup-surface updates needed to keep the refreshed scope coherent
- Explicit remaining gaps only when follow-up is still needed

## Done When
- The documents or standards in scope match the current repository structure, behavior, and governing family rules.
- Stale, conflicting, or placeholder content has been removed or corrected.
- The refresh reflects applicable internal standards, canonical references, existing repository patterns, and any required operationalization surfaces.
- Related docs and companion lookup or enforcement surfaces are no longer contradicting each other within the refreshed scope.
- The refreshed documents are easier to navigate, classify, and maintain.
- Low-value boilerplate or placeholder content has been removed from the refreshed scope.
- A post-refresh review pass has finished and any remaining blind spots are explicit.
