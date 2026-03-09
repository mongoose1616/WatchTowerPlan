---
id: "std.documentation.readme_md"
title: "README.md Standard"
summary: "This standard defines the role, structure, and boundary rules for `README.md` files used as directory-level orientation documents in this repository."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "readme_md"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
---

# README.md Standard

## Summary
This standard defines the role, structure, and boundary rules for `README.md` files used as directory-level orientation documents in this repository.

## Purpose
Keep `README.md` files compact, trustworthy, and useful as the first-stop reference for what a directory is for and what the main entries inside it mean.

## Scope
- Applies to `README.md` files used to describe a directory in this repository.
- Covers title format, required orientation content, inventory structure, and what should stay out of a README.
- Does not define task-execution behavior, repository-wide instruction behavior, or document lifecycle policy for other document families.

## Use When
- Creating a new directory README.
- Refreshing a README after a directory's purpose, boundaries, or key contents change.
- Reviewing whether a README is carrying content that belongs in `AGENTS.md`, `docs/standards/**`, or `workflows/**` instead.

## Related Standards and Sources
- [agents_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/agents_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [readme_template.md](/home/j/WatchTowerPlan/docs/templates/readme_template.md): authoring scaffold that should stay aligned with this standard.
## Guidance
- A `README.md` should describe the current directory, not the repository in general and not a neighboring directory.
- A `README.md` should act as a quick-reference orientation layer before broader scans.
- Use exactly one `README.md` per directory.
- Do not add front matter or lifecycle `status` to a directory README.
- Keep the document short enough to scan quickly.
- The title should be the repository-relative directory path in backticks. Use `# \`.\`` for the repository root.
- Include a `Description` section that states what belongs in the directory and any important usage boundaries.
- Include one inventory section:
  - Use `Files` when the directory is primarily file-oriented.
  - Use `Paths` when the directory is primarily organized around important child directories or path families.
- Inventory sections must use a Markdown table.
- Inventory tables must use exactly two columns: `Path` and `Description`.
- Do not use bullet lists or prose paragraphs as the primary inventory format.
- Default the inventory to the directory's direct entrypoints and most important child paths rather than a recursive dump of everything below it.
- Include the local `README.md` itself in the inventory table.
- Add `Boundaries` only when the directory has important exclusions, ownership limits, or storage rules that a reader needs immediately.
- Prefer linking to companion documents rather than copying their detailed content into the README.
- Do not turn a README into a standards document, workflow module, changelog, or broad narrative overview.
- Do not embed local operating instructions that belong in `AGENTS.md`.

## Structure or Data Model
- Title in the form `# \`<repo-relative-directory-path>\``
- Required section:
  - `## Description`
- Required inventory section:
  - `## Files` or
  - `## Paths`
- Required inventory table with columns:
  - `Path`
  - `Description`
- Optional sections when materially useful:
  - `## Boundaries`
  - `## Notes`

## Validation
- The directory purpose should be clear from the title and `Description`.
- The README should stay focused on the directory it lives in.
- The inventory should point to real local files or paths and describe why a reader would care about them.
- The inventory should be expressed as a Markdown table with the standard two-column shape.
- The file should be short and scannable enough to serve as quick context before deeper reading.
- The README should not contain front matter, workflow procedure, or broad repository policy that belongs elsewhere.

## Change Control
- Update a directory README when the directory's purpose, boundaries, or key entrypoints change materially.
- Update this standard and the README template in the same change set when the expected README structure changes.
- Update related `AGENTS.md`, workflow, or standards documents in the same change set when README boundaries change between those surfaces.

## References
- [readme_template.md](/home/j/WatchTowerPlan/docs/templates/readme_template.md)
- [agents_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/agents_md_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)

## Notes
- A good README helps a contributor understand a directory before opening many files.
- If a README needs long procedural content or repository-wide rules, that content probably belongs in a companion document instead.

## Updated At
- `2026-03-09T23:02:08Z`
