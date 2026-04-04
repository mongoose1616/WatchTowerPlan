# Standards Alignment Review Workflow

## Purpose
Use this workflow to audit and remediate standards, references, templates, and governed authoring surfaces so published governance contracts stay current, correctly owned, machine-enforced where practical, and aligned with implementation.

## Use When
- The task is a focused standards, references, or governed-template audit rather than a broad repository review.
- A review or maintenance pass needs to verify whether the repository relies on norms, naming rules, lifecycle rules, validation expectations, or workflow requirements that are not actually documented in the owning governed surface.
- Published standards or references may be stale, contradictory, unimplemented, or missing enforcement paths.
- Missing governed docs should be generated when existing instructions or templates imply they should exist.

## Inputs
- Scoped standards-alignment review request
- In-scope standards, references, templates, and closely related command-doc or workflow-doc surfaces
- Current repository implementation, schemas, registries, validators, and workflow surfaces that the standards claim to govern
- Internal standards, templates, and canonical references applied
- Known governance gaps, stale authority, or enforcement weaknesses already suspected

## Additional Files to Load
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md): defines the broad validation baseline the review must verify against.

## Workflow
1. Build the governed-surface inventory.
   - List the in-scope standards, references, templates, and companion command-doc or workflow-doc surfaces that define repository policy or authoring shape.
   - Identify which surfaces are authoritative governance contracts, which are enforcement mechanisms, and which are merely descriptive.
   - Record any intentionally excluded governance families and remaining blind spots.
2. Check for undocumented norms.
   - Identify naming rules, lifecycle rules, validation expectations, or workflow requirements the repository relies on that are not actually documented in an owning governed surface.
   - When the repository enforces a convention only in code or workflow prose but no standard publishes it, report the missing authority as a distinct finding.
3. Check published authority for staleness and contradiction.
   - Compare each in-scope standard or reference against the current implementation, schemas, registries, validators, command surfaces, and workflow behavior.
   - Distinguish between missing authority, stale authority, weak enforcement, and implementation drift.
   - Cite the exact governing path and implementation evidence for every compliance or drift statement.
4. Check enforcement strength.
   - For each rule that should be machine-enforced, verify whether an enforcing validator, schema, suite, or workflow instruction exists and catches representative violations.
   - If enforcement is prose-only and the rule is machine-enforceable, report the weak enforcement as a distinct finding.
   - If a validator exists but does not catch a representative failure, report the false-green gap.
5. Generate or repair missing governed surfaces.
   - When instructions or templates imply a standard, reference, or template should exist but it does not, create the missing governed doc using the repository's existing template and authority flow.
   - Keep shared reusable standards under `core/docs/` and pack-only standards under the pack docs root.
   - Do not duplicate a reusable standard into pack-local docs just because a pack surfaced the problem first.
6. Synthesize findings and remediation.
   - Record each finding with severity, governance family, ownership target, affected paths, observed evidence, why it matters, recommended remediation, and enforcement-strengthening opportunity.
   - Separate missing authority, stale authority, weak enforcement, implementation drift, and missing governed surfaces into distinct finding classes.
7. Validate the repaired governance posture.
   - Run the repository's doc and standards validation flows.
   - Verify examples, command references, and workflow references against live surfaces.
   - Rebuild indexes or registries that publish standards or reference metadata when those surfaces changed.
   - Add or strengthen validators when a standards gap or stale reference could recur silently.

## Data Structure
- Governed-surface inventory with authority type and enforcement mechanism
- Undocumented-norm findings
- Staleness and contradiction findings by governance family
- Enforcement-strength assessment per rule
- Missing governed-surface register
- Validation and proof results

## Outputs
- A findings-first standards-alignment review with explicit governance gaps, stale authority, weak enforcement, and implementation drift
- Created or repaired governed surfaces when missing authority was identified
- Updated validators, indexes, or companion enforcement surfaces
- Explicit remaining gaps when governance cannot be fully closed in the current pass

## Done When
- All scoped standards, references, and templates are current, owned correctly, and aligned with implementation.
- Missing governed surfaces implied by existing instructions have been created with the correct shape and in the correct owning root.
- Enforcement strength has been assessed and strengthened where practical.
- Related validators, examples, indexes, or command docs are updated where needed.
- Relevant validation passes and the findings report distinguishes observed facts from inferred risks.
