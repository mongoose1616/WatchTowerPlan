# Repository Assessment Workflow

## Purpose
Use this workflow to assess an inventoried repository for coherence, authority alignment, freshness, maintainability, validation coverage, operational risk, and developer experience.

## Use When
- A repository review has already established the current inventory and now needs quality assessment.
- The active review should evaluate the repository across multiple quality dimensions rather than only one narrow concern.
- A reviewer needs a structured assessment before findings are prioritized and summarized.

## Inputs
- Scoped repository-review brief
- Repository inventory and coverage map
- Current repository docs, code, tooling, configs, and control-plane artifacts
- Internal standards and canonical references applied
- External guidance notes when needed

## Workflow
1. Assess architecture, scope, and authority boundaries.
   - Review whether foundations, standards, docs, workflows, code, and machine-readable artifacts describe the same current repository boundary.
   - Flag source-of-truth ambiguity, boundary leakage, accidental duplication, or scope drift.
2. Assess documentation, workflow, and governed-artifact coherence.
   - Check README files, standards, commands, workflows, templates, indexes, registries, schemas, examples, and planning or control-plane joins for freshness and discoverability.
   - Note stale guidance, missing operationalization, broken lookup paths, or mismatches between human and machine surfaces.
3. Assess implementation and validation posture.
   - Evaluate code quality, hotspots, coupling, error handling, compatibility boundaries, test coverage, validators, sync paths, query paths, and release-risk controls where they exist.
   - Note where validation expectations are missing, weak, or not enforced.
4. Assess security, operational readiness, and contributor experience.
   - Check secret handling, auth boundaries, dependency risk, unsafe defaults, rollout or incident-readiness signals, diagnostics, and local setup ergonomics.
   - Record friction that makes common contributor tasks harder than they should be.
5. Separate actionable issues from intentional explicitness and unknowns.
   - Record where redundancy or verbosity is required by governance, traceability, or paired authority rather than being accidental sprawl.
   - Capture evidence gaps or areas that still need deeper validation before a strong claim is made.

## Data Structure
- Architecture, scope, and authority assessment
- Documentation, workflow, and governed-artifact assessment
- Implementation and validation assessment
- Security and operational readiness assessment
- Developer experience assessment
- Intentional explicitness versus actionable drift

## Outputs
- A structured repository assessment across the main review dimensions
- A short record of confirmed risks, suspected drift, weak controls, and evidence gaps found during assessment

## Done When
- The repository has been assessed across the key review dimensions rather than only one slice.
- Risks, drift, weak controls, and intentional explicitness are visible before findings are prioritized.
- The review is ready for findings synthesis and remediation planning.
