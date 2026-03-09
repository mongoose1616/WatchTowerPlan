# Reference Distillation Workflow

## Purpose
Use this workflow to extract durable local guidance from external source material and map it cleanly to repository needs.

## Use When
- An external standard, specification, framework guide, vendor document, or best-practice source is being consulted repeatedly and needs a local distilled reference.
- The repository needs a local mapping from external guidance to internal standards, workflows, design choices, or implementation constraints.
- A source-heavy research task needs to be converted into a durable repository reference rather than left as ad hoc notes.
- The primary need is distillation and local mapping; if the requested deliverable is a new repository document, merge this workflow with `documentation_generation.md`.

## Inputs
- Scoped distillation brief
- External source material with canonical upstream links
- Distillation goal or target question
- Relevant repository context and neighboring docs
- Internal standards and canonical references applied
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md)
- Related local references, standards, or design documents
- External guidance notes when needed
- Version, baseline, or date-sensitivity information when relevant
- Open questions or uncertainties in the source material

## Workflow
1. Read and verify the source material directly.
   - Review the canonical upstream sources rather than relying on secondhand summaries when possible.
   - Confirm which source version, date, or baseline is being distilled.
   - Separate authoritative statements from interpretation, commentary, and uncertainty.
2. Extract the durable local guidance.
   - Distill the source material into concise rules, mappings, decision points, or lookup content relevant to this repository.
   - Answer the recurring practical questions directly in the distillation rather than forcing later readers to reopen the upstream source for every common case.
   - Capture defaults, required or disallowed patterns, decision boundaries, edge cases, and failure modes when those details materially affect safe or correct local use.
   - Preserve the meaning of the source without copying long passages into the local artifact.
   - Keep the output focused on durable guidance rather than transient research notes.
3. Map the guidance to repository context.
   - Explain how the distilled guidance applies to local standards, workflows, architecture, tooling, or implementation patterns.
   - Identify where local policy differs from or narrows the upstream source.
   - Call out version-sensitive or environment-sensitive constraints explicitly.
4. Choose the repository output shape.
   - Decide whether the result should become a local reference, a standards update, supporting design input, or a companion document set.
   - Keep normative policy in `docs/standards/**` and supporting lookup material in `docs/references/**` when documentation changes are required.
   - If the requested deliverable is a new repository document, add `documentation_generation.md` rather than treating distillation notes as the final document implicitly.
   - Split the output if multiple unrelated references would otherwise be forced into one file.
5. Review for accuracy and maintainability.
   - Check that source attribution is clear, local mappings are accurate, and unsupported interpretation is avoided.
   - Reject output that mostly acts as a link list instead of a reusable distilled reference.
   - For ambiguous or high-risk topics, confirm that unresolved ambiguity and local interpretation boundaries are explicit.
   - Confirm the distilled output is concise enough to be maintained and specific enough to be reused.

## Data Structure
- Distillation goal
- Source scope boundary
- Canonical upstream sources
- Distilled rules or guidance
- Local mappings
- Version or baseline notes
- Target repository artifact or follow-up destination
- Open questions

## Outputs
- A distilled local reference package or clear distillation notes ready for documentation generation
- A short record of the canonical upstream sources and version-sensitive notes used during distillation
- A local mapping from source guidance to repository context
- A list of version-sensitive notes, gaps, and follow-up work

## Done When
- The external source material has been distilled into durable repository-relevant guidance.
- Applicable internal standards, canonical references, and repository patterns have shaped the output.
- The local mapping is specific enough that future work does not need to re-derive the same interpretation.
- Documentation generation has been added or explicitly deferred when the requested output is a new repository document.
- The output is ready to support a reference, standard, design, or implementation artifact without carrying raw research sprawl.
