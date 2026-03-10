"""Repo-specific semantic validation for governed Markdown document families."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.adapters import (
    extract_external_urls,
    extract_repo_path_references,
    extract_sections,
    extract_title,
    extract_updated_at_from_section,
    load_front_matter,
    load_markdown_body,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ValidatorDefinition
from watchtower_core.repo_ops.planning_documents import (
    DECISION_OPTIONAL_EXPLAINED_SECTIONS,
    DECISION_REQUIRED_SECTIONS,
    FEATURE_DESIGN_OPTIONAL_EXPLAINED_SECTIONS,
    FEATURE_DESIGN_REQUIRED_SECTIONS,
    IMPLEMENTATION_PLAN_OPTIONAL_EXPLAINED_SECTIONS,
    IMPLEMENTATION_PLAN_REQUIRED_SECTIONS,
    PRD_OPTIONAL_EXPLAINED_SECTIONS,
    PRD_REQUIRED_SECTIONS,
    load_governed_document,
    validate_explained_bullet_section,
    validate_required_section_order,
)
from watchtower_core.repo_ops.sync.decision_index import DECISION_FRONT_MATTER_SCHEMA_ID
from watchtower_core.repo_ops.sync.design_document_index import (
    FEATURE_DESIGN_FRONT_MATTER_SCHEMA_ID,
    IMPLEMENTATION_PLAN_FRONT_MATTER_SCHEMA_ID,
)
from watchtower_core.repo_ops.sync.foundation_index import FOUNDATION_FRONT_MATTER_SCHEMA_ID
from watchtower_core.repo_ops.sync.prd_index import PRD_FRONT_MATTER_SCHEMA_ID
from watchtower_core.repo_ops.sync.reference_index import REFERENCE_FRONT_MATTER_SCHEMA_ID
from watchtower_core.repo_ops.sync.standard_index import STANDARD_FRONT_MATTER_SCHEMA_ID
from watchtower_core.repo_ops.sync.workflow_index import load_workflow_document
from watchtower_core.validation.common import matches_applies_to, resolve_target_path
from watchtower_core.validation.errors import ValidationExecutionError, ValidationSelectionError
from watchtower_core.validation.models import ValidationIssue, ValidationResult

DOCUMENT_SEMANTICS_ARTIFACT_KIND = "documentation_semantics"


class DocumentSemanticsValidationService:
    """Validate one governed Markdown document against repo-native semantic rules."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def validate(self, path: str | Path, validator_id: str | None = None) -> ValidationResult:
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

        if validator_id == "validator.documentation.reference_semantics":
            self._validate_reference_document(relative_target_path, resolved_path)
            return
        if validator_id == "validator.documentation.foundation_semantics":
            self._validate_foundation_document(relative_target_path, resolved_path)
            return
        if validator_id == "validator.documentation.standard_semantics":
            self._validate_standard_document(relative_target_path, resolved_path)
            return
        if validator_id == "validator.documentation.prd_semantics":
            self._validate_prd_document(relative_target_path)
            return
        if validator_id == "validator.documentation.decision_record_semantics":
            self._validate_decision_document(relative_target_path)
            return
        if validator_id == "validator.documentation.feature_design_semantics":
            self._validate_feature_design_document(relative_target_path)
            return
        if validator_id == "validator.documentation.implementation_plan_semantics":
            self._validate_implementation_plan_document(relative_target_path)
            return
        if validator_id == "validator.documentation.workflow_semantics":
            load_workflow_document(self._loader, relative_target_path)
            return

        raise ValidationExecutionError(f"Unsupported document-semantics validator: {validator_id}")

    def _validate_reference_document(self, relative_path: str, resolved_path: Path) -> None:
        front_matter = load_front_matter(resolved_path)
        self._loader.schema_store.validate_instance(
            front_matter,
            schema_id=REFERENCE_FRONT_MATTER_SCHEMA_ID,
        )
        markdown = load_markdown_body(resolved_path)
        sections = extract_sections(markdown)
        required_sections = (
            "Canonical Upstream",
            "Quick Reference or Distilled Reference",
            "References",
            "Updated At",
        )
        self._validate_title_and_required_sections(
            relative_path,
            markdown,
            sections,
            front_matter_title=str(front_matter["title"]),
            required_sections=required_sections,
        )
        if extract_updated_at_from_section(sections["Updated At"]) != front_matter["updated_at"]:
            raise ValueError(
                f"{relative_path} Updated At section does not match front matter updated_at."
            )
        if not extract_external_urls(sections["Canonical Upstream"]):
            raise ValueError(
                f"{relative_path} Canonical Upstream section does not publish any external URL."
            )

    def _validate_foundation_document(self, relative_path: str, resolved_path: Path) -> None:
        front_matter = load_front_matter(resolved_path)
        self._loader.schema_store.validate_instance(
            front_matter,
            schema_id=FOUNDATION_FRONT_MATTER_SCHEMA_ID,
        )
        markdown = load_markdown_body(resolved_path)
        sections = extract_sections(markdown)
        required_sections = ("References", "Updated At")
        self._validate_title_and_required_sections(
            relative_path,
            markdown,
            sections,
            front_matter_title=str(front_matter["title"]),
            required_sections=required_sections,
        )
        if extract_updated_at_from_section(sections["Updated At"]) != front_matter["updated_at"]:
            raise ValueError(
                f"{relative_path} Updated At section does not match front matter updated_at."
            )

    def _validate_standard_document(self, relative_path: str, resolved_path: Path) -> None:
        front_matter = load_front_matter(resolved_path)
        self._loader.schema_store.validate_instance(
            front_matter,
            schema_id=STANDARD_FRONT_MATTER_SCHEMA_ID,
        )
        markdown = load_markdown_body(resolved_path)
        sections = extract_sections(markdown)
        required_sections = (
            "Summary",
            "Purpose",
            "Scope",
            "Use When",
            "Related Standards and Sources",
            "Guidance",
            "Validation",
            "Change Control",
            "References",
            "Updated At",
        )
        self._validate_title_and_required_sections(
            relative_path,
            markdown,
            sections,
            front_matter_title=str(front_matter["title"]),
            required_sections=required_sections,
        )
        validate_explained_bullet_section(
            relative_path,
            "Related Standards and Sources",
            sections["Related Standards and Sources"],
        )
        if extract_updated_at_from_section(sections["Updated At"]) != front_matter["updated_at"]:
            raise ValueError(
                f"{relative_path} Updated At section does not match front matter updated_at."
            )
        related_external_urls = extract_external_urls(sections["Related Standards and Sources"])
        reference_paths = extract_repo_path_references(
            sections["References"],
            self._loader.repo_root,
        )
        if related_external_urls and not any(
            path.startswith("docs/references/") for path in reference_paths
        ):
            raise ValueError(
                f"{relative_path} cites external authority directly but does not cite a "
                "governed local reference doc under docs/references/."
            )

    def _validate_prd_document(self, relative_path: str) -> None:
        load_governed_document(
            self._loader,
            relative_path,
            schema_id=PRD_FRONT_MATTER_SCHEMA_ID,
            id_label="PRD ID",
            status_label="Status",
            required_sections=PRD_REQUIRED_SECTIONS,
            optional_explained_sections=PRD_OPTIONAL_EXPLAINED_SECTIONS,
        )

    def _validate_decision_document(self, relative_path: str) -> None:
        load_governed_document(
            self._loader,
            relative_path,
            schema_id=DECISION_FRONT_MATTER_SCHEMA_ID,
            id_label="Decision ID",
            status_label="Record Status",
            required_sections=DECISION_REQUIRED_SECTIONS,
            optional_explained_sections=DECISION_OPTIONAL_EXPLAINED_SECTIONS,
        )

    def _validate_feature_design_document(self, relative_path: str) -> None:
        load_governed_document(
            self._loader,
            relative_path,
            schema_id=FEATURE_DESIGN_FRONT_MATTER_SCHEMA_ID,
            id_label="Design ID",
            status_label="Design Status",
            required_sections=FEATURE_DESIGN_REQUIRED_SECTIONS,
            optional_explained_sections=FEATURE_DESIGN_OPTIONAL_EXPLAINED_SECTIONS,
        )

    def _validate_implementation_plan_document(self, relative_path: str) -> None:
        load_governed_document(
            self._loader,
            relative_path,
            schema_id=IMPLEMENTATION_PLAN_FRONT_MATTER_SCHEMA_ID,
            id_label="Plan ID",
            status_label="Plan Status",
            required_sections=IMPLEMENTATION_PLAN_REQUIRED_SECTIONS,
            optional_explained_sections=IMPLEMENTATION_PLAN_OPTIONAL_EXPLAINED_SECTIONS,
        )

    def _validate_title_and_required_sections(
        self,
        relative_path: str,
        markdown: str,
        sections: dict[str, str],
        *,
        front_matter_title: str,
        required_sections: tuple[str, ...],
    ) -> None:
        visible_title = extract_title(markdown)
        if visible_title != front_matter_title:
            raise ValueError(
                f"{relative_path} H1 title does not match front matter title: "
                f"{visible_title!r} != {front_matter_title!r}"
            )
        missing_sections = [title for title in required_sections if title not in sections]
        if missing_sections:
            joined = ", ".join(missing_sections)
            raise ValueError(f"{relative_path} is missing required sections: {joined}")
        validate_required_section_order(relative_path, sections, required_sections)
