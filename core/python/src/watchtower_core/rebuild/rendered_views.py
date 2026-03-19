"""Registry-backed rendered-view building and markdown reconciliation helpers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal

from watchtower_core.adapters import render_rendered_surface
from watchtower_core.control_plane import TemplateCatalogHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import RenderedSurfaceDefinition
from watchtower_core.rebuild.harness import RebuildOutput

MarkdownReconciliationCode = Literal[
    "missing_expected_content",
    "missing_output",
    "content_drift",
]


@dataclass(frozen=True, slots=True)
class RenderedViewSpec:
    """One rendered-view build request over a governed rendered-surface entry."""

    surface_id: str
    data: Mapping[str, object]
    path_params: Mapping[str, str] = field(default_factory=dict)
    relative_output_path: str | None = None
    title: str | None = None
    artifact_kind: str = "rendered_view"


@dataclass(frozen=True, slots=True)
class RenderedViewResult:
    """One registry-backed rendered markdown output."""

    surface_id: str
    title: str
    relative_output_path: str
    content: str
    artifact_kind: str = "rendered_view"

    def as_rebuild_output(self) -> RebuildOutput:
        """Return this rendered view as a rebuild-harness markdown output."""

        return RebuildOutput(
            relative_output_path=self.relative_output_path,
            artifact_kind=self.artifact_kind,
            output_format="markdown",
            content=self.content,
        )


@dataclass(frozen=True, slots=True)
class MarkdownReconciliationIssue:
    """One rendered markdown reconciliation issue."""

    relative_output_path: str
    issue_code: MarkdownReconciliationCode


class RenderedViewBuilder:
    """Build rendered markdown views from governed rendered-surface registry entries."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._registry = loader.load_rendered_surface_registry()
        self._template_helper = TemplateCatalogHelper.from_loader(loader)

    def build_view(self, spec: RenderedViewSpec) -> RenderedViewResult:
        """Build one rendered markdown view from a governed surface definition."""

        surface = self._registry.get(spec.surface_id)
        self._validate_surface_contract(surface, spec.data)
        effective_surface = _surface_with_title_override(surface, spec.title)
        relative_output_path = (
            spec.relative_output_path
            if spec.relative_output_path is not None
            else _resolve_output_path(surface.output_path, spec.path_params)
        )
        return RenderedViewResult(
            surface_id=spec.surface_id,
            title=effective_surface.title,
            relative_output_path=relative_output_path,
            content=render_rendered_surface(effective_surface, spec.data),
            artifact_kind=spec.artifact_kind,
        )

    def _validate_surface_contract(
        self,
        surface: RenderedSurfaceDefinition,
        data: Mapping[str, object],
    ) -> None:
        templates = self._template_helper.templates_for_surface(surface.surface_id)
        if len(templates) != 1:
            raise ValueError(
                f"Rendered surface {surface.surface_id} must resolve to exactly one template entry."
            )
        template = templates[0]
        surface_section_ids = tuple(section.section_id for section in surface.sections)
        if surface_section_ids != template.section_order:
            raise ValueError(
                f"Rendered surface {surface.surface_id} section order does not match template "
                f"contract: {surface_section_ids!r} != {template.section_order!r}"
            )
        missing_source_keys = tuple(
            section.source_key
            for section in surface.sections
            if section.source_key not in data
        )
        if missing_source_keys:
            raise ValueError(
                f"Rendered surface {surface.surface_id} is missing renderer payload keys: "
                f"{', '.join(missing_source_keys)}"
            )

    def build_views(
        self,
        specs: tuple[RenderedViewSpec, ...],
    ) -> tuple[RenderedViewResult, ...]:
        """Build multiple rendered markdown views."""

        return tuple(self.build_view(spec) for spec in specs)

    def build_rebuild_outputs(
        self,
        specs: tuple[RenderedViewSpec, ...],
    ) -> tuple[RebuildOutput, ...]:
        """Build multiple rendered views as rebuild-harness outputs."""

        return tuple(result.as_rebuild_output() for result in self.build_views(specs))


class MarkdownReconciliationHelper:
    """Compare expected rendered markdown against the current workspace state."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._repo_root = loader.repo_root

    def expected_issues(
        self,
        expected_markdown: Mapping[str, str],
    ) -> tuple[MarkdownReconciliationIssue, ...]:
        """Return rendered markdown drift issues for the expected output mapping."""

        issues: list[MarkdownReconciliationIssue] = []
        for relative_output_path, expected in expected_markdown.items():
            if not expected:
                issues.append(
                    MarkdownReconciliationIssue(
                        relative_output_path=relative_output_path,
                        issue_code="missing_expected_content",
                    )
                )
                continue
            candidate = self._repo_root / relative_output_path
            if not candidate.exists():
                issues.append(
                    MarkdownReconciliationIssue(
                        relative_output_path=relative_output_path,
                        issue_code="missing_output",
                    )
                )
                continue
            if _normalize_markdown(candidate.read_text(encoding="utf-8")) != _normalize_markdown(
                expected
            ):
                issues.append(
                    MarkdownReconciliationIssue(
                        relative_output_path=relative_output_path,
                        issue_code="content_drift",
                    )
                )
        return tuple(issues)


def _resolve_output_path(template: str, path_params: Mapping[str, str]) -> str:
    try:
        return template.format_map(path_params)
    except KeyError as exc:
        missing_key = exc.args[0]
        raise ValueError(
            f"Rendered view output path {template} requires missing path param {missing_key}."
        ) from exc


def _surface_with_title_override(
    surface: RenderedSurfaceDefinition,
    title: str | None,
) -> RenderedSurfaceDefinition:
    if title is None:
        return surface
    return RenderedSurfaceDefinition(
        surface_id=surface.surface_id,
        title=title,
        output_path=surface.output_path,
        sections=surface.sections,
        notes=surface.notes,
    )


def _normalize_markdown(content: str) -> str:
    normalized = content.rstrip()
    if not normalized:
        return ""
    return f"{normalized}\n"


__all__ = [
    "MarkdownReconciliationCode",
    "MarkdownReconciliationHelper",
    "MarkdownReconciliationIssue",
    "RenderedViewBuilder",
    "RenderedViewResult",
    "RenderedViewSpec",
]
