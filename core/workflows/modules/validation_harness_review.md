# Validation Harness Review Workflow

## Purpose
Use this workflow to audit and harden validators, validation suites, tests, regression harnesses, and coverage gaps so claimed protections fail closed and false-green behavior is detected and eliminated.

## Use When
- The task is a focused validation, harness, or test-coverage audit rather than a broad repository review or code-quality pass.
- A review or maintenance pass needs to verify whether current validation actually catches representative failures in docs, schemas, registries, workflow wiring, runtime behavior, naming rules, portability, and core/pack boundaries.
- Validator weakness, false-positive green states, or coverage blind spots are suspected.
- New or strengthened harnesses are needed to close gaps found during review or remediation.

## Inputs
- Scoped validation-harness review request
- In-scope validators, validation suites, tests, fixtures, and harness surfaces
- Current validator registries, validation-suite registries, and test documentation
- Governing standards, schemas, and contracts the validators claim to enforce
- Known coverage gaps, false-green symptoms, or validation weaknesses already suspected

## Additional Files to Load
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md): defines the broad validation baseline and suite expectations this review must verify.

## Workflow
1. Build the validation coverage map.
   - Inventory the in-scope validators, validation suites, tests, fixtures, and mutation checks.
   - Map each validator or suite to the standard, schema, contract, or behavioral claim it is supposed to enforce.
   - Record which failure modes are covered, which are untested, and which are explicitly out of scope.
2. Assess fail-closed behavior.
   - For each high-risk validator or gate, verify whether it fails closed when confronted with representative defects.
   - Prefer explicit negative tests and fail-closed validation over optimistic green-path checks.
   - Check whether validators produce false-green results by accepting inputs that should be rejected.
3. Perform representative challenge tests.
   - In disposable copies or isolated test fixtures, introduce representative defects and verify whether the claimed validation surfaces reject them.
   - Examples: schema or registry drift, broken command docs, missing registry entries, undeclared runtime targets, broken links, stale manifest wiring, naming drift that should be rejected, or pack/core boundary leakage.
   - If a validator misses a representative failure, report the false-green gap as a distinct finding with the specific defect that escaped.
4. Perform mutation-style checks where practical.
   - Intentionally create small but representative faults and test whether the relevant validator catches them.
   - Focus mutation checks on validators that guard high-risk boundaries: schemas, registries, export/bootstrap flows, portability checks, and naming enforcement.
   - Record which mutations were caught and which escaped.
5. Assess coverage depth and harness durability.
   - Distinguish failures already caught, failures escaping current validation, and failures requiring new harnesses.
   - Check whether test fixtures are durable and representative or fragile and overfit to current implementation details.
   - Verify that coverage is not concentrated on easy-to-test low-risk paths while high-risk boundaries remain undertested.
6. Strengthen or add harnesses where needed.
   - Add the narrowest durable harness needed when current coverage is insufficient.
   - Strengthen companion docs, standards, or workflow guidance when the validation gap exists because the repository never published the rule clearly.
   - Keep shared reusable validators in `core/` and pack-only validators under the pack root.
   - Do not patch a pack-local harness to compensate for a missing reusable-core validator when the failure mode is actually shared.
7. Validate the strengthened harness posture.
   - Re-run repo-native validation suites, schema checks, docs checks, portability checks, and test commands relevant to the touched surfaces.
   - Re-run the strengthened harness against the representative faults from earlier challenge tests to prove the false-green gap is closed.
   - Collect coverage or comparative proof where meaningful.

## Data Structure
- Validation coverage map with validator-to-claim traceability
- Fail-closed assessment results per high-risk validator
- Challenge-test register with representative defects introduced and validation outcomes
- Mutation-check register with faults created and catch/escape results
- Coverage-depth assessment distinguishing caught, escaped, and new-harness-required failures
- Strengthened or added harness register

## Outputs
- A findings-first validation-harness review with explicit false-green gaps, coverage blind spots, and enforcement weaknesses
- Strengthened or added validators, tests, or fixtures with proving challenge-test evidence
- An explicit residual-risk statement for coverage gaps that could not be closed in the current pass
- Updated companion docs, standards, or workflow guidance when validation gaps stemmed from unpublished rules

## Done When
- The scoped validation surfaces catch the representative failures they claim to protect against, or the remaining gap is named explicitly.
- False-green behavior has been tested for and either eliminated or documented.
- New or strengthened harnesses are durable, owned correctly, and documented where needed.
- Challenge tests and mutation checks have been performed for high-risk validators and the results are recorded.
- Relevant validation passes and the completed review distinguishes confirmed coverage from still-unverified areas.
