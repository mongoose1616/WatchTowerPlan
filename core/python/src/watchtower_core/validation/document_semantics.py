"""Reusable-core document-semantics validation for shared governed Markdown surfaces."""

from __future__ import annotations

from pathlib import PurePosixPath

from jsonschema import ValidationError as JsonSchemaValidationError

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.documentation.command_semantics import validate_command_document
from watchtower_core.documentation.markdown_semantics import (
    validate_repo_local_markdown_links,
)
from watchtower_core.sync.cache import (
    finalize_document_sync_cache,
    prepare_document_sync_cache,
)
from watchtower_core.sync.foundation_index import FoundationIndexSyncService
from watchtower_core.sync.reference_index import ReferenceIndexSyncService
from watchtower_core.sync.standard_index import StandardIndexSyncService
from watchtower_core.sync.workflow_index import (
    WorkflowDocumentContext,
    build_workflow_document_context,
    load_workflow_document,
)
from watchtower_core.validation.common import resolve_target_path
from watchtower_core.validation.models import ValidationIssue, ValidationResult

_CORE_FOUNDATION_DOC_ROOT = "core/docs/foundations/"
_COMMAND_DOC_SEGMENT = "/docs/commands/"
_REFERENCE_DOC_SEGMENT = "/docs/references/"
_STANDARD_DOC_SEGMENT = "/docs/standards/"
_WORKFLOW_MODULE_SEGMENT = "/workflows/modules/"
_WORKFLOW_ROLE_SEGMENT = "/workflows/roles/"


class CoreDocumentSemanticsValidationService:
    """Validate shared governed command, reference, standard, foundation, and workflow docs."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._foundation_doc_paths: frozenset[str] | None = None
        self._foundation_doc_error: ValueError | JsonSchemaValidationError | None = None
        self._reference_doc_paths: frozenset[str] | None = None
        self._reference_doc_error: ValueError | JsonSchemaValidationError | None = None
        self._standard_doc_paths: frozenset[str] | None = None
        self._standard_doc_error: ValueError | JsonSchemaValidationError | None = None
        self._workflow_context: WorkflowDocumentContext | None = None

    def validate(
        self,
        target: str,
        *,
        validator_id: str | None = None,
    ) -> ValidationResult:
        """Validate one repository-local Markdown target through reusable-core semantics."""

        _, target_path, relative_target_path = resolve_target_path(self._loader, target)
        if relative_target_path is None:
            return self._failure_result(
                validator_id=validator_id or "validator.documentation.command_semantics",
                target_path=target_path,
                location=target_path,
                message="Document-semantics validation requires a repository-local target.",
            )

        try:
            self._validate_relative_target(relative_target_path)
        except (ValueError, JsonSchemaValidationError) as exc:
            return self._failure_result(
                validator_id=self._validator_id_for_target(relative_target_path),
                target_path=target_path,
                location=relative_target_path,
                message=str(exc),
            )

        return ValidationResult(
            validator_id=self._validator_id_for_target(relative_target_path),
            target_path=target_path,
            engine="python",
            schema_ids=(),
            passed=True,
            issues=(),
        )

    def _validate_relative_target(self, relative_target_path: str) -> None:
        resolved_path = self._loader.resolve_path(relative_target_path)
        if self._is_command_doc(relative_target_path):
            validate_command_document(
                relative_path=relative_target_path,
                resolved_path=resolved_path,
                repo_root=self._loader.repo_root,
            )
            return
        validate_repo_local_markdown_links(
            relative_path=relative_target_path,
            repo_root=self._loader.repo_root,
            markdown=resolved_path.read_text(encoding="utf-8"),
            source_path=resolved_path,
        )
        if relative_target_path.startswith(_CORE_FOUNDATION_DOC_ROOT):
            self._validate_foundation_document(relative_target_path)
            return
        if _REFERENCE_DOC_SEGMENT in relative_target_path:
            self._validate_reference_document(relative_target_path)
            return
        if _STANDARD_DOC_SEGMENT in relative_target_path:
            self._validate_standard_document(relative_target_path)
            return
        if self._is_workflow_doc(relative_target_path):
            load_workflow_document(
                self._loader,
                relative_target_path,
                context=self._workflow_context_or_build(),
            )
            return
        raise ValueError(
            "Unsupported document-semantics target for the reusable-core runtime. "
            f"Expected command docs, reference docs, standards, foundations, or workflows: "
            f"{relative_target_path}"
        )

    def _validate_foundation_document(self, relative_target_path: str) -> None:
        if relative_target_path not in self._load_foundation_doc_paths():
            raise ValueError(
                f"{relative_target_path} did not validate as a governed foundation doc."
            )

    def _validate_reference_document(self, relative_target_path: str) -> None:
        if relative_target_path not in self._load_reference_doc_paths():
            raise ValueError(
                f"{relative_target_path} did not validate as a governed reference doc."
            )

    def _validate_standard_document(self, relative_target_path: str) -> None:
        if relative_target_path not in self._load_standard_doc_paths():
            raise ValueError(f"{relative_target_path} did not validate as a governed standard doc.")

    def _load_foundation_doc_paths(self) -> frozenset[str]:
        if self._foundation_doc_paths is not None:
            return self._foundation_doc_paths
        if self._foundation_doc_error is not None:
            raise self._foundation_doc_error

        try:
            service = FoundationIndexSyncService(self._loader)
            document = self._load_or_build_cached_document(
                service,
                relative_output_path=service.OUTPUT_PATH,
            )
        except (ValueError, JsonSchemaValidationError) as exc:
            self._foundation_doc_error = exc
            raise
        self._foundation_doc_paths = self._doc_paths_from_index(document)
        return self._foundation_doc_paths

    def _load_reference_doc_paths(self) -> frozenset[str]:
        if self._reference_doc_paths is not None:
            return self._reference_doc_paths
        if self._reference_doc_error is not None:
            raise self._reference_doc_error

        try:
            service = ReferenceIndexSyncService(self._loader)
            document = self._load_or_build_cached_document(
                service,
                relative_output_path=service.OUTPUT_PATH,
            )
        except (ValueError, JsonSchemaValidationError) as exc:
            self._reference_doc_error = exc
            raise
        self._reference_doc_paths = self._doc_paths_from_index(document)
        return self._reference_doc_paths

    def _load_standard_doc_paths(self) -> frozenset[str]:
        if self._standard_doc_paths is not None:
            return self._standard_doc_paths
        if self._standard_doc_error is not None:
            raise self._standard_doc_error

        try:
            service = StandardIndexSyncService(self._loader)
            document = self._load_or_build_cached_document(
                service,
                relative_output_path=service.OUTPUT_PATH,
            )
        except (ValueError, JsonSchemaValidationError) as exc:
            self._standard_doc_error = exc
            raise
        self._standard_doc_paths = self._doc_paths_from_index(document)
        return self._standard_doc_paths

    def _load_or_build_cached_document(
        self,
        service: FoundationIndexSyncService | ReferenceIndexSyncService | StandardIndexSyncService,
        *,
        relative_output_path: str,
    ) -> dict[str, object]:
        prepared_cache = prepare_document_sync_cache(
            self._loader,
            service,
            relative_output_path=relative_output_path,
        )
        document = (
            prepared_cache.document if prepared_cache.document is not None else None
        ) or service.build_document()
        self._loader.schema_store.validate_instance(document)
        finalize_document_sync_cache(prepared_cache, document=document)
        return document

    @staticmethod
    def _doc_paths_from_index(document: dict[str, object]) -> frozenset[str]:
        entries = document.get("entries")
        if not isinstance(entries, list):
            entries = []
        return frozenset(
            entry["doc_path"]
            for entry in entries
            if isinstance(entry, dict) and isinstance(entry.get("doc_path"), str)
        )

    def _workflow_context_or_build(self) -> WorkflowDocumentContext:
        if self._workflow_context is None:
            self._workflow_context = build_workflow_document_context(self._loader)
        return self._workflow_context

    @staticmethod
    def _is_command_doc(relative_target_path: str) -> bool:
        name = PurePosixPath(relative_target_path).name
        return (
            _COMMAND_DOC_SEGMENT in relative_target_path
            and name.startswith("watchtower_core")
            and name.endswith(".md")
        )

    @staticmethod
    def _is_workflow_doc(relative_target_path: str) -> bool:
        return relative_target_path.endswith(".md") and (
            _WORKFLOW_MODULE_SEGMENT in relative_target_path
            or _WORKFLOW_ROLE_SEGMENT in relative_target_path
        )

    @staticmethod
    def _validator_id_for_target(relative_target_path: str) -> str:
        if CoreDocumentSemanticsValidationService._is_command_doc(relative_target_path):
            return "validator.documentation.command_semantics"
        if relative_target_path.startswith(_CORE_FOUNDATION_DOC_ROOT):
            return "validator.documentation.foundation_semantics"
        if _REFERENCE_DOC_SEGMENT in relative_target_path:
            return "validator.documentation.reference_semantics"
        if _STANDARD_DOC_SEGMENT in relative_target_path:
            return "validator.documentation.standard_semantics"
        return "validator.documentation.workflow_semantics"

    @staticmethod
    def _failure_result(
        *,
        validator_id: str,
        target_path: str,
        location: str,
        message: str,
    ) -> ValidationResult:
        return ValidationResult(
            validator_id=validator_id,
            target_path=target_path,
            engine="python",
            schema_ids=(),
            passed=False,
            issues=(
                ValidationIssue(
                    code="document_semantics_invalid",
                    message=message,
                    location=location,
                ),
            ),
        )


__all__ = ["CoreDocumentSemanticsValidationService"]
