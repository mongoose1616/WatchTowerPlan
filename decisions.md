# Capture-First Plan Workspace Decisions

This file records the locked decisions gathered during the requirements clarification pass for [requirements.md](requirements.md).

## Context
- Source requirements: `requirements.md`
- Purpose: backup copy of the locked planning decisions for the capture-first plan workspace initiative
- Recorded at: `2026-03-16 America/New_York`

## Locked Decisions
1. `Q1=2` `forward-only full initiative packages`
   Every new initiative going forward must be fully captured.
2. `Q2=10` `maximum upfront capture`
   Require the full package before implementation starts.
3. `Q3=4` `machine-first with authored intake docs`
   Machine state is authoritative after bootstrap; authored intake docs remain inputs.
4. `Q4=10` `everything materially connected`
   Capture every materially related item up front.
5. `Q5=10` `strict no-start gate`
   No implementation starts until the full package is captured, validated, reviewed, approved, and execution-ready.
6. `Q6=7` `any one authorized maintainer`
   Readiness approval can be given by any authorized maintainer.
7. `Q7=6` `human default, agent exception`
   Humans approve by default; agents only when explicitly delegated.
8. `Q8=1` `simple owner note`
   Agent delegation uses a simple owner note.
9. `Q9=9` `policy-assisted manual choice`
   Pack-wide versus project-scoped classification is manual with policy guidance.
10. `Q10=1` `freeze and replace`
    Freeze `docs/planning/**` immediately and cut over to the new model.
11. `Q11=6` `dual required with same stem`
    Require both `initiative_id` and `trace_id`, derived from one canonical stem.
12. `Q12=8` `author inside initiative root, promote later`
    Authored intake docs live inside each initiative root.
13. `Q13=4` `docs remain editable inputs`
    Intake docs stay editable after bootstrap.
14. `Q14=5` `docs propose, machine confirms`
    Doc changes propose updates; machine state confirms them.
15. `Q15=10` `maximum audit trail`
    Require a full pre-execution event trail.
16. `Q16=7` `evidence contract stub`
    Use a structured evidence placeholder before execution.
17. `Q17=8` `structured closeout shell`
    Use a machine-readable closeout placeholder before execution.
18. `Q18=8` `structured promotion shell plus provenance`
    Use a machine-readable promotion placeholder with provenance expectations.
19. `Q19=8` `deferred-item contract plus gate`
    Unknown required items need deferred records, and some still block execution.
20. `Q20=10` `strict full project bootstrap gate`
    No project-scoped initiative starts until the full project container exists.
21. `Q21=10` `two-stage bootstrap authority`
    First create the `plan/**` workspace, then bootstrap the first normal initiative.
22. `Q22=9` `strict bounded backlog`
    Every known pre-closeout action must be a task or deferred-item record.
23. `Q23=10` `strict boundedness rule`
    If new work breaks the original bounded package, create a new initiative.
24. `Q24=4` `archive whole package read-only`
    Closed initiatives are archived read-only for now.
25. `Q25=3` `both roots, pack-wide primary`
    First tranche supports both pack-wide and project-scoped roots, with pack-wide primary.
26. `Q26=9` `bootstrap plus gate first`
    First implementation priority is end-to-end bootstrap and execution gating.
27. `Q27=6` `authorized-maintainer approval sync`
    Post-bootstrap doc-to-machine confirmations require an authorized maintainer.
28. `Q28=8` `discrepancy plus gate`
    Unconfirmed required changes create discrepancies and block according to severity.
29. `Q29=9` `bootstrap workflow harness`
    First-tranche automation should be a workflow or harness, not just a command.
30. `Q30=9` `pack-wide and project-scoped flows proven`
    First milestone proves the full loop for one pack-wide and one project-scoped initiative.
31. `Q31=1` `archive is transitional only`
    Whole-package archive is temporary, not the clean-endstate retention rule.
32. `Q32=10` `strict tracked bootstrap`
    Stage 1 setup work must itself be fully tracked.
33. `Q33=10` `two-step seed`
    Create bare `plan/**` roots first, then immediately create the tracked bootstrap record inside `plan/.wt/`.
34. `Q34=7` `strict full lifecycle`
    Initiative lifecycle: `capture_incomplete -> ready_for_review -> ready_for_execution -> in_progress -> blocked -> closing -> completed/superseded/cancelled`.
35. `Q35=6` `operational plus handoff`
    Task lifecycle: `planned -> ready -> in_progress -> in_review -> blocked -> completed/cancelled`.
36. `Q36=9` `full project bootstrap package`
    Project containers need record, repo map, project-context support, rendered basics, and validation-ready structure.
37. `Q37=9` `rendered views tied to scope`
    Readiness requires all rendered views relevant to the initiative scope and root.
38. `Q38=9` `pre-execution full proof`
    Readiness validation must prove full package integrity, scope rules, approval rules, and no-start enforcement.
39. `Q39=9` `README -> overview`
    Human entrypoint is `plan/README.md`, which routes to `plan_overview.md`.
40. `Q40=2` `repo maintainers only`
    Default human authorized maintainers are repo maintainers.
41. `Q41=9` `hybrid tasks plus artifacts`
    Deferred items use dedicated artifacts, with linked tasks only when work becomes actionable.
42. `Q42=9` `task or new initiative based on boundedness`
    Actionable deferred items become tasks if in-bounds, or a new initiative if out-of-bounds.
43. `Q43=10` `maximum query surface`
    First tranche should provide coordination, readiness, initiative, task, project, and discrepancy queries.
44. `Q44=8` `category plus severity`
    Discrepancies carry both category and severity.
45. `Q45=9` `state, events, and optional review hook`
    Store current approval state in snapshots and history in events, with room for future review records.
46. `Q46=10` `maximum strictness`
    Any stale required rendered or aggregate surface fails readiness and creates a blocking discrepancy.
47. `Q47=1` `hard cutover`
    Replace existing planning entrypoints immediately with `plan/**`-backed ones.
48. `Q48=9` `hard cutover with no history surfacing`
    New operational model ignores old history during the first cutover.
49. `Q49=8` `three-file core plus decisions`
    Initiative roots contain `initiative_brief.md`, `design_record.md`, `implementation_slice.md`, and optional `decision_notes.md`.
50. `Q50=10` `requirements-alignment follow-up`
    The implementation plan must include a later tranche to reconcile history and retention with the requirements endstate.

## Key Tensions Already Resolved
- `Q24` and `Q31`: archive-whole-package is allowed only as a transitional policy.
- `Q10` and `Q48`: hard cutover applies to new authority, while historical `docs/planning/**` handling is intentionally deferred.
- `Q13`, `Q14`, `Q27`, and `Q28`: intake docs stay editable, but machine state remains authoritative through proposal, confirmation, and discrepancy gates.

## Working Summary
- The plan must prioritize capture and storage before execution.
- The new authority model is machine-first under `plan/.wt/**`.
- Both pack-wide and project-scoped initiatives are in scope from the first tranche.
- The first implementation milestone must prove the full capture-first loop for one initiative of each scope type.
