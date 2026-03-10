# Commit Closeout Workflow

## Purpose
Use this workflow to evaluate commit readiness, prepare a repository-compliant commit message, and create the Git commit when requested.

## Use When
- A change set is ready to be committed after implementation, documentation, or planning work.
- A user explicitly asks to create a Git commit.
- A workflow needs structured commit preparation, message drafting, or commit-quality checks before handoff.

## Inputs
- Scoped closeout brief
- Completed change set
- `git status` and staged diff context
- Relevant task summary, acceptance criteria, or rationale for the change
- Internal standards and canonical references applied
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)
- Open questions about scope, breaking-change status, or related footers

## Additional Files to Load
- [git_commit_message_guidance_reference.md](/home/j/WatchTowerPlan/docs/references/git_commit_message_guidance_reference.md): defines the local commit-message shape this workflow should preserve when writing the final commit.
- [conventional_commits_reference.md](/home/j/WatchTowerPlan/docs/references/conventional_commits_reference.md): provides the commit prefix guidance used when a conventional commit style is helpful.

## Workflow
1. Inspect the change set and confirm commit readiness.
   - Review `git status`, staged files, and the staged diff.
   - Verify that the intended change set is complete enough to close out.
   - Check whether unresolved errors, validation failures, or decision blockers should prevent committing.
   - Confirm that the commit represents one logical change or split the work before proceeding.
2. Apply the Git commit standard and draft the message.
   - Use [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md) as the governing policy for type, scope, description, body, and footers.
   - Choose the commit type and optional scope that best reflect the dominant effect of the change.
   - Write the subject in imperative voice with 72 characters or fewer and no trailing punctuation.
   - Add a body and footers when the change is complex, risky, trace-linked, or breaking.
3. Validate the commit message and create the commit when requested.
   - Check the message against the repository regex and commit-message rules from the standard.
   - Confirm the message accurately matches the staged change set.
   - Use the validated message to create the Git commit when requested.
   - If commit creation is deferred or fails, record the prepared message or failure clearly.

## Data Structure
- Change set summary
- Commit readiness status
- Governing commit standard
- Chosen type and scope
- Breaking-change decision
- Draft commit message
- Validation checks applied
- Commit result

## Outputs
- A repository-compliant Git commit or a validated commit message draft
- A short record of the standard used to govern the commit
- A short record of commit validation checks applied
- A short record of any commit blockers, deferrals, or follow-up work

## Done When
- The change set has been evaluated for commit readiness.
- The Git commit standard has been applied to the commit message.
- A valid commit has been created or the commit has been explicitly deferred or blocked with a recorded reason.
- The closeout result is clear enough for downstream handoff or follow-up.
