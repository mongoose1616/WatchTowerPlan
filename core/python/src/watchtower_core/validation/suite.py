"""Registry-backed validation suite runtime."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import ValidationSuiteStepDefinition, ValidatorDefinition
from watchtower_core.pack_integration.runtime import load_pack_validation_runtime
from watchtower_core.telemetry import telemetry_operation
from watchtower_core.validation.artifact import ArtifactValidationService
from watchtower_core.validation.common import discover_repository_targets
from watchtower_core.validation.context import PackValidationContext
from watchtower_core.validation.errors import ValidationExecutionError, ValidationSelectionError
from watchtower_core.validation.front_matter import FrontMatterValidationService
from watchtower_core.validation.models import (
    ValidationIssue,
    ValidationResult,
    ValidationSuiteRecord,
    ValidationSuiteResult,
)
from watchtower_core.validation.pack_contract import PackContractValidationService

DOCUMENT_SEMANTICS_ARTIFACT_KIND = "documentation_semantics"


class DocumentSemanticsValidationService(Protocol):
    """Structural protocol for pack-owned document-semantics validators."""

    def validate(
        self,
        target: str,
        *,
        validator_id: str | None = None,
    ) -> ValidationResult:
        """Validate one Markdown target through pack-owned semantic rules."""


DocumentSemanticsFactory = Callable[[ControlPlaneLoader], DocumentSemanticsValidationService]
ValidationSuiteTargetResolver = Callable[
    [PackValidationContext, ValidationSuiteStepDefinition],
    tuple[str, ...] | None,
]
PackContractIssueProvider = Callable[[ControlPlaneLoader, str], tuple[ValidationIssue, ...]]


class ValidationSuiteService:
    """Execute validation suites declared in the active validation-suite registry."""

    def __init__(
        self,
        loader: ControlPlaneLoader,
        *,
        document_semantics_factory: DocumentSemanticsFactory | None = None,
        target_resolver: ValidationSuiteTargetResolver | None = None,
        pack_contract_issue_provider: PackContractIssueProvider | None = None,
    ) -> None:
        self._loader = loader
        self._document_semantics_factory = (
            document_semantics_factory or _default_document_semantics_factory
        )
        self._target_resolver = target_resolver
        self._pack_contract_issue_provider = pack_contract_issue_provider

    def run(
        self,
        suite_id: str,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
        included_step_kinds: tuple[str, ...] | None = None,
    ) -> ValidationSuiteResult:
        """Run one declared validation suite and return aggregate results."""
        with telemetry_operation(
            "validation_suite",
            suite_id,
            attributes={
                "pack_settings_path": pack_settings_path,
                "included_step_kinds": included_step_kinds,
            },
        ) as operation:
            context = PackValidationContext.from_loader(
                self._loader,
                pack_settings_path=pack_settings_path,
            )
            try:
                suite = context.validation_suite_registry.get(suite_id)
            except KeyError as exc:
                raise ValidationSelectionError(f"Unknown validation suite ID: {suite_id}") from exc

            artifact: ArtifactValidationService | None = None
            front_matter: FrontMatterValidationService | None = None
            document_semantics: DocumentSemanticsValidationService | None = None
            pack_contract = PackContractValidationService(
                context.loader,
                extra_issue_provider=self._pack_contract_issue_provider,
            )

            allowed_step_kinds = (
                set(included_step_kinds) if included_step_kinds is not None else None
            )
            steps = tuple(
                step
                for step in suite.steps
                if allowed_step_kinds is None or step.step_kind in allowed_step_kinds
            )

            records: list[ValidationSuiteRecord] = []
            for step in steps:
                if step.step_kind == "pack_contract":
                    records.append(
                        ValidationSuiteRecord(
                            step_id=step.step_id,
                            step_kind=step.step_kind,
                            target=context.pack_settings_path,
                            result=pack_contract.validate(context.pack_settings_path),
                        )
                    )
                    continue

                if step.step_kind == "artifact":
                    if artifact is None:
                        artifact = ArtifactValidationService(context.loader)
                    records.extend(
                        self._run_validation_step(
                            context,
                            step,
                            service=artifact,
                            suffixes=(".json",),
                        )
                    )
                    continue
                if step.step_kind == "front_matter":
                    if front_matter is None:
                        front_matter = FrontMatterValidationService(context.loader)
                    records.extend(
                        self._run_validation_step(
                            context,
                            step,
                            service=front_matter,
                            suffixes=(".md",),
                        )
                    )
                    continue
                if step.step_kind == "document_semantics":
                    if document_semantics is None:
                        document_semantics = self._document_semantics_factory(context.loader)
                    records.extend(
                        self._run_validation_step(
                            context,
                            step,
                            service=document_semantics,
                            suffixes=(".md",),
                        )
                    )
                    continue

                raise ValidationExecutionError(
                    f"Unsupported validation suite step kind: {step.step_kind}"
                )

            result = ValidationSuiteResult(
                suite_id=suite.suite_id,
                pack_settings_path=context.pack_settings_path,
                records=tuple(records),
            )
            if operation is not None:
                operation.set_result(
                    status="ok" if result.passed else "failed",
                    total_count=result.total_count,
                    passed_count=result.passed_count,
                    failed_count=result.failed_count,
                    pack_settings_path=result.pack_settings_path,
                )
            return result

    def _run_validation_step(
        self,
        context: PackValidationContext,
        step: ValidationSuiteStepDefinition,
        *,
        service: Any,
        suffixes: tuple[str, ...],
    ) -> tuple[ValidationSuiteRecord, ...]:
        if step.paths:
            targets = step.paths
        else:
            resolved_targets = (
                self._target_resolver(context, step) if self._target_resolver is not None else None
            )
            targets = (
                resolved_targets
                if resolved_targets is not None
                else self._auto_discover_targets(context, step, suffixes=suffixes)
            )
        if not targets:
            return (
                ValidationSuiteRecord(
                    step_id=step.step_id,
                    step_kind=step.step_kind,
                    target=step.step_id,
                    result=self._step_failure_result(
                        step,
                        target=step.step_id,
                        code="validation_target_missing",
                        message=(
                            "Validation suite step did not resolve any targets from the "
                            "active validator registry."
                        ),
                    ),
                ),
            )

        records: list[ValidationSuiteRecord] = []
        for target in targets:
            try:
                result = service.validate(target, validator_id=step.validator_id)
            except (ValidationExecutionError, ValidationSelectionError) as exc:
                result = self._step_failure_result(
                    step,
                    target=target,
                    code="validation_step_error",
                    message=str(exc),
                )
            records.append(
                ValidationSuiteRecord(
                    step_id=step.step_id,
                    step_kind=step.step_kind,
                    target=target,
                    result=result,
                )
            )
        return tuple(records)

    def _auto_discover_targets(
        self,
        context: PackValidationContext,
        step: ValidationSuiteStepDefinition,
        *,
        suffixes: tuple[str, ...],
    ) -> tuple[str, ...]:
        validators = self._candidate_validators(context, step)
        patterns = tuple(pattern for validator in validators for pattern in validator.applies_to)
        return discover_repository_targets(
            context.loader,
            patterns,
            suffixes=suffixes,
        )

    def _candidate_validators(
        self,
        context: PackValidationContext,
        step: ValidationSuiteStepDefinition,
    ) -> tuple[ValidatorDefinition, ...]:
        registry = context.validator_registry
        if step.validator_id is not None:
            try:
                validator = registry.get(step.validator_id)
            except KeyError as exc:
                raise ValidationSelectionError(
                    f"Unknown validator ID: {step.validator_id}"
                ) from exc
            if not self._step_kind_matches_validator(step.step_kind, validator):
                raise ValidationSelectionError(
                    "Validation suite step validator does not match the step kind: "
                    f"{step.validator_id} for {step.step_kind}"
                )
            return (validator,)

        return tuple(
            validator
            for validator in registry.validators
            if validator.status == "active"
            and self._step_kind_matches_validator(step.step_kind, validator)
        )

    def _step_kind_matches_validator(
        self,
        step_kind: str,
        validator: ValidatorDefinition,
    ) -> bool:
        if step_kind == "artifact":
            return validator.engine == "json_schema" and validator.artifact_kind not in {
                "documentation_front_matter",
                DOCUMENT_SEMANTICS_ARTIFACT_KIND,
            }
        if step_kind == "front_matter":
            return (
                validator.engine == "json_schema"
                and validator.artifact_kind == "documentation_front_matter"
            )
        if step_kind == "document_semantics":
            return (
                validator.engine == "python"
                and validator.artifact_kind == DOCUMENT_SEMANTICS_ARTIFACT_KIND
            )
        return False

    def _step_failure_result(
        self,
        step: ValidationSuiteStepDefinition,
        *,
        target: str,
        code: str,
        message: str,
    ) -> ValidationResult:
        return ValidationResult(
            validator_id=step.validator_id or f"suite:{step.step_kind}:auto",
            target_path=target,
            engine="python",
            schema_ids=(),
            passed=False,
            issues=(
                ValidationIssue(
                    code=code,
                    message=message,
                    location=target,
                ),
            ),
        )


def _default_document_semantics_factory(
    loader: ControlPlaneLoader,
) -> DocumentSemanticsValidationService:
    runtime = load_pack_validation_runtime(loader)
    return runtime.document_semantics_factory(loader)


__all__ = ["ValidationSuiteService", "ValidationSuiteTargetResolver"]
