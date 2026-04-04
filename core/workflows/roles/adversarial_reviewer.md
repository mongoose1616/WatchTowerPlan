# Adversarial Reviewer Role

## Purpose
Use this role to apply a contradiction-oriented, false-green-resistant review lens so repository audits challenge claimed protections, prove adjacent boundaries, and surface issues that a proportional default review might leave untested.

## Use When
- The request explicitly asks for an adversarial review, full-spectrum audit, contradiction-oriented audit, or false-green challenge pass.
- A repository review needs stronger proof than normal green-path inspection because hidden drift, validator weakness, portability risk, or staged-artifact leakage are part of the concern.
- The task should preserve a clear distinction between standard repository review behavior and a higher-cost adversarial audit posture.

## Inputs
- Scoped adversarial review request
- In-scope repository surfaces, review boundaries, and governing standards
- Current runtime, validator, documentation, route, command, and machine-readable surfaces that make claims worth challenging

## Composes Modules
- [repository_inventory_review.md](../modules/repository_inventory_review.md): builds the review coverage map and hotspot inventory that the adversarial pass must challenge instead of sampling blindly.
- [repository_assessment.md](../modules/repository_assessment.md): evaluates architecture, workflow, validation, governance, and contributor-surface contradictions before findings are synthesized.
- [code_validation.md](../modules/code_validation.md): executes challenge tests, mutation-style checks, and other proof paths needed when claimed protections must fail closed.
- [repository_review.md](../modules/repository_review.md): turns the adversarial evidence set into a findings-first report with explicit residual risk and proof boundaries.

## Workflow
1. Raise the proof bar before accepting any green signal.
   - Treat passing tests, validators, sync commands, or apparently coherent docs as evidence, not as conclusion.
   - Build a contradiction map that names the claims worth challenging across runtime behavior, command docs, indexes, validators, staged artifacts, and export or bootstrap boundaries.
2. Probe high-risk boundaries directly.
   - Re-check important claims from more than one angle, including human-readable docs, machine-readable authority, live command behavior, validator coverage, and representative workflows.
   - Prefer the narrowest disposable challenge that can prove whether a claimed protection actually fails closed.
3. Run adversarial proof techniques where they matter.
   - Use mutation-style or fault-injection checks when validators, indexes, schemas, or command surfaces claim to guard against representative failures.
   - Use staged-artifact, bootstrap, or portability simulations when the task scope includes export-safe or pack-boundary claims.
   - Keep the disposable challenge bounded to the review task; do not turn the role into a blanket destructive test harness.
4. Keep findings first and residual uncertainty explicit.
   - Record severity, affected surfaces, governing sources, observed evidence, why the contradiction matters, and the recommended repair or proof gap for each finding.
   - Separate confirmed defects, false-green validator gaps, downgraded candidate issues, and still-unverified boundaries instead of flattening them into one risk list.
5. Stop only at a real review boundary.
   - Continue until contradiction-oriented checks stop producing new actionable findings or a clearly stated verification boundary is reached.
   - If the residual limit is tooling, environment, or scope rather than repository health, say that directly.

## Data Structure
- Contradiction map covering the claimed protections and boundaries under challenge
- Adversarial findings register with confirmed defects, false-green gaps, downgraded candidates, and unverified boundaries
- Proof matrix tying each major claim to the checks, simulations, or challenge tests that were used

## Outputs
- A findings-first adversarial repository review with stronger-than-default proof expectations
- Explicit evidence for false-green gaps, contradicted claims, or cleared high-risk boundaries
- A clear residual-risk statement when the review stops at an environment or verification boundary rather than a clean result

## Done When
- The repository review has been challenged from enough angles that green-path claims are not being accepted on trust alone.
- The findings report distinguishes confirmed contradictions, false-green protections, cleared boundaries, and still-unverified areas explicitly.
- The next contributor can tell why the audit was adversarial, what it proved, and what remains open without replaying the full challenge pass.
