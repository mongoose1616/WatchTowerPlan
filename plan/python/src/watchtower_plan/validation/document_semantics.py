"""Repo-specific semantic validation for governed Markdown document families."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.adapters import extract_sections, extract_title, load_markdown_body
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ValidatorDefinition
from watchtower_core.documentation.governed_documents import validate_required_section_order
from watchtower_core.documentation.markdown_semantics import (
    validate_blank_line_before_heading_after_list,
)
from watchtower_core.validation.common import matches_applies_to, resolve_target_path
from watchtower_core.validation.document_semantics import (
    CoreDocumentSemanticsValidationService,
)
from watchtower_core.validation.errors import (
    ValidationExecutionError,
    ValidationSelectionError,
)
from watchtower_core.validation.models import ValidationIssue, ValidationResult

DOCUMENT_SEMANTICS_ARTIFACT_KIND = "documentation_semantics"
INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID = (
    "validator.plan.initiative_handoff_document_semantics"
)
INITIATIVE_TEMPLATE_EXACT_SEMANTICS_FILENAMES = frozenset(
    {"README.md", "plan.md", "progress.md", "summary.md"}
)
INITIATIVE_DYNAMIC_TEMPLATE_SEMANTICS_FILENAMES = frozenset(
    {"phase_output_manifest.md", "phase_closeout_checklists.md"}
)
INITIATIVE_FINDINGS_SECTION_TITLES = (
    "Cold-Start Findings",
    "First-Pass Findings",
)
INITIATIVE_GENERIC_REQUIRED_SECTION_GROUPS: dict[
    str, tuple[tuple[str, ...], ...]
] = {
    "cold_start_runbook.md": (
        ("Summary",),
        INITIATIVE_FINDINGS_SECTION_TITLES,
        ("Read Order",),
        ("Questions To Answer",),
        ("Command Anchors",),
        ("Where To Record Outcomes",),
        ("Done When",),
    ),
    "initiative_brief.md": (
        ("Summary",),
        ("Identity", "Problem Statement"),
        ("Initial Task Set", "Goals", "Execution Task Chain"),
    ),
    "design_record.md": (
        ("Summary",),
        ("Initial Design Boundary", "Design Goals", "Preservation Architecture"),
    ),
    "implementation_slice.md": (
        ("Summary",),
        (
            "Initial Work Breakdown",
            "Execution Boundary",
            "Same-Initiative Execution Task Chain",
            "First Post-Approval Execution Slice",
        ),
        ("Gate",),
    ),
    "decision_notes.md": (("Summary",),),
    "conditional_revisit_queue.md": (
        ("Summary",),
        ("Revisit Rules",),
        ("Conditional Revisit Items",),
        ("Governing Surfaces When A Revisit Fires",),
    ),
    "contradiction_sweep_ledger.md": (
        ("Summary",),
        ("Use Rules",),
        ("Resolved Tensions",),
        ("Still Open Only If Triggered",),
    ),
}
INITIATIVE_TEMPLATE_ROOT = Path("plan/.wt/templates/initiatives")
INITIATIVE_REQUIRED_CANONICAL_READ_ORDER = (
    "initiative_brief.md",
    "design_record.md",
    "implementation_slice.md",
)
INITIATIVE_TERMINAL_DISCREPANCY_STATUSES = frozenset(
    {"resolved", "closed", "completed", "cancelled"}
)
INITIATIVE_EMPTY_SCOPE_FALLBACK_LINE = (
    "No explicit non-goals or deferred scope items are recorded."
)
_CORE_VALIDATOR_IDS = frozenset(
    {
        "validator.documentation.command_semantics",
        "validator.documentation.reference_semantics",
        "validator.documentation.foundation_semantics",
        "validator.documentation.standard_semantics",
        "validator.documentation.workflow_semantics",
    }
)


class DocumentSemanticsValidationService:
    """Validate one governed Markdown document against repo-native semantic rules."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._core_service = CoreDocumentSemanticsValidationService(loader)
        self._initiative_template_section_cache: dict[str, tuple[str, ...]] = {}

    def validate(
        self, path: str | Path, validator_id: str | None = None
    ) -> ValidationResult:
        """Validate one Markdown document through registry-backed semantic rules."""

        resolved_path, target_path, relative_target_path = resolve_target_path(self._loader, path)
        validator = self._resolve_validator(relative_target_path, validator_id)

        try:
            self._validate_document(
                validator.validator_id,
                resolved_path=resolved_path,
                relative_target_path=relative_target_path,
            )
        except (ValueError, ValidationExecutionError) as exc:
            return ValidationResult(
                validator_id=validator.validator_id,
                target_path=target_path,
                engine=validator.engine,
                schema_ids=(),
                passed=False,
                issues=(
                    ValidationIssue(
                        code="document_semantics_error",
                        message=str(exc),
                        location=target_path,
                    ),
                ),
            )

        return ValidationResult(
            validator_id=validator.validator_id,
            target_path=target_path,
            engine=validator.engine,
            schema_ids=(),
            passed=True,
            issues=(),
        )

    def _resolve_validator(
        self,
        relative_target_path: str | None,
        validator_id: str | None,
    ) -> ValidatorDefinition:
        registry = self._loader.load_validator_registry()
        if validator_id is not None:
            try:
                validator = registry.get(validator_id)
            except KeyError as exc:
                raise ValidationSelectionError(f"Unknown validator ID: {validator_id}") from exc
            return self._validate_registry_record(validator)

        if relative_target_path is None:
            raise ValidationSelectionError(
                "Auto-selection requires a repository-local path. Use --validator-id "
                "for external files."
            )

        candidates = [
            validator
            for validator in registry.validators
            if validator.artifact_kind == DOCUMENT_SEMANTICS_ARTIFACT_KIND
            and validator.status == "active"
            and any(
                matches_applies_to(relative_target_path, pattern)
                for pattern in validator.applies_to
            )
        ]
        if not candidates:
            raise ValidationSelectionError(
                f"No active document-semantics validator applies to {relative_target_path}."
            )
        if len(candidates) > 1:
            candidate_ids = ", ".join(sorted(candidate.validator_id for candidate in candidates))
            raise ValidationSelectionError(
                "Multiple document-semantics validators apply to "
                f"{relative_target_path}: {candidate_ids}"
            )
        return self._validate_registry_record(candidates[0])

    def _validate_registry_record(self, validator: ValidatorDefinition) -> ValidatorDefinition:
        if validator.status != "active":
            raise ValidationSelectionError(
                f"Validator is not active and cannot be selected: {validator.validator_id}"
            )
        if validator.artifact_kind != DOCUMENT_SEMANTICS_ARTIFACT_KIND:
            raise ValidationSelectionError(
                "Requested validator does not target governed document semantics: "
                f"{validator.validator_id}"
            )
        if validator.engine != "python":
            raise ValidationExecutionError(
                f"Unsupported validator engine for document semantics: {validator.engine}"
            )
        return validator

    def _validate_document(
        self,
        validator_id: str,
        *,
        resolved_path: Path,
        relative_target_path: str | None,
    ) -> None:
        if relative_target_path is None:
            raise ValidationExecutionError(
                "Document-semantics validation requires a repository-local path."
            )

        if validator_id in _CORE_VALIDATOR_IDS:
            result = self._core_service.validate(
                relative_target_path,
                validator_id=validator_id,
            )
            if not result.passed:
                if result.issues:
                    raise ValidationExecutionError(result.issues[0].message)
                raise ValidationExecutionError(
                    f"Core document-semantics validation failed for {relative_target_path}."
                )
            return

        if validator_id == INITIATIVE_HANDOFF_DOCUMENT_SEMANTICS_VALIDATOR_ID:
            self._validate_initiative_handoff_document(relative_target_path, resolved_path)
            return

        raise ValidationExecutionError(
            f"Unsupported document-semantics validator: {validator_id}"
        )

    def _validate_initiative_handoff_document(
        self,
        relative_path: str,
        resolved_path: Path,
    ) -> None:
        markdown = load_markdown_body(resolved_path)
        sections = extract_sections(markdown)
        filename = resolved_path.name
        if filename in INITIATIVE_TEMPLATE_EXACT_SEMANTICS_FILENAMES:
            self._validate_markdown_title_and_required_section_groups(
                relative_path,
                markdown,
                sections,
                required_section_groups=self._template_required_section_groups(filename),
            )
        elif filename in INITIATIVE_DYNAMIC_TEMPLATE_SEMANTICS_FILENAMES:
            prefix_sections = self._initiative_template_sections(filename)[:2]
            self._validate_markdown_title_and_required_section_groups(
                relative_path,
                markdown,
                sections,
                required_section_groups=tuple((title,) for title in prefix_sections),
            )
            self._validate_additional_sections_after_prefix(
                relative_path,
                sections,
                prefix_sections=prefix_sections,
                minimum_count=1,
            )
        else:
            required_section_groups = INITIATIVE_GENERIC_REQUIRED_SECTION_GROUPS.get(filename)
            if required_section_groups is None:
                raise ValidationExecutionError(
                    f"Unsupported initiative handoff semantics target: {relative_path}"
                )
            self._validate_markdown_title_and_required_section_groups(
                relative_path,
                markdown,
                sections,
                required_section_groups=required_section_groups,
            )
        if filename == "cold_start_runbook.md":
            self._validate_initiative_cold_start_read_order(
                relative_path,
                resolved_path.parent,
                sections["Read Order"],
            )
        if filename == "plan.md":
            self._validate_initiative_rendered_plan(
                relative_path,
                resolved_path,
                sections,
            )

    def _initiative_template_sections(self, filename: str) -> tuple[str, ...]:
        cached = self._initiative_template_section_cache.get(filename)
        if cached is not None:
            return cached

        template_path = self._loader.repo_root / INITIATIVE_TEMPLATE_ROOT / filename
        if not template_path.exists():
            raise ValidationExecutionError(
                f"Missing initiative template for semantic validation: {template_path}"
            )
        titles = tuple(extract_sections(load_markdown_body(template_path)).keys())
        if not titles:
            raise ValidationExecutionError(
                f"Initiative template does not publish any H2 sections: {template_path}"
            )
        self._initiative_template_section_cache[filename] = titles
        return titles

    def _template_required_section_groups(
        self,
        filename: str,
    ) -> tuple[tuple[str, ...], ...]:
        section_titles = self._initiative_template_sections(filename)
        if filename != "cold_start_runbook.md":
            return tuple((title,) for title in section_titles)
        return (
            (section_titles[0],),
            INITIATIVE_FINDINGS_SECTION_TITLES,
            *((title,) for title in section_titles[2:]),
        )

    def _validate_additional_sections_after_prefix(
        self,
        relative_path: str,
        sections: dict[str, str],
        *,
        prefix_sections: tuple[str, ...],
        minimum_count: int,
    ) -> None:
        ordered_titles = tuple(sections.keys())
        trailing_titles = ordered_titles[ordered_titles.index(prefix_sections[-1]) + 1 :]
        if len(trailing_titles) >= minimum_count:
            return
        joined = ", ".join(prefix_sections)
        raise ValueError(
            f"{relative_path} must publish at least {minimum_count} additional section "
            f"after {joined}."
        )

    def _validate_initiative_cold_start_read_order(
        self,
        relative_path: str,
        initiative_root: Path,
        read_order_section: str,
    ) -> None:
        required_docs = list(INITIATIVE_REQUIRED_CANONICAL_READ_ORDER)
        decision_notes_path = initiative_root / "decision_notes.md"
        if decision_notes_path.exists():
            required_docs.insert(2, "decision_notes.md")
        missing_docs = [name for name in required_docs if name not in read_order_section]
        if missing_docs:
            joined = ", ".join(missing_docs)
            raise ValueError(
                f"{relative_path} Read Order is missing required canonical docs: {joined}"
            )
        canonical_doc_positions = [read_order_section.index(name) for name in required_docs[:-1]]
        implementation_slice_position = read_order_section.index("implementation_slice.md")
        if any(position > implementation_slice_position for position in canonical_doc_positions):
            ordered_docs = ", ".join(required_docs[:-1])
            raise ValueError(
                f"{relative_path} Read Order must place {ordered_docs} before "
                "implementation_slice.md."
            )

    def _load_sibling_sections_if_present(
        self,
        resolved_path: Path,
        sibling_name: str,
    ) -> dict[str, str] | None:
        sibling_path = resolved_path.with_name(sibling_name)
        if not sibling_path.exists():
            return None
        return extract_sections(load_markdown_body(sibling_path))

    def _validate_initiative_rendered_plan(
        self,
        relative_path: str,
        resolved_path: Path,
        sections: dict[str, str],
    ) -> None:
        scope_section = sections["Scope and Non-Goals"]
        initiative_brief_sections = self._load_sibling_sections_if_present(
            resolved_path,
            "initiative_brief.md",
        )
        decision_note_sections = self._load_sibling_sections_if_present(
            resolved_path,
            "decision_notes.md",
        )
        if (
            (
                self._bullet_lines(
                    None
                    if initiative_brief_sections is None
                    else initiative_brief_sections.get("Non-Goals")
                )
                or self._bullet_lines(
                    None
                    if decision_note_sections is None
                    else decision_note_sections.get("Locked Post-V1 Deferrals")
                )
            )
            and INITIATIVE_EMPTY_SCOPE_FALLBACK_LINE in scope_section
        ):
            raise ValueError(
                f"{relative_path} Scope and Non-Goals still claims there are no explicit "
                "non-goals or deferred scope items even though the canonical docs publish them."
            )

        for line in sections["Dependencies and Risks"].splitlines():
            stripped = line.strip()
            if not stripped.startswith("- Discrepancy "):
                continue
            if any(
                f"`{status}`" in stripped
                for status in INITIATIVE_TERMINAL_DISCREPANCY_STATUSES
            ):
                raise ValueError(
                    f"{relative_path} Dependencies and Risks must not present resolved "
                    "or terminal discrepancies as current risk lines."
                )

    def _bullet_lines(self, section_text: str | None) -> tuple[str, ...]:
        if section_text is None:
            return ()
        items: list[str] = []
        for line in section_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                items.append(stripped[2:].strip())
        return tuple(items)

    def _validate_markdown_title_and_required_section_groups(
        self,
        relative_path: str,
        markdown: str,
        sections: dict[str, str],
        *,
        required_section_groups: tuple[tuple[str, ...], ...],
    ) -> tuple[str, ...]:
        validate_blank_line_before_heading_after_list(relative_path, markdown)
        visible_title = extract_title(markdown).strip()
        if not visible_title:
            raise ValueError(f"{relative_path} must publish one H1 title.")
        matched_sections: list[str] = []
        missing_sections: list[str] = []
        for section_group in required_section_groups:
            matched_title = next((title for title in section_group if title in sections), None)
            if matched_title is None:
                missing_sections.append(" / ".join(section_group))
                continue
            matched_sections.append(matched_title)
        if missing_sections:
            joined = ", ".join(missing_sections)
            raise ValueError(f"{relative_path} is missing required sections: {joined}")
        resolved_order = tuple(matched_sections)
        validate_required_section_order(relative_path, sections, resolved_order)
        return resolved_order
