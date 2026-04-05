# Adversarial Reviewer Role

## Purpose
Use this role to apply a contradiction-oriented, false-green-resistant review and remediation lens so audits, benchmark passes, refactors, and findings-fix loops challenge claimed protections instead of accepting the green path on trust.

## Use When
- The request explicitly asks for an adversarial review, full-spectrum audit, contradiction-oriented audit, or false-green challenge pass.
- The active route is a review, validation, optimization, implementation, or findings-remediation task that should keep an adversarial lens instead of silently downgrading to the default posture.
- A repository review, workflow review, benchmark pass, refactor, or fix loop needs stronger proof than normal green-path inspection because hidden drift, validator weakness, portability risk, or staged-artifact leakage are part of the concern.
- The task should preserve a clear distinction between standard review or remediation behavior and a higher-cost adversarial posture.

## Inputs
- Scoped adversarial review request
- In-scope repository surfaces, review or remediation boundaries, and governing standards
- Current runtime, validator, documentation, route, command, and machine-readable surfaces that make claims worth challenging
- The starting review or fix prompt, or an equivalent rerun-safe prompt record when the adversarial pass may seed a later remediation loop

## Composes Modules
- [adversarial_lens.md](../modules/adversarial_lens.md): applies the contradiction-oriented overlay to the active review, validation, implementation, optimization, or remediation route without hardwiring the role to one base task permutation.
- [code_validation.md](../modules/code_validation.md): executes challenge tests, mutation-style checks, and other proof paths needed when claimed protections must fail closed.

## Adversarial Lenses
Apply these lenses systematically rather than sampling opportunistically:
- Missing capability and broken or misleading CLI surfaces
- Standards drift and standard noncompliance
- Missing standards or references that should exist under current instructions
- Spec-to-implementation mismatch
- Validation weakness and false-positive green states
- Workflow system gaps
- Pack integration and boundary violations
- Runtime, package, export, and bootstrap gaps
- Documentation and command-doc drift
- Coverage blind spots and readiness blockers
- Human-render versus machine-authority disagreement
- Code quality defects, maintainability debt, and abstraction debt
- Error handling and recovery gaps
- Duplication, dead code, and brittle logic
- Boundary and ownership violations between shared core and the hosted pack
- Naming convention drift across docs, schemas, commands, runtime code, and tests
- Portability and release-sanitization failures
- Bootstrap safety gaps
- Fail-open or fail-weak validator behavior
- Staged artifact contamination
- Hidden dependency on donor-specific pack sets or donor-local environments
- Performance regressions and unnecessary heavy paths

## Workflow
1. Raise the proof bar before accepting any green signal.
   - Treat passing tests, validators, sync commands, or apparently coherent docs as evidence, not as conclusion.
   - Do not accept "tests pass", "lint passes", or "type checks pass" as sufficient evidence of correctness, code quality, performance safety, or standards adherence.
   - Do not treat one passing proof path or one green validation suite as sufficient while adjacent contradiction-prone surfaces remain unchecked.
   - Build a contradiction map that names the claims worth challenging across runtime behavior, command docs, indexes, validators, staged artifacts, export or bootstrap boundaries, and the active review or remediation family.
2. Probe high-risk boundaries directly.
   - Re-check important claims from more than one angle, including human-readable docs, machine-readable authority, live command behavior, validator coverage, and representative workflows or fix paths.
   - Probe contradiction-prone boundaries: runtime discovery versus registry authority, docs versus live CLI/help, workflow docs versus actual route/command behavior, pack contract declarations versus executable handlers, standards claims versus current implementation, and target repo core versus canonical shared core.
   - Prefer the narrowest disposable challenge that can prove whether a claimed protection actually fails closed.
3. Run adversarial proof techniques where they matter.
   - Perform validator challenge tests: in disposable copies, introduce representative defects such as schema/registry drift, broken command docs, missing registry entries, undeclared runtime targets, stale manifest wiring, naming drift, or pack/core boundary leakage and verify the claimed validation surfaces fail closed.
   - Perform mutation-style checks: intentionally create small but representative faults and test whether the relevant validator catches them. If a validator misses a representative failure, report that as a distinct false-green finding.
   - Execute documented command examples where practical, not just parser-level validation. Run them far enough to verify operability or identify the exact execution boundary.
   - Build staged release/bootstrap artifacts or curated disposable copies and diff them against the source repository and governing portability expectations. Check for leaked tests, caches, virtualenvs, donor-specific paths, retained runtime residue, and other non-portable content.
   - Run copied-repo or staged-repo simulations for more than one compatibility scenario when hosted-pack portability or bootstrap behavior is in scope.
   - When a broad validation, remediation, or bootstrap command claims to make the repo safe or operable, test post-command reality, not just the command's exit code.
   - Keep the disposable challenge bounded to the review task; do not turn the role into a blanket destructive test harness.
4. Keep findings first and residual uncertainty explicit.
   - Produce an uncapped findings inventory. If there are 3 findings, report 3. If there are 30, report 30.
   - Split materially distinct issues into separate findings when paths, impact, remediation, ownership target, or violated standard differ.
   - Record severity, finding class, ownership target (`baseline_core`, `repo_core_drift`, `pack_owned`, or `cross_boundary`), affected surfaces, governing sources, observed evidence, why the contradiction matters, recommended remediation, and likely remediation slice for each finding.
   - When the review runs outside `WatchTowerCore` and a finding would require a shared `core/` edit, mark the ownership target as upstream `WatchTowerCore/core` plus downstream `shared_core_refresh.md` follow-through instead of presenting recipient-local `core/` patching as the primary remediation path.
   - Separate confirmed defects, false-green validator gaps, downgraded candidate issues, and still-unverified boundaries instead of flattening them into one risk list.
   - Preserve the starting or original review or fix prompt, or the narrowest prompt-equivalent that produced the current findings set, so a later review-remediation loop can rerun the same ask instead of substituting a looser summary.
5. Stop only at a real review boundary.
   - Continue until contradiction-oriented checks stop producing new actionable findings or a clearly stated verification boundary is reached.
   - Do not stop merely because you already found a critical issue.
   - Do not stop merely because the current live repo is green; continue until staged-failure, portability, bootstrap, doc/example, naming, interoperability, and adjacent contradiction checks stop producing new actionable findings.
   - If the residual limit is tooling, environment, or scope rather than repository health, say that directly.

## Data Structure
- Contradiction map covering the claimed protections and boundaries under challenge
- Starting or original review prompt record suitable for rerun in a remediation loop
- Adversarial findings register with confirmed defects, false-green gaps, downgraded candidates, and unverified boundaries
- Proof matrix tying each major claim to the checks, simulations, or challenge tests that were used
- Challenge-test and mutation-check register with representative defects introduced and outcomes observed
- Staged-artifact and portability simulation results when export or bootstrap boundaries are in scope
- Role-overlay decision record when the adversarial lens is paired with another review, benchmark, implementation, or remediation route

## Outputs
- A findings-first adversarial review or remediation result with stronger-than-default proof expectations
- Explicit evidence for false-green gaps, contradicted claims, or cleared high-risk boundaries
- A stable rerun-ready review prompt or explicit prompt-recovery limitation for downstream review-remediation loops
- A clear residual-risk statement when the review stops at an environment or verification boundary rather than a clean result
- After findings: executive summary, shared-core versus pack-boundary summary, standards-and-references summary, code-quality and naming summary, validation/harness summary, performance/refactor summary, coverage summary, commands/checks executed, workflow simulations performed, mutation/fault-injection experiments performed, staged-artifact simulations performed, confirming evidence, cleared or downgraded candidates, proposed remediation slices, and residual risks

## Done When
- The active review, validation, implementation, or remediation route has been challenged from enough angles that green-path claims are not being accepted on trust alone.
- The findings report distinguishes confirmed contradictions, false-green protections, cleared boundaries, and still-unverified areas explicitly.
- The next contributor can tell why the pass was adversarial, what it proved, what prompt should be rerun in a later fix loop, and what remains open without replaying the full challenge pass.
