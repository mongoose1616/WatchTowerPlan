---
id: "std.engineering.git_commit"
title: "Git Commit Standard"
summary: "This standard defines the repository commit-message policy for human maintainers and assistant contributors. It combines Conventional Commits v1.0.0 with local commit-writing guidance so history remains human-auditable and machine-parseable."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "git_commit"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:23:35Z"
audience: "shared"
authority: "authoritative"
---

# Git Commit Standard

## Summary
This standard defines the repository commit-message policy for human maintainers and assistant contributors. It combines Conventional Commits v1.0.0 with local commit-writing guidance so history remains human-auditable and machine-parseable.

## Purpose
- Align repository commits to Conventional Commits v1.0.0 while honoring local repository guardrails.
- Serve both human maintainers and LLM or agent contributors with one normative commit standard.
- Enable deterministic automation such as changelog generation, semantic versioning, compliance checks, and cross-team reviews.

## Scope
- Covers commit message format, allowed types, scope usage, breaking-change notation, body and footer expectations, and local automation guidance.
- Applies to commits created for this repository by human maintainers and assistant contributors.
- Does not define branch naming, pull-request title policy, or broader release-management process.

## Guidance
### Canonical Format and Quick Reference
```text
<type>[optional scope][optional !]: <short description>

[optional body]

[optional footer(s)]
```

- Use one blank line between description, body, and footer sections.
- Keep the subject at 72 characters or fewer, imperative voice, with no trailing punctuation.
- Wrap body lines near 80 characters for readability.
- Put each footer on its own line after a blank separator using `Token: value` or `Token #value`.
- When sharing commit text in tools, reviews, or documentation, wrap the message in fenced code blocks with the `text` info string.

### Allowed Types
| Type | Use When | Semantic Version Effect | Example |
|---|---|---|---|
| `feat` | Adds a new user-facing capability or workflow behavior | MINOR bump | `feat(workflows): add feature design planning route` |
| `fix` | Resolves a bug or regression visible to contributors or consumers | PATCH bump | `fix(routing_table): route design requests correctly` |
| `docs` | Documentation-only updates | None | `docs(workflows): clarify documentation gap handling` |
| `style` | Formatting or lint-only work | None | `style(templates): normalize markdown spacing` |
| `refactor` | Internal restructuring without behavior change | None | `refactor(workflows): separate design from implementation planning` |
| `perf` | Performance-centric change | PATCH bump | `perf(retrieval): reduce redundant reference scans` |
| `test` | Adds or modifies tests only | None | `test(validators): cover workflow routing checks` |
| `build` | Build tooling or dependency updates | None | `build(tooling): add commit message hook setup` |
| `ci` | Local quality-automation changes such as hooks, gate scripts, or guard workflows | None | `ci(local_qa): enforce commit message checks` |
| `chore` | Maintenance tasks that do not alter runtime behavior | None | `chore(repo): prune stale planning notes` |
| `revert` | Reverts a previous commit | Mirrors reverted change | `revert: feat(workflows): add feature design planning route` |

*Guidance: Prefer the core rows for clarity. Use extended types only when they describe intent more precisely than `chore`.*

### Component Standards
#### Type (required)
- Pick the type that reflects user or consumer impact first. When in doubt, prioritize `feat` or `fix`, then `perf`, `refactor`, and finally `chore`.
- Validation regex for the first line: `^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9_-]+\))?(!)?: .{1,72}$`

#### Scope (optional)
- Use lower-case nouns in parentheses to name the subsystem, workflow, directory, or surface, such as `feat(workflows): ...`.
- Use `_` for multi-word scopes.
- Omit the scope when the change is clearly repo-wide or the scope adds no value.

#### Breaking Marker (optional)
- Add `!` immediately after the type or scope when external behavior changes.
- Always include a `BREAKING CHANGE:` footer for major shifts so downstream automation captures context.

#### Description (required)
- Use imperative, present tense wording with no trailing punctuation.
- Keep the subject focused on what changes and the value delivered.
- Example descriptions: `add commit message hook setup`, `clarify design handoff requirements`.

#### Body (optional but encouraged for non-trivial work)
- Explain context, approach, impact, and migration steps when needed.
- Use bullets or short paragraphs wrapped near 80 characters.
- Preferred outline: Context -> Solution -> Impact -> Migration, when a migration note is needed.

#### Footers (optional metadata)
- Put each footer on its own line after a blank separator.
- Common tokens: `BREAKING CHANGE:`, `Closes: #123`, `Refs: #45`, `Acked-by: role@example.org`, `Co-authored-by: Name <email>`.
- Order footers as: breaking notice, issue references, acknowledgments or sign-offs.

### Breaking Change Guidance
1. Use both the `!` marker and a `BREAKING CHANGE:` footer for high-impact changes when feasible.
2. State what breaks, why it breaks, how to migrate, and any enforcement timeline.
3. Do not label internal-only refactors as breaking unless external contributors or automation must adapt.

**Example**
```text
feat(workflows)!: require feature design before implementation planning

BREAKING CHANGE: Implementation planning now expects an approved
feature design or technical design as input. Existing planning flows
must add a design handoff before using the implementation planning
workflow.
```

## Process
1. Gather context.
   - Run `git status` and `git diff --cached` to confirm staged files and dependencies.
   - Review prior commits for continuity when the change extends ongoing work.
2. Select type and scope.
   - Map the dominant effect of the diff to the allowed types.
   - Split the work into separate commits when multiple types would be required.
3. Craft the description.
   - Summarize the change in 72 characters or fewer using imperative wording.
   - Capture the value of the change rather than just the implementation detail.
4. Add the body when needed.
   - Explain rationale, edge cases, or side effects.
   - Include migration instructions for breaking changes.
5. Append footers.
   - Add tickets, approvals, and co-authors to preserve traceability.
6. Share for review.
   - When posting commit text in collaboration tools or review threads, wrap it in fenced `text` blocks for exact copying.
7. Record rationale.
   - If the commit satisfies a governance control or evidence requirement, mention it in the body or footers.

### Quick Prompts for LLMs and Agents
- "Summarize the functional change in 72 characters or fewer using `<type>(<scope>): <verb phrase>`."
- "List the motivations or impacts that justify this change in one or two sentences."
- "Identify related tickets or issues for `Refs:` or `Closes:` footers."
- "Does contributor-facing or automation-facing behavior change? If yes, draft a `BREAKING CHANGE:` note."
- "Who reviewed or acknowledged the change for `Acked-by:` entries?"

### Structured Parsing Template
```json
{
  "type": "feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert",
  "scope": "string|null",
  "breaking": "true|false",
  "description": "<=72 char string",
  "body": "string|null",
  "footers": [
    {"token": "BREAKING CHANGE|Refs|Closes|Acked-by|...", "value": "text"}
  ]
}
```

## Validation
- One logical change per commit. Refactors, fixes, and docs should be separate when practical.
- The subject line uses an allowed type, optional scope, imperative verb, 72 characters or fewer, and no trailing punctuation.
- The body explains context or migration steps when the change is complex, risky, or non-obvious, with lines wrapped near 80 characters.
- Footers capture breaking changes, issues, approvals, and collaborators using `Token: value` format.
- Commit text is reviewed for spelling, case, and placeholder removal before commit or before being shared for review.

## Examples
### Scenario A: Simple Bug Fix
```text
fix(routing_table): route design requests correctly

Correct the feature design keywords so design-planning requests load
the dedicated workflow instead of falling through to implementation
planning.

Closes: #42
```

### Scenario B: New Feature with Breaking Change
```text
feat(workflows)!: require feature design before implementation planning

Introduce a dedicated design handoff so major feature work is reviewed
as a technical design before it becomes an execution plan.

BREAKING CHANGE: Implementation planning now expects an approved
feature design or technical design as input. Existing planning flows
must add a design handoff before using the implementation planning
workflow.

Refs: #57
```

### Scenario C: Combined Human and Agent Work
```text
docs(standards_engineering): codify git commit policy

Align the repository commit guidance with the Conventional Commits and
git commit message references so maintainers and agents use the same
commit contract.

Acked-by: reviewer@example.org
```

## Anti-patterns to Avoid
- `update stuff`: vague and missing type and scope.
- `feat: Added authentication.`: past tense with trailing punctuation.
- `fix: fix bug`: redundant and lacking detail.
- Mixing unrelated refactors, fixes, and docs into one commit.
- Omitting breaking-change notices when contributor-facing or automation-facing contracts shift.
- Leaving prompt fragments or diff dumps inside the body.

## Tooling and Automation
- Configure `commitlint`, a `commit-msg` hook, or a lightweight local script to enforce the subject-line regex.
- Use changelog or release tooling that maps types to semantic version signals when release automation is introduced.
- Keep local guard automation aligned with this standard so invalid commit messages fail fast.

### Building Validation Tooling
Use the shared regex in a lightweight script or `commit-msg` hook so contributors get immediate feedback before pushing:

```bash
#!/bin/bash
commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

pattern='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9_-]+\))?(!)?: .{1,72}$'

if ! echo "$commit_msg" | head -n1 | grep -Eq "$pattern"; then
    echo "Error: commit message must follow <type>(<scope>): <description>"
    echo "Valid types: feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"
    exit 1
fi
```

- Wire the script to Git's `commit-msg` hook or wrap it with local automation so commits fail fast when they do not meet the format.
- Extend the script with additional checks such as body wrapping or required footers only if the repository formally adopts those stricter policies.

## Change Control
- Update this standard when the repository commit policy changes materially.
- Update companion references, hook examples, and automation guidance in the same change set when the standard changes.
- Update contributor-facing workflows or templates in the same change set when commit expectations change for humans or agents.

## References
- [conventional_commits_reference.md](/home/j/WatchTowerPlan/docs/references/conventional_commits_reference.md)
- [git_commit_message_guidance_reference.md](/home/j/WatchTowerPlan/docs/references/git_commit_message_guidance_reference.md)
- [semantic_versioning_reference.md](/home/j/WatchTowerPlan/docs/references/semantic_versioning_reference.md)
- [reference_distillation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/reference_distillation_standard.md)

## Notes
- This is the normative repository policy for Git commit messages.
- The reference documents remain supporting context and should not override this standard.

## Updated At
- `2026-03-09T05:23:35Z`
