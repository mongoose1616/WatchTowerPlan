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
- Current branch identity when the work is happening on a bounded branch
- Relevant task summary, acceptance criteria, or rationale for the change
- Current repository-local task or trace outcome when the change is non-trivial
- Internal standards and canonical references applied
- [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md)
- Open questions about scope, breaking-change status, or related footers

## Additional Files to Load
- [git_workflow_standard.md](/core/docs/standards/engineering/git_workflow_standard.md): defines the bounded-branch naming and lifecycle checks that should still hold before closeout.
- [git_commit_message_guidance_reference.md](/core/docs/references/git_commit_message_guidance_reference.md): defines the local commit-message shape this workflow should preserve when writing the final commit.
- [conventional_commits_reference.md](/core/docs/references/conventional_commits_reference.md): provides the commit prefix guidance used when a conventional commit style is helpful.

## Workflow
1. Inspect the change set and confirm commit readiness.
   - Review `git status`, staged files, and the staged diff.
   - When the work is on a bounded branch, review `git branch --show-current` and confirm the branch name still reflects the git-workflow standard's origin-aware branch contract instead of a stale or ambiguous source context.
   - Verify that the intended change set is complete enough to close out.
   - Check whether unresolved errors, validation failures, or decision blockers should prevent committing.
   - Confirm that the commit represents one logical change or split the work before proceeding.
2. Apply the Git commit standard and draft the message.
   - Use [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md) as the governing policy for type, scope, description, body, and footers.
   - Choose the commit type and optional scope that best reflect the dominant effect of the change.
   - Write the subject in imperative voice with 72 characters or fewer and no trailing punctuation.
   - Add a body and footers when the change is complex, risky, task-linked, trace-linked, or breaking.
   - For non-trivial work, include repository-specific tracking footers such as `Trace-ID`, `Task-ID`, or an explicit `No-Task-Reason` only when the active pack or repository rules require durable outcome tracking.
   - Prefer repository-semantic trace or task identifiers over opaque UUIDs when adding commit metadata.
3. Validate the commit message and create the commit when requested.
   - Check the message against the repository regex and commit-message rules from the standard.
   - Confirm the message accurately matches the staged change set.
   - Use the validated message to create the Git commit when requested.
   - If commit creation is deferred or fails, record the prepared message or failure clearly.

## Data Structure
- Change set summary
- Current branch identity and readiness status when applicable
- Commit readiness status
- Governing commit standard
- Chosen type and scope
- Breaking-change decision
- Draft commit message
- Validation checks applied
- Commit result

## Outputs
- A repository-compliant Git commit or a validated commit message draft
- An explicit record of the standard used to govern the commit
- An explicit record of commit validation checks applied
- An explicit record of any commit blockers, deferrals, or follow-up work

## Done When
- The change set has been evaluated for commit readiness.
- The Git commit standard has been applied to the commit message.
- A valid commit has been created or the commit has been explicitly deferred or blocked with a recorded reason.
- The closeout result is clear enough for downstream handoff or follow-up.
