"""Shared fixture writers for focused document-semantics validation suites."""

from __future__ import annotations

from pathlib import Path
from shutil import copytree
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parents[4]


def copy_control_plane_repo(tmp_path: Path) -> Path:
    """Copy the governed control-plane subtree into a temporary repo root."""

    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def write_repo_file(path: Path, content: str = "# Placeholder\n") -> None:
    """Write one placeholder repo-local file used by semantic fixtures."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def repo_markdown_link(target: Path) -> str:
    """Return one repository-native Markdown link target for a fixture path."""

    repo_root = _find_fixture_repo_root(target)
    return f"/{target.relative_to(repo_root).as_posix()}"


def _find_fixture_repo_root(path: Path) -> Path:
    """Return the temporary repo root that contains one fixture path."""

    for candidate in (path, *path.parents):
        if (candidate / "core" / "control_plane").exists():
            return candidate
    raise ValueError(f"Could not determine fixture repo root for {path}")


def write_reference_fixture(
    path: Path,
    *,
    support_target: Path,
    include_canonical_upstream: bool = True,
    repository_status_line: str = (
        "Supporting authority for current repository docs, standards, commands, "
        "or control-plane surfaces."
    ),
    include_current_touchpoints: bool = True,
) -> None:
    """Write one governed reference fixture with configurable support sections."""

    path.parent.mkdir(parents=True, exist_ok=True)
    canonical_upstream = (
        "## Canonical Upstream\n- [Example upstream](https://example.com/reference)\n\n"
        if include_canonical_upstream
        else ""
    )
    current_touchpoints = (
        f"### Current Touchpoints\n- [support_target.md]({repo_markdown_link(support_target)})\n\n"
        if include_current_touchpoints
        else ""
    )
    path.write_text(
        dedent(
            """\
            ---
            id: "ref.example"
            title: "Example Reference"
            summary: "Provides governed local reference coverage for semantic tests."
            type: "reference"
            status: "active"
            tags:
              - "reference"
              - "example"
            owner: "repository_maintainer"
            updated_at: "2026-03-11T17:35:00Z"
            audience: "shared"
            authority: "supporting"
            ---

            # Example Reference

            __CANONICAL_UPSTREAM__## Quick Reference or Distilled Reference
            One compact reference fixture.

            ## Local Mapping in This Repository
            ### Current Repository Status
            - __REPOSITORY_STATUS_LINE__

            __CURRENT_TOUCHPOINTS__### Why It Matters Here
            - Keep the fixture tied to one local repository surface.

            ## References
            - [support_target.md](__SUPPORT_TARGET__)

            ## Updated At
            - `2026-03-11T17:35:00Z`
            """
        )
        .replace("__CANONICAL_UPSTREAM__", canonical_upstream)
        .replace("__REPOSITORY_STATUS_LINE__", repository_status_line)
        .replace("__CURRENT_TOUCHPOINTS__", current_touchpoints)
        .replace("__SUPPORT_TARGET__", repo_markdown_link(support_target)),
        encoding="utf-8",
    )


def write_standard_fixture(
    path: Path,
    *,
    related_target: Path,
    reference_target: Path,
    blank_line_before_guidance: bool = True,
    operationalization_surfaces: tuple[str, ...] = (
        "core/docs/standards/documentation/example_standard.md",
    ),
) -> None:
    """Write one standard fixture with configurable formatting and path coverage."""

    path.parent.mkdir(parents=True, exist_ok=True)
    guidance_heading = "\n## Guidance" if blank_line_before_guidance else "## Guidance"
    operationalization_surface_list = "; ".join(
        f"`{surface}`" for surface in operationalization_surfaces
    )
    content = dedent(
        f"""\
        ---
        id: "std.documentation.example"
        title: "Example Standard"
        summary: "Defines one example standard for semantic validation tests."
        type: "standard"
        status: "active"
        tags:
          - "standard"
          - "documentation"
          - "example"
        owner: "repository_maintainer"
        updated_at: "2026-03-10T20:33:00Z"
        audience: "shared"
        authority: "authoritative"
        ---

        # Example Standard

        ## Summary
        Defines one example standard for semantic validation tests.

        ## Purpose
        Keep the test fixture simple and valid apart from the targeted issue.

        ## Scope
        - Applies to one example fixture.

        ## Use When
        - Running semantic validation tests.

        ## Related Standards and Sources
        - [example_reference.md]({repo_markdown_link(related_target)}): defines a local test target.
        __GUIDANCE_HEADING__
        - Keep fixtures small and deterministic.

        ## Operationalization
        - `Modes`: `documentation`
        - `Operational Surfaces`: {operationalization_surface_list}

        ## Validation
        - Semantic validation should fail only for the targeted issue.

        ## Change Control
        - Update the validator and template together if this rule changes.

        ## References
        - [supporting_template.md]({repo_markdown_link(reference_target)})

        ## Updated At
        - `2026-03-10T20:33:00Z`
        """
    ).replace("__GUIDANCE_HEADING__", guidance_heading)
    path.write_text(content, encoding="utf-8")


def write_standard_reference_rule_fixture(
    path: Path,
    *,
    related_lines: tuple[str, ...],
    reference_lines: tuple[str, ...],
) -> None:
    """Write one standard fixture that exercises related-source accounting rules."""

    path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        dedent(
            """\
        ---
        id: "std.documentation.example"
        title: "Example Standard"
        summary: "Exercises standard reference-accounting semantics."
        type: "standard"
        status: "active"
        tags:
          - "standard"
          - "documentation"
          - "example"
        owner: "repository_maintainer"
        updated_at: "2026-03-11T17:35:00Z"
        audience: "shared"
        authority: "authoritative"
        ---

        # Example Standard

        ## Summary
        Exercises standard reference-accounting semantics.

        ## Purpose
        Keep the fixture focused on governed external-authority rules.

        ## Scope
        - Applies to one standard-semantics fixture.

        ## Use When
        - Validating governed local-reference enforcement.

        ## Related Standards and Sources
        __RELATED_LINES__

        ## Guidance
        - Keep standard reference-accounting deterministic.

        ## Operationalization
        - `Modes`: `documentation`
        - `Operational Surfaces`: `core/docs/standards/documentation/example_standard.md`

        ## Validation
        - Standard semantic validation should stay aligned with standard-index sync.

        ## Change Control
        - Update validation and sync helpers together if this rule changes.

        ## References
        __REFERENCE_LINES__

        ## Updated At
        - `2026-03-11T17:35:00Z`
        """
        )
        .replace("__RELATED_LINES__", "\n".join(related_lines))
        .replace(
            "__REFERENCE_LINES__",
            "\n".join(reference_lines),
        )
    )
    path.write_text(content, encoding="utf-8")
